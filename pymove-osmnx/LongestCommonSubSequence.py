import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import osmnx as ox
import numpy as np
from difflib import SequenceMatcher 
from map_matching_osmnx import map_matching_edge


def generate_lcss(
    move_data_id1, 
    move_data_id2, 
    tolerance
):
    """Generate Longest Commum Sub-Sequence.
     Parameters
    ----------
    move_data : MoveDataFrame
       The input trajectories data
    move_data : 

    Returns
    -------
        move_data : MoveDataFrame
            A move_data containing the largest sub-sequence between imove_data_id1 and move_data_id1.
        None
            When there is no sub-sequence.
    """

    move_data_id1 = map_matching_edge(move_data_id1)
    move_data_id2 = map_matching_edge(move_data_id2)

    seqMatch = SequenceMatcher(None,list(move_data_id1['Edge']), list(move_data_id2['Edge'])) 
      
    matchs = seqMatch.get_matching_blocks() 
    df_mat = pd.DataFrame(matchs)
    df_mat.sort_values(['size'], ascending=False, inplace=True)

    for m in df_mat.values:
        equals = []
        differences = []
        teste = True
        for i in range(0, m[2]):
            dif = list(move_data_id1['datetime'])[m[0] + i] - list(move_data_id2['datetime'])[m[1] + i]
            differences.append(dif.seconds)
            if(dif.seconds > tol):
                v = False
                teste = False
            else:
                v = True
            equals.append(v)
        if(teste == True):
            data = {
                'ida': list(move_data_id1['id'])[m[0]: m[0] + m[2]],
                'idb': list(move_data_id2['id'])[m[1]: m[1] + m[2]],
                'datetime_ida': list(move_data_id1['datetime'])[m[0]: m[0] + m[2]],
                'datetime_idb': list(move_data_id2['datetime'])[m[1]: m[1] + m[2]],
                'difference': differences,
                'equals': equals,
                'edge': list(move_data_id1['Edge'].apply(list))[m[0]: m[0] + m[2]]
            }
            return pd.DataFrame(data)
    return None
