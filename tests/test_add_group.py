import pytest
import allure
from domain_model.group import Group


@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Test add group: {json_groups}")
@pytest.mark.regression
def test_add_group(app, json_groups: Group):
    old_groups = app.group.get_group_list()
    app.group.create(json_groups)

    with allure.step('comparison of the number of groups before and after adding'):
        assert len(old_groups) + 1 == app.group.count()

    new_groups = app.group.get_group_list()
    old_groups.append(json_groups)

    with allure.step('comparison of the list of groups before and after adding'):
        assert sorted(old_groups) == sorted(new_groups)
