"""Testy przygotowania danych w Sprincie 2."""

import pandas as pd

from asi_project.pipelines.data_processing.nodes import (
    filter_data,
    normalize_data,
)


def test_normalize_data():
    df = pd.DataFrame(
        {
            "job": [" admin. ", "unknown"],
            "education": [" secondary ", "tertiary"],
        }
    )

    result = normalize_data(df)

    assert result["job"].iloc[0] == "admin."
    assert pd.isna(result["job"].iloc[1])
    assert result["education"].iloc[0] == "secondary"


def test_filter_data():
    df = pd.DataFrame(
        {
            "age": [30, 40],
            "y": ["yes", None],
        }
    )

    result = filter_data(df)

    assert len(result) == 1
    assert result["y"].iloc[0] == "yes"
