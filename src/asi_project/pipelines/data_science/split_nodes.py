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
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Dzieli dane zgodnie z kontraktem i parametrami Kedro."""
    config = load_project_config()
    contract = get_contract(config)

    return split_train_test(
        X,
        y,
        contract,
        test_size=test_size,
        random_state=random_state,
    )
