import time
from typing import Optional, Text

import numpy as np
import osmnx as ox
from pandas import DataFrame, Timestamp
from pymove.utils.constants import TID
from pymove.utils.log import progress_bar
from pymove.utils.trajectories import shift
from scipy.interpolate import interp1d

from pymove_osmnx.utils.transformation import (
    feature_values_using_filter,
    feature_values_using_filter_and_indexes,
)


def check_time_dist(
    move_data: DataFrame,
    index_name: Optional[Text] = TID,
    tids: Optional[Text] = None,
    max_dist_between_adj_points: Optional[float] = 5000,
    max_time_between_adj_points: Optional[float] = 900,
    max_speed: Optional[float] = 30
):
    """
    Used to verify that the trajectories points are in the correct order after
    map matching, considering time and distance.

    Parameters
    ----------
    move_data : dataframe
     The input trajectories data
    index_name: str, optional
     The name of the column to set as the new index during function execution,
     by default TID
    tids: array, optional
     The list of the unique keys of the index_name column, by default None
    max_dist_between_adj_points: float, optional
     The maximum distance between two adjacent points, by default 5000
    max_time_between_adj_points: float, optional
     The maximum time interval between two adjacent points, by default 900
    max_speed: float, optional
     The maximum speed between two adjacent points, by default 30

    Raises
    ------
    ValueError
        if the data is not in order
    """
    if move_data.index.name is not None:
        print('reseting index...')
        move_data.reset_index(inplace=True)

    if tids is None:
        tids = move_data[index_name].unique()

    if move_data.index.name is None:
        print('creating index...')
        move_data.set_index(index_name, inplace=True)

    move_data['isNone'] = move_data['datetime'].isnull()

    for tid in progress_bar(
        tids, desc='checking ascending distance and time'
    ):
        filter_ = move_data.at[tid, 'isNone']

        # be sure that distances are in ascending order
        dists = move_data.at[tid, 'distFromTrajStartToCurrPoint'][filter_]
        if not np.all(dists[:-1] < dists[1:]):
            raise ValueError('distance feature is not in ascending order')

        # be sure that times are in ascending order
        times = move_data.at[tid, 'datetime'][filter_].astype(int)
        if not np.all(times[:-1] < times[1:]):
            raise ValueError('time feature is not in ascending order')

    count = 0

    for tid in progress_bar(
        tids, desc='checking delta_times, delta_dists and speeds'
    ):
        filter_ = move_data.at[tid, 'isNone']

        dists = move_data.at[tid, 'distFromTrajStartToCurrPoint'][filter_]
        delta_dists = (shift(dists, -1) - dists)[
            :-1
        ]

        if not np.all(delta_dists <= max_dist_between_adj_points):
            raise ValueError(
                'delta_dists must be <= {}'.format(
                    max_dist_between_adj_points
                )
            )

        times = move_data.at[tid, 'datetime'][filter_].astype(int)
        delta_times = ((shift(times, -1) - times) / 1000.0)[
            :-1
        ]

        if not np.all(delta_times <= max_time_between_adj_points):
            raise ValueError(
                'delta_times must be <= {}'.format(
                    max_time_between_adj_points
                )
            )

        if not np.all(delta_times > 0):
            raise ValueError('delta_times must be > 0')

        speeds = delta_dists / delta_times
        if not np.all(speeds <= max_speed):
            raise ValueError('speeds > {}'.format(max_speed))

        size_id = 1 if filter_.shape == () else filter_.shape[0]
        count += size_id

    move_data.reset_index(inplace=True)


def fix_time_not_in_ascending_order_id(
    move_data: DataFrame,
    id_: Text,
    index_name: Optional[Text] = TID,
    inplace: Optional[bool] = True
) -> Optional[DataFrame]:
    """
    Used to correct time order between points of a  trajectory, after map
    matching operations.

    Parameters
    ----------
    move_data : dataframe
       The input trajectories data
    id_ : str
        The tid of the trajectory the user want to correct.
    index_name: str, optional
        The name of the column to set as the new index during function execution.
        Indicates the tid column, by default TID
    inplace: boolean, optional
        if set to true the original dataframe will be altered,
        otherwise the alteration will be made in a copy, that will be returned,
        by default True

    Returns
    -------
    DataFrame
        Dataframe sorted by time on id_ or none

    Notes
    -----
        Do not use trajectories with only 1 point.
    """

    if not inplace:
        move_data = move_data.copy()

    if 'deleted' not in move_data:
        move_data['deleted'] = False

    if move_data.index.name is None:
        print('creating index...')
        move_data.set_index(index_name, inplace=True)

    move_data['isNone'] = move_data['datetime'].isnull()

    filter_ = move_data.at[id_, 'isNone'] & ~move_data.at[id_, 'deleted']

    if filter_.shape == ():
        move_data.at[id_, 'deleted'] = True
    else:
        times = move_data.at[id_, 'datetime'][filter_]
        idx_not_in_ascending_order = np.where(times[:-1] >= times[1:])[0] + 1

        if idx_not_in_ascending_order.shape[0] > 0:
            move_data.feature_values_using_filter_and_indexes(
                move_data,
                id_,
                'deleted',
                filter_,
                idx_not_in_ascending_order,
                True,
            )

            fix_time_not_in_ascending_order_id(
                move_data, id_, index_name=index_name
            )

    if inplace:
        return move_data


