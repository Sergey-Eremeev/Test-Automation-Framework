from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from fixture.session import SessionObject
from fixture.group import GroupObject


class Application:

    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox(executable_path='./driver/geckodriver')
        elif browser == "chrome":
            self.wd = webdriver.Chrome(executable_path='./driver/chromedriver')
        elif browser == "ie":
            self.wd = webdriver.Ie()
        elif browser == "remote":
            self.wd = webdriver.Remote(
                command_executor='http://192.168.1.39:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME,
            )
        else:
            raise ValueError(f"Unrecognized browser: {browser}")

        self.wd.implicitly_wait(1)
        self.session = SessionObject(self)
        self.group = GroupObject(self)
        self.base_url = base_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()
