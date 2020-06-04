import allure
from domain_model.group import Group


class GroupObject:

    def __init__(self, app):
        self.app = app

    def create(self, group):
        with allure.step(f'create group: {group}'):
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
            if not (wd.current_url.endswith('/group.php') and len(wd.find_elements_by_name('new')) > 0):
                wd.find_element_by_link_text("groups").click()

    def fill_group_form(self, group):
        with allure.step(f'fill group form {group}'):
            self.change_field_value('group_name', group.name)
            self.change_field_value('group_header', group.header)
            self.change_field_value('group_footer', group.footer)

    def change_field_value(self, field_name, text):
        with allure.step(f'change field value {field_name}:{text}'):
            wd = self.app.wd
            if text is not None:
                wd.find_element_by_name(field_name).click()
                wd.find_element_by_name(field_name).clear()
                wd.find_element_by_name(field_name).send_keys(f"{text}")

    def return_to_groups_page(self):
        with allure.step('return to groups page'):
            wd = self.app.wd
            wd.find_element_by_link_text('groups').click()

    def count(self):
        with allure.step('count groups'):
            wd = self.app.wd
            self.open_groups_page()
            return len(wd.find_elements_by_name('selected[]'))

    group_cache = None

    def get_group_list(self):
        if self.app.db is None:
            with allure.step('get group list through UI'):
                if self.group_cache is None:
                    wd = self.app.wd
                    self.open_groups_page()
                    self.group_cache = []
                    for element in wd.find_elements_by_css_selector('span.group'):
                        text = element.text
                        id = element.find_element_by_name('selected[]').get_attribute('value')
                        self.group_cache.append(Group(name=text, id=id))
            return list(self.group_cache)
        else:
            with allure.step('get group list from DB'):
                if self.group_cache is None:
                    self.group_cache = []
                    self.group_cache = self.app.db.get_group_list()
            return list(self.group_cache)

    def delete_group_by_id(self, id):
        wd = self.app.wd
        self.open_groups_page()
        self.select_group_by_id(id)

        with allure.step('submit deletion'):
            wd.find_element_by_name('delete').click()

        self.return_to_groups_page()
        self.group_cache = None

    def select_group_by_id(self, id):
        with allure.step(f'select group by id: {id}'):
            wd = self.app.wd
            wd.find_element_by_css_selector(f'input[value="{id}"]').click()

    def modify_group_by_id(self, id, new_group_data):
        with allure.step(f'modify group by id: {id}:{new_group_data}'):
            wd = self.app.wd
            self.open_groups_page()
            self.select_group_by_id(id)

            with allure.step('open modification form'):
                wd.find_element_by_name('edit').click()

            self.fill_group_form(new_group_data)

            with allure.step('submit modification'):
                wd.find_element_by_name('update').click()

            self.return_to_groups_page()
            self.group_cache = None
