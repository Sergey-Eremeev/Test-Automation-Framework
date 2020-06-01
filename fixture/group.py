import allure
from domain_model.group import Group


class GroupObject:

    def __init__(self, app):
        self.app = app

    def create(self, group):
        with allure.step('create group'):
            wd = self.app.wd
            self.open_groups_page()

            with allure.step('init group creation'):
                wd.find_element_by_name("new").click()

            self.fill_group_form(group)

            with allure.step('submit group creation'):
                wd.find_element_by_name("submit").click()

            self.return_to_groups_page()
            self.group_cache = None

    def open_groups_page(self):
        with allure.step('Open groups page'):
            wd = self.app.wd
            if not (wd.current_url.endswith("/group.php") and len(wd.find_elements_by_name("new")) > 0):
                wd.find_element_by_link_text("groups").click()

    def fill_group_form(self, group):
        with allure.step('fill group form'):
            self.change_field_value("group_name", group.name)
            self.change_field_value("group_header", group.header)
            self.change_field_value("group_footer", group.footer)

    def change_field_value(self, field_name, text):
        with allure.step('change field value'):
            wd = self.app.wd
            if text is not None:
                wd.find_element_by_name(field_name).click()
                wd.find_element_by_name(field_name).clear()
                wd.find_element_by_name(field_name).send_keys("%s" % text)

    def return_to_groups_page(self):
        with allure.step('return to groups page'):
            wd = self.app.wd
            wd.find_element_by_link_text("groups").click()

    def count(self):
        with allure.step('count groups'):
            wd = self.app.wd
            self.open_groups_page()
            return len(wd.find_elements_by_name("selected[]"))

    group_cache = None

    def get_group_list(self):
        with allure.step('get group list'):
            if self.group_cache is None:
                wd = self.app.wd
                self.open_groups_page()
                self.group_cache = []
                for element in wd.find_elements_by_css_selector("span.group"):
                    text = element.text
                    id = element.find_element_by_name("selected[]").get_attribute("value")
                    self.group_cache.append(Group(name=text, id=id))
        return list(self.group_cache)
