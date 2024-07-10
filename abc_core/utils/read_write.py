import json
import logging
import os
import pickle
from typing import Any, Dict

import arviz as az
import pandas as pd
from box import Box
from matplotlib.figure import Figure
from unidecode import unidecode

from abc_core.schema.base_schema import BaseSchema

logger = logging.getLogger(__name__)


def read_file(
    base_directory: str,
    file_name: str,
    time_connector: str = None,
    read_type: str = "pandas_df",
    **kwargs,
):
    """Handler to call correct read function given input read_type arg."""
    function_map = {
        "pandas_df": read_file_as_df,
        "python_dict": read_file_as_dict,
        "arviz_idata": read_file_as_arviz,
        "sklearn_model": read_file_as_model,
        "python_list": read_file_as_list,
        "yaml_config": read_file_as_yaml,
    }
    if read_type in function_map:
        # call the function associated with the input string
        result = function_map[read_type](
            file_name=file_name,
            time_connector=time_connector,
            base_directory=base_directory,
            **kwargs,
        )
        return result
    else:
        raise ("Read type argument not supported.")


def read_file_as_yaml(base_directory: str, time_connector: str, file_name: str) -> dict:
    """Load data from yaml file."""
    path_to_load = os.path.join(base_directory, time_connector, file_name)
    yaml_box = Box.from_yaml(filename=path_to_load)
    return yaml_box


def read_file_as_df(
    base_directory: str,
    time_connector: str,
    file_name: str,
    skiprows: int = None,
    pipeline_name: str = None,
    sheet_name_split: bool = False,
    sheet_name: str = None,
    separator: str = None,
    schema: BaseSchema = None,
    skipcols: list = [],
) -> pd.DataFrame:
    """Load data in pandas DataFrame format."""
    if pipeline_name:
        base_directory = os.path.join(base_directory, pipeline_name)
    path_to_load = os.path.join(base_directory, time_connector, file_name)
    if file_name.endswith(".json"):
        df = pd.read_json(path_to_load)
    elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        if sheet_name_split:
            df = pd.read_excel(
                path_to_load,
                sheet_name=None,
                skiprows=skiprows,
                usecols=lambda x: x not in skipcols,
            )
        else:
            if isinstance(sheet_name, str):
                df = pd.read_excel(
                    path_to_load,
                    sheet_name=sheet_name,
                    skiprows=skiprows,
                    usecols=lambda x: x not in skipcols,
                )
            else:
                df = pd.read_excel(
                    path_to_load,
                    skiprows=skiprows,
                    usecols=lambda x: x not in skipcols,
                )
    elif file_name.endswith(".parquet"):
        df = pd.read_parquet(path_to_load)
    elif file_name.endswith(".txt") or file_name.endswith(".csv"):
        df = pd.read_csv(path_to_load, sep=separator, engine='python')
    elif file_name.endswith(".pickle"):
        df = pd.read_pickle(path_to_load)
    else:
        raise ValueError("Table format not supported")

    if isinstance(df, pd.DataFrame):
        df.columns = [
            unidecode(str(col)) for col in df.columns
        ]  # Remove accents from column names
        df.columns = df.columns.str.replace("\n", " ", regex=False).str.lower()
        df.columns = df.columns.str.replace("-", " ", regex=False).str.lower()
        df.columns = df.columns.str.replace(".", "", regex=False).str.lower()
        df.columns = df.columns.str.replace(",", " ", regex=False).str.lower()
        df.columns = df.columns.str.replace(")", "", regex=False).str.lower()
        df.columns = df.columns.str.replace("(", "", regex=False).str.lower()
        df.columns = df.columns.str.replace("+", "", regex=False).str.lower()
        df.columns = df.columns.str.replace(" ", "_", regex=False).str.lower()
        df.columns = df.columns.str.replace("/", "_", regex=False).str.lower()
        df.columns = df.columns.str.replace(":", "", regex=False).str.lower()
        df.columns = df.columns.str.replace("#", "Number", regex=False).str.lower()
        if schema:
            df = df[schema.get_column_names()]
            df = schema.cast(df)
    return df


def read_file_as_model(
    base_directory: str,
    time_connector: str,
    file_name: str,
    pipeline_name: str = None,
):
    """Load data in sklearn model regressor format."""
    if pipeline_name:
        base_directory = os.path.join(base_directory, pipeline_name)
    path_to_load = os.path.join(base_directory, time_connector, file_name)
    if file_name.endswith(".pickle"):
        model = read_pickle(path_to_load)
    else:
        raise ValueError("Model file type not supported")
    return model


