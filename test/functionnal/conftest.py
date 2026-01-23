import os.path as op
import pytest
import pandas as pd
import responses

from typing import Any, Dict, Generator


def pytest_addoption(parser):
    parser.addoption("--endpoint", action="store")


@pytest.fixture
def fts_editorial(pytestconfig) -> Generator[responses.RequestsMock, Any, None]:
    sb = op.join(pytestconfig.getoption("endpoint"),
                 "ValueSet/$expand?url=http://snomed.info/sct/900000000000207008?fhir_vs=ecl/%3C%3C%20260787004") # noqa
    me = op.join(pytestconfig.getoption("endpoint"),
                 "ValueSet/$expand?url=http://snomed.info/sct/900000000000207008?fhir_vs=ecl/%3C%3C%20373873005") # noqa

    with responses.RequestsMock() as mock:
        mock.add(method=responses.GET, url=sb,
                 json={"expansion": {"contains": [{"code": "C2"}, {"code": "C26"},
                                                  {"code": "C27"}, {"code": "C28"}]}})

        mock.add(method=responses.GET, url=me,
                 json={"expansion": {"contains": [{"code": "C22"}, {"code": "C23"},
                                                  {"code": "C24"}, {"code": "C25"}]}})

        yield mock


@pytest.fixture
def df_editorial() -> pd.DataFrame:
    return pd.DataFrame(
        {"conceptId": [f"C{i}" for i in range(1, 44)],
         "term": ["la prothèse de hanche", "prothèse de la hanche",
                  "genou", "genou", "hanche", "dos de la main", "oeil",
                  "coeur", "petit orteil", "jambe", "bras", "encéphale",
                  "cerveau", "observation neurologique", "calcium augmenté",
                  "blessure par pression de la hanche",
                  "trouble épileptique", "déficience visuelle",
                  "syphilis", "engelure de la main gauche", "anthrax",
                  "amoxicilline", "amoxicilline", "amoxicilline",
                  "amoxicilline libération conventionnelle",
                  "tube sous vide EDTA avec anticoagulant irréversible-K2/aprotinine",
                  "acide borique pour prélèvement urinaire",
                  "stent", "intervention neuromusculaire",
                  "entretien téléphonique", "extraction d'un corps étranger",
                  "biopsie", "biopsie", "imagerie du tibia", "échographie",
                  "fluoroscopie de la trachée", "formation sur l'amputation",
                  "antécédents familiaux d'asthme", "lavage pharyngien",
                  "liquide de perfusion", "Ig antirabique",
                  "méta-hydroxybenzoate", "moénomycine B>1<"],
         "caseSignificanceId": ["CS", "ci", "ci", "ci", "ci", "ci", "ci", "ci", "ci",
                                "ci", "ci", "ci", "ci", "ci", "ci", "ci", "ci", "ci",
                                "ci", "ci", "ci", "ci", "ci", "ci", "ci", "ci", "ci",
                                "ci", "ci", "ci", "ci", "ci", "ci", "ci", "ci", "ci",
                                "ci", "ci", "ci", "ci", "ci", "ci", "cI"],
         "acceptabilityId": ["PREFERRED"] * 43,
         "FSN": ["", "", "Knee joint (body structure)",
                 "Entire knee (body structure)", "Hip region (body structure)",
                 "Dorsal area of hand (body structure)",
                 "Eye proper (body structure)", "Apex of heart (body structure)",
                 "Lesser toe (body structure)", "Lower limb (body structure)",
                 "Upper limb (body structure)", "Cerebrum (body structure)",
                 "Brain (body structure)", "Neurological finding (finding)",
                 "Calcium above reference range (finding)",
                 "Pressure injury of hip (disorder)", "Seizure disorder (disorder)",
                 "Visual impairment (disorder)", "Primary syphilis (disorder)",
                 "Frostbite of left hand (disorder)", "Anthrax (disorder)",
                 "Product containing amoxicillin (product)",
                 "Product containing only amoxicillin (product)",
                 "Product containing precisely amoxicillin (clinical drug)",
                 "Amoxicillin conventional release (product)",
                 "Evacuated blood collection tube, K2EDTA/aprotinin (product)",
                 "Evacuated urine specimen container, boric acid (H3BO3) (product)",
                 "Stent (physical object)", "Neuromuscular procedure (procedure)",
                 "Telephonic consultation (procedure)",
                 "Removal of foreign body (procedure)",
                 "Excisional biopsy (procedure)", "Incisional biopsy (procedure)",
                 "MRI of tibia (procedure)",
                 "Procedure using ultrasound guidance (procedure)",
                 "Fluoroscopy of trachea (procedure)",
                 "Amputation education (procedure)",
                 "Asthma familial history (situation)",
                 "Pharyngeal washings (specimen)",
                 "Intraveinous infusion fluid sample (specimen)",
                 "Rabies virus antibody (substance)",
                 "Meta-hydroxybenzoate (substance)", "Moenomycin B>1< (substance)"]}
    )


