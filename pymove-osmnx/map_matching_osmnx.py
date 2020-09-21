import pandas as pd
import networkx as nx
import osmnx as ox
import numpy as np
from pymove.core.dataframe import MoveDataFrame


def map_matching_node(
    move_data, 
    inplace=True
):
    """Generate Map matching.
     Parameters
    ----------
    move_data : MoveDataFrame
       The input trajectories data
    inplace: boolean, optional(True by default)
        if set to true the original dataframe will be altered,
        otherwise the alteration will be made in a copy, that will be returned.

    Returns
    -------
        move_data : dataframe
            A copy of the original dataframe, with the alterations done by the function. (When inplace is False)
        None
            When inplace is True
    """
    
    bbox = move_data.get_bbox()
    G = ox.graph_from_bbox(bbox[0], bbox[2], bbox[1], bbox[3], network_type='all_private')    
    nodes = ox.get_nearest_nodes(G,X=move_data['lon'],Y=move_data['lat'], method='kdtree')
    gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
    df_nodes = gdf_nodes.loc[nodes]
    move_data['lat'] = list(df_nodes.y)
    move_data['lon'] = list(df_nodes.x)
    move_data['geometry'] = list(df_nodes.geometry)
    
    if not inplace:
        return move_data

def map_matching_edge(
    move_data, 
    inplace=True
):
    """Generate Map matching.
     Parameters
    ----------
    move_data : MoveDataFrame
       The input trajectories data
    inplace: boolean, optional(True by default)
        if set to true the original dataframe will be altered,
        otherwise the alteration will be made in a copy, that will be returned.

    Returns
    -------
        move_data : dataframe
            A copy of the original dataframe, with the alterations done by the function. (When inplace is False)
        None
            When inplace is True
    """
    bbox = move_data.get_bbox()
    G = ox.graph_from_bbox(bbox[0], bbox[2], bbox[1], bbox[3], network_type='all_private')    
    edges = ox.get_nearest_edges(G,X=move_data['lon'],Y=move_data['lat'], method='kdtree')

    move_data['edge'] = edges
    move_data['edge'].apply(tuple)

    if not inplace:
        return move_data