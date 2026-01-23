import pandas as pd
import pytest

from typing import Callable
from validateur_batch.control import editorial_check


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("su", "su1")])
def test_check_su1(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (input.loc[:, "acceptabilityId"] == "ACCEPTABLE")
    pd.testing.assert_frame_equal(editorial_check._check_su1(input, pt, syn), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("su", "su3")])
def test_check_su3(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   semtag: Callable[[int], pd.Series],
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    tag = semtag(len(input))
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    pd.testing.assert_frame_equal(editorial_check._check_su3(input, tag, pt), output)


@pytest.mark.parametrize("df_in, df_out", [("null", "null"), ("su", "su8")])
def test_check_su8(df_in: pd.DataFrame, df_out: pd.DataFrame,
                   semtag: Callable[[int], pd.Series],
                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    tag = semtag(len(input))
    pt = (input.loc[:, "acceptabilityId"] == "PREFERRED")
    pd.testing.assert_frame_equal(editorial_check._check_su8(input, tag, pt), output)
