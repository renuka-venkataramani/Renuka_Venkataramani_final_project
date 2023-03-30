"""Tasks for managing the data."""

import pytask

from final_project.config import BLD, SRC
from final_project.data_management import (
    build_dataset,
    load_data,
)
from final_project.utilities import read_yaml


@pytask.mark.depends_on(
    {
        "scripts": ["clean_data.py"],
        "data_info": SRC / "data_management" / "data_info.yaml",
        "data_1": SRC / "data" / "data.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "data_clean1.csv")
def task_clean_data_python(depends_on, produces):
    """Clean the data (Python version)."""
    read_yaml(depends_on["data_info"])
    data_1 = load_data(depends_on["data_1"])
    data_1.to_csv(produces, index=False)


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