def read_file_as_list(
    base_directory: str,
    time_connector: str,
    file_name: str,
    pipeline_name: str = None,
):
    """Load data with python data types from pickle."""
    if pipeline_name:
        base_directory = os.path.join(base_directory, pipeline_name)
    path_to_load = os.path.join(base_directory, time_connector, file_name)
    if file_name.endswith(".pickle"):
        list_obj = read_pickle(path_to_load)
    else:
        raise ValueError("List file type not supported")
    return list_obj


def read_file_as_dict(
    base_directory: str,
    time_connector: str,
    file_name: str,
    pipeline_name: str = None,
) -> Dict:
    """Load data in python dict format."""
    if pipeline_name:
        base_directory = os.path.join(base_directory, pipeline_name)
    path_to_load = os.path.join(base_directory, time_connector, file_name)
    if file_name.endswith(".json"):
        with open(path_to_load, "rb") as file:
            dict_in = json.load(file)
    elif file_name.endswith(".pickle"):
        with open(path_to_load, "rb") as file:
            dict_in = pickle.load(file)
    else:
        raise ValueError("Dictionary format not supported")
    return dict_in


def read_file_as_arviz(
    base_directory: str,
    time_connector: str,
    file_name: str,
    pipeline_name: str = None,
) -> az.InferenceData:
    """Load data in arviz idata format."""
    if pipeline_name:
        base_directory = os.path.join(base_directory, pipeline_name)
    path_to_load = os.path.join(base_directory, time_connector, file_name)
    if file_name.endswith(".nc"):
        idata = az.from_netcdf(path_to_load)
    elif file_name.endswith(".json"):
        idata = az.from_json(path_to_load)
    else:
        raise ValueError("Arviz idata format not supported")
    return idata


def write_file(
    out_obj: pd.DataFrame | dict | az.InferenceData | Figure,
    base_directory: str,
    time_connector: str,
    file_name: str,
    pipeline_name: str = None,
):
    """General write data method for variable formats."""
    if pipeline_name:
        base_directory = os.path.join(base_directory, pipeline_name)
    root_path = os.path.join(base_directory, time_connector)
    file_path = os.path.join(root_path, file_name)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    if file_name.endswith(".json"):
        if isinstance(out_obj, dict):
            with open(file_path, "w") as fp:
                json.dump(out_obj, fp)
        elif isinstance(out_obj, az.InferenceData):
            az.to_json(out_obj, file_path)
        elif isinstance(out_obj, pd.DataFrame):
            out_obj.to_json(file_path)
        else:
            raise ValueError("Object type not supported for chosen format")
    elif file_name.endswith(".xlsx"):
        logger.warning(f"{file_name} table shape is {out_obj.shape}")
        out_obj.to_excel(file_path)
    elif file_name.endswith(".csv"):
        logger.warning(f"{file_name} table shape is {out_obj.shape}")
        out_obj.to_csv(file_path, index=False)
    elif file_name.endswith(".parquet"):
        logger.warning(f"{file_name} table shape is {out_obj.shape}")
        out_obj.to_parquet(file_path)
    elif file_name.endswith(".pickle"):
        if isinstance(out_obj, dict):
            save_pickle(out_obj, file_path)
        elif isinstance(out_obj, pd.DataFrame):
            out_obj.to_pickle(file_path)
        else:  # stan model, ml model
            save_pickle(out_obj, file_path)
    elif file_name.endswith(".nc"):
        if isinstance(out_obj, az.InferenceData):
            az.to_netcdf(out_obj, os.path.join(root_path, file_name))
        else:
            raise ValueError("Object type not supported for chosen format")
    elif file_name.endswith(".png"):
        if isinstance(out_obj, Figure):
            out_obj.savefig(os.path.join(root_path, file_name))
        else:
            raise ValueError("Object type not supported for chosen format")
    else:
        raise ValueError("Write output format not supported")

def save_pickle(output: Any, output_filepath: str) -> None:
    """Save output as pickle to local."""
    with open(output_filepath, "wb") as file:
        pickle.dump(output, file)


def read_pickle(input_filepath: str) -> Any:
    """Read pickle input from local."""
    with open(input_filepath, "rb") as file:
        input_file = pickle.load(file)
    return input_file
