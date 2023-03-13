"""Tasks for managing the data."""

import pandas as pd
import pytask

from final_project.config import BLD, SRC
from final_project.data_management import clean_data, load_data
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
    data_info = read_yaml(depends_on["data_info"])
    data_1 = pd.read_csv(depends_on["data_1"])
    data_1 = clean_data(data_1, data_info)
    data_1.to_csv(produces, index=False)


@pytask.mark.depends_on(
    {
        "scripts": ["clean_data.py"],
        "data": SRC / "data" / "data_raw.dta",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "data_clean.csv")
def task_clean_data(depends_on, produces):
    """Clean the data (Python version)."""
    data = load_data(depends_on["data"])
    data.to_csv(produces, index=False)
