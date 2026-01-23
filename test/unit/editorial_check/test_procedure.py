import pandas as pd
import pytest

from typing import Callable
from validateur_batch.control import editorial_check


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("pr", "pr2")])
def test_check_pr2(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(editorial_check._check_pr2(input, pt, syn), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("pr", "pr3")])
def test_check_pr3(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(editorial_check._check_pr3(input), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("pr", "pr4")])
def test_check_pr4(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(editorial_check._check_pr4(input, pt, syn), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("pr", "pr9")])
def test_check_pr9(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(editorial_check._check_pr9(input, pt, syn), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("pr", "pr10")])
def test_check_pr10(df_in: pd.DataFrame, df_out: pd.DataFrame,
                    request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(editorial_check._check_pr10(input), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("pr", "pr12")])
def test_check_pr12(df_in: pd.DataFrame, df_out: pd.DataFrame,
                    request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(
        editorial_check._check_pr12(input, pt, syn), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("pr", "pr13")])
def test_check_pr13(df_in: pd.DataFrame, df_out: pd.DataFrame,
                    request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(
        editorial_check._check_pr13(input, pt, syn), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("pr", "pr14")])
def test_check_pr14(df_in: pd.DataFrame, df_out: pd.DataFrame,
                    request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(
        editorial_check._check_pr14(input, pt, syn), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("pr", "pr15")])
def test_check_pr15(df_in: pd.DataFrame, df_out: pd.DataFrame,
                    semtag: Callable[[int], pd.Series],
                    request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    tag = semtag(len(input))
    pd.testing.assert_frame_equal(editorial_check._check_pr15(input, tag), output)
