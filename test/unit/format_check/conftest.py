import os.path as op
import pytest
import pandas as pd
import responses

from typing import Any, Dict, Generator


def pytest_addoption(parser):
    parser.addoption("--endpoint", action="store")


####################################
# Fixtures mimant une réponse JSON #
####################################
@pytest.fixture
def active_concept():
    return {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "property", "part": [
                {"name": "code", "valueCode": "inactive"},
                {"name": "value", "valueBoolean": False}
            ]},
        ]
    }


@pytest.fixture
def inactive_concept():
    return {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "property", "part": [
                {"name": "code", "valueCode": "inactive"},
                {"name": "value", "valueBoolean": True}
            ]}
        ]
    }


##########################
# Fixtures mimant le FTS #
##########################
@pytest.fixture
def fts_active(active_concept: Dict,
               pytestconfig) -> Generator[responses.RequestsMock, Any, None]:
    url = op.join(pytestconfig.getoption("endpoint"),
                  "CodeSystem/$lookup?system=http://snomed.info/sct&version=http://snomed.info/sct/900000000000207008&code=C1") # noqa

    with responses.RequestsMock() as mock:
        mock.add(method=responses.GET, url=url, json=active_concept)

        yield mock


@pytest.fixture
def fts_inactive(inactive_concept: Dict,
                 pytestconfig) -> Generator[responses.RequestsMock, Any, None]:
    url = op.join(pytestconfig.getoption("endpoint"),
                  "CodeSystem/$lookup?system=http://snomed.info/sct&version=http://snomed.info/sct/900000000000207008&code=C2") # noqa

    with responses.RequestsMock() as mock:

        mock.add(method=responses.GET, url=url, json=inactive_concept)

        yield mock


@pytest.fixture
def fts_both(active_concept: Dict, inactive_concept: Dict,
             pytestconfig) -> Generator[responses.RequestsMock, Any, None]:
    valid = op.join(pytestconfig.getoption("endpoint"),
                    "CodeSystem/$lookup?system=http://snomed.info/sct&version=http://snomed.info/sct/900000000000207008&code=C1") # noqa
    invalid = op.join(pytestconfig.getoption("endpoint"),
                      "CodeSystem/$lookup?system=http://snomed.info/sct&version=http://snomed.info/sct/900000000000207008&code=C2") # noqa

    with responses.RequestsMock() as mock:
        mock.add(method=responses.GET, url=valid, json=active_concept)

        mock.add(method=responses.GET, url=invalid, json=inactive_concept)

        yield mock


@pytest.fixture
def fts_null() -> Generator[responses.RequestsMock, Any, None]:
    with responses.RequestsMock() as mock:
        yield mock


##################################
# Fixtures des batchs d"addition #
##################################
@pytest.fixture
def valid_add() -> pd.DataFrame:
    return pd.DataFrame({
        "Concept ID": ["C1"],
        "GB/US FSN Term (For reference only)": [""],
        "Preferred Term (For reference only)": [""],
        "Translated Term": ["concept SNOMED CT"],
        "Language Code": ["fr"],
        "Case significance": ["cI"],
        "Type": ["SYNONYM"],
        "Language reference set": ["French"],
        "Acceptability": ["PREFERRED"]
    })


@pytest.fixture
def invalid_add() -> pd.DataFrame:
    return pd.DataFrame({
        "Concept ID": ["C2"] * 2,
        "GB/US FSN Term (For reference only)": [""] * 2,
        "Preferred Term (For reference only)": [""] * 2,
        "Translated Term": ["concept SNOMED CT"] * 2,
        "Language Code": ["", "fr"],
        "Case significance": ["cI", "SC"],
        "Type": ["SYNONYM", "SYN"],
        "Language reference set": ["French", "FR"],
        "Acceptability": ["PREFERRED", "PREF"]
    })


@pytest.fixture
def empty_add(invalid_add) -> pd.DataFrame:
    return pd.concat([invalid_add, pd.Series(["1", float("nan")],
                                             name="W_cellule_vide")], axis=1)


@pytest.fixture
def sctid_add(invalid_add) -> pd.DataFrame:
    return pd.concat([invalid_add, pd.DataFrame({"E_concept_inactif": ["1", "1"]})],
                     axis=1)


@pytest.fixture
def duplicated_add(invalid_add) -> pd.DataFrame:
    return pd.concat([invalid_add, pd.Series(["1", "1"],
                                             name="W_terme_dupliqué")], axis=1)


@pytest.fixture
def lang_c_add(invalid_add) -> pd.DataFrame:
    return pd.concat([invalid_add, pd.Series(["1", float("nan")],
                                             name="E_language_code")], axis=1)


