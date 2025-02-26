import os
import ast
import warnings
from multiprocessing import Pool

from tqdm import tqdm
import pandas as pd
import geopandas as gpd
from osmnx.routing import shortest_path
from collections import Counter
from shapely import Point, LineString
from abc import ABC, abstractmethod
from networkx import exception
from .utils import groupby_imsi

from .network import Network

warnings.filterwarnings("ignore", 'SettingWithCopyWarning')


class RoutesDataFrame:
    """
    Description
    ----------
    The class is used to create routes from dataframe
    """

    def __init__(self, network: Network, routes_dataframe: pd.DataFrame) -> None:
        """
        Description
        ----------
        Initialize the RoutesDataFrame class

        Parameters
        ----------
        :param network: Network object
        :param routes_dataframe: dataframe with routes
        """
        self.network = network
        self.routes_dataframe = routes_dataframe

    def __from_df_to_list(self):
        """Convert route column to list and create tuple of route and user and route number"""
        self.routes_dataframe['route_number'] = self.routes_dataframe.index
        route_numbers = self.routes_dataframe['route_number'].to_list()
        routes = self.routes_dataframe["route"].tolist()
        users = self.routes_dataframe["imsi"].tolist()
        if isinstance(routes[0], str):
            routes = [
                tuple((ast.literal_eval(route), user, number))
                for route, user, number in zip(routes, users, route_numbers)
                if not isinstance(route, float)
            ]
        else:
            routes = [
                tuple((route, user, number))
                for route, user, number in zip(routes, users, route_numbers)
            ]

        return routes
    
    def __form_list_to_df(self, routes: list) -> pd.DataFrame:
        """Convert list of routes to dataframe"""
        routes_dict = []
        for route in tqdm(routes, desc="Converting routes to dict", total=len(routes)):

            _route = [{"osmid": osm, "imsi": route[1], 
                       "route_number": route[2], "route_member": index} 
                      for index, osm in enumerate(route[0])]
            
            routes_dict.extend(_route)

        df = pd.DataFrame(routes_dict)

        return df

    def __get_nodes(self, routes_df: pd.DataFrame):  

        nodes = self.network.nodes.reset_index()

        # Merge nodes with routes
        routes_df = pd.merge(routes_df, nodes, on="osmid", how="inner")

        return routes_df

    def get_edges(self, min_length: int = 2) -> gpd.GeoDataFrame:
        """Create lines from routes dataframe"""
        
        # Get routes from dataframe
        routes = self.__from_df_to_list()
        # Create dataframe from list
        df_routes = self.__form_list_to_df(routes)
        # Exctract nodes from osm network by routes osmids
        df_nodes = self.__get_nodes(df_routes)

        # Group by route_number and filter groups with more than min_length
        grouped = df_nodes.groupby("route_number")
        dfs = [group for _, group in grouped if len(group) >= min_length]

        # If no routes meet the minimum length criteria, return an empty GeoDataFrame
        if not dfs:
            return gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")

        # Concatenate all groups
        df_nodes = pd.concat(dfs)
        df_nodes.reset_index(inplace=True, drop=True)

        # Create line from nodes
        df = df_nodes.groupby("route_number").agg({"imsi": "first", 
                                                   "route_number": "first", 
                                                   "highway": "first", 
                                                   'geometry': lambda x: LineString(x.tolist())})
        
        df.reset_index(inplace=True, drop=True)
        
        # Create GeoDataFrame
        gdf_lines = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")

        return gdf_lines

    def get_osm_ids_count(self):
        routes = self.routes_dataframe["route"].tolist()
        if isinstance(routes[0], str):
            routes = [ast.literal_eval(route) for route in routes if not isinstance(route, float)]
        else:
            routes = [route for route in routes]
        
        osm_ids = [int(id) for route in routes for id in route]
        osm_ids_count = Counter(osm_ids)

        return osm_ids_count


