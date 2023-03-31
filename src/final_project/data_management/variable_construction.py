import numpy as np
import pandas as pd

from final_project.data_management import select_partial_data


def construct_control_variables_dataset(data, data_info, outcome_data):
    crop_share = _crop_shares(data, data_info)
    cs_no_plantaion_crop = crop_share.drop(columns=["plantation_crops"])
    # plantation_crop is included while creating largest_share categorical variable
    dominant_crop_indicators = _dominant_indicators(data=crop_share)
    # plantation_crop is excluded while creating largest_share categorical variable
    largest_crop_indicators = __max_share_dummies(
        data=cs_no_plantaion_crop,
        dummy_name="largest_",
    )
    share_above_point_50 = _above_value_indicators(data=cs_no_plantaion_crop, num=0.50)
    # subset data includes only share of  'wheat', 'corn', 'cotton', 'hay', 'animal_slaughtered'
    share_above_point_25 = _above_value_indicators(
        data=select_partial_data(
            crop_share,
            variables_list=(
                list(np.array(crop_share.columns.to_list())[[0, 2, 6, 16, 35]])
            ),
        ),
        num=0.25,
    )
    state_dummies = pd.get_dummies(outcome_data["state"]).rename(
        columns=lambda x: f"state_{x}",
    )
    control_variables = pd.concat(
        [
            crop_share,
            state_dummies,
            dominant_crop_indicators,
            largest_crop_indicators,
            share_above_point_50,
            share_above_point_25,
        ],
        axis=1,
    )
    return control_variables


def _crop_shares(data, data_info):
    data = data.drop(columns=data_info["drop_construction_variable_columns"])
    agri_crop_output = __select_agricrop_output(data, data_info)
    crop_shares = __crop_share_dataset(agri_crop_output)
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


def __crop_share_dataset(agri_crop_output):
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


def _dominant_indicators(data):
    # plantation_crop type is included
    dominant_share_dummies = __max_share_dummies(data, dummy_name="dominant_")
    # subset includes dominant_share_indicators of  'wheat', 'corn', 'cotton', 'hay', 'animal_slaughtered', 'plantation_crops'
    dominant_dummy_subset = select_partial_data(
        dominant_share_dummies,
        variables_list=(list(np.array(data.columns.to_list())[[0, 2, 6, 16, 35, 36]])),
    )
    return dominant_dummy_subset


def __max_share_dummies(data, dummy_name):
    crop_share_data = data.copy()
    crop_share_data["dominant_crop"] = data.idxmax(axis=1)
    dominant_share_dummies = pd.get_dummies(crop_share_data["dominant_crop"]).rename(
        columns=lambda x: dummy_name + str(x),
    )
    return dominant_share_dummies


def _above_value_indicators(data, num):
    share_above_value = pd.DataFrame()
    for col in data.columns:
        share_above_value[f"above_{num}_{col}"] = (data[col] > num).astype(int)
    return share_above_value
