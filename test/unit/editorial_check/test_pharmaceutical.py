import pandas as pd
import pytest

from typing import Callable
from validateur_batch.control import editorial_check


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("me", "me1")])
def test_check_me1(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   semtag: Callable[[int], pd.Series],
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    tag = semtag(len(input))
    pd.testing.assert_frame_equal(editorial_check._check_me1(input, tag), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("me", "me2")])
def test_check_me2(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   semtag: Callable[[int], pd.Series],
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    tag = semtag(len(input))
    pd.testing.assert_frame_equal(editorial_check._check_me2(input, tag), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("me", "me3")])
def test_check_me3(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   semtag: Callable[[int], pd.Series],
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    tag = semtag(len(input))
    pd.testing.assert_frame_equal(editorial_check._check_me3(input, tag), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("me", "me4")])
def test_check_me4(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   semtag: Callable[[int], pd.Series],
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    tag = semtag(len(input))
    pd.testing.assert_frame_equal(editorial_check._check_me4(input, tag), output)
