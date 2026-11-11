"""Przygotowanie danych do modelowania."""

import pandas as pd

from asi_project.config import get_contract, load_project_config
from asi_project.data import make_xy, split_train_test


def prepare_xy(
    processed_data: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """Oddziela cechy modelu od targetu."""
    config = load_project_config()
    contract = get_contract(config)

    return make_xy(
        processed_data,
        contract,
        config.model_features,
    )


def prepare_train_test(
    X: pd.DataFrame,
    y: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Dzieli dane na zbiór treningowy i testowy."""
    config = load_project_config()
    contract = get_contract(config)

    return split_train_test(
        X,
        y,
        contract,
        test_size=config.test_size,
        random_state=config.random_state,
    )
