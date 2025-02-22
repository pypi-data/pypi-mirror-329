import os
import time
import json
import requests
import logging
from datetime import datetime
from ratelimit import limits, sleep_and_retry

# Создаём базовый логгер
logger = logging.getLogger(__name__)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

RATE_LIMIT = 7  # Максимум 7 запросов в секунду

class Deal(dict):
    """
    Объект сделки расширяет стандартный словарь данными из custom_fields_values.

    Обеспечивает два способа доступа к кастомным полям:
      1. get(key): при обращении по названию (строкой) или по ID поля (integer)
         возвращает текстовое значение поля (например, «Дурина Юлия»).
      2. get_id(key): возвращает идентификатор выбранного варианта (enum_id) для полей типа select.
         Если в данных enum_id отсутствует, производится поиск в переданной конфигурации полей,
         сравнение выполняется без учёта регистра и лишних пробелов.

    Параметр custom_fields_config – словарь, где ключи – ID полей, а значения – модели полей.
    """
    def __init__(self, data, custom_fields_config=None):
        super().__init__(data)
        self._custom = {}
        self._custom_config = custom_fields_config  # сохраняем конфигурацию кастомных полей
        custom = data.get("custom_fields_values") or []
        logger.debug(f"Processing custom_fields_values: {custom}")
        for field in custom:
            if isinstance(field, dict):
                field_name = field.get("field_name")
                values = field.get("values")
                if field_name and values and isinstance(values, list) and len(values) > 0:
                    key_name = field_name.lower().strip()
                    stored_value = values[0].get("value")
                    stored_enum_id = values[0].get("enum_id")  # может быть None для некоторых полей
                    # Сохраняем полную информацию (и для get() и для get_id())
                    self._custom[key_name] = {"value": stored_value, "enum_id": stored_enum_id}
                    logger.debug(f"Set custom field '{key_name}' = {{'value': {stored_value}, 'enum_id': {stored_enum_id}}}")
                field_id = field.get("field_id")
                if field_id is not None and values and isinstance(values, list) and len(values) > 0:
                    stored_value = values[0].get("value")
                    stored_enum_id = values[0].get("enum_id")  # может быть None для некоторых полей
                    self._custom[int(field_id)] = {"value": stored_value, "enum_id": stored_enum_id}
                    logger.debug(f"Set custom field id {field_id} = {{'value': {stored_value}, 'enum_id': {stored_enum_id}}}")
        if custom_fields_config:
            for cid, field_obj in custom_fields_config.items():
                key = field_obj.get("name", "").lower().strip() if isinstance(field_obj, dict) else str(field_obj).lower().strip()
                if key not in self._custom:
                    self._custom[key] = None
                    logger.debug(f"Field '{key}' not found in deal data; set to None")

    def __getitem__(self, key):
        if key in super().keys():
            return super().__getitem__(key)
        if isinstance(key, str):
            lower_key = key.lower().strip()
            if lower_key in self._custom:
                stored = self._custom[lower_key]
                return stored.get("value") if isinstance(stored, dict) else stored
        if isinstance(key, int):
            if key in self._custom:
                stored = self._custom[key]
                return stored.get("value") if isinstance(stored, dict) else stored
        raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def get_id(self, key, default=None):
        """
        Возвращает идентификатор выбранного варианта (enum_id) для кастомного поля.
        Если значение enum_id отсутствует в данных, производится поиск в конфигурации кастомных полей,
        сравнение значения выполняется без учёта регистра и пробелов.

        :param key: Название поля (строка) или ID поля (integer).
        :param default: Значение по умолчанию, если enum_id не найден.
        :return: Идентификатор выбранного варианта (целое число) или default.
        """
        stored = None
        if isinstance(key, str):
            lower_key = key.lower().strip()
            if lower_key in self._custom:
                stored = self._custom[lower_key]
        elif isinstance(key, int):
            if key in self._custom:
                stored = self._custom[key]
        if isinstance(stored, dict):
            enum_id = stored.get("enum_id")
            if enum_id is not None:
                return enum_id
            if self._custom_config:
                field_def = None
                if isinstance(key, int):
                    field_def = self._custom_config.get(key)
                else:
                    for fid, fdef in self._custom_config.items():
                        if fdef.get("name", "").lower().strip() == key.lower().strip():
                            field_def = fdef
                            break
                if field_def:
                    enums = field_def.get("enums") or []
                    for enum in enums:
                        if enum.get("value", "").lower().strip() == stored.get("value", "").lower().strip():
                            return enum.get("id", default)
        return default

