# """Tasks running the core analyses."""

import pytask

from final_project.analysis.tables import create_table_1_agricultural_production_data
from final_project.config import BLD, SRC
from final_project.data_management import load_data
from final_project.utilities import read_yaml


# @pytask.mark.depends_on(
#    },
# @pytask.mark.produces(BLD / "python" / "models" / "model.pickle")
# def task_fit_model_python(depends_on, produces):
#

# for group in GROUPS:


#    @pytask.mark.depends_on(
#        },
#    @pytask.mark.task(id=group, kwargs=kwargs)
#    def task_predict_python(depends_on, group, produces):
@pytask.mark.depends_on(
    {
        "scripts": ["model.py", "predict.py"],
        "main_data": BLD / "python" / "data" / "outcome_variables_data.csv",
        "data": BLD / "python" / "data" / "geoclimatic_controls.csv",
        "data_info": SRC / "data_management" / "data_info.yaml",
    },
)
@pytask.mark.produces(
    BLD / "python" / "predictions" / "Table1_agricultural_production_data.csv",
)
def task_table_1_agricultural_production_data(depends_on, produces):
    """Clean the data (Python version)."""
    data = load_data(depends_on["data"])
    outcome_variable_data = load_data(depends_on["main_data"])
    data_info = read_yaml(depends_on["data_info"])
    outcome_variables_data = create_table_1_agricultural_production_data(
        data,
        outcome_variable_data,
        data_info,
    )
    outcome_variables_data.to_csv(produces, index=False)