@pytest.fixture
def case_add(invalid_add) -> pd.DataFrame:
    return pd.concat([invalid_add, pd.Series([float("nan"), "1"],
                                             name="E_case_significance")], axis=1)


@pytest.fixture
def type_add(invalid_add) -> pd.DataFrame:
    return pd.concat([invalid_add, pd.Series([float("nan"), "1"], name="E_type")],
                     axis=1)


@pytest.fixture
def lang_rs_add(invalid_add) -> pd.DataFrame:
    return pd.concat([invalid_add, pd.Series([float("nan"), "1"],
                                             name="E_language_refset")], axis=1)


@pytest.fixture
def accept_add(invalid_add) -> pd.DataFrame:
    return pd.concat([invalid_add, pd.Series([float("nan"), "1"],
                                             name="E_acceptability")], axis=1)


#####################################
# Fixtures des batchs de changement #
#####################################
@pytest.fixture
def valid_chg() -> pd.DataFrame:
    return pd.DataFrame({
        "Description ID": ["D1"],
        "Preferred Term (For reference only)": [""],
        "Term (For reference only)": [""],
        "Case significance": ["ci"],
        "Type": ["SYNONYM"],
        "Language reference set": ["French"],
        "Acceptability": ["PREFERRED"]
    })


@pytest.fixture
def invalid_chg() -> pd.DataFrame:
    return pd.DataFrame({
        "Description ID": ["D1"],
        "Preferred Term (For reference only)": [""],
        "Term (For reference only)": [""],
        "Case significance": ["SC"],
        "Type": [""],
        "Language reference set": ["FR"],
        "Acceptability": ["PREF"]
    })


@pytest.fixture
def empty_chg(invalid_chg) -> pd.DataFrame:
    return pd.concat([invalid_chg, pd.Series(["1"], name="W_cellule_vide")], axis=1)


@pytest.fixture
def case_chg(invalid_chg) -> pd.DataFrame:
    return pd.concat([invalid_chg, pd.Series(["1"], name="E_case_significance")],
                     axis=1)


@pytest.fixture
def type_chg(invalid_chg) -> pd.DataFrame:
    return pd.concat([invalid_chg, pd.Series(["1"], name="E_type")], axis=1)


@pytest.fixture
def lang_rs_chg(invalid_chg) -> pd.DataFrame:
    return pd.concat([invalid_chg, pd.Series(["1"], name="E_language_refset")],
                     axis=1)


@pytest.fixture
def accept_chg(invalid_chg) -> pd.DataFrame:
    return pd.concat([invalid_chg, pd.Series(["1"], name="E_acceptability")],
                     axis=1)


######################################
# Fixtures des batchs d"inactivation #
######################################
@pytest.fixture
def valid_ina() -> pd.DataFrame:
    return pd.DataFrame({
        "Description ID Or Term": ["D1"],
        "Language Code (require if the term is specified)": [""],
        "Concept ID (Optional)": [""],
        "Preferred Term (For reference only)": [""],
        "Term (For reference only)": [""],
        "Inactivation Reason": ["Not semantically equivalent"],
        "Association Target ID1": ["C2"],
        "Association Target ID2": [""],
        "Association Target ID3": [""],
        "Association Target ID4": [""]
    })


@pytest.fixture
def invalid_ina() -> pd.DataFrame:
    return pd.DataFrame({
        "Description ID Or Term": ["D1", "D2", ""],
        "Language Code (require if the term is specified)": [""] * 3,
        "Concept ID (Optional)": [""] * 3,
        "Preferred Term (For reference only)": [""] * 3,
        "Term (For reference only)": [""] * 3,
        "Inactivation Reason": ["Not semantically equivalent",
                                "Not semantically equivalent", "Wrong"],
        "Association Target ID1": ["C2", "", ""],
        "Association Target ID2": [""] * 3,
        "Association Target ID3": [""] * 3,
        "Association Target ID4": [""] * 3
    })


@pytest.fixture
def empty_ina(invalid_ina) -> pd.DataFrame:
    return pd.concat([invalid_ina, pd.Series([float("nan"), float("nan"), "1"],
                                             name="W_cellule_vide")], axis=1)


@pytest.fixture
def inact_ina(invalid_ina) -> pd.DataFrame:
    return pd.concat([invalid_ina, pd.Series([float("nan"), float("nan"), "1"],
                                             name="E_inactivation_reason")], axis=1)


@pytest.fixture
def target_ina(invalid_ina) -> pd.DataFrame:
    return pd.concat([invalid_ina,
                      pd.DataFrame({"E_association_target": [float("nan"), "1",
                                                             float("nan")],
                                    "E_association_target_inactive": ["1", "", ""]})],
                     axis=1)


