from pandas import DataFrame, Timestamp
from pandas.testing import assert_frame_equal
from pymove.core.dataframe import MoveDataFrame

from pymove_osmnx.utils.interpolate import (
    check_time_dist,
    feature_values_using_filter,
    fix_time_not_in_ascending_order_all,
    fix_time_not_in_ascending_order_id,
    generate_distances,
)

list_data = [
    [-3.779936, -38.679217, '2008-06-04 09:04:59', '1'],
    [-3.779240, -38.678747, '2008-06-04 09:05:59', '1'],
    [-3.778692, -38.678440, '2008-06-04 09:06:59', '1'],
    [-3.778191, -38.678071, '2008-06-04 09:07:59', '1'],
    [-3.779200, -38.675917, '2008-06-04 09:08:59', '1'],
]



def _default_move_df():
    return MoveDataFrame(
        data=[
            [39.984094, 116.319236, '2008-10-23 05:53:05', 1],
            [39.984198, 116.319322, '2008-10-23 05:53:06', 1],
            [39.984224, 116.319402, '2008-10-23 05:53:11', 1],
            [39.984224, 116.319402, '2008-10-23 05:53:11', 2],
        ]
    )

move_df = MoveDataFrame(
    data=list_data,
    latitude=0,
    longitude=1,
    datetime=2,
    traj_id=3,
)

def test_generate_distances():

    move_distances = generate_distances(move_df)

    cols = [
        'lat',
        'lon',
        'datetime',
        'id',
        'edgeDistance',
        'distFromTrajStartToCurrPoint'
    ]

    expected = DataFrame(
        data=[
            [
                -3.779936,
                -38.679217,
                Timestamp('2008-06-04 09:04:59'),
                '1',
                0.0,
                0.0
            ],
            [
                -3.77924,
                -38.678747,
                Timestamp('2008-06-04 09:05:59'),
                '1',
                0.0,
                0.0
            ],
            [
                -3.778692,
                -38.67844,
                Timestamp('2008-06-04 09:06:59'),
                '1',
                70.121,
                70.121
            ],
            [
                -3.778191,
                -38.678071,
                Timestamp('2008-06-04 09:07:59'),
                '1',
                69.14,
                139.261
            ],
            [
                -3.7792,
                -38.675917,
                Timestamp('2008-06-04 09:08:59'),
                '1',
                254.009,
                393.27
            ]
        ],
        columns=cols
    )

    assert_frame_equal(move_distances, expected)
    assert len(move_distances) == 5

def test_check_time_dist():
    check_time = check_time_dist(generate_distances(move_df), index_name = 'id')

    assert check_time == True

def test_fix_time_not_in_ascending_order_id():
    time_ascending = fix_time_not_in_ascending_order_id(
        generate_distances(move_df), tid='1', index_name = 'id'
    )

    assert time_ascending == 5

def test_fix_time_not_in_ascending_order_all():
    time_ascending = fix_time_not_in_ascending_order_all(
        generate_distances(move_df), index_name = 'id'
    )

    assert time_ascending == 0
