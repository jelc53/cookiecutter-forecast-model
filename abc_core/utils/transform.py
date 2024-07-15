import pandas as pd
from typing import List
from itertools import product

from abc_core.schema.base_schema import BaseSchema

def apply_schema(df: pd.DataFrame, schema: BaseSchema) -> pd.DataFrame:
    """Apply schema to processed data."""
    df = schema.handle_missing_columns(df)
    df = df[schema.get_column_names()]
    df = schema.cast(df)
    return df


def handle_datetime_dtype(df: pd.DataFrame, col: str, format: str = "%Y%m") -> pd.DataFrame:
    """Handle datetime typing for specified columns."""
    df[col] = pd.to_datetime(df[col], errors="raise", format=format)
    return df


def capitalize_columns(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """Standardise id columns, e.g., product_id, line."""
    for col in cols:
        df[col] = df[col].str.upper()
    return df


def standardize_naming(df: pd.DataFrame, col: str, name_list: List[str]) -> pd.DataFrame:
    """Standardize naming in free text column e.g., products."""
    in_col = df[col].str.upper().copy()
    df[col] = None
    for name in name_list:
        boo = df[col].isna()
        boo &= in_col.str.contains(name, case=False, na=False)
        df.loc[boo, col] = name
    return df


def init_df_from_list_combos(lists: List[list], cols: List[str]) -> pd.DataFrame:
    """Create empty dataframe from list combinations."""
    return pd.DataFrame(list(product(*lists)), columns=cols)
