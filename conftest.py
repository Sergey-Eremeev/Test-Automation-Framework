import pytest
import json
import jsonpickle
import os.path
import importlib
from fixture.application import Application

fixture_app = None
config = None


def load_config(file):
    global config
    if config is None:
        config_file = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)), file
        )
        with open(config_file) as f:
            config = json.load(f)
    return config


@pytest.fixture
def app(request):
    global fixture_app

    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--config"))["web"]
    if fixture_app is None or not fixture_app.is_valid():
        fixture_app = Application(
            browser=browser,
            base_url=web_config["baseUrl"]
        )
    fixture_app.session.ensure_login(
        username=web_config["username"],
        password=web_config["password"]
    )
    return fixture_app


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture_app.session.ensure_logout()
        fixture_app.destroy()

    request.addfinalizer(fin)
    return fixture_app


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--config", action="store", default="config.json")


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("json_"):
            testdata = load_form_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])


def load_form_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())