class UsageCalculator:

    def __init__(
        self,
        nodes: gpd.GeoDataFrame,
        edges: gpd.GeoDataFrame,
        routes: gpd.GeoDataFrame,
        partition: bool = False,
    ) -> None:
        self.nodes = nodes
        self.edges = edges
        self.routes = routes
        self.partition_by = partition

    @staticmethod
    def df_join(edges, df) -> pd.DataFrame:
        intersected = gpd.sjoin(edges, df, how="inner", predicate="within")
        return intersected

    def __insersecting_edges(self) -> pd.DataFrame:

        # Ensure both GeoDataFrames have a spatial index for faster queries
        if self.edges.sindex is None:
            self.edges = self.edges.set_geometry("geometry")

        if self.routes.sindex is None:
            self.routes = self.routes.set_geometry("geometry")

        if self.partition_by:
            dfs = groupby_imsi(self.routes, min_events=1)

        with Pool() as poll:
            intersections = poll.starmap(
                self.df_join,
                [(self.edges, df) for df in dfs],
            )

        intersected = pd.concat(intersections)
        intersected.reset_index(drop=True, inplace=True)

        return intersected

    def calculate_usage_by_nodes(self):

        intersects = self.__insersecting_edges()
        nodes_usage = self.nodes_usage(intersects)

        return nodes_usage

    def calculate_usage_by_edges(self, null_values: bool = False) -> gpd.GeoDataFrame:

        intersects = self.__insersecting_edges()

        # Group by key and sum count
        usage_df = intersects.groupby("key").size().reset_index(name="usage")

        if null_values:
            how = "left"
        else:
            how = "inner"

        edges_usage = pd.merge(self.edges, usage_df, on="key", how=how)
        edges_usage.fillna({'usage':0}, inplace=True)

        edges_usage = edges_usage.dissolve(by="osmid", aggfunc="max").reset_index()

        return edges_usage

    @staticmethod
    def nodes_usage(intersects) -> pd.DataFrame:

        intersect_ids = intersects["osmid"].tolist()
        count = Counter(intersect_ids)

        df_osm = pd.DataFrame.from_dict(count, orient="index")
        df_osm.reset_index(inplace=True)
        df_osm = df_osm.rename(columns={"index": "osmid", 0: "usage"})
        return df_osm

    @staticmethod
    def get_values(df: pd.DataFrame) -> list:

        df = df[['osmid', 'usage']]
        return df

from networkx import MultiDiGraph


class Routing:

    def __init__(self, network: MultiDiGraph) -> None:
        self.network = network
        self._osm_ids = {}

    def routing(self, start_node, end_node, by: str = "length") -> list:
        """
        Description
        ----------
        Create a path from start to end based on speed or route length

        Parameters
        --------
        :param start_node: start node id
        :param end_node: end node id
        :param by: calculate shortest path by attribute ('length', 'travel_time', 'elevation_gain')

        Returns
        ------
        route: list
            List of nodes from start to end node
        """
        # Calculate shortest path
        try:
            route = shortest_path(self.network, start_node, end_node, weight=by)
        except exception.NodeNotFound:
            route = []

        return route

    def multiprocess_routing(self, pairs: list, cpus: int = 6) -> list:
        """
        Description
        ----------
        Create shortest path from start to end node using multiprocessing

        Parameters
        --------
        :param pairs: list of start and end node pairs
        :param max_workers: maximum number of workers

        Returns
        ------
        routes: list
            List of nodes from start to end node
        """
        with Pool(cpus) as p:
            routes = list(tqdm(p.imap(self.routing, pairs), total=len(pairs)))

        self.osm_ids_list = routes

        return routes

    @property
    def osm_ids(self) -> list:
        """
        Description
        ----------
        Get list of osm ids

        Returns
        ------
        osm_ids_list: list
            List of osm ids
        """
        return self._osm_ids

    @osm_ids.setter
    def osm_ids(self):
        ids = [id for id in self.osm_ids_list]
        ids_count = Counter(ids)
        self._osm_ids = dict(ids_count)


