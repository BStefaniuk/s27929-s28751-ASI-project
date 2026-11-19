"""Trenowanie i ewaluacja modeli."""

import pandas as pd

from asi_project.config import get_contract, load_project_config
from asi_project.metrics import build_metrics_record, compute_metrics
from asi_project.model import build_baseline_pipeline, make_dummy


def train_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
):
    """Trenuje model Dummy i regresję logistyczną."""
    config = load_project_config()

    dummy = make_dummy()
    dummy.fit(X_train, y_train)

    logistic = build_baseline_pipeline(
        config.numeric_features,
        config.categorical_features,
    )
    logistic.fit(X_train, y_train)

    return dummy, logistic


def evaluate_models(
    dummy_model,
    logistic_model,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    data_mode: str,
):
    """Oblicza metryki modeli na zbiorze testowym."""
    config = load_project_config()
    contract = get_contract(config)

    results = {
        "dummy": compute_metrics(y_test, dummy_model.predict(X_test)),
        "logistic_regression": compute_metrics(
            y_test,
            logistic_model.predict(X_test),
        ),
    }

    return build_metrics_record(
        contract=contract,
        config=config,
        features=config.model_features,
        n_train=len(X_train),
        n_test=len(X_test),
        data_mode=data_mode,
        results=results,
    )
