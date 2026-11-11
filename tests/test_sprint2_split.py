"""Testy przygotowania danych do modelowania."""

import pandas as pd

from asi_project.pipelines.data_science.split_nodes import (
    prepare_train_test,
    prepare_xy,
)


def make_test_data():
    """Tworzy mały zbiór zgodny z konfiguracją Bank Marketing."""
    n = 20

    return pd.DataFrame(
        {
            "age": [30] * n,
            "balance": [1000] * n,
            "campaign": [1] * n,
            "pdays": [10] * n,
            "previous": [0] * n,
            "job": ["admin."] * n,
            "marital": ["single"] * n,
            "education": ["secondary"] * n,
            "default": ["no"] * n,
            "housing": ["yes"] * n,
            "loan": ["no"] * n,
            "contact": ["cellular"] * n,
            "day": [10] * n,
            "month": ["may"] * n,
            "poutcome": ["unknown"] * n,
            "y": ["no", "yes"] * 10,
        }
    )


def test_prepare_xy():
    df = make_test_data()

    X, y = prepare_xy(df)

    assert len(X) == len(y)
    assert X.shape[1] == 15
    assert "y" not in X.columns
    assert set(y.unique()) == {0, 1}


def test_prepare_train_test():
    df = make_test_data()
    X, y = prepare_xy(df)

    X_train, X_test, y_train, y_test = prepare_train_test(X, y)

    assert len(X_train) == 16
    assert len(X_test) == 4
    assert set(y_train.unique()) == {0, 1}
    assert set(y_test.unique()) == {0, 1}

    # Podział chronologiczny, bez mieszania kolejności
    assert X_train.index.max() < X_test.index.min()