def fix_time_not_in_ascending_order_all(
    move_data: DataFrame,
    index_name: Optional[Text] = TID,
    drop_marked_to_delete: Optional[bool] = False,
    inplace: Optional[bool] = True
) -> Optional[DataFrame]:
    """
    Used to correct time order between points of the trajectories, after map
    matching operations.

    Parameters
    ----------
    move_data : dataframe
       The input trajectories data
    index_name: str, optional
        The name of the column to set as the new index during function execution,
        by default TID
    drop_marked_to_delete: boolean, optional
        Indicates if rows marked as deleted should be dropped, by default False
    inplace: boolean, optional
        if set to true the original dataframe will be altered,
        otherwise the alteration will be made in a copy, that will be returned,
        by default True

    Returns
    -------
    DataFrame
        Dataframe sorted by time or none
    """

    if not inplace:
        move_data = move_data.copy()

    if TID not in move_data:
        move_data.generate_tid_based_on_id_datetime()

    if move_data.index.name is not None:
        print('reseting index...')
        move_data.reset_index(inplace=True)
    move_data['isNone'] = move_data['datetime'].isnull()
    print('dropping duplicate distances... shape before:', move_data.shape)

    move_data.drop_duplicates(
        subset=[index_name, 'isNone', 'distFromTrajStartToCurrPoint'],
        keep='first',
        inplace=True,
    )
    print('shape after:', move_data.shape)

    print('sorting by id and distance...')
    move_data.sort_values(
        by=[index_name, 'distFromTrajStartToCurrPoint'], inplace=True
    )
    print('sorting done')

    tids = move_data[index_name].unique()
    move_data['deleted'] = False

    print('starting fix...')
    time.time()
    for tid in progress_bar(tids):
        fix_time_not_in_ascending_order_id(move_data, tid, index_name)

    move_data.reset_index(inplace=True)
    idxs = move_data[move_data['deleted']].index
    size_idx = idxs.shape[0]
    print('{} rows marked for deletion.'.format(size_idx))

    if idxs.shape[0] > 0 and drop_marked_to_delete:
        print('shape before dropping: {}'.format(move_data.shape))
        move_data.drop(index=idxs, inplace=True)
        move_data.drop(labels='deleted', axis=1, inplace=True)
        print('shape after dropping: {}'.format(move_data.shape))

    if inplace:
        return move_data