#######################################
# Fixtures des batchs de remplacement #
#######################################
@pytest.fixture
def valid_rep() -> pd.DataFrame:
    return pd.DataFrame({
        "Concept ID": ["C1", "C1"],
        "Description ID": ["D1", "D2"],
        "Preferred Term (For reference only)": [""] * 2,
        "Term (For reference only)": [""] * 2,
        "Inactivation Reason": ["Not semantically equivalent", "Outdated"],
        "Association Target ID1": ["C1", ""],
        "Association Target ID2": [""] * 2,
        "Association Target ID3": [""] * 2,
        "Association Target ID4": [""] * 2,
        "New Replacement Description ID": ["D3", ""],
        "Replacement term (For reference only)": [""] * 2,
        "New Translated Term": ["", "concept SNOMED CT"],
        "Language Code": ["fr", "fr"],
        "Case significance": ["cI", "cI"],
        "Type": ["SYNONYM", "SYNONYM"],
        "Language reference set": ["French", "French"],
        "Acceptability": ["PREFERRED", "PREFERRED"]
    })


@pytest.fixture
def invalid_rep() -> pd.DataFrame:
    return pd.DataFrame({
        "Concept ID": ["C1", "C2", "C2"],
        "Description ID": ["", "D2", "D3"],
        "Preferred Term (For reference only)": [""] * 3,
        "Term (For reference only)": [""] * 3,
        "Inactivation Reason": ["Not semantically equivalent",
                                "Not semantically equivalent", "Wrong"],
        "Association Target ID1": ["C2", "", ""],
        "Association Target ID2": [""] * 3,
        "Association Target ID3": [""] * 3,
        "Association Target ID4": [""] * 3,
        "New Replacement Description ID": ["D3", "", ""],
        "Replacement term (For reference only)": [""] * 3,
        "New Translated Term": ["", "concept SNOMED CT", "concept SNOMED CT"],
        "Language Code": ["", "fr", "fr"],
        "Case significance": ["", "cI", "cI"],
        "Type": ["", "SYNONYM", "SYNONYM"],
        "Language reference set": ["FR", "French", "French"],
        "Acceptability": ["PREF", "PREFERRED", "PREFERRED"]
    })


@pytest.fixture
def empty_rep(invalid_rep) -> pd.DataFrame:
    return pd.concat([invalid_rep, pd.Series(["1", float("nan"), float("nan")],
                                             name="W_cellule_vide")], axis=1)


@pytest.fixture
def sctid_rep(invalid_rep) -> pd.DataFrame:
    return pd.concat([invalid_rep, pd.DataFrame({"E_concept_inactif": ["", "1", "1"]})],
                     axis=1)


@pytest.fixture
def duplicated_rep(invalid_rep) -> pd.DataFrame:
    return pd.concat([invalid_rep, pd.Series([float("nan"), "1", "1"],
                                             name="W_terme_dupliqué")], axis=1)


@pytest.fixture
def lang_c_rep(invalid_rep) -> pd.DataFrame:
    return pd.concat([invalid_rep, pd.Series(["1", float("nan"), float("nan")],
                                             name="E_language_code")], axis=1)


@pytest.fixture
def case_rep(invalid_rep) -> pd.DataFrame:
    return pd.concat([invalid_rep, pd.Series(["1", float("nan"), float("nan")],
                                             name="E_case_significance")], axis=1)


@pytest.fixture
def type_rep(invalid_rep) -> pd.DataFrame:
    return pd.concat([invalid_rep, pd.Series(["1", float("nan"), float("nan")],
                                             name="E_type")], axis=1)


@pytest.fixture
def lang_rs_rep(invalid_rep) -> pd.DataFrame:
    return pd.concat([invalid_rep, pd.Series(["1", float("nan"), float("nan")],
                                             name="E_language_refset")], axis=1)


@pytest.fixture
def accept_rep(invalid_rep) -> pd.DataFrame:
    return pd.concat([invalid_rep, pd.Series(["1", float("nan"), float("nan")],
                                             name="E_acceptability")], axis=1)


@pytest.fixture
def inact_rep(invalid_rep) -> pd.DataFrame:
    return pd.concat([invalid_rep, pd.Series([float("nan"), float("nan"), "1"],
                                             name="E_inactivation_reason")], axis=1)


@pytest.fixture
def target_rep(invalid_rep) -> pd.DataFrame:
    return pd.concat([invalid_rep,
                      pd.DataFrame({"E_association_target": [float("nan"), "1",
                                                             float("nan")],
                                    "E_association_target_inactive": ["1", "", ""]})],
                     axis=1)
