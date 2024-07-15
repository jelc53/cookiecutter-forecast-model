import logging
import pandas as pd
import numpy as np
from typing import Dict

from sklearn.metrics import mean_absolute_error, r2_score

logger = logging.getLogger(__name__)


def compute_mape(y_true: pd.Series, y_pred: pd.Series) -> float:
    """Computes the Mean Absolute Percentage Error (MAPE)."""
    y_true = np.where(y_true == 0.0, np.finfo(float).eps, y_true)
    abs_percentage_error = abs((y_pred - y_true) / y_true)
    mape = abs_percentage_error.mean() * 100  # return as percentage
    return mape

def compute_bias(y_true, y_pred):
    """Calculates bias of our predictions."""
    bias = np.mean((y_pred - y_true) / y_pred) * 100
    return bias

def get_accuracy_metrics(
    metrics: dict, pred_df: pd.DataFrame, mode: str = "train"
) -> Dict:
    """Compute fit accuracy metrics dict."""
    y_true, y_pred = pred_df["y_true"], pred_df["y_pred"]
    r2 = r2_score(y_true=y_true, y_pred=y_pred)
    mae = mean_absolute_error(y_true=y_true, y_pred=y_pred)
    mape = compute_mape(y_true=y_true, y_pred=y_pred)
    bias = compute_bias(y_true=y_true, y_pred=y_pred)
    logger.warn(f"Metrics for {mode}: r2 {r2: .2f}, mae {mae: .2f}, mape {mape: .2f}, bias {bias:.2f}")
    metrics[mode] = {"r2": r2, "mae": mae, "mape": mape, "bias": bias}
    return metrics

