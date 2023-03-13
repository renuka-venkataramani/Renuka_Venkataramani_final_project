"""Function(s) for cleaning the data set(s)."""

import pandas as pd


def clean_data(data_1, data_info):
    """Clean data set.

    Information on data columns is stored in ``data_management/data_info.yaml``.

    Args:
        data (pandas.DataFrame): The data set.
        data_info (dict): Information on data set stored in data_info.yaml. The
            following keys can be accessed:
            - 'outcome': Name of dependent variable column in data
            - 'outcome_numerical': Name to be given to the numerical version of outcome
            - 'columns_to_drop': Names of columns that are dropped in data cleaning step
            - 'categorical_columns': Names of columns that are converted to categorical
            - 'column_rename_mapping': Old and new names of columns to be renamend,
                stored in a dictionary with design: {'old_name': 'new_name'}
            - 'url': URL to data set

    Returns:
        pandas.DataFrame: The cleaned data set.

    """
    data_1 = data_1.drop(columns=data_info["columns_to_drop"])
    data_1 = data_1.dropna()
    for cat_col in data_info["categorical_columns"]:
        data_1[cat_col] = data_1[cat_col].astype("category")
    data_1 = data_1.rename(columns=data_info["column_rename_mapping"])

    numerical_outcome = pd.Categorical(data_1[data_info["outcome"]]).codes
    data_1[data_info["outcome_numerical"]] = numerical_outcome

    return data_1


def load_data(file_path):
    """This function imports either stata or csv data file.

    Parameters
    ----------
    file_path:  str
         The path to the data file.

    Returns:
    -------
    df: pd.DataFrame
        Data in pandas dataframe

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
