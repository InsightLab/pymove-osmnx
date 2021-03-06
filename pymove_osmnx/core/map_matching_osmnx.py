from typing import Optional, Text, Tuple, Union

import osmnx as ox
from networkx import MultiDiGraph
from pandas.core.frame import DataFrame
from pymove import PandasMoveDataFrame
from pymove.core.dask import DaskMoveDataFrame
from pymove.core.pandas_discrete import PandasDiscreteMoveDataFrame


def map_matching_node(
    move_data: Union[PandasMoveDataFrame, DaskMoveDataFrame, PandasDiscreteMoveDataFrame],
    inplace: Optional[bool] = True,
    bbox: Optional[Tuple[float, float, float, float]] = None,
    place: Optional[Text] = None,
    G: Optional[MultiDiGraph] = None
) -> Optional[DataFrame]:
    """
    Generate Map matching using the graph nodes

    Parameters
    ----------
    move_data : MoveDataFrame
       The input trajectories data
    inplace: bool, optional
        if set to true the original dataframe will be altered,
        otherwise the alteration will be made in a copy, that will be returned,
        by default True
    bbox : tuple, optional
        The bounding box as (north, east, south, west), by default None
    place : string, optional
        The query to geocode to get place boundary polygon, by default None
    G : MultiDiGraph, optional
        The input graph, by default None

    Returns
    -------
    move_data : MoveDataFrame
        A copy of the original dataframe or None

    """
    if(G is None):
        if(bbox is None):
            bbox = move_data.get_bbox()
        G = ox.graph_from_bbox(
            bbox[0], bbox[2], bbox[1], bbox[3], network_type='all_private'
        )
    elif(place is not None):
        G = ox.footprints_from_place(query=place, tags={'network_type': 'all_private'})

    if not inplace:
        move_data = move_data[:]

    nodes = ox.get_nearest_nodes(
        G, X=move_data['lon'], Y=move_data['lat'], method='kdtree'
    )

    gdf_nodes = ox.graph_to_gdfs(G, edges=False)
    df_nodes = gdf_nodes.loc[nodes]

    move_data['lat'] = list(df_nodes.y)
    move_data['lon'] = list(df_nodes.x)
    move_data['geometry'] = list(df_nodes.geometry)

    if not inplace:
        return move_data


def map_matching_edge(
    move_data: Union[PandasMoveDataFrame, DaskMoveDataFrame, PandasDiscreteMoveDataFrame],
    inplace: Optional[bool] = True,
    bbox: Optional[Tuple[float, float, float, float]] = None,
    place: Optional[Text] = None,
    G: Optional[MultiDiGraph] = None
) -> Optional[DataFrame]:
    """
    Generate Map matching using the graph edges

    Parameters
    ----------
    move_data : MoveDataFrame
       The input trajectories data
    inplace: bool, optional
        if set to true the original dataframe will be altered,
        otherwise the alteration will be made in a copy, that will be returned,
        by default True
    bbox : tuple, optional
        The bounding box as (north, east, south, west), by default None
    place : string, optional
        The query to geocode to get place boundary polygon, by default None
    G : MultiDiGraph, optional
        The input graph, by default None

    Returns
    -------
    move_data : MoveDataFrame
        A copy of the original dataframe or None

    """
    if(G is None):
        if(bbox is None):
            bbox = move_data.get_bbox()
        G = ox.graph_from_bbox(
            bbox[0], bbox[2], bbox[1], bbox[3], network_type='all_private'
        )
    elif(place is not None):
        G = ox.footprints_from_place(query=place, tags={'network_type': 'all_private'})

    if not inplace:
        move_data = move_data[:]

    edges = ox.get_nearest_edges(
        G, X=move_data['lon'], Y=move_data['lat'], method='kdtree'
    )
    gdf_edges = ox.graph_to_gdfs(G, nodes=False)

    geometries = []
    for e in edges:
        df_edges = gdf_edges[
            (gdf_edges.index.get_level_values('u') == e[0])
            & (gdf_edges.index.get_level_values('v') == e[1])
        ]
        geometries.append(df_edges['geometry'])

    move_data['edge'] = [*map(lambda x: tuple([x[0], x[1]]), edges)]
    move_data['geometry'] = geometries

    if not inplace:
        return move_data
