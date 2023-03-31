"""Tasks for managing the data."""

import pytask

from final_project.config import BLD, SRC
from final_project.data_management import (
    build_crop_specific_controls,
    build_dataset,
    build_geoclimatic_controls,
    build_socioeconomic_controls,
    construct_control_variables_dataset,
    load_data,
)
from final_project.utilities import read_yaml


@pytask.mark.depends_on(
    {
        "scripts": ["clean_data.py"],
        "data_info": SRC / "data_management" / "data_info.yaml",
        "data": SRC / "data" / "data_raw.dta",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "outcome_variables_data.csv")
def task_build_dataset(depends_on, produces):
    """Clean the data (Python version)."""
    data = load_data(depends_on["data"])
    data_info = read_yaml(depends_on["data_info"])
    outcome_variables_data = build_dataset(data=data, data_info=data_info)
    outcome_variables_data.to_csv(produces, index=False)


@pytask.mark.depends_on(
    {
        "scripts": ["variable_construction.py"],
        "data_info": SRC / "data_management" / "data_info.yaml",
        "data": SRC / "data" / "data_to_construct_variables.dta",
        "outcome_data": SRC / "data" / "data_raw.dta",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "constructed_variables.csv")
def task_constructed_variables(depends_on, produces):
    """Clean the data (Python version)."""
    data = load_data(depends_on["data"])
    outcome_data = load_data(depends_on["outcome_data"])
    data_info = read_yaml(depends_on["data_info"])
    outcome_variables_data = construct_control_variables_dataset(
        data,
        data_info,
        outcome_data,
    )
    outcome_variables_data.to_csv(produces, index=False)


@pytask.mark.depends_on(
    {
        "scripts": ["variable_construction.py"],
        "data_info": SRC / "data_management" / "data_info.yaml",
        "constructed_data": BLD / "python" / "data" / "constructed_variables.csv",
        "data": SRC / "data" / "data_raw.dta",
    },
)
@pytask.mark.produces(
    {
        "geoclimatic": BLD / "python" / "data" / "geoclimatic_control_variables.csv",
        "socioeconomic": BLD
        / "python"
        / "data"
        / "socioeconomic_control_variables.csv",
        "crop_specific": BLD / "python" / "data" / "cropspecific_control_variables.csv",
    },
)
def task_build_control_variables(depends_on, produces):
    """Clean the data (Python version)."""
    data = load_data(depends_on["data"])
    constructed_data = load_data(depends_on["constructed_data"])
    data_info = read_yaml(depends_on["data_info"])
    geoclimatic_controls_data = build_geoclimatic_controls(
        data,
        var=data_info["geoclimatic_controls_column_rename_mapping"],
        data_info=data_info,
    )
    socioeconomic_controls = build_socioeconomic_controls(data, data_info)
    crop_specific_controls = build_crop_specific_controls(sub_data=constructed_data)
    geoclimatic_controls_data.to_csv(produces["geoclimatic"], index=False)
    socioeconomic_controls.to_csv(produces["socioeconomic"], index=False)
    crop_specific_controls.to_csv(produces["crop_specific"], index=False)
