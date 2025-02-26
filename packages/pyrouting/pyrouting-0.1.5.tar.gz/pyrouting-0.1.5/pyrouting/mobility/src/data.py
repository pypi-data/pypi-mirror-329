import pandas as pd
import geopandas as gpd
from pandas.api.types import is_datetime64_any_dtype
from .errors import missing_columns

class RawDataWrangler:
    def __init__(self, df: pd.DataFrame):
        missing_columns(df, ["imsi", "report_time", "latitude", "longitude"])
        self.df = df

        if not is_datetime64_any_dtype(self.df["report_time"]):
            self.apply_datetime()

    def apply_datetime(self):
        
        self.df["report_time"] = self.df["report_time"].str.split(".").str[0]
        if 'T' in self.df["report_time"][0]:
            self.df["report_time"] = self.df["report_time"].str.replace("T", " ")
        else:
            pass

        self.df["report_time"] = pd.to_datetime(
                     self.df["report_time"], format="%Y-%m-%d %H:%M:%S", errors="coerce"
                )
        self.df.dropna(inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        # Sort dataframe by datetime
        self.df.sort_values(by="report_time", inplace=True, ignore_index=True)

    def filter_by_date(self, start_date: str = None, end_date: str = None, inplace: bool = False) -> pd.DataFrame:

        if start_date and end_date:

            df = self.df.loc[
                (self.df["report_time"] >= start_date)
                & (self.df["report_time"] < end_date)
            ]

        elif start_date:
            df = self.df.loc[self.df["report_time"] >= start_date]
        elif end_date:
            df = self.df.loc[self.df["report_time"] < end_date]
        else:
            pass

        if inplace:
            self.df = df

        return df

    def apply_geodataframe(self, crs: str = "EPSG:3346", inplace: bool = False):
        df = gpd.GeoDataFrame(
            self.df,
            geometry=gpd.points_from_xy(self.df.longitude, self.df.latitude),
            crs=crs,
        )

        if inplace:
            self.df = df

        return df
