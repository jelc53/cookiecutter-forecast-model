import pandas as pd
import os


def read_file(base_directory: str, time_connector: str, file_name: str) -> pd.DataFrame:
    """Load data in pandas DataFrame format"""
    path_to_load = os.path.join(base_directory, time_connector, file_name)
    if file_name.endswith(".json"):
        df = pd.read_json(path_to_load)
    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(path_to_load)
    elif file_name.endswith(".parquet"):
        df = pd.read_parquet(path_to_load)
    else:
        raise ValueError("Table format not supported")
    return df


def write_file(
    df: pd.DataFrame,
    base_directory: str,
    time_connector: str,
    file_name: str,
):
    """Write data from pandas DataFrame format"""
    root_path = os.path.join(base_directory, time_connector)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    if file_name.endswith(".json"):
        df.to_json(os.path.join(root_path, file_name))
    elif file_name.endswith(".xlsx"):
        df.to_excel(os.path.join(root_path, file_name))
    elif file_name.endswith(".parquet"):
        df.to_parquet(os.path.join(root_path, file_name))
    else:
        raise ValueError("Table format not supported")
