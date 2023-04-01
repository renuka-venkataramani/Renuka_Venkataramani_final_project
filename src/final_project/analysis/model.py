import pandas as pd
import statsmodels.api as sm


def OLS_no_controls(dependent_variable, endo_var):
    model = sm.formula.ols(
        formula="endo_var ~ agriculture_diversity",
        data=dependent_variable,
    )
    return model


# ols regression:
def OLS_controls_state(state_fixed_effects, endo_var, dependent_variable):
    """OLS regression1:  controls: state FE.

    Args:
        constructed_data (dataframe): constructed dataframe
        outcome_var_data (dataframe): outcome variable dataframe

    Returns:
        _model: Regression_output

    """
    model_data = state_fixed_effects
    mod = _create_OLS_formula(model_data, endo_var, dependent_variable)
    return mod


def _create_OLS_formula(
    model_data,
    endo_var,
    dependent_variable,
    exo_var="agriculture_diversity",
):
    """Sub function to create ols formula and regression table.

    Args:
        model_data (dataframe): regression data

    Returns:
        expression: regression output

    """
    model_data_1 = model_data.copy()
    model_data_1.columns = [f"C({c})" for c in model_data.columns]
    all_columns = "+".join(model_data_1.columns)
    ols_formula = "{endo_var} ~ {exo_var}" + "+" + all_columns
    model_data = pd.concat([model_data, dependent_variable], axis=1)
    mod = sm.formula.ols(formula=ols_formula, data=model_data)
    return mod


def OLS_controls_state_geoclimate(
    state_fixed_effects,
    geoclimatic_controls,
    endo_var,
    dependent_variable,
):
    model_data = pd.concat([state_fixed_effects, geoclimatic_controls], axis=1)
    mod = _create_OLS_formula(model_data)
    return mod


def OLS_controls_state_geo_crop(
    state_fixed_effects,
    dependent_variable,
    geoclimatic_controls,
    crop_specific_controls,
):
    model_data = pd.concat(
        [state_fixed_effects, geoclimatic_controls, crop_specific_controls],
        axis=1,
    )
    mod = _create_OLS_formula(model_data)
    return mod


def OLS_controls_state_geo_crop_socio(
    state_fixed_effects,
    dependent_variable,
    geoclimatic_controls,
    crop_specific_controls,
    socioeconomic_controls,
    endo_var,
):
    model_data = pd.concat(
        [
            state_fixed_effects,
            geoclimatic_controls,
            crop_specific_controls,
            socioeconomic_controls,
        ],
        axis=1,
    )
    mod = _create_OLS_formula(model_data)
    return mod
