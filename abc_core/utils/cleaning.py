import pandas as pd
from typing import List
import logging

logger = logging.getLogger(__name__)

def remove_rows_with_null_values(df: pd.DataFrame, excl_cols: List[str]) -> pd.DataFrame:
    """Remove rows with null values."""
    tmp_df = df.drop(columns=excl_cols).copy()
    mask_for_null_values = tmp_df.isna().any(axis=1)
    logger.warn(f"Removed {mask_for_null_values.sum()} rows with null values.")
    return df[~mask_for_null_values].reset_index(drop=True).copy()