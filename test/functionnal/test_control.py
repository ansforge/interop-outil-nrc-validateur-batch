import pandas as pd
import pytest

from typing import Generator
from validateur_batch.control import editorial_check, format_check
from validateur_batch.object import server


def test_editorial_check(df_editorial: pd.DataFrame, df_editorial_output: pd.DataFrame,
                         fts_editorial: Generator, pytestconfig: pytest.Config) -> None:
    endpoint = server.Server(pytestconfig.getoption("endpoint"))
    pd.testing.assert_frame_equal(
        editorial_check.run_editorial_check(df_editorial, endpoint),
        df_editorial_output)


@pytest.mark.parametrize("df_in, df_out, type, fts",
                         [("add", "add_output", "ADD", "fts_inactive"),
                          ("chg", "chg_output", "CHG", "fts_null"),
                          ("ina", "ina_output", "INA", "fts_inactive"),
                          ("rep", "rep_output", "REP", "fts_both")])
def test_format_check(df_in: pd.DataFrame, df_out: pd.DataFrame, type: str,
                      fts: Generator, pytestconfig: pytest.Config,
                      request: pytest.FixtureRequest) -> None:
    endpoint = server.Server(pytestconfig.getoption("endpoint"))
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    fts = request.getfixturevalue(fts)
    pd.testing.assert_frame_equal(
        format_check.run_format_check(input, type, endpoint), output)
