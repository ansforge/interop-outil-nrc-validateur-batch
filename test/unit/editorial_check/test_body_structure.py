import pandas as pd
import pytest

from typing import Callable
from validateur_batch.control import editorial_check


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("bs", "bs2")])
def test_check_bs2(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(editorial_check._check_bs2(input), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("bs", "bs3")])
def test_check_bs3(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   semtag: Callable[[int], pd.Series],
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    tag = semtag(len(input))
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(
        editorial_check._check_bs3(input, tag, pt, syn), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("bs", "bs5")])
def test_check_bs5(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   semtag: Callable[[int], pd.Series],
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    tag = semtag(len(input))
    pd.testing.assert_frame_equal(editorial_check._check_bs5(input, tag), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("bs", "bs6")])
def test_check_bs6(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   semtag: Callable[[int], pd.Series],
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    tag = semtag(len(input))
    pd.testing.assert_frame_equal(editorial_check._check_bs6(input, tag), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("bs", "bs7")])
def test_check_bs7(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   semtag: Callable[[int], pd.Series],
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    tag = semtag(len(input))
    pd.testing.assert_frame_equal(editorial_check._check_bs7(input, tag), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("bs", "bs8")])
def test_check_bs8(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(editorial_check._check_bs8(input, pt, syn), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("bs", "bs9")])
def test_check_bs9(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(editorial_check._check_bs9(input, pt, syn), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("bs", "bs10")])
def test_check_bs10(df_in: pd.DataFrame, df_out: pd.DataFrame,
                    request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(
        editorial_check._check_bs10(input, pt, syn), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("bs", "bs11")])
def test_check_bs11(df_in: pd.DataFrame, df_out: pd.DataFrame,
                    request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(
        editorial_check._check_bs11(input, pt, syn), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("bs", "bs12")])
def test_check_bs12(df_in: pd.DataFrame, df_out: pd.DataFrame,
                    request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(editorial_check._check_bs12(input), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("bs", "bs13")])
def test_check_bs13(df_in: pd.DataFrame, df_out: pd.DataFrame,
                    request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(editorial_check._check_bs13(input), output)
