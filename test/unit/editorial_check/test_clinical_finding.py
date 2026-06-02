import pandas as pd
import pytest

from typing import Callable
from validateur_batch.control import editorial_check


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("co_pa", "co2")])
def test_check_co2(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   semtag: Callable[[int], pd.Series],
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    tag = semtag(len(input))
    pd.testing.assert_frame_equal(editorial_check._check_co2(input, tag), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("co_pa", "co6")])
def test_check_co6(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   semtag: Callable[[int], pd.Series],
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    tag = semtag(len(input))
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(editorial_check._check_co6(input, tag, pt, syn),
                                  output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("co_pa", "pa2")])
def test_check_pa2(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(editorial_check._check_pa2(input, pt, syn), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("co_pa", "pa3_1")])
def test_check_pa3_1(df_in: pd.DataFrame, df_out: pd.DataFrame,
                     request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(editorial_check._check_pa3_1(input), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("co_pa", "pa4")])
def test_check_pa4(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(editorial_check._check_pa4(input), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("co_pa", "pa6")])
def test_check_pa6(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    pd.testing.assert_frame_equal(editorial_check._check_pa6(input, pt), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("co_pa", "pa7")])
def test_check_pa7(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(editorial_check._check_pa7(input), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("co_pa", "pa8")])
def test_check_pa8(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(editorial_check._check_pa8(input), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("co_pa", "pa9")])
def test_check_pa9(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(editorial_check._check_pa9(input), output)
