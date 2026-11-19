"""Testy nodów treningu i ewaluacji."""

import numpy as np
import pytest
from sklearn.metrics import f1_score

from asi_project.data import normalize_input
from asi_project.pipelines.data_science.split_nodes import (
    prepare_train_test,
    prepare_xy,
)
from asi_project.pipelines.data_science.train_nodes import (
    evaluate_models,
    train_models,
)


@pytest.fixture
def trained_models(project):
    data = normalize_input(project.sample)
    X, y = prepare_xy(data)

    X_train, X_test, y_train, y_test = prepare_train_test(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )
    dummy, logistic = train_models(X_train, y_train)

    return dummy, logistic, X_train, X_test, y_test


def test_train_models_returns_fitted_models(trained_models):
    dummy, logistic, _, X_test, _ = trained_models

    for model in (dummy, logistic):
        predictions = model.predict(X_test)
        assert len(predictions) == len(X_test)
        assert set(predictions).issubset({0, 1})

    probabilities = logistic.predict_proba(X_test)
    assert probabilities.shape == (len(X_test), 2)
    assert np.allclose(probabilities.sum(axis=1), 1.0)


def test_evaluate_models_returns_correct_metrics(trained_models):
    dummy, logistic, X_train, X_test, y_test = trained_models

    record = evaluate_models(
        dummy,
        logistic,
        X_train,
        X_test,
        y_test,
        data_mode="sample",
    )

    assert record["data_mode"] == "sample"
    assert record["split"]["strategy"] == "time_ordered"
    assert record["split"]["n_train"] == len(X_train)
    assert record["split"]["n_test"] == len(X_test)

    for name, model in (
        ("dummy", dummy),
        ("logistic_regression", logistic),
    ):
        metrics = record["models"][name]
        expected_f1 = f1_score(
            y_test,
            model.predict(X_test),
            zero_division=0,
        )
        assert metrics["f1"] == pytest.approx(expected_f1)
        assert sum(metrics["confusion_matrix"].values()) == len(y_test)
