import pandas as pd
from statsmodels.stats.weightstats import DescrStatsW


def create_table_1_agricultural_production_data(data, outcome_variable_data, data_info):
    """Function to create Table1: Summary statistics.

    Args:
        data (dataframe): geoclimatic controls table
        outcome_variable_data (dataframe): outcome variables/ dependent variable dataframe
        data_info (.yaml): .yaml file that describes the data

    Returns:
        Dataframe: Table 1: Agriculture_Productivity

    """
    crop_share_stat = _col_max_mean(data, outcome_variable_data, data_info)
    dominant_stat = _col_dominant_abovepoint5(custom_keywords="dominant_", data=data)
    above_point5_stat = _col_dominant_abovepoint5(
        custom_keywords="above_0.5_",
        data=data,
    )
    summary_stat = crop_share_stat.merge(dominant_stat, on="Product", how="left")
    summary_statistics = pd.concat(
        [summary_stat, above_point5_stat["above_0.5_"]],
        axis=1,
        ignore_index=True,
    ).fillna(f"{0:.2%}")
    summary_statistics.columns = ["Product", "Mean", "Maximum", "Dominant", ">50%"]
    summary_statistics = summary_statistics.replace("\\%", "", regex=True)
    return summary_statistics


def _col_max_mean(data, outcome_variable_data, data_info):
    """Subfunction to create table1.

    Args:
        data (dataframe): geoclimatic controls table
        outcome_variable_data (dataframe): outcome variables/ dependent variable dataframe
        data_info (.yaml): .yaml file that describes the data
    Returns:
        pd.Dataframe: To create 1: Maximum and 2: Minimum columns

    """
    summary_statistics = pd.DataFrame()
    for col in data_info["agriculture_products"]:  # use data_info instead
        wdf = DescrStatsW(
            data[col],
            weights=outcome_variable_data["agriculture_output"],
            ddof=1,
        )
        Mean = format(wdf.mean, ".2%")
        Max = format(data[col].max(), ".2%")
        statistics = pd.DataFrame({"Product": [col], "Mean": [Mean], "Maximum": [Max]})
        summary_statistics = pd.concat(
            [summary_statistics, statistics],
            axis=0,
            ignore_index=True,
        )
    return summary_statistics


def _col_dominant_abovepoint5(custom_keywords, data):
    """Sub-function to create Table1.

    Args:
        custom_keywords (string): dominant_ or above_.50_
        data (dataframe): Input dataframe

    Returns:
        Dataframe: Builts column 3. Dominant and 4. >50%

    """
    summary_statistics = pd.DataFrame()
    for col in data.filter(
        like=custom_keywords,
    ).columns.to_list():  # use data_info instead
        Mean = format(data[col].mean(), ".2%")
        statistics = pd.DataFrame({custom_keywords: [Mean], "Product": [col]})
        statistics["Product"] = statistics["Product"].str.replace(
            custom_keywords,
            "",
            regex=True,
        )
        summary_statistics = pd.concat(
            [summary_statistics, statistics],
            axis=0,
            ignore_index=True,
        )
    return summary_statistics
