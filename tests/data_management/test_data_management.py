import pandas as pd
import pytest
from final_project.config import TEST_DIR
from final_project.data_management import (
    build_crop_specific_controls,
    build_dataset,
    build_geoclimatic_controls,
    build_socioeconomic_controls,
    load_data,
    select_partial_data,
)
from final_project.utilities import read_yaml


@pytest.fixture()
def data():
    return pd.read_csv(TEST_DIR / "data_management" / "test_data.csv")


@pytest.fixture()
def data_info():
    return read_yaml(TEST_DIR / "data_management" / "data_info_fixture.yaml")


def test_select_partial_data(data, data_info):
    x = select_partial_data(data=data, variables_list=data_info["variable_list"])
    assert x.columns.to_list() == ["bankdens_1920", "farmout_1860", "ShNewSkills1940"]


def test_build_dataset(data, data_info):
    x = build_dataset(data, data_info)
    assert {
        "skill_intensive_share",
        "knowledge_intensive_share",
        "agriculture_output",
    }.issubset(x.columns) is True


def test_build_geoclimatic_controls(data, data_info):
    x = build_geoclimatic_controls(
        data,
        var=data_info["geoclimatic_controls_column_rename_mapping"],
        data_info=data_info,
    )
    assert not set(data_info["drop_outcome_variables"]).intersection(set(x.columns))


def test_build_socioeconomic_controls(data, data_info):
    x = build_socioeconomic_controls(data, data_info)
    assert not set(data_info["socioeconomic_controls_rename"].keys()).intersection(
        set(x.columns),
    )


@pytest.fixture()
def setup():
    inputs = {"file_path": TEST_DIR / "data_management" / "data_info_fixture.yaml"}
    return inputs


def test_load_data(setup):
    with pytest.raises(
        ValueError,
        match="Datafile should be either .dta or .csv file!",
    ):
        load_data(setup["file_path"])


# input should have been dataset generated from constructed_variable file, not the raw_data
@pytest.mark.xfail(reason="Invalid inputs")
def test_build_crop_specific_controls(data):
    x = build_crop_specific_controls(data)
    assert {
        "dominant_corn",
    }.issubset(x.columns)