class AmoCRMClient:
    """
    Клиент для работы с API amoCRM.

    Основные функции:
      - load_token: Загружает и проверяет токен авторизации.
      - _make_request: Выполняет HTTP-запрос с учетом ограничения по скорости.
      - get_deal_by_id: Получает данные сделки по ID и возвращает объект Deal.
      - get_custom_fields_mapping: Загружает и кэширует список кастомных полей.
      - find_custom_field_id: Ищет кастомное поле по его названию.
      - update_lead: Обновляет сделку, включая стандартные и кастомные поля.

    Дополнительно можно задать уровень логирования через параметр log_level,
    либо полностью отключить логирование, установив disable_logging=True.
    """
    def __init__(
        self, 
        base_url, 
        token_file=None, 
        cache_file=None, 
        log_level=logging.INFO, 
        disable_logging=False,
        cache_enabled=True,
        cache_storage='file',         # 'file' или 'memory'
        cache_hours=24                # время жизни кэша в часах, или None для бесконечного кэша
    ):
        """
        Инициализирует клиента, задавая базовый URL, токен авторизации и настройки кэша для кастомных полей.
        
        :param base_url: Базовый URL API amoCRM.
        :param token_file: Файл, содержащий токен авторизации.
        :param cache_file: Файл для кэширования данных кастомных полей.
        :param log_level: Уровень логирования (например, logging.DEBUG, logging.INFO).
        :param disable_logging: Если True, логирование будет отключено.
        :param cache_enabled: Если False, кэширование отключается (остальные параметры игнорируются).
        :param cache_storage: 'file' для файлового кэша, 'memory' для кэша только в оперативной памяти.
        :param cache_hours: Время жизни кэша в часах. Если None – кэш считается бесконечным.
        """
        self.base_url = base_url.rstrip('/')
        domain = self.base_url.split("//")[-1].split(".")[0]
        self.domain = domain
        self.token_file = token_file or os.path.join(os.path.expanduser('~'), '.amocrm_token.json')
        
        # Если выбран файловый кэш, определяем имя файла, иначе он не используется
        if cache_storage.lower() == 'file':
            if not cache_file:
                cache_file = f"custom_fields_cache_{self.domain}.json"
            self.cache_file = cache_file
        else:
            self.cache_file = None
        self.cache_enabled = cache_enabled
        self.cache_storage = cache_storage.lower()  # 'file' или 'memory'
        self.cache_hours = cache_hours
        
        self.token = self.load_token()
        self._custom_fields_mapping = None

        if disable_logging:
            logging.disable(logging.CRITICAL)
        else:
            logger.setLevel(log_level)
        
        logger.debug(f"AmoCRMClient initialized for domain {self.domain}")

    def load_token(self):
        """
        Загружает токен авторизации из файла или строки, проверяет его срок действия.

        :return: Действительный access_token.
        :raises Exception: Если токен не найден или истёк.
        """
        data = None
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as f:
                data = json.load(f)
            logger.debug(f"Token loaded from file: {self.token_file}")
        else:
            try:
                data = json.loads(self.token_file)
                logger.debug("Token parsed from provided string.")
            except Exception as e:
                raise Exception("Токен не найден и не удалось распарсить переданное содержимое.") from e

        expires_at_str = data.get('expires_at')
        try:
            expires_at = datetime.fromisoformat(expires_at_str).timestamp()
        except Exception:
            expires_at = float(expires_at_str)
        
        if expires_at and time.time() < expires_at:
            logger.debug("Token is valid.")
            return data.get('access_token')
        else:
            raise Exception("Токен найден, но он истёк. Обновите токен.")

    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=1)
    def _make_request(self, method, endpoint, params=None, data=None):
        """
        Выполняет HTTP-запрос к API amoCRM с учетом ограничения по скорости (rate limit).

        :param method: HTTP-метод (GET, PATCH, POST, DELETE и т.д.).
        :param endpoint: Конечная точка API (начинается с /api/v4/).
        :param params: GET-параметры запроса.
        :param data: Данные, отправляемые в JSON-формате.
        :return: Ответ в формате JSON или None (если статус 204).
        :raises Exception: При получении кода ошибки, отличного от 200/204.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        logger.debug(f"Making {method} request to {url} with params {params} and data {data}")
        response = requests.request(method, url, headers=headers, params=params, json=data)
        if response.status_code not in (200, 204):
            logger.error(f"Request error {response.status_code}: {response.text}")
            raise Exception(f"Ошибка запроса: {response.status_code}, {response.text}")
        if response.status_code == 204:
            return None
        return response.json()

    def get_deal_by_id(self, deal_id):
        """
        Получает данные сделки по её ID и возвращает объект Deal.

        :param deal_id: ID сделки.
        :return: Объект Deal, включающий данные стандартных и кастомных полей.
        """
        endpoint = f"/api/v4/leads/{deal_id}"
        params = {'with': 'contacts,companies,catalog_elements,loss_reason,tags'}
        data = self._make_request("GET", endpoint, params=params)
        custom_config = self.get_custom_fields_mapping()
        logger.debug(f"Deal {deal_id} data received (содержимое полей не выводится полностью).")
        return Deal(data, custom_fields_config=custom_config)

    def _save_custom_fields_cache(self, mapping):
        """
        Сохраняет кэш кастомных полей в файл, если используется файловый кэш.
        Если кэширование отключено или выбран кэш в памяти, операция пропускается.
        """
        if not self.cache_enabled:
            logger.debug("Caching disabled; cache not saved.")
            return
        if self.cache_storage != 'file':
            logger.debug("Using memory caching; no file cache saved.")
            return
        cache_data = {"last_updated": time.time(), "mapping": mapping}
        with open(self.cache_file, "w") as f:
            json.dump(cache_data, f)
        logger.debug(f"Custom fields cache saved to {self.cache_file}")

    def _load_custom_fields_cache(self):
        """
        Загружает кэш кастомных полей из файла, если используется файловый кэш.
        Если кэширование отключено или выбран кэш в памяти, возвращает None.
        """
        if not self.cache_enabled:
            logger.debug("Caching disabled; no cache loaded.")
            return None
        if self.cache_storage != 'file':
            logger.debug("Using memory caching; cache will be kept in memory only.")
            return None
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                try:
                    cache_data = json.load(f)
                    logger.debug("Custom fields cache loaded successfully.")
                    return cache_data
                except Exception as e:
                    logger.error(f"Error loading cache: {e}")
                    return None
        return None

    def get_custom_fields_mapping(self, force_update=False):
        """
        Возвращает словарь отображения кастомных полей для сделок.
        Если данные кэшированы и не устарели, возвращает кэш; иначе выполняет запросы для получения данных.
        """
        if not force_update and self._custom_fields_mapping is not None:
            return self._custom_fields_mapping

        cache_data = self._load_custom_fields_cache() if self.cache_enabled else None
        if cache_data:
            last_updated = cache_data.get("last_updated", 0)
            if self.cache_hours is not None:
                if time.time() - last_updated < self.cache_hours * 3600:
                    self._custom_fields_mapping = cache_data.get("mapping")
                    logger.debug("Using cached custom fields mapping.")
                    return self._custom_fields_mapping
            else:
                # Бесконечный кэш – не проверяем срок
                self._custom_fields_mapping = cache_data.get("mapping")
                logger.debug("Using cached custom fields mapping (infinite cache).")
                return self._custom_fields_mapping

        mapping = {}
        page = 1
        total_pages = 1  # Значение по умолчанию
        while page <= total_pages:
            endpoint = f"/api/v4/leads/custom_fields?limit=250&page={page}"
            response = self._make_request("GET", endpoint)
            if response and "_embedded" in response and "custom_fields" in response["_embedded"]:
                for field in response["_embedded"]["custom_fields"]:
                    mapping[field["id"]] = field
                total_pages = response.get("_page_count", page)
                logger.debug(f"Fetched page {page} of {total_pages}")
                page += 1
            else:
                break

        logger.debug("Custom fields mapping fetched (содержимое маппинга не выводится полностью).")
        self._custom_fields_mapping = mapping
        if self.cache_enabled:
            self._save_custom_fields_cache(mapping)
        return mapping

    def find_custom_field_id(self, search_term):
        """
        Ищет кастомное поле по заданному названию (или части названия).

        :param search_term: Строка для поиска по имени поля.
        :return: Кортеж (field_id, field_obj) если найдено, иначе (None, None).
        """
        mapping = self.get_custom_fields_mapping()
        search_term_lower = search_term.lower().strip()
        for key, field_obj in mapping.items():
            if isinstance(field_obj, dict):
                name = field_obj.get("name", "").lower().strip()
            else:
                name = str(field_obj).lower().strip()
            if search_term_lower == name or search_term_lower in name:
                logger.debug(f"Found custom field '{name}' with id {key}")
                return int(key), field_obj
        logger.debug(f"Custom field containing '{search_term}' not found.")
        return None, None

    def update_lead(self, lead_id, update_fields: dict, tags_to_add: list = None, tags_to_delete: list = None):
        """
        Обновляет сделку, задавая новые значения для стандартных и кастомных полей.

        Для кастомных полей:
          - Если значение передается как целое число, оно интерпретируется как идентификатор варианта (enum_id)
            для полей типа select.
          - Если значение передается как строка, используется ключ "value".

        :param lead_id: ID сделки, которую нужно обновить.
        :param update_fields: Словарь с полями для обновления. Ключи могут быть стандартными или названием кастомного поля.
        :param tags_to_add: Список тегов для добавления к сделке.
        :param tags_to_delete: Список тегов для удаления из сделки.
        :return: Ответ API в формате JSON.
        :raises Exception: Если одно из кастомных полей не найдено.
        """
        payload = {}
        standard_fields = {
            "name", "price", "status_id", "pipeline_id", "created_by", "updated_by",
            "closed_at", "created_at", "updated_at", "loss_reason_id", "responsible_user_id"
        }
        custom_fields = []
        for key, value in update_fields.items():
            if key in standard_fields:
                payload[key] = value
                logger.debug(f"Standard field {key} set to {value}")
            else:
                if isinstance(value, int):
                    field_value_dict = {"enum_id": value}
                else:
                    field_value_dict = {"value": value}
                try:
                    field_id = int(key)
                    custom_fields.append({"field_id": field_id, "values": [field_value_dict]})
                    logger.debug(f"Custom field by id {field_id} set to {value}")
                except ValueError:
                    field_id, field_obj = self.find_custom_field_id(key)
                    if field_id is not None:
                        custom_fields.append({"field_id": field_id, "values": [field_value_dict]})
                        logger.debug(f"Custom field '{key}' found with id {field_id} set to {value}")
                    else:
                        raise Exception(f"Custom field '{key}' не найден.")
        if custom_fields:
            payload["custom_fields_values"] = custom_fields
        if tags_to_add:
            payload["tags_to_add"] = tags_to_add
        if tags_to_delete:
            payload["tags_to_delete"] = tags_to_delete
        logger.debug("Update payload for lead {} prepared (содержимое payload не выводится полностью).".format(lead_id))
        endpoint = f"/api/v4/leads/{lead_id}"
        response = self._make_request("PATCH", endpoint, data=payload)
        logger.debug("Update response received.")
        return response