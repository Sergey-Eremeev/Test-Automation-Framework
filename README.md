# Test Automation Framework

Описание
==========================
Тестовый Фреймворк на базе python, pytest, selenium webdriver:

* Написание тестов с использованием PageObject.
* Отчеты Allure.
* Чтение тестовых данных из JSON файла.

Установка зависимостей
=====================
* ``pip install -r requirements.txt``


Запуск тестов
==================

``py.test --alluredir=allure_report tests/test_login.py``

``allure serve allure_report``

Конфигурационный файл
==================
* Запуск тестов используя конфигурационный файл ``py.test --config config.json``, значение по умолчанию ``config.json``

		{
		    "web": {
		        "baseUrl": "https://...",
		        "username": "...",
		        "password": "..."
		    }
		}

