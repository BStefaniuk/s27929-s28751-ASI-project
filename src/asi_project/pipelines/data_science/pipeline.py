"""Pipeline data science."""

from kedro.pipeline import Pipeline, node, pipeline

from .split_nodes import prepare_train_test, prepare_xy
from .train_nodes import evaluate_models, train_models


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=prepare_xy,
                inputs="processed_data",
                outputs=["X", "y"],
                name="prepare_xy",
            ),
            node(
                func=prepare_train_test,
                inputs=[
                    "X",
                    "y",
                    "params:test_size",
                    "params:random_state",
                ],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="prepare_train_test",
            ),
            node(
                func=train_models,
                inputs=["X_train", "y_train"],
                outputs=["dummy_model", "logistic_model"],
                name="train_models",
            ),
            node(
                func=evaluate_models,
                inputs=[
                    "dummy_model",
                    "logistic_model",
                    "X_train",
                    "X_test",
                    "y_test",
                    "params:data_mode",
                ],
                outputs="evaluation_metrics",
                name="evaluate_models",
            ),
        ]
    )
