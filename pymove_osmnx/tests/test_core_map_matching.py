from pandas import DataFrame, Timestamp
from pandas.testing import assert_frame_equal
from pymove.core.dataframe import MoveDataFrame
from shapely.geometry import LineString
from shapely.geometry.point import Point

from pymove_osmnx.core.map_matching_osmnx import map_matching_edge, map_matching_node

dict_data = {
    'id':  [1, 1, 1, 1],
    'lat': [-3.779936, -3.779240, -3.778692, -3.778191],
    'lon': [-38.67921, -38.678747, -38.678440, -38.678071],
    'datetime': [
        '2008-06-12 12:00:50',
        '2008-06-12 12:00:56',
        '2008-06-12 12:01:01',
        '2008-06-12 12:01:06'
    ]
}

def test_map_matching_node():
    move_df = MoveDataFrame(
        data=dict_data
    )

    map_matching_node(move_df)

    cols = [
        'id',
        'lat',
        'lon',
        'datetime',
        'geometry'
    ]

    expected = DataFrame(
        data=[
            [
                1,
                -3.779240,
                -38.678747,
                Timestamp('2008-06-12 12:00:50'),
                Point(-38.6787469, -3.7792405),
            ],
            [
                1,
                -3.779240,
                -38.678747,
                Timestamp('2008-06-12 12:00:56'),
                Point(-38.6787469, -3.7792405),
            ],
            [
                1,
                -3.778692,
                -38.678440,
                Timestamp('2008-06-12 12:01:01'),
                Point(-38.6784397, -3.7786924),
            ],
            [
                1,
                -3.778692,
                -38.678440,
                Timestamp('2008-06-12 12:01:06'),
                Point(-38.6784397, -3.7786924)
            ],
        ],
        columns=cols,
        index=[0, 1, 2, 3],
    )

    assert_frame_equal(move_df, expected)

    assert move_df.len() == 4


def test_map_matching_edge():
    move_df = MoveDataFrame(
        data=dict_data
    )

    map_matching_edge(move_df)

    cols = ['id', 'lat', 'lon', 'datetime', 'edge', 'geometry']

    expected = DataFrame(
        data=[
            [
                1,
                -3.779936,
                -38.67921,
                Timestamp('2008-06-12 12:00:50'),
                (3971291384, 7625732459),
                LineString([
                    (-38.6784397,-3.7786924),
                    (-38.6784773,-3.7787981),
                    (-38.6785128,-3.7788737),
                    (-38.678547,-3.7789333),
                    (-38.6787079,-3.7791822),
                    (-38.6787469,-3.7792405),
                ])
            ],
            [
                1,
                -3.779240,
                -38.678747,
                Timestamp('2008-06-12 12:00:56'),
                (3971291384, 7625732459),
                LineString([
                    (-38.6784397,-3.7786924),
                    (-38.6784773,-3.7787981),
                    (-38.6785128,-3.7788737),
                    (-38.678547,-3.7789333),
                    (-38.6787079,-3.7791822),
                    (-38.6787469,-3.7792405),
                ])
            ],
            [
                1,
                -3.778692,
                -38.67844,
                Timestamp('2008-06-12 12:01:01'),
                (3971291384, 7625732459),
                LineString([
                    (-38.6784397,-3.7786924),
                    (-38.6784773,-3.7787981),
                    (-38.6785128,-3.7788737),
                    (-38.678547,-3.7789333),
                    (-38.6787079,-3.7791822),
                    (-38.6787469,-3.7792405),
                ])
            ],
            [
                1,
                -3.778191,
                -38.678071,
                Timestamp('2008-06-12 12:01:06'),
                (3971291384, 7625732459),
                LineString([
                    (-38.6784397,-3.7786924),
                    (-38.6784773,-3.7787981),
                    (-38.6785128,-3.7788737),
                    (-38.678547,-3.7789333),
                    (-38.6787079,-3.7791822),
                    (-38.6787469,-3.7792405),
                ])
            ],
        ],
        columns=cols,
        index=[0, 1, 2, 3],
    )

    assert_frame_equal(move_df, expected)

    assert move_df.len() == 4
