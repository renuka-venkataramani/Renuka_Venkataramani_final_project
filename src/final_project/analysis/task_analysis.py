# """Tasks running the core analyses."""
import pandas as pd
import pytask
from statsmodels.iolib.summary2 import summary_col

from final_project.analysis.model import (
    OLS_controls_state,
    OLS_controls_state_geoclimate,
    OLS_no_controls,
)
from final_project.config import BLD, REG_GROUP, SRC

for group in REG_GROUP:

    kwargs = {
        "group": group,
    }

    @pytask.mark.depends_on(
        {
            "script": ["model.py"],
            "outcome_var_data": BLD / "python" / "data" / "outcome_variables_data.csv",
            "constructed_data": BLD / "python" / "data" / "constructed_variables.csv",
            "geo_control": BLD
            / "python"
            / "data"
            / "geoclimatic_control_variables.csv",
            "crop_controls": BLD
            / "python"
            / "data"
            / "cropspecific_control_variables.csv",
            "socio_controls": BLD
            / "python"
            / "data"
            / "socioeconomic_control_variables.csv",
            "data_info": SRC / "data_management" / "data_info.yaml",
        },
    )
    @pytask.mark.produces(
        {
            "model_1": BLD / "python" / "figures" / f"no_controls_{group}.csv",
        },
    )
    @pytask.mark.task(id=group, kwargs=kwargs)
    def task_regression_outputs(depends_on, group, produces):
        """

        Args:
            depends_on (_type_): _description_
            group (_type_): _description_
            produces (_type_): _description_.
        """
        outcome_var_data = pd.read_csv(depends_on["outcome_var_data"])
        constructed_data = pd.read_csv(depends_on["constructed_data"])
        geo_control = pd.read_csv(depends_on["geo_control"])
        pd.read_csv(depends_on["socio_controls"])
        pd.read_csv(depends_on["crop_controls"])
        no_control = OLS_no_controls(
            dependent_variable=outcome_var_data,
            endo_var=group,
            exo_var="agriculture_diversity",
        )
        control_state = OLS_controls_state(
            exo_var="agriculture_diversity",
            endo_var=group,
            constructed_data=constructed_data,
            outcome_var_data=outcome_var_data,
        )
        control_state_geoclimate = OLS_controls_state_geoclimate(
            exo_var="agriculture_diversity",
            endo_var=group,
            constructed_data=constructed_data,
            outcome_var_data=outcome_var_data,
            geo_control=geo_control,
        )
        dfoutput = summary_col(
            [no_control, control_state, control_state_geoclimate],
            stars=True,
            float_format="%0.4f",
            model_names=[
                "no_control",
                "state Fixed Effect",
                "control_state_geoclimate",
            ],
            info_dict={
                "N": lambda x: f"{int(x.nobs):d}",
                "R2": lambda x: f"{x.rsquared:.2f}",
            },
            regressor_order=["Intercept", "agriculture_diversity"],
        )
        dfoutput.tables[0].to_csv(produces["model_1"])
