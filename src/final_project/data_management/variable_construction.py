import numpy as np
import pandas as pd

from final_project.data_management import select_partial_data


def construct_control_variables_dataset(data, data_info):
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
    control_variables = pd.concat(
        [
            crop_share,
            dominant_crop_indicators,
            largest_crop_indicators,
            share_above_point_50,
            share_above_point_25,
        ],
        axis=1,
    )
    return control_variables
