import logging
import pandas as pd

from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import KFold

logger = logging.getLogger(__name__)


def get_model(model_name: str, model_params: dict = None):
    """Get base model for machine learning forecast."""
    if model_name == "lin_reg":
        if model_params is None:
            model = LinearRegression()
        else:
            model = LinearRegression(**model_params)
    elif model_name == "random_forest":
        if model_params is None:
            model = RandomForestRegressor()
        else:
            model = RandomForestRegressor(**model_params)
    elif model_name == "xgboost":
        if model_params is None:
            model = XGBRegressor()
        else:
            model = XGBRegressor(**model_params)
    else:
        raise NotImplementedError(f"ABC only supports \
            random_forest and xgboost, got {model_name}.")
    return model


def tune_hyperparameters(
    X_train: pd.DataFrame,
    y_train: pd.DataFrame,
    model_config: dict,
):
    """Tune hyperparameters for sklearn models."""
    hp_tuning_config = model_config.hyperparameters
    model_name = model_config.model_name
    model = get_model(model_name=model_name)
    cv = KFold(n_splits=hp_tuning_config.cv_splits)
    gs = RandomizedSearchCV(
        estimator=model,
        scoring=model_config.scoring,
        param_distributions=hp_tuning_config[model_name],
        n_iter=hp_tuning_config.n_iter,
        cv=cv,
        return_train_score=True,
        random_state=model_config.random_state,
    )
    gs.fit(X_train, y_train)
    best_params = gs.best_params_
    best_score = gs.best_score_
    logger.info(f"Grid search of best parameters: {best_params}")
    logger.info(f"Grid search best score: {best_score}")
    return best_params, best_score
