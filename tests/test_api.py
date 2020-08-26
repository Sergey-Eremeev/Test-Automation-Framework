import json
import datetime
import pytest
import allure
import requests
import jsonschema
from jsonschema import validate
from jsonschema.exceptions import ValidationError

test_data_gender = ["male", "female"]
test_data_id = [10, 15]

schema = requests.get("https://dev.coolrocket.com/test/api.json").json()
resolver = jsonschema.RefResolver(base_uri='', referrer=schema, store={'': schema})


def basic_checks(response, expected_status_code=200):
    with allure.step(f'Проверка статус кода, ожидается {expected_status_code}'):
        assert response.status_code == expected_status_code
    with allure.step('Проверка кодировки, ожидается utf-8'):
        assert response.encoding.upper() == "UTF-8"
    with allure.step('Проверка "Content-Type", ожидается "application/json"'):
        assert "application/json" in response.headers['Content-Type'].lower()


@allure.title("Запрос списка идентификаторов пользователей по критерию: {gender}")
@pytest.mark.parametrize("gender", test_data_gender)
def test_get_list_of_user_id_by_gender(gender):
    with allure.step(f'Выполняется запрос GET https://dev.coolrocket.com/api/test/users?gender={gender}'):
        response = requests.get("https://dev.coolrocket.com/api/test/users", params={'gender': gender})

    basic_checks(response)

    try:
        with allure.step('Получение json'):
            document = response.json()
        with allure.step('Проверка, что массив с идентификаторами пользователей не пуст '):
            assert len(document["result"]) > 0
        with allure.step('Валидация по Схеме TestResponseOfListOfint'):
            validate(document, schema["definitions"]["TestResponseOfListOfint"])
    except json.JSONDecodeError:
        allure.attach(json.dumps(response.json()), "Invalid JSON")
        raise Exception('Invalid JSON')
    except ValidationError as exc:
        allure.attach(json.dumps(response.json()), "Invalid document")
        allure.attach(json.dumps(schema["definitions"]["TestResponseOfListOfint"], indent=2), "schema")
        raise Exception(exc.message)


@allure.title("Запрос информации о пользователе c id: {id} ")
@pytest.mark.parametrize("id", test_data_id)
def test_user_information_request_by_id(id):
    with allure.step(f'Выполняется запрос GET  https://dev.coolrocket.com/api/test/user/{id}'):
        response = requests.get(f"https://dev.coolrocket.com/api/test/user/{id}")

    basic_checks(response)

    try:
        with allure.step('Получение json'):
            document = response.json()
        with allure.step('Проверяем что id пользователя равен запрашиваемому id'):
            assert document["result"]["id"] == id
        with allure.step('Проверка соответствия даты и времени формату: 2018-10-16T06:54:29 с миллисекундами и без'):
            datetime.datetime.strptime(document["result"]["registrationDate"][:19], '%Y-%m-%dT%H:%M:%S')
        with allure.step('Валидация по Схеме TestResponseOfTestUser'):
            validate(document, schema["definitions"]["TestResponseOfTestUser"], resolver=resolver)
    except json.JSONDecodeError:
        allure.attach(json.dumps(response.json()), "Invalid JSON")
        raise Exception('Invalid JSON')
    except ValidationError as exc:
        allure.attach(json.dumps(response.json()), "Invalid document")
        allure.attach(json.dumps(schema["definitions"]["TestResponseOfTestUser"], indent=2),
                      "schema TestResponseOfTestUser")
        allure.attach(json.dumps(schema["definitions"]["TestUser"], indent=2), "schema TestUser")
        raise Exception(exc.message)


@allure.title("Некорректный запрос, ожидается статус код 400: ")
def test_bad_request_expected_status_code_400():
    with allure.step('Выполняется запрос GET https://dev.coolrocket.com/api/test/usersgender'):
        response = requests.get("https://dev.coolrocket.com/api/test/users?gendergender")

    basic_checks(response, 400)

    try:
        with allure.step('Получение json'):
            document = response.json()
        with allure.step('Валидация по Схеме ErrorDTO'):
            validate(document, schema["definitions"]["ErrorDTO"])
    except json.JSONDecodeError:
        allure.attach(response.json(), "Invalid JSON")
        raise Exception('Invalid JSON')
    except ValidationError as exc:
        allure.attach(json.dumps(response.json()), "Invalid document")
        allure.attach(json.dumps(schema["definitions"]["ErrorDTO"], indent=2), "schema")
        raise Exception(exc.message)
