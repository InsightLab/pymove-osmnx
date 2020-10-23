from pandas import DataFrame, Timestamp
from pandas.testing import assert_frame_equal
from pymove.core.dataframe import MoveDataFrame
from pymove.utils.constants import DATETIME, LATITUDE, LONGITUDE, TRAJ_ID

from pymove_osmnx.utils.similarity import generate_lcss

list_data = [
    [-3.83613, -38.49421, '2019-06-05 06:57:42', 1],
    [-3.84036, -38.49431, '2019-06-05 06:58:42', 1],
    [-3.84582, -38.49454, '2019-06-05 06:59:42', 1],
    [-3.84941, -38.49504, '2019-06-05 07:00:42', 1],
    [-3.85109, -38.49620, '2019-06-05 07:01:42', 1],
    [-3.85607, -38.49620, '2019-06-05 07:02:42', 1],
    [-3.86400, -38.49780, '2019-06-05 07:03:42', 1],
    [-3.87173, -38.49885, '2019-06-05 07:04:42', 1],
    [-3.87943, -38.50081, '2019-06-05 07:05:42', 1],
    [-3.88593, -38.50163, '2019-06-05 07:06:42', 1]
]

list_data_2 = [
    [-3.84936, -38.49504, '2019-06-05 07:00:40', 2],
    [-3.85071, -38.49636, '2019-06-05 07:01:40', 2],
    [-3.85525, -38.49604, '2019-06-05 07:02:40', 2],
    [-3.86307, -38.49764, '2019-06-05 07:03:40', 2],
    [-3.87110, -38.49864, '2019-06-05 07:04:40', 2],
    [-3.87866, -38.50071, '2019-06-05 07:05:40', 2],
    [-3.88523, -38.50150, '2019-06-05 07:06:40', 2],
    [-3.89176, -38.50226, '2019-06-05 07:07:40', 2],
    [-3.89843, -38.50389, '2019-06-05 07:08:40', 2],
    [-3.90216, -38.50499, '2019-06-05 07:09:40', 2]
]


def test_lcss():
    move_df = MoveDataFrame(
        data=list_data,
        latitude=LATITUDE,
        longitude=LONGITUDE,
        datetime=DATETIME,
        traj_id=TRAJ_ID,
    )

    move_df_2 = MoveDataFrame(
        data=list_data_2,
        latitude=LATITUDE,
        longitude=LONGITUDE,
        datetime=DATETIME,
        traj_id=TRAJ_ID,
    )

    move_lcss = generate_lcss(move_df, move_df_2, 60)

    cols = [
        'ida',
        'idb',
        'datetime_ida',
        'datetime_idb',
        'difference',
        'equals',
        'edge'
    ]

    expected = DataFrame(
        data=[
            [
                1,
                 2,
                Timestamp('2019-06-05 07:02:42'),
                Timestamp('2019-06-05 07:02:40'),
                2,
                True,
                list([1938809894, 2527401909])
            ],
               [
                   1,
                   2,
                   Timestamp('2019-06-05 07:03:42'),
                Timestamp('2019-06-05 07:03:40'),
                2,
                True,
                list([2527401903, 2527388956])
            ],
               [
                   1,
                   2,
                   Timestamp('2019-06-05 07:04:42'),
                Timestamp('2019-06-05 07:04:40'),
                2,
                True,
                list([2527401895, 6502622934])],
               [
                   1,
                   2,
                   Timestamp('2019-06-05 07:05:42'),
                Timestamp('2019-06-05 07:05:40'),
                2,
                True,
                list([2862103272, 2862103258])]
        ],
        columns=cols,
        index=[0, 1, 2, 3],
    )

    assert_frame_equal(move_lcss, expected)
    assert len(move_lcss) == 4
