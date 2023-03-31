import pytest
from final_project.config import TEST_DIR
from final_project.data_management import (
    select_partial_data,
)
from final_project.utilities import read_yaml


@pytest.fixture()
def data():
    return pd.read_csv(TEST_DIR / "data_management" / "test_data.csv")


@pytest.fixture()
def data_info():
    return read_yaml(TEST_DIR / "data_management" / "data_info_fixture.yaml")


def test_select_partial_data(data, variable_list):
    x = select_partial_data(
        data=data,
        variable_list=["bankdens_1920", "farmout_1860", "ShNewSkills1940"],
    )
    assert x.columns.to_list() == ["bankdens_1920", "farmout_1860", "ShNewSkills1940"]
