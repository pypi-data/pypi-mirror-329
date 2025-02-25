"""Contains utility functions for mobility-data-routing project."""
from networkx import MultiDiGraph
import numpy as np
import geopandas as gpd
import osmnx as ox
from shapely.geometry import Polygon
import pandas as pd
# Plotting
import matplotlib.pyplot as plt
import contextily as cx

def create_grid(gdf: gpd.GeoDataFrame, delta: int) -> gpd.GeoDataFrame:
    """
    Description:
    ------------
    Create a grid of polygons from a GeoDataFrame bounds.

    Parameters:
    -----------
    :param gdf: geopandas GeoDataFrame to create grid from
    :param delta: x and y size of grid cell

    Returns:
    --------
    :return: geopandas GeoDataFrame of grid polygons
    """
    # Get bounds of GeoDataFrame
    minx, miny, maxx, maxy = gdf.total_bounds

    # Calculate number of grid cells in x and y directions
    nx = int((maxx - minx) / delta)
    ny = int((maxy - miny) / delta)

    # Calcuate steps in x and y directions
    gx, gy = np.linspace(minx, maxx, nx), np.linspace(miny, maxy, ny)

    # Create grid polygons
    grids = []
    for i in range(len(gx) - 1):
        for j in range(len(gy) - 1):
            poly_ij = Polygon(
                [
                    [gx[i], gy[j]],
                    [gx[i], gy[j + 1]],
                    [gx[i + 1], gy[j + 1]],
                    [gx[i + 1], gy[j]],
                ]
            )
            grid.append(poly_ij)

    # Create GeoDataFrame of grid polygons
    grid = gpd.GeoDataFrame(geometry=grids, crs=gdf.crs)
    return grid


def network_graph(polygon_path: str, travel_type: str='drive', highway_types: str= None, simplify: bool = False) -> MultiDiGraph:
    """
    Description
    -----------
    The function returns Open Street Map (OSM) street network
    of Vilnius and its periphery

    Parameters
    ----------
    :param polygon_path: path to polygon file

    Returns
    ------
    :graph: OSM network graph
    """
    # use only allowed travel types
    if travel_type not in ["all_public", "bike", "drive", "walk"]:
        raise ValueError("Invalid travel type. Choose from: 'all_public', 'bike', 'drive', 'walk'")

    # Get Vilnius polygon with periphery
    polygon_gdf = gpd.read_file(polygon_path)
    polygon_gdf = polygon_gdf.to_crs(4326)
    for index, values in polygon_gdf.iterrows():
        poly = values["geometry"]

    # Getting OSM graph from polygon
    graph = ox.graph_from_polygon(
        poly, network_type=travel_type, custom_filter=highway_types, simplify=simplify
    )

    return graph


def groupby_imsi(df: pd.DataFrame, min_events: int = 2) -> list[pd.DataFrame]:
    """
    Description
    ------------
    Group dataframe by imsi and filter out groups with less than min_events

    Parameters
    ------------
    :param df: dataframe with user events
    :param min_events: minimum number of events per user
    """
    dfs = [
        v.reset_index(drop=True) for l, v in df.groupby("imsi") if len(v) > min_events
    ]
    return dfs


def get_geomety_centroid(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if gdf.geometry.geom_type[0] == "Point":
        gdf['x'] = gdf.geometry.x
        gdf['y'] = gdf.geometry.y

    else:
        gdf['x'] = gdf.geometry.centroid.x
        gdf['y'] = gdf.geometry.centroid.y

    return gdf


def plot_data(
    dataframes: list[gpd.GeoDataFrame], center_x, center_y
):

    fig, ax = plt.subplots(figsize=(20, 20))

    # Create bounding box
    min_x = center_x - 150
    max_x = center_x + 150
    min_y = center_y - 150
    max_y = center_y + 150

    bbox = Polygon(
        ((min_x, max_y), (max_x, max_y), (max_x, min_y), (min_x, min_y), (min_x, max_y))
    )

    for df in dataframes:
        df = df[df.within(bbox)]
        df.reset_index(drop=True, inplace=True)
        df = df.to_crs(epsg=3857)
        # Plotting Geopandas datafrmae
        df.plot(column="usage", cmap="OrRd", legend=True, ax=ax, aspect=1)

        df = get_geomety_centroid(df)

        color = random_color()

        # Plot usage labels
        for x, y, label in zip(df["x"], df['y'], df["usage"]):
            ax.text(x, y, label, fontsize=8, color=color)

    # Adding basemap to plot
    cx.add_basemap(ax, source=cx.providers.CartoDB.DarkMatter)

    # Plotting
    plt.figure()
    # Turn off axis
    ax.axis("off")
    plt.show()

# Generate random color

def random_color() -> str:
    """
    Description
    ------------
    Generate random color

    Returns
    -------
    :return: random color
    """
    r = lambda: np.random.randint(0, 255)
    return "#%02X%02X%02X" % (r(), r(), r())


# Function to handle datetime in dataframes
def human_readable_to_unix(unix_timestamp):
    time_unix = unix_timestamp.timestamp()
    return time_unix
