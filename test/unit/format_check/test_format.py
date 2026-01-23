from __future__ import annotations

import pandas as pd
import pytest

from typing import Dict, Generator, TYPE_CHECKING
from validateur_batch.control import format_check
from validateur_batch.object import server

if TYPE_CHECKING:
    from validateur_batch.object import batch


@pytest.mark.parametrize("df_in, df_out, type", [("invalid_add", "empty_add", "ADD"),
                                                 ("valid_add", "valid_add", "ADD"),
                                                 ("invalid_chg", "empty_chg", "CHG"),
                                                 ("valid_chg", "valid_chg", "CHG"),
                                                 ("invalid_ina", "empty_ina", "INA"),
                                                 ("valid_ina", "valid_ina", "INA"),
                                                 ("invalid_rep", "empty_rep", "REP"),
                                                 ("valid_rep", "valid_rep", "REP")])
def test_find_empty_cell(df_in: pd.DataFrame, df_out: pd.DataFrame,
                         type: "batch.BATCH_TYPE",
                         request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(format_check._find_empty_cell(input, type), output)


@pytest.mark.parametrize("json, status", [("active_concept", ""),
                                          ("inactive_concept", "1")])
def test_sctid_is_inactive(json: Dict, status: str, request: pytest.FixtureRequest):
    json = request.getfixturevalue(json)
    assert format_check._sctid_is_inactive(json) == status


@pytest.mark.parametrize("df_in, df_out, fts",
                         [("invalid_add", "sctid_add", "fts_inactive"),
                          ("invalid_rep", "sctid_rep", "fts_both")])
def test_validate_sctid(df_in: pd.DataFrame, df_out: pd.DataFrame,
                        fts: Generator, pytestconfig: pytest.Config,
                        request: pytest.FixtureRequest) -> None:
    endpoint = server.Server(pytestconfig.getoption("endpoint"))
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    fts = request.getfixturevalue(fts)
    pd.testing.assert_frame_equal(format_check._validate_sctid(input, endpoint),
                                  output)


@pytest.mark.parametrize("df_in, df_out, col",
                         [("invalid_add", "duplicated_add", "Translated Term"),
                          ("valid_add", "valid_add", "Translated Term"),
                          ("invalid_rep", "duplicated_rep", "New Translated Term"),
                          ("valid_rep", "valid_rep", "New Translated Term")])
def test_duplicated_term(df_in: pd.DataFrame, df_out: pd.DataFrame, col: str,
                         request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(format_check._duplicated_term(input, col), output)


@pytest.mark.parametrize("df_in, df_out", [("invalid_add", "lang_c_add"),
                                           ("valid_add", "valid_add"),
                                           ("invalid_chg", "invalid_chg"),
                                           ("valid_chg", "valid_chg"),
                                           ("invalid_ina", "invalid_ina"),
                                           ("valid_ina", "valid_ina"),
                                           ("invalid_rep", "lang_c_rep"),
                                           ("valid_rep", "valid_rep")])
def test_check_language_code(df_in: pd.DataFrame, df_out: pd.DataFrame,
                             request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(format_check._check_language_code(input), output)


@pytest.mark.parametrize("df_in, df_out", [("invalid_add", "case_add"),
                                           ("valid_add", "valid_add"),
                                           ("invalid_chg", "case_chg"),
                                           ("valid_chg", "valid_chg"),
                                           ("invalid_ina", "invalid_ina"),
                                           ("valid_ina", "valid_ina"),
                                           ("invalid_rep", "case_rep"),
                                           ("valid_rep", "valid_rep")])
def test_check_case_significance(df_in: pd.DataFrame, df_out: pd.DataFrame,
                                 request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(format_check._check_case_significance(input), output)


@pytest.mark.parametrize("df_in, df_out", [("invalid_add", "type_add"),
                                           ("valid_add", "valid_add"),
                                           ("invalid_chg", "type_chg"),
                                           ("valid_chg", "valid_chg"),
                                           ("invalid_ina", "invalid_ina"),
                                           ("valid_ina", "valid_ina"),
                                           ("invalid_rep", "type_rep"),
                                           ("valid_rep", "valid_rep")])
def test_check_type(df_in: pd.DataFrame, df_out: pd.DataFrame,
                    request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(format_check._check_type(input), output)


@pytest.mark.parametrize("df_in, df_out", [("invalid_add", "lang_rs_add"),
                                           ("valid_add", "valid_add"),
                                           ("invalid_chg", "lang_rs_chg"),
                                           ("valid_chg", "valid_chg"),
                                           ("invalid_ina", "invalid_ina"),
                                           ("valid_ina", "valid_ina"),
                                           ("invalid_rep", "lang_rs_rep"),
                                           ("valid_rep", "valid_rep")])
def test_check_language_refset(df_in: pd.DataFrame, df_out: pd.DataFrame,
                               request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(format_check._check_language_refset(input), output)


@pytest.mark.parametrize("df_in, df_out", [("invalid_add", "accept_add"),
                                           ("valid_add", "valid_add"),
                                           ("invalid_chg", "accept_chg"),
                                           ("valid_chg", "valid_chg"),
                                           ("invalid_ina", "invalid_ina"),
                                           ("valid_ina", "valid_ina"),
                                           ("invalid_rep", "accept_rep"),
                                           ("valid_rep", "valid_rep")])
def test_check_acceptability(df_in: pd.DataFrame, df_out: pd.DataFrame,
                             request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(format_check._check_acceptability(input), output)


@pytest.mark.parametrize("df_in, df_out", [("invalid_add", "invalid_add"),
                                           ("valid_add", "valid_add"),
                                           ("invalid_chg", "invalid_chg"),
                                           ("valid_chg", "valid_chg"),
                                           ("invalid_ina", "inact_ina"),
                                           ("valid_ina", "valid_ina"),
                                           ("invalid_rep", "inact_rep"),
                                           ("valid_rep", "valid_rep")])
def test_check_inactivation_reason(df_in: pd.DataFrame, df_out: pd.DataFrame,
                                   request: pytest.FixtureRequest) -> None:
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    pd.testing.assert_frame_equal(format_check._check_inactivation_reason(input),
                                  output)


@pytest.mark.parametrize("df_in, df_out, fts",
                         [("invalid_add", "invalid_add", "fts_null"),
                          ("valid_add", "valid_add", "fts_null"),
                          ("invalid_chg", "invalid_chg", "fts_null"),
                          ("valid_chg", "valid_chg", "fts_null"),
                          ("invalid_ina", "target_ina", "fts_inactive"),
                          ("valid_ina", "valid_ina", "fts_inactive"),
                          ("invalid_rep", "target_rep", "fts_inactive"),
                          ("valid_rep", "valid_rep", "fts_active")])
def test_check_association_target(df_in: pd.DataFrame, df_out: pd.DataFrame,
                                  fts: Generator, pytestconfig: pytest.Config,
                                  request: pytest.FixtureRequest) -> None:
    endpoint = server.Server(pytestconfig.getoption("endpoint"))
    input = request.getfixturevalue(df_in)
    output = request.getfixturevalue(df_out)
    fts = request.getfixturevalue(fts)
    pd.testing.assert_frame_equal(
        format_check._check_association_target(input, endpoint), output)
