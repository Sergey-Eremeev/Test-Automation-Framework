# Test Automation Framework

Описание
==========================
Фреймворк для автотестов на базе python, pytest, selenium webdriver:

* Написание тестов с использованием PageObject.
* Отчеты Allure.
* Чтение тестовых данных из JSON файла.

Установка зависимостей
=====================
* ``pip install -r requirements.txt``


Запуск тестов
==================
##### с проверкой через пользовательский интерфейс
``py.test --alluredir=allure_report tests/ --check_ui``

##### с проверкой через Базу Данных
``py.test --alluredir=allure_report tests/ ``

``allure serve allure_report``

Конфигурационный файл
==================
* Запуск тестов используя конфигурационный файл ``py.test --config config.json``, значение по умолчанию ``config.json``

		{
		    "web": {
		        "baseUrl": "https://...",
		        "username": ...,
		        "password": ...
		    },
		    "db": {
                "host": ...,
                "name": ...,
                "user": ...,
                "password": ...
             }
		}