def create_chunks(n: int, data: list) -> list:
    chunks = [data[i * n : (i + 1) * n] for i in range((len(data) + n - 1) // n)]

    return chunks


class RouterMobility:
    """
    Description
    ----------
    The class is used to route mobility data on a network.
    """

    def __init__(
        self,
        mobility_data: gpd.GeoDataFrame,
        lower_limit: int = 0,
        upper_limit: int = 999999,
    ) -> None:
        """
        Parameters
        ----------
        :param mobility_data: geopandas GeoDataFrame with mobility data
        :param network: Open Sreet Map network graph
        """
        if "report_time" not in mobility_data.columns:
            raise Exception('Column "report_time" not found in dataframe')

        if "geometry" not in mobility_data.columns:
            raise Exception('Column "geometry" not found in dataframe')

        if "imsi" not in mobility_data.columns:
            raise Exception('Column "imsi" not found in dataframe')
        # Check if multiple users in the dataset
        imsi = mobility_data["imsi"].unique()
        if len(imsi) > 1:
            raise Exception("Multiple users in the dataset")

        if lower_limit < 0:
            raise Exception("Lower limit must be greater than 0")

        self.imsi = imsi[0]
        mobility_data = mobility_data.sort_values(by="report_time")
        mobility_data = mobility_data.reset_index(drop=True)

        self.mobility_data = mobility_data
        self.crs = mobility_data.crs

        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

    def __create_lines(self) -> gpd.GeoDataFrame:
        """
        Description
        -----------
        Remove points from geopandas dataframe by speed

        Parameters
        ----------
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

        # Set placeholders
        data = []
        for _ in range(len(self.mobility_data) - 1):
            time_diff = (
                self.mobility_data["report_time"][_ + 1]
                - self.mobility_data["report_time"][_]
            )
            seconds = time_diff.total_seconds()

            # Check if seconds not equal to 0
            if seconds == 0:
                continue

            # Calculate distance between points
            start_point = self.mobility_data["geometry"][_]
            end_point = self.mobility_data["geometry"][_ + 1]
            distance = end_point.distance(start_point)

            # Calculate speed
            speed = distance / seconds
            # To km per hour
            speed = speed * 3.6

            if speed > self.upper_limit or speed < self.lower_limit:
                continue

            # Create data row
            data_row = {
                "speed": speed,
                "distance": distance,
                "start_time": self.mobility_data["report_time"][_],
                "end_time": self.mobility_data["report_time"][_ + 1],
                "time": seconds,
                "geometry": LineString([start_point, end_point]),
                "imsi": self.imsi,
            }
            # Append to list
            data.append(data_row)

        gdf = gpd.GeoDataFrame(data, crs=self.crs, geometry="geometry")

        return gdf

    def create_row(self, geometry: Point, report_time: str) -> dict:
        """
        Description
        -----------
        Create row for geopandas dataframe

        Parameters
        ----------
        :param geometry: shapely Point
        :param report_time: report time

        Returns
        -------
        :return data : dictionary with data
        """
        data = {
            "imsi": self.imsi,
            "report_time": report_time,
            "latitude": geometry.y,
            "longitude": geometry.x,
            "geometry": geometry,
        }

        return data

    def create_route_points(self, inplace: bool = True) -> gpd.GeoDataFrame:
        """
        Description
        -----------
        Create nodes from mobility data for routing on network

        Parameters
        ----------
        :param inplace : replace mobility data with route points

        Returns
        -------
        :return nodes : list of nodes from mobility data
        """
        mobility_lines = self.__create_lines()
        mobility_lines["start_node"] = mobility_lines.apply(
            lambda x: Point(x.geometry.coords[0]), axis=1
        )
        mobility_lines["end_node"] = mobility_lines.apply(
            lambda x: Point(x.geometry.coords[-1]), axis=1
        )

        data = []
        if len(mobility_lines) == 1:
            data.append(
                self.create_row(
                    mobility_lines["start_node"][0], mobility_lines["start_time"][0]
                )
            )
            data.append(
                self.create_row(
                    mobility_lines["end_node"][0], mobility_lines["end_time"][0]
                )
            )

        else:
            data.append(
                self.create_row(
                    mobility_lines["start_node"][0], mobility_lines["start_time"][0]
                )
            )
            for _ in range(len(mobility_lines) - 1):
                if mobility_lines["start_node"][_] != mobility_lines["end_node"][_ + 1]:
                    data.append(
                        self.create_row(
                            mobility_lines["end_node"][_ + 1],
                            mobility_lines["end_time"][_ + 1],
                        )
                    )

        df = pd.DataFrame(data)
        gdf = gpd.GeoDataFrame(df, crs=self.crs, geometry="geometry")

        if inplace:
            self.mobility_data = gdf

        return gdf


class Routes(ABC):
    pass


class RouteNodes(Routes):

    def __init__(
        self, network_nodes: gpd.GeoDataFrame, df_routes: pd.DataFrame
    ) -> None:
        self.network_nodes = network_nodes
        self.df_routes = df_routes

    def __from_df_to_list(self):
        """Convert route column to list and create tuple of route and user and route number"""
        # Give route number to each route
        self.df_routes["route_number"] = self.df_routes.index
        # Get route numbers
        route_numbers = self.df_routes["route_number"].to_list()
        # Convert route column to list
        routes = self.df_routes["route"].tolist()
        # Get users
        users = self.df_routes["imsi"].tolist()
        # Check if route is string or list
        if isinstance(routes[0], str):
            routes = [
                tuple((ast.literal_eval(route), user, number))
                for route, user, number in zip(routes, users, route_numbers)
                if not isinstance(route, float)
            ]
        else:
            routes = [
                tuple((route, user, number))
                for route, user, number in zip(routes, users, route_numbers)
            ]

        return routes
    
    def __form_list_to_df(self, routes: list) -> pd.DataFrame:
        """Convert list of routes to dataframe"""
        routes_dict = []
        for route in tqdm(routes, desc="Converting routes to dict", total=len(routes)):

            _route = [{"osmid": osm, "imsi": route[1], 
                       "route_number": route[2], "route_member": index} 
                      for index, osm in enumerate(route[0])]
            
            routes_dict.extend(_route)

        df = pd.DataFrame(routes_dict)

        return df
    

    def __get_nodes(self, routes_df: pd.DataFrame):  

        # Merge nodes with routes
        routes_df = pd.merge(routes_df, self.network_nodes, on="osmid", how="inner")

        return routes_df
    

    def get_edges(self, min_length: int = 2) -> gpd.GeoDataFrame:
        """Create lines from routes dataframe"""
        
        # Get routes from dataframe
        routes = self.__from_df_to_list()
        # Create dataframe from list
        df_routes = self.__form_list_to_df(routes)
        # Exctract nodes from osm network by routes osmids
        df_nodes = self.__get_nodes(df_routes)

        # Group by route_number and filter groups with more than min_length
        grouped = df_nodes.groupby("route_number")
        dfs = [group for _, group in grouped if len(group) >= min_length]

        # If no routes meet the minimum length criteria, return an empty GeoDataFrame
        if not dfs:
            return gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")

        # Concatenate all groups
        df_nodes = pd.concat(dfs)
        df_nodes.reset_index(inplace=True, drop=True)

        # Create line from nodes
        df = df_nodes.groupby("route_number").agg({"imsi": "first", 
                                                   "route_number": "first", 
                                                   "highway": "first", 
                                                   'geometry': lambda x: LineString(x.tolist())})
        
        df.reset_index(inplace=True, drop=True)
        
        # Create GeoDataFrame
        gdf_lines = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")

        return gdf_lines