@pytest.fixture
def df_editorial_output(df_editorial) -> pd.DataFrame:
    check = pd.DataFrame(
        {"ar2": ["1", float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "ar6": [float("nan"), "1", float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "bs2": [float("nan"), float("nan"), "1", float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "bs3": [float("nan"), float("nan"), float("nan"), "1", float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "bs5": [float("nan"), float("nan"), float("nan"), float("nan"), "1",
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "bs6": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 "1", float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "bs7": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), "1", float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "bs8": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), "1", float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "bs9": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), "1", float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "bs10": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), "1",
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan")],
         "bs11": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  "1", float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan")],
         "bs12": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), "1", float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan")],
         "bs13": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), "1", float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan")],
         "co2": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), "1", float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "co6": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), "1",
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "pa3.1": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                   float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                   float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                   "1", float("nan"), float("nan"), float("nan"), float("nan"),
                   float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                   float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                   float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                   float("nan"), float("nan"), float("nan"), float("nan"),
                   float("nan"), float("nan"), float("nan"), float("nan")],
         "pa4": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), "1", float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "pa6": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), "1", float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "pa7": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), "1", float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "pa8": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), "1",
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "pa9": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 "1", float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "me1": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), "1", float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "me2": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), "1", float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "me3": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), "1", float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "me4": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), "1",
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "sb1": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 "1", float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "sb2": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), "1", float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "sb3": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), "1", float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "pr2": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), "1", float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "pr3": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), "1",
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "pr4": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 "1", float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "pr9": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), "1", float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "pr10": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), "1", float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan")],
         "pr12": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), "1", float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan")],
         "pr13": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), "1",
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan")],
         "pr14": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  "1", float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan")],
         "pr15": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                  float("nan"), "1", float("nan"), float("nan"), float("nan"),
                  float("nan"), float("nan"), float("nan")],
         "hs1": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), "1", float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "ec2": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), "1", float("nan"),
                 float("nan"), float("nan"), float("nan")],
         "ec4": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), "1",
                 float("nan"), float("nan"), float("nan")],
         "su1": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 "1", float("nan"), float("nan")],
         "su3": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), "1", float("nan")],
         "su8": [float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),
                 float("nan"), float("nan"), "1"]}
    )
    return pd.concat([df_editorial, check], axis=1)


@pytest.fixture
def active_concept():
    return {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "property", "part": [
                {"name": "code", "valueCode": "inactive"},
                {"name": "value", "valueBoolean": False}
            ]},
            {"name": "designation", "part": [
                {"name": "language", "valueCode": "en"},
                {"name": "use", "valueCoding": {
                    "system": "http://snomed.info/sct",
                    "code": "900000000000003001",
                    "display": "Fully specified name"
                }},
                {"name": "value", "valueString": "Clinical finding (finding)"}
            ]}
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
            ]},
            {"name": "designation", "part": [
                {"name": "language", "valueCode": "en"},
                {"name": "use", "valueCoding": {
                    "system": "http://snomed.info/sct",
                    "code": "900000000000003001",
                    "display": "Fully specified name"
                }},
                {"name": "value", "valueString": "Scar NOS (disorder)"}
            ]}
        ]
    }


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


@pytest.fixture
def add() -> pd.DataFrame:
    return pd.DataFrame({
        "Concept ID": ["C2"] * 2,
        "GB/US FSN Term (For reference only)": [""] * 2,
        "Preferred Term (For reference only)": [""] * 2,
        "Translated Term": ["concept SNOMED CT"] * 2,
        "Language Code": ["", "fr"],
        "Case significance": ["cI", "SC"],
        "Type": ["SYNONYM", "SYN"],
        "Language reference set": ["French", "FR"],
        "Acceptability": ["PREFERRED", "PREF"],
        "_FSN_": ["Scar NOS (disorder)"] * 2
    })


@pytest.fixture
def chg() -> pd.DataFrame:
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
def ina() -> pd.DataFrame:
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
def rep() -> pd.DataFrame:
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
        "Acceptability": ["PREF", "PREFERRED", "PREFERRED"],
        "_FSN_": ["Clinical finding (finding)", "Scar NOS (disorder)",
                  "Scar NOS (disorder)"]
    })


@pytest.fixture
def add_output(add) -> pd.DataFrame:
    check = pd.DataFrame({"W_cellule_vide": ["1", float("nan")],
                          "E_concept_inactif": ["1", "1"],
                          "W_terme_dupliqué": ["1", "1"],
                          "E_language_code": ["1", float("nan")],
                          "E_case_significance": [float("nan"), "1"],
                          "E_type": [float("nan"), "1"],
                          "E_language_refset": [float("nan"), "1"],
                          "E_acceptability": [float("nan"), "1"]})

    return pd.concat([add, check], axis=1)


@pytest.fixture
def chg_output(chg) -> pd.DataFrame:
    check = pd.DataFrame({"W_cellule_vide": ["1"],
                          "E_case_significance": ["1"],
                          "E_type": ["1"],
                          "E_language_refset": ["1"],
                          "E_acceptability": ["1"]})

    return pd.concat([chg, check], axis=1)


@pytest.fixture
def ina_output(ina) -> pd.DataFrame:
    check = pd.DataFrame({"W_cellule_vide": [float("nan"), float("nan"), "1"],
                          "E_inactivation_reason": [float("nan"), float("nan"), "1"],
                          "E_association_target": [float("nan"), "1", float("nan")],
                          "E_association_target_inactive": ["1", "", ""]})

    return pd.concat([ina, check], axis=1)


@pytest.fixture
def rep_output(rep) -> pd.DataFrame:
    check = pd.DataFrame({"W_cellule_vide": ["1", float("nan"), float("nan")],
                          "E_concept_inactif": ["", "1", "1"],
                          "W_terme_dupliqué": [float("nan"), "1", "1"],
                          "E_language_code": ["1", float("nan"), float("nan")],
                          "E_case_significance": ["1", float("nan"), float("nan")],
                          "E_type": ["1", float("nan"), float("nan")],
                          "E_language_refset": ["1", float("nan"), float("nan")],
                          "E_acceptability": ["1", float("nan"), float("nan")],
                          "E_inactivation_reason": [float("nan"), float("nan"), "1"],
                          "E_association_target": [float("nan"), "1", float("nan")],
                          "E_association_target_inactive": ["1", "", ""]
                          })

    return pd.concat([rep, check], axis=1)
