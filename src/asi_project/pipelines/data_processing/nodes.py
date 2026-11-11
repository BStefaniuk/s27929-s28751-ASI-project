"""Funkcje przygotowania danych dla Kedro."""

import pandas as pd

from asi_project.config import get_contract, load_project_config
from asi_project.data import assert_valid, filter_training_rows, normalize_input


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Sprawdza, czy dane są poprawne."""
    config = load_project_config()
    contract = get_contract(config)
    assert_valid(df, contract, config)
    return df


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Porządkuje wartości w danych."""
    return normalize_input(df)


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    """Usuwa rekordy, których nie używamy do treningu."""
    config = load_project_config()
    contract = get_contract(config)
    return filter_training_rows(df, contract)
