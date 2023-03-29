import pandas as pd

from final_project.data_management import select_partial_data


def _construct_crop_shares(data, data_info):
    data = data.drop(columns=data_info["drop_construction_variable_columns"])
    agri_crop_output = __select_agricrop_output(data, data_info)
    crop_shares = __construct_crop_share_dataset(agri_crop_output)
    return crop_shares


def __select_agricrop_output(data, data_info):
    agri_crop_output_col = (
        data.filter(like="ag10").columns.to_list()
        + data.filter(like="agz00").columns.to_list()
    )
    agri_crop_output = select_partial_data(
        data=data,
        variables_list=agri_crop_output_col,
    )
    agri_crop_output.rename(
        columns={
            agri_crop_output_col[i]: data_info["agriculture_products"][i]
            for i in range(len(agri_crop_output_col))
        },
        inplace=True,
    )
    agri_crop_output["plantation_crops"] = (
        agri_crop_output.iloc[:, 4]
        + agri_crop_output.iloc[:, 5]
        + agri_crop_output.iloc[:, 27]
        + agri_crop_output.iloc[:, 29]
    )
    return agri_crop_output


def __construct_crop_share_dataset(agri_crop_output):
    farm_output = agri_crop_output.sum(axis=1)
    crop_share_data = pd.DataFrame()
    for col in agri_crop_output.columns:
        agri_crop_shares = pd.DataFrame()
        for i, output in enumerate(agri_crop_output[col]):
            agri_crop_share = pd.DataFrame(pd.Series(output / farm_output[i]))
            agri_crop_shares = pd.concat(
                [agri_crop_shares, agri_crop_share],
                axis=0,
                ignore_index=True,
            )
        crop_share_data = pd.concat([crop_share_data, agri_crop_shares], axis=1)
    crop_share_data.columns = agri_crop_output.columns.to_list()
    return crop_share_data
