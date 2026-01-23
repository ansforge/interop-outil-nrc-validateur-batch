import pandas as pd
import pytest

from validateur_batch.control import editorial_check


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("sb", "sb1")])
def test_check_sb1(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(editorial_check._check_sb1(input), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("sb", "sb2")])
def test_check_sb2(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(editorial_check._check_sb2(input), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("sb", "sb3")])
def test_check_sb3(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(editorial_check._check_sb3(input, pt, syn), output)
