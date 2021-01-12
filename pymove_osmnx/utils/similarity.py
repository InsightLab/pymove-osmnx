from difflib import SequenceMatcher

import pandas as pd

from pymove_osmnx.core.map_matching_osmnx import map_matching_edge


def generate_lcss(
    move_data_id1,
    move_data_id2,
    tolerance
):
    """Generate Longest Commum Sub-Sequence between two trajectories.
     Parameters
    ----------
    move_data_id1 : MoveDataFrame
       The input trajectories data
    move_data_id2 : MoveDataFrame
       The input trajectories data
    tolerance : int
        Time in seconds regarding the tolerance of the time difference
        between a move_data_id1 and move_data_id2 point

    Returns
    -------
        move_data : MoveDataFrame
            A move_data containing the largest sub-sequence between
            move_data_id1 and move_data_id1.
        None
            When there is no sub-sequence.
    """

    move_data_id1 = map_matching_edge(move_data_id1, inplace=False)
    move_data_id2 = map_matching_edge(move_data_id2, inplace=False)

    seqMatch = SequenceMatcher(
        None, list(move_data_id1['edge']), list(move_data_id2['edge'])
    )

    matchs = seqMatch.get_matching_blocks()
    df_mat = pd.DataFrame(matchs)
    df_mat.sort_values(['size'], ascending=False, inplace=True)

    for m in df_mat.values:
        equals = []
        differences = []
        teste = True
        for i in range(0, m[2]):
            m0 = list(move_data_id1['datetime'])[m[0] + i]
            m1 = list(move_data_id2['datetime'])[m[1] + i]
            dif = m0 - m1
            differences.append(dif.seconds)
            if(dif.seconds > tolerance):
                v = False
                teste = False
            else:
                v = True
            equals.append(v)
        if(teste):
            data = {
                'ida': list(move_data_id1['id'])[m[0]: m[0] + m[2]],
                'idb': list(move_data_id2['id'])[m[1]: m[1] + m[2]],
                'datetime_ida': list(move_data_id1['datetime'])[m[0]: m[0] + m[2]],
                'datetime_idb': list(move_data_id2['datetime'])[m[1]: m[1] + m[2]],
                'difference': differences,
                'equals': equals,
                'edge': list(move_data_id1['edge'].apply(list))[m[0]: m[0] + m[2]]
            }
            return pd.DataFrame(data)
    return None
