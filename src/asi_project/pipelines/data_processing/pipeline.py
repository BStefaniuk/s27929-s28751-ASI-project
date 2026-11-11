"""Pipeline przygotowania danych."""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import filter_data, normalize_data, validate_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=validate_data,
                inputs="raw_data",
                outputs="validated_data",
                name="validate_data",
            ),
            node(
                func=normalize_data,
                inputs="validated_data",
                outputs="normalized_data",
                name="normalize_data",
            ),
            node(
                func=filter_data,
                inputs="normalized_data",
                outputs="processed_data",
                name="filter_data",
            ),
        ]
    )
