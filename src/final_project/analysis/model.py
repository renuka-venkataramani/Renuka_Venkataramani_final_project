import pandas as pd
import statsmodels.api as sm


def OLS_no_controls(dependent_variable, endo_var, exo_var="agriculture_diversity"):
    model = sm.formula.ols(
        formula=f"{endo_var} ~ {exo_var}",
        data=dependent_variable,
    )
    res = model.fit()
    return res


# ols regression:
def OLS_controls_state(exo_var, endo_var, constructed_data, outcome_var_data):
    model_data = constructed_data.filter(like="state_")
    dependent_variable = outcome_var_data[[endo_var, "agriculture_diversity"]]
    model_data_1 = model_data.copy()
    model_data_1.columns = [f"C({c})" for c in model_data.columns]
    all_columns = "+".join(model_data_1.columns)
    ols_formula = f"{endo_var} ~ {exo_var}" + "+" + all_columns
    model_data = pd.concat([model_data, dependent_variable], axis=1)
    model_state_FE = sm.formula.ols(formula=ols_formula, data=model_data)
    res = model_state_FE.fit()
    return res


def OLS_controls_state_geoclimate(
    exo_var,
    endo_var,
    constructed_data,
    outcome_var_data,
    geo_control,
):
    state_fixed_effects = constructed_data.filter(like="state_")
    dependent_variable = outcome_var_data[[endo_var, "agriculture_diversity"]]
    geoclimatic_controls = geo_control[
        [
            "county_area",
            "temperature",
            "latitude",
            "longitude",
            "avr_crop_specific_productivity",
            "max_crop_specific_productivity",
        ]
    ]
    model_data = pd.concat([state_fixed_effects, geoclimatic_controls], axis=1)
    model_data.columns = [f"C({c})" for c in model_data.columns]
    all_columns = "+".join(model_data.columns)
    ols_formula = f"{endo_var} ~ {exo_var}" + "+" + all_columns
    model_data_FE = pd.concat(
        [state_fixed_effects, dependent_variable, geoclimatic_controls],
        axis=1,
    )
    model_state_control = sm.formula.ols(formula=ols_formula, data=model_data_FE)
    res = model_state_control.fit()
    return res
