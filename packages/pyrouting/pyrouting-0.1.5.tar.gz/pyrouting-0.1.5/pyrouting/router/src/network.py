from networkx import MultiDiGraph
import osmnx as ox
import geopandas as gpd
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from .utils import groupby_imsi


class Network:

    def __init__(self, network_graph: MultiDiGraph, fill_speed: int = None) -> None:
        self.network_graph = network_graph
        self.nodes, self.edges = self.exctract_nodes_edges()
        self.fill_speed = fill_speed
        if fill_speed:
            self.edges.fillna(50, inplace=True)
            self.edges["maxspeed"] = self.edges["maxspeed"].astype(int)

        self.edges["length"] = self.edges["length"].astype(float)

    def apply_weights(self, weights_dict: dict = None, by: str = 'shortest', inplace: bool = False) -> MultiDiGraph:

        # Create local copy of edges
        edges = self.edges

        # Apply weights to edges based on the method
        edges = self.select_routing_method(edges, weights_dict, by, self.fill_speed)

        # Inplace edges update
        if inplace:
            self.edges = edges

        # Create a network graph
        network = ox.graph_from_gdfs(self.nodes, edges)

        if inplace:
            self.network_graph = network

        return network

    @staticmethod
    def select_routing_method(
        edges: gpd.GeoDataFrame, weights_dict: dict = None, by: str = "shortest", fill_speed: bool = False
    ) -> str:

        if by == 'shortest':
            edges["weight"] = edges.length

        elif by == 'fastest' and fill_speed:
            edges["weight"] = edges.length / edges.maxspeed

        elif by == 'fastest' and not fill_speed:
            raise Exception("Fill speed is not provided")

        elif by == 'weight':
            edges["highway_weight"] = edges["highway"].map(weights_dict)
            edges["weight"] = (edges.length / edges.maxspeed) * edges.highway_weight

        elif by == 'weight' and not fill_speed and not weights_dict:
            raise Exception("Fill speed and weights is not provided")

        else:
            raise Exception("Unknown method")

        return edges

    def exctract_nodes_edges(self) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
        """
        Description
        -----------
        The function returns nodes and edges of the network graph

        Returns
        -------
        :return: tuple of nodes and edges
        """

        nodes, edges = ox.graph_to_gdfs(
            self.network_graph, nodes=True, edges=True
        )

        return nodes, edges

    def drop_reversed_edges(self, inplace: bool = False):
        """
        Description
        -----------
        The function drops reversed edges from the network graph
        """

        edges = self.edges.reset_index()
        edges_v = edges["v"].tolist()
        edges_u = edges["u"].tolist()

        # Create a list of list wiht v and u pairs
        edges_list = list(map(list, zip(edges_v, edges_u)))

        # Create a dictionary with dropped v, u pairs
        dropped = {tuple(sorted(i)): i for i in edges_list}.values()

        # Convert dictionary to list
        edges_droped = list(dropped)

        # Convert list of list to list of tuples
        edges_droped = [tuple(i) for i in edges_droped]

        # Create a dataframe with dropped v, u pairs
        data = []
        for _el in edges_droped:
            v, u = _el
            key = f"{v}_{u}"
            data.append({"key": key})

        data = pd.DataFrame(data)

        # Create key column in edges dataframe
        edges["key"] = edges.apply(lambda row: f"{row['v']}_{row['u']}", axis=1)

        # Merge edges and keys dataframes
        edges = pd.merge(edges, data, on="key")

        # Inplace update
        if inplace:
            self.edges = edges

        return edges

    @staticmethod
    def parse_edge(edge:tuple) -> tuple:
        """
        Description
        -----------
        The function parses edge tuple to a tuple of integers

        Parameters
        ----------
        :param edge: tuple of edges

        Returns
        -------
        :return: tuple of integers
        """

        v, u = edge
        return tuple(u,v)


