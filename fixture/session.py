import allure


class SessionObject:

    def __init__(self, app):
        self.app = app

    def login(self, username, password):
        with allure.step(f'login: {username}'):
            wd = self.app.wd
            self.app.open_home_page()
            wd.find_element_by_name("user").clear()
            wd.find_element_by_name("user").send_keys(f'{username}')
            wd.find_element_by_name("pass").click()
            wd.find_element_by_name("pass").clear()
            wd.find_element_by_name("pass").send_keys(f'{password}')
            wd.find_element_by_css_selector('input[type="submit"]').click()

    def logout(self):
        with allure.step('logout'):
            wd = self.app.wd
            wd.find_element_by_link_text('Logout').click()

    def is_logged_in(self):
        with allure.step('is logged in'):
            wd = self.app.wd
            return len(wd.find_elements_by_link_text('Logout')) > 0

    def is_logged_in_as(self, username):
        with allure.step(f'is logged in as: {username}'):
            return self.get_logged_user() == username

    def get_logged_user(self):
        with allure.step('get logged user'):
            wd = self.app.wd
            return wd.find_element_by_xpath('//div/div[1]/form/b').text[1:-1]

    def ensure_logout(self):
        with allure.step('ensure logout'):
            if self.is_logged_in():
                self.logout()

    def ensure_login(self, username, password):
        with allure.step(f'ensure login: {username}'):
            if self.is_logged_in():
                if self.is_logged_in_as(username):
                    return
                else:
                    self.logout()
            self.login(username, password)
