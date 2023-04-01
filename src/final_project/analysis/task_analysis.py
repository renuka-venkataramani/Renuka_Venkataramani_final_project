# """Tasks running the core analyses."""
import pandas as pd
import pytask

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
            "model_1": BLD / "python" / "figures" / f"no_controls_{group}.png",
            "model_2": BLD / "python" / "figures" / f"state_{group}.png",
            "model_3": BLD / "python" / "figures" / f"state_geo_{group}.png",
            "model_4": BLD / "python" / "figures" / f"state_geo_crop_{group}.png",
            "model_5": BLD / "python" / "figures" / f"state_geo_crop_socio_{group}.png",
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
        model_1 = OLS_no_controls(
            dependent_variable=outcome_var_data,
            endo_var=group,
            exo_var="agriculture_diversity",
        )
        model_2 = OLS_controls_state(
            exo_var="agriculture_diversity",
            endo_var=group,
            constructed_data=constructed_data,
            outcome_var_data=outcome_var_data,
        )
        model_3 = OLS_controls_state_geoclimate(
            exo_var="agriculture_diversity",
            endo_var=group,
            constructed_data=constructed_data,
            outcome_var_data=outcome_var_data,
            geo_control=geo_control,
        )
        model_1.savefig(produces["model1"])
        model_2.savefig(produces["model1"])
        model_3.savefig(produces["model1"])