class Nodes:
    """
    Description
    ----------
    The class is used to get network nodes from network graph by given user points.

    Parameters
    ----------
    :param network: GeoDataFrame of network nodes
    :param buffer_radius: buffer radius around point
    """

    def __init__(self, nodes: gpd.GeoDataFrame, buffer_radius: int = 1000) -> None:
        """
        Parameters
        ----------
        :param network_nodes: Open Sreet Map network graph nodes
        :param buffer_radius: buffer radius around point

        """
        self.nodes = nodes.reset_index()
        self.buffer_radius = buffer_radius
        self._route_pairs = None


    def nearest_nodes(self, mobility_data: gpd.GeoDataFrame) -> gpd.GeoDataFrame:

        # Parse the geometries to a list
        nodes_geoms = list(self.nodes.geometry.apply(lambda row: (row.x, row.y)))
        mobility_data_geoms = list(mobility_data.geometry.apply(lambda row: (row.x, row.y)))

        # Convert the lists to numpy arrays
        nodes_geom_array = np.array(nodes_geoms)
        mobility_data_geom_array = np.array(mobility_data_geoms)

        # Create a KDTree
        btree = cKDTree(nodes_geom_array)
        distances, idx = btree.query(mobility_data_geom_array, k=1)

        # Add distances and node_id to mobility data
        mobility_data["distance"] = distances
        mobility_data["node_id"] = idx

        # Drop geometry column from mobility data
        mobility_data.drop(columns=["geometry"], inplace=True)

        # Add node id to mobility data
        self.nodes["node_id"] = self.nodes.index

        gdf = pd.merge(mobility_data, self.nodes, on="node_id", how="left")

        return gdf
    

class NodesOneUser(Nodes):

    def __init__(self, network: Network, buffer_radius: int = 1000) -> None:
        super().__init__(network, buffer_radius)
        self._route_pairs = None

    def calculate_nodes(self, mobility_data):
        routes_nodes = self.nodes_from_points(mobility_data)
        routes_nodes = routes_nodes.loc[routes_nodes["osmid"].notnull()]
        routes_nodes.reset_index(drop=True, inplace=True)

        return routes_nodes


class NodesMultiUser(Nodes):

    def __init__(self, network: Network, buffer_radius: int = 1000) -> None:
        super().__init__(network, buffer_radius)
        self._route_pairs = None

    def calculate_nodes(self, mobility_data):
        dfs = groupby_imsi(mobility_data)
        dfs = [self.nodes_from_points(df) for df in dfs]
        dfs = [df.loc[df["osmid"].notnull()] for df in dfs]
        dfs = [df.reset_index(drop=True) for df in dfs]

        return dfs

class RoutePairs:

    @staticmethod
    def calculate_route_pairs(df_nodes: pd.DataFrame, lower_limit: int, upper_limit: int, min_events: int= 5) -> list:
        nodes = groupby_imsi(df_nodes, min_events)
        if isinstance(nodes, pd.DataFrame):
            nodes = [nodes]
        else:
            pass

        nodes = [RoutePairs.remove_by_speed(df, lower_limit, upper_limit) for df in nodes]
        nodes = [pair for pairs in nodes for pair in pairs]

        nodes = RoutePairs.delete_identical(nodes)

        return nodes

    @staticmethod
    def delete_identical(route_pairs: list) -> list:
        index = []
        for idx, pair in enumerate(route_pairs):
            if pair[0] == pair[1]:
                index.append(idx)

        route_pairs = [i for j, i in enumerate(route_pairs) if j not in index]

        return route_pairs

    @staticmethod
    def remove_by_speed(dataframe: gpd.GeoDataFrame, lower_limit: int, upper_limit: int):
        """
        Description
        -----------
        Remove points from geopandas dataframe by speed

        Parameters
        ----------
        :param data : gpd.GeoDataFreame
        :param lower_limit : minimum speed in km/h
        :param upper_limit : maximum speed in km/h

        Returns
        -------
        :speeds, data : list, list
            - speeds : list of speeds
            - data : list of data rows
                rows with speed not in range [lower_limit, upper_limit] are removed
                rows contains dictionary with speed, distance, time and geometry
                geometry is LineString of two points
        """
        if 'report_time' not in dataframe.columns:
            raise Exception('Column "report_time" not found in dataframe')

        if 'geometry' not in dataframe.columns:
            raise Exception('Column "geometry" not found in dataframe')

        # Set placeholders
        data = []
        imsi = dataframe['imsi'][0]
        for _ in range(len(dataframe) - 1):
            
            time_diff = dataframe['report_time'][_ + 1] - dataframe['report_time'][_]
            seconds = time_diff.total_seconds()

            # Check if seconds not equal to 0
            if seconds == 0:
                continue

            # Calculate distance between points
            start_point = dataframe['geometry'][_]
            end_point = dataframe['geometry'][_ + 1]
            distance = end_point.distance(start_point)

            # Calculate speed
            speed = distance / seconds
            # To km per hour
            speed = speed * 3.6

            # if speed not in range continue
            if speed > upper_limit or speed < lower_limit:
                continue

            start_node = dataframe['osmid'][_]
            end_node = dataframe['osmid'][_ + 1]

            # Create data row
            data_row = (start_node, end_node, imsi)
            # Append to list
            data.append(data_row)

        return data
