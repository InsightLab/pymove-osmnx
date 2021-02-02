from typing import Any, List, Optional, Text, Union

from pandas.core.frame import DataFrame


def feature_values_using_filter(
    move_data: DataFrame,
    id_: Union[Text, int],
    feature_name: Text,
    filter_: List,
    values: Any,
    inplace: Optional[bool] = True
) -> Optional[DataFrame]:
    """
    Changes the values of the feature defined by the user.
    Parameters
    ----------
    move_data : DataFrame
       The input trajectories data.
    id_ : str
        Indicates the index to be changed.
    feature_name : str
        The name of the column that the user wants to change values for.
    filter_ : list or array
        Indicates the rows with the index "id_" of the "feature_name"
        that must be changed.
    values : any
        THe new values to be set to the selected feature.
    inplace: boolean, optional(True by default)
        if set to true the original dataframe will be altered,
        otherwise the alteration will be made in a copy, that will be returned.
    Returns
    -------
    DataFrame
        A copy of the original dataframe or None

    """

    if not inplace:
        move_data = move_data.copy()

    values_feature = move_data.at[id_, feature_name]

    if filter_.shape == ():
        move_data.at[id_, feature_name] = values
    else:
        values_feature.iloc[filter_] = values
        move_data.at[id_, feature_name] = values_feature

    if not inplace:
        return move_data
    else:
        return None


def feature_values_using_filter_and_indexes(
    move_data: DataFrame,
    id_: Union[int, Text],
    feature_name: Text,
    filter_: List,
    idxs: List,
    values: Any,
    inplace: Optional[bool] = True
):
    """
    Create or update move and stop by radius.
    Parameters
    ----------
    move_data : dataframe
       The input trajectories data.
    id_ : str
        Indicates the index to be changed.
    feature_name : str
        The name of the column that the user wants to change values for.
    filter_ : array
        Indicates the rows with the index "id_" of the "feature_name"
        that must be changed.
    idxs : array like of indexes
        Indexes to atribute value
    values : any
        The new values to be set to the selected feature.
    inplace: bool, optional
        if set to true the original dataframe will be altered,
        otherwise the alteration will be made in a copy, that will be returned,
        by default True

    Returns
    -------
    DataFrame
        A copy of the original dataframe or None
    """

    if not inplace:
        move_data = move_data.copy()

    values_feature = move_data.at[id_, feature_name]
    values_feature_filter = values_feature.iloc[filter_]
    values_feature_filter.iloc[idxs] = values
    values_feature.iloc[filter_] = values_feature_filter
    move_data.at[id_, feature_name] = values_feature

    if not inplace:
        return move_data
    else:
        return None
