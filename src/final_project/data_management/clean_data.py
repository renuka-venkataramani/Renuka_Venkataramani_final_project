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
    """To select a part of the data from the main data set.

    Args:
        data (pd.DataFrame): DataFrame from which subset data should be extracted
        variables_list (list): List of columns to be included in the dataset

    Returns:
        pd.DataFrame: a partial subset of the main DataFrame

    """
    outcome_variables_data = pd.DataFrame()
    for col_name in variables_list:
        outcome_variable = data.loc[:, data.columns.str.contains(col_name)]
        outcome_variables_data = pd.concat(
            [outcome_variables_data, outcome_variable],
            axis=1,
        )
    return outcome_variables_data


def build_dataset(data, data_info):
    """To build outcome/dependent variables dataset. Renames all the columns to
    meaningful names.

    Args:
        data (pd.DataFrame): raw_file that needs to be cleaned
        data_info (.yaml file): contains the name of the dictionaries used to rename the columns.

    Returns:
        pd.DataFrame: Returns datframe containing all the dependent variable used in the anlaysis

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
    """It is a sub function as a part of build_dataset func. Cannot be used
    individually. Removes nan values if present in all the rows, and drops unwanted
    columns.

    Args:
        data (pd.DataFrame): DataFrame to be cleaned
        data_info (.yaml): Contains list and dictionaries with information about the data

    Returns:
        pd.Dataframe: Returns cleaned dataframe

    """
    for col in data.filter(like="state_").columns.to_list():
        data = data.drop(columns=col)
    data = data.drop(columns=data_info["drop_outcome_variables"])
    return data


def _change_column_names(custom_rename_func):
    """Func used to rename timeseries column names with '_' in between and a year at
    last.

    Args:
        custom_rename_func (func reference): user-defined func given as an input to the main func. Func uses decorators

    """

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
    """A function that makes changes to the _change_column_names func added as a
    decorator.

    Args:
        data_subset (dataframe): Subset that contains 'DivMf' columns
        data_info (.yaml): Contains list and dictionaries with information about the data

    Returns:
        Dataframe : Dataframe with DivMf columns appropriately renamed

    """
    rename_DivMf_col = (
        "manufacturing_diversity"
        + "_"
        + data_subset.filter(like="DivMf").columns.to_series().str[5:9]
    )
    data_subset.rename(columns=rename_DivMf_col.to_dict(), inplace=True)
    return data_subset


def build_geoclimatic_controls(data, var, data_info):
    """Builds dataset containing geoclimatic control variables.

    Args:
        data (dataframe): The source data
        var (dict): dictionary taken from data_info that contains rename keys and values
        data_info (.yaml): Description of the columns in data

    Returns:
        Dataframe: Geoclimatic dataframe

    """
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
    """Build socioeconomic control variables datasets.

    Args:
        data (pd.DataFrame): Socioeconomic DataFrame to be cleaned
        data_info (.yaml): Contains list and dictionaries with information about the data

    Returns:
        dataframe: returns dataframe containing socioeconomic controls

    """
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
    """Build crop-specific control variables datasets.

    Args:
        data (pd.DataFrame): crop-specific DataFrame to be cleaned
        data_info (.yaml): Contains list and dictionaries with information about the data

    Returns:
        dataframe: returns dataframe containing socioeconomic controls

    """
    crop_specific_controls = select_partial_data(
        data=sub_data,
        variables_list=sub_data.filter(like="dominant_").columns.to_list(),
    )
    return crop_specific_controls
