"""Function(s) for cleaning the data set(s)."""


import pandas as pd


def load_data(file_path):
    """This function imports either stata or csv data file.

    Args:
    file_path (str): The path to the data file.

    Returns:
    data (pandas.DataFrame): Data in pandas dataframe

    """
    file_extension = str(file_path).split(".")[-1]
    try:
        if any(i in "dta" for i in file_extension) is True:
            data = pd.read_stata(file_path)
        else:
            data = pd.read_csv(file_path)
    except ValueError as error:
        info = "Datafile should be either .dta or .csv file!"
        raise ValueError(info) from error
    return data


def select_partial_data(data, variables_list):
    outcome_variables_data = pd.DataFrame()
    for col_name in variables_list:
        outcome_variable = data.loc[:, data.columns.str.contains(col_name)]
        outcome_variables_data = pd.concat(
            [outcome_variables_data, outcome_variable],
            axis=1,
        )
    return outcome_variables_data


def build_dataset(data, data_info):
    """

    Args:
        data (_type_): _description_
        data_info (_type_): _description_.
    """
    # keep columns present in data_info['outcome_variables']
    cross_sectional_data = select_partial_data(
        data=data,
        variables_list=data_info["outcome_variables_cs_rename_mapping"].keys(),
    )
    cross_sectional_data = _drop_nan(data=cross_sectional_data, data_info=data_info)
    cross_sectional_data.rename(
        columns=data_info["outcome_variables_cs_rename_mapping"],
        inplace=True,
    )
    time_series_variable_rename = _outcome_variables_rename(
        data_subset=select_partial_data(
            data=data,
            variables_list=data_info["outcome_variables_ts_rename_mapping"].keys(),
        ),
        data_info=data_info,
    )
    outcome_variables_data = pd.concat(
        [cross_sectional_data, time_series_variable_rename],
        axis=1,
    )
    return outcome_variables_data


def _drop_nan(data, data_info):
    """"""
    for col in data.filter(like="state_").columns.to_list():
        data = data.drop(columns=col)
    data = data.drop(columns=data_info["drop_outcome_variables"])
    return data


def _change_column_names(custom_rename_func):
    def _rename_columns(data_subset, data_info):
        change_col_name = (
            data_subset.filter(like="_")
            .columns.to_series()
            .str.rsplit("_")
            .str[-2]
            .map(data_info["outcome_variables_ts_rename_mapping"])
            + "_"
            + data_subset.filter(like="_").columns.to_series().str.rsplit("_").str[-1]
        )
        data_subset.rename(columns=change_col_name.to_dict(), inplace=True)
        custom_rename_func(data_subset, data_info)
        return data_subset

    return _rename_columns


@_change_column_names
def _outcome_variables_rename(data_subset, data_info):
    rename_DivMf_col = (
        "manufacturing_diversity"
        + "_"
        + data_subset.filter(like="DivMf").columns.to_series().str[5:9]
    )
    data_subset.rename(columns=rename_DivMf_col.to_dict(), inplace=True)
    return data_subset


def build_geoclimatic_controls(data, var, data_info):
    geoclimatic_data = select_partial_data(data=data, variables_list=var.keys())
    for key, value in var.items():
        geoclimatic_data.columns = geoclimatic_data.columns.str.replace(key, value)
    subset_geo_control = select_partial_data(
        data=data,
        variables_list=data_info["agriculture_products"],
    )
    geoclimatic_data = pd.concat([geoclimatic_data, subset_geo_control], axis=1)
    return geoclimatic_data


def build_socioeconomic_controls(data, data_info):
    socioeconomic_controls = select_partial_data(
        data=data,
        variables_list=data_info["socioeconomic_controls_rename"].keys(),
    )
    socioeconomic_controls.rename(
        columns=data_info["socioeconomic_controls_rename"],
        inplace=True,
    )
    return socioeconomic_controls


def build_crop_specific_controls(sub_data):
    crop_specific_controls = select_partial_data(
        data=sub_data,
        variables_list=sub_data.filter(like="dominant_").columns.to_list(),
    )
    return crop_specific_controls