def interpolate_add_deltatime_speed_features(
    move_data: DataFrame,
    label_tid: Optional[Text] = TID,
    max_dist_between_adj_points: Optional[float] = 5000,
    max_time_between_adj_points: Optional[float] = 900,
    max_speed: Optional[float] = 30,
    inplace: Optional[bool] = True
) -> Optional[DataFrame]:
    """
    Use to interpolate distances (x) to find times (y).

     Parameters
    ----------
    move_data : dataframe
       The input trajectories data
    label_tid: str, optional("tid" by default)
        The name of the column to set as the new index during function execution.
        Indicates the tid column.
        max_dist_between_adj_points: float, optional
     The maximum distance between two adjacent points, by default 5000
    max_time_between_adj_points: float, optional
     The maximum time interval between two adjacent points, by default 900
    max_speed: float, optional
     The maximum speed between two adjacent points, by default 30
    inplace: boolean, optional
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

    if TID not in move_data:
        move_data.generate_tid_based_on_id_datetime()

    if move_data.index.name is not None:
        print('reseting index...')
        move_data.reset_index(inplace=True)

    tids = move_data[label_tid].unique()
    move_data['isNone'] = move_data['datetime'].isnull()

    if move_data.index.name is None:
        print('creating index...')
        move_data.set_index(label_tid, inplace=True)

    drop_trajectories = []
    size = move_data.shape[0]
    count = 0
    time.time()

    move_data['delta_time'] = np.nan
    move_data['speed'] = np.nan

    for tid in progress_bar(tids):
        filter_nodes = move_data.at[tid, 'isNone']
        size_id = 1 if filter_nodes.shape == () else filter_nodes.shape[0]
        count += size_id

        y_ = move_data.at[tid, 'time'][~filter_nodes]
        if y_.shape[0] < 2:
            drop_trajectories.append(tid)
            continue

        assert np.all(
            y_[1:] >= y_[:-1]
        ), 'time feature is not in ascending order'

        x_ = move_data.at[tid, 'distFromTrajStartToCurrPoint'][
            ~filter_nodes
        ]

        assert np.all(
            x_[1:] >= x_[:-1]
        ), 'distance feature is not in ascending order'

        idx_duplicates = np.where(x_[1:] == x_[:-1])[0]
        if idx_duplicates.shape[0] > 0:
            x_ = np.delete(x_, idx_duplicates)
            y_ = np.delete(y_, idx_duplicates)

        if y_.shape[0] < 2:
            drop_trajectories.append(tid)
            continue

        delta_time = ((shift(y_.astype(np.float64), -1) - y_) / 1000.0)[
            :-1
        ]
        dist_curr_to_next = (shift(x_, -1) - x_)[:-1]
        speed = (dist_curr_to_next / delta_time)[:-1]

        assert np.all(
            delta_time <= max_time_between_adj_points
        ), 'delta_time between points cannot be more than {}'.format(
            max_time_between_adj_points
        )
        assert np.all(
            dist_curr_to_next <= max_dist_between_adj_points
        ), 'distance between points cannot be more than {}'.format(
            max_dist_between_adj_points
        )
        assert np.all(
            speed <= max_speed
        ), 'speed between points cannot be more than {}'.format(max_speed)

        assert np.all(
            x_[1:] >= x_[:-1]
        ), 'distance feature is not in ascending order'

        f_intp = interp1d(x_, y_, fill_value='extrapolate')

        x2_ = move_data.at[tid, 'distFromTrajStartToCurrPoint'][
            filter_nodes
        ]
        assert np.all(
            x2_[1:] >= x2_[:-1]
        ), 'distances in nodes are not in ascending order'

        intp_result = f_intp(x2_)
        assert np.all(
            intp_result[1:] >= intp_result[:-1]
        ), 'resulting times are not in ascending order'

        assert ~np.isin(
            np.inf, intp_result
        ), 'interpolation results with np.inf value(srs)'

        # update time features for nodes. initially they are empty.
        values = intp_result.astype(np.int64)
        feature_values_using_filter(
            move_data, tid, 'time', filter_nodes, values
        )

        values = (
            shift(
                move_data.at[tid, 'time'][filter_nodes].astype(np.float64),
                -1,
            )
            - move_data.at[tid, 'time'][filter_nodes]
        ) / 1000
        feature_values_using_filter(
            move_data, tid, 'delta_time', filter_nodes, values
        )

        move_data['datetime'] = None
        datetime = []
        for d in move_data['time'].values:
            data = Timestamp(int(d), unit='s', tz='America/Fortaleza')
            datetime.append(str(data)[:-6])
        move_data['datetime'] = datetime

        values = (
            move_data.at[tid, 'edgeDistance'][filter_nodes]
            / move_data.at[tid, 'delta_time'][filter_nodes]
        )
        feature_values_using_filter(
            move_data, tid, 'speed', filter_nodes, values
        )

    print(count, size)
    print(
        'we still need to drop {} trajectories with only 1 gps point'.format(
            len(drop_trajectories)
        )
    )
    move_data.reset_index(inplace=True)
    idxs_drop = move_data[
        move_data[label_tid].isin(drop_trajectories)
    ].index.values
    print(
        'dropping {} rows in {} trajectories with only 1 gps point'.format(
            idxs_drop.shape[0], len(drop_trajectories)
        )
    )
    if idxs_drop.shape[0] > 0:
        print('shape before dropping: {}'.format(move_data.shape))
        move_data.drop(index=idxs_drop, inplace=True)
        print('shape after dropping: {}'.format(move_data.shape))

    if not inplace:
        return move_data


def generate_distances(
    move_data: DataFrame,
    inplace: Optional[bool] = False
) -> Optional[DataFrame]:
    """Use generate columns distFromTrajStartToCurrPoint and edgeDistance.
     Parameters
    ----------
    move_data : dataframe
       The input trajectories data
    inplace: boolean, optional
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
    bbox = move_data.get_bbox()

    G = ox.graph_from_bbox(bbox[0], bbox[2], bbox[1], bbox[3])
    nodes = ox.get_nearest_nodes(
        G, X=move_data['lon'], Y=move_data['lat'], method='kdtree'
    )

    distances = []
    edgeDistance = []
    dist = 0.0
    node_ant = nodes[0]
    distances.append(dist)
    edgeDistance.append(dist)

    gdf_edges = ox.graph_to_gdfs(G, nodes=False)

    for node in nodes[1:]:
        df_u = gdf_edges[gdf_edges.index.get_level_values('u') == node_ant]
        df_edge = df_u[df_u.index.get_level_values('v') == node]

        if(len(df_edge) == 0):
            dist += 0
            edgeDistance.append(dist)
        else:
            dist += df_edge['length'].values[0]
            edgeDistance.append(df_edge['length'].values[0])
        distances.append(dist)
        node_ant = node

    move_data['edgeDistance'] = edgeDistance
    move_data['distFromTrajStartToCurrPoint'] = distances

    if not inplace:
        return move_data
