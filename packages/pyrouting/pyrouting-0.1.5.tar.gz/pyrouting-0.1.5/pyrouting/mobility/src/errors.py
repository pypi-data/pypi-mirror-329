import pandas as pd

def missing_columns(df: pd.DataFrame, columns: list) -> dict:
    for col in columns:
        if col not in df.columns:
            raise ValueError(f"{col} column is missing from the dataframe")
