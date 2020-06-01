import pytest
import allure
from domain_model.group import Group
import random


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Test delete some group")
@pytest.mark.regression
def test_delete_some_group(app):
    if app.group.count() == 0:
        app.group.create(Group(name="test"))

    old_groups = app.group.get_group_list()
    group = random.choice(old_groups)
    app.group.delete_group_by_id(group.id)
    new_groups = app.group.get_group_list()

    with allure.step('comparison of the number of groups before and after removal'):
        assert len(old_groups) - 1 == len(new_groups)

    old_groups.remove(group)

    with allure.step('comparison of the number of groups before and after removal'):
        assert old_groups == new_groups
