from setuptools import setup, find_packages

setup(
    name='amochka',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
         'requests',
         'ratelimit'
    ],
    author='Timurka',
    author_email='timurdt@gmail.com',
    description='Библиотека для работы с API amoCRM',
    url='',  # Укажите ваш URL репозитория
    classifiers=[
         'Programming Language :: Python :: 3',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)