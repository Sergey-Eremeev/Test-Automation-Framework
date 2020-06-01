import pytest
import allure
from domain_model.group import Group
import random


@allure.severity(allure.severity_level.CRITICAL)
@allure.title('Test modify group name')
@pytest.mark.regression
def test_modify_group(app, json_groups: Group):
    if app.group.count() == 0:
        app.group.create(Group(name='test'))
    old_groups = app.group.get_group_list()
    group = random.choice(old_groups)

    app.group.modify_group_by_id(group.id, json_groups)
    new_groups = app.group.get_group_list()

    with allure.step('comparison of the number of groups before and after modify'):
        assert len(old_groups) == len(new_groups)

    old_groups[old_groups.index(group)] = group + json_groups

    with allure.step('comparison of the list of groups before and after modify'):
        assert sorted(old_groups) == sorted(new_groups)
