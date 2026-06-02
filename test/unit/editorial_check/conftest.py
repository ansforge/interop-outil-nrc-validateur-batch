import pytest
import pandas as pd


######################
# Fixtures générales #
######################
@pytest.fixture
def null() -> pd.DataFrame:
    return pd.DataFrame(
        {"conceptId": ["1"], "FSN": ["SNOMED CT Concept"],
         "term": ["Concept SNOMED CT"], "acceptabilityId": ["PREFERRED"]}
    )


@pytest.fixture
def null_pt() -> pd.Series:
    return pd.Series(["PREFERRED"], name="acceptabilityId")


@pytest.fixture
def null_syn() -> pd.Series:
    return pd.Series(["ACCEPTABLE"], name="acceptabilityId")


@pytest.fixture
def semtag() -> pd.Series:
    def generate_series(n: int):
        return pd.Series([True] * n)
    return generate_series


###################################
# Fixtures pour règles génériques #
###################################
@pytest.fixture
def case() -> pd.DataFrame:
    return pd.DataFrame(
        {"term": ["Escherichia coli", "présence d'IgM", "pH mesuré", "kg"],
         "caseSignificanceId": ["CS"] * 4}
    )


@pytest.fixture
def case_output() -> pd.DataFrame:
    return pd.DataFrame({"caseSignificanceId": ["cI"]}, index=[1])


@pytest.fixture
def ar() -> pd.DataFrame:
    return pd.DataFrame(
        {"term": ["Les prothèses de hanche", "le dipositif pour le bras",
                  "la prothèse de la hanche", "un dispositif pour un bras",
                  "une prothèse pour une hanche", "dispositif d'un bras",
                  "prothèse d'une hanche", "prothèse de hanche"]}
    )


@pytest.fixture
def ar2(ar) -> pd.DataFrame:
    ar2 = pd.Series(["1", "1", "1", "1", "1", float("nan"), float("nan"),
                     float("nan")], name="ar2")

    return pd.concat([ar, ar2], axis=1)


@pytest.fixture
def ar6(ar) -> pd.DataFrame:
    ar6 = pd.Series([float("nan"), "1", "1", "1", "1", "1", "1", float("nan")],
                    name="ar6")

    return pd.concat([ar, ar6], axis=1)


#######################################
# Fixtures pour règles Body structure #
#######################################
@pytest.fixture
def bs() -> pd.DataFrame:
    return pd.DataFrame(
        {"conceptId": ["bs2", "bs2", "bs2",
                       "bs3_s1", "bs3_s1", "bs3_s2", "bs3_s2", "bs3_s3", "bs3_s3", "bs3_s3",  # noqa
                       "bs3_e", "bs3_e", "bs3_e",
                       "bs3_p", "bs3_p",
                       "bs5", "bs5", "bs5",
                       "bs6_z", "bs6_z", "bs6_z", "bs6_z", "bs6_z",
                       "bs6_a", "bs6_a", "bs6_a", "bs6_a", "bs6_a",
                       "bs7", "bs7", "bs7", "bs7", "bs7",
                       "bs8", "bs8", "bs8",
                       "bs9_1", "bs9_1", "bs9_2", "bs9_2", "bs9_3", "bs9_3", "bs9_3", "bs9_4",  # noqa
                       "bs10_limb", "bs10_limb", "bs10_leg", "bs10_leg",
                       "bs11_limb", "bs11_limb", "bs11_arm", "bs11_arm",
                       "bs12", "bs12", "bs12",
                       "bs13", "bs13", "bs13", "bs13_bs", "bs13_bs"],
         "FSN": ["Knee joint", "Knee joint", "Knee joint",  # bs2
                 "Knee structure", "Knee structure", "Knee structure", "Knee structure", "Knee structure", "Knee structure", "Knee structure",  # bs3 Structure # noqa
                 "Entire patella", "Entire patella", "Entire patella",  # bs3 Entire
                 "Part of knee", "Part of knee",  # bs3 Part
                 "Knee region", "Knee region", "Knee region",  # bs5
                 "Knee zone", "Knee zone", "Knee zone", "Knee zone", "Knee zone",  # bs6 Zone # noqa
                 "Knee area", "Knee area", "Knee area", "Knee area", "Knee area",  # bs6 Area # noqa
                 "Proper patella", "Proper patella", "Proper patella", "Proper patella", "Proper patella",  # bs7 # noqa
                 "Apex of lung", "Apex of lung", "Apex of lung",  # bs8
                 "Skin of lesser toe", "Skin of lesser toe", "Skin of lesser toe", "Skin of lesser toe", "Skin of lesser toe", "Skin of lesser toe", "Skin of lesser toe", "Skin of lesser toe",  # bs9 # noqa
                 "Skin of lower limb", "Skin of lower limb", "Skin of lower leg", "Skin of lower leg",  # bs10 # noqa
                 "Skin of upper limb", "Skin of upper limb", "Skin of upper arm", "Skin of upper arm",  # bs11 # noqa
                 "Cerebrum surface", "Cerebrum surface", "Cerebrum surface",  # bs12
                 "Brain surface", "Brain surface", "Brain surface", "Brainstem nerve", "Brainstem nerve"],  # bs13 # noqa
         "term": ["articulation du genou", "genou", "genou",  # bs2
                  "genou", "genou", "genou, structure", "genou, structure", "genou", "genou", "genou, structure",  # bs3 Structure # noqa
                  "rotule entière", "os entier de la rotule", "rotule",  # bs3 Entire
                  "partie du genou", "genou",  # bs3 Part
                  "région du genou", "genou", "genou",  # bs5
                  "zone du genou", "surface du genou", "aire du genou", "genou", "genou",  # bs6 Zone # noqa
                  "zone du genou", "surface du genou", "aire du genou", "genou", "genou",  # bs6 Area # noqa
                  "rotule propre", "rotule proprement dite", "os de la rotule proprement dit", "rotule", "rotule",  # bs7 # noqa
                  "apex du poumon", "poumon", "poumon",  # bs8
                  "peau d'orteil excepté l'hallux", "peau d'orteil excepté l'hallux", "peau d'orteil latéral", "peau d'orteil latéral", "peau d'orteil excepté l'hallux", "peau d'orteil excepté l'hallux", "peau d'orteil latéral", "peau de petit orteil", # bs9 # noqa
                  "Peau du membre inférieur", "Peau de la jambe", "Peau de la partie inférieure de la jambe", "Peau de la jambe",  # bs10 # noqa
                  "Peau du membre supérieur", "Peau du bras", "Peau de la partie supérieure du bras", "Peau du bras",  # bs11 # noqa
                  "surface du cerveau", "surface cérébrale", "surface encéphalique",  # bs12 # noqa
                  "surface de l'encéphale", "surface encéphalique", "surface cérébrale", "nerf du tronc cérébral", "nerf du tronc encéphalique"],  # bs13 # noqa
         "acceptabilityId": ["PREFERRED", "ACCEPTABLE", "PREFERRED",  # bs2
                             "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE",  # bs3 Structure # noqa
                             "PREFERRED", "PREFERRED", "PREFERRED",  # bs3 Entire
                             "PREFERRED", "PREFERRED",  # bs3 Part
                             "PREFERRED", "ACCEPTABLE", "PREFERRED",  # bs5
                             "PREFERRED", "PREFERRED", "PREFERRED", "ACCEPTABLE", "PREFERRED",  # bs6 Zone # noqa
                             "PREFERRED", "PREFERRED", "PREFERRED", "ACCEPTABLE", "PREFERRED",  # bs6 Area # noqa
                             "PREFERRED", "PREFERRED", "PREFERRED", "ACCEPTABLE", "PREFERRED",  # bs7 # noqa
                             "PREFERRED", "ACCEPTABLE", "PREFERRED",  # bs8
                             "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE", "PREFERRED",  # bs9 # noqa
                             "PREFERRED", "PREFERRED", "PREFERRED", "PREFERRED",  # bs10
                             "PREFERRED", "PREFERRED", "PREFERRED", "PREFERRED",  # bs11
                             "PREFERRED", "PREFERRED", "PREFERRED",  # bs12
                             "PREFERRED", "PREFERRED", "PREFERRED", "PREFERRED", "PREFERRED"]}  # bs13 # noqa
    )


@pytest.fixture
def bs2(bs) -> pd.DataFrame:
    bs2 = pd.Series([float("nan"), float("nan"), "1",  # bs2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs3 Structure # noqa
                     float("nan"), float("nan"), float("nan"),  # bs3 Entire
                     float("nan"), float("nan"),  # bs3 Part
                     float("nan"), float("nan"), float("nan"),  # bs5
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Zone # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Area # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs7 # noqa
                     float("nan"), float("nan"), float("nan"),  # bs8
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs9 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"),  # bs10
                     float("nan"), float("nan"), float("nan"), float("nan"),  # bs11
                     float("nan"), float("nan"), float("nan"),  # bs12
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),], name="bs2")  # bs13 # noqa
    return pd.concat([bs, bs2], axis=1)


@pytest.fixture
def bs3(bs) -> pd.DataFrame:
    bs3 = pd.Series([float("nan"), float("nan"), float("nan"),  # bs2
                     float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan"),  # bs3 Structure # noqa
                     float("nan"), float("nan"), "1",  # bs3 Entire
                     float("nan"), "1",  # bs3 Part
                     float("nan"), float("nan"), float("nan"),  # bs5
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Zone # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Area # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs7 # noqa
                     float("nan"), float("nan"), float("nan"),  # bs8
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs9 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"),  # bs10
                     float("nan"), float("nan"), float("nan"), float("nan"),  # bs11
                     float("nan"), float("nan"), float("nan"),  # bs12
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),], name="bs3")  # bs13 # noqa
    return pd.concat([bs, bs3], axis=1)


@pytest.fixture
def bs5(bs) -> pd.DataFrame:
    bs5 = pd.Series([float("nan"), float("nan"), float("nan"),  # bs2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs3 Structure # noqa
                     float("nan"), float("nan"), float("nan"),  # bs3 Entire
                     float("nan"), float("nan"),  # bs3 Part
                     float("nan"), float("nan"), "1",  # bs5
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Zone # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Area # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs7 # noqa
                     float("nan"), float("nan"), float("nan"),  # bs8
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs9 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"),  # bs10
                     float("nan"), float("nan"), float("nan"), float("nan"),  # bs11
                     float("nan"), float("nan"), float("nan"),  # bs12
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),], name="bs5")  # bs13 # noqa
    return pd.concat([bs, bs5], axis=1)


@pytest.fixture
def bs6(bs) -> pd.DataFrame:
    bs6 = pd.Series([float("nan"), float("nan"), float("nan"),  # bs2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs3 Structure # noqa
                     float("nan"), float("nan"), float("nan"),  # bs3 Entire
                     float("nan"), float("nan"),  # bs3 Part
                     float("nan"), float("nan"), float("nan"),  # bs5
                     float("nan"), float("nan"), float("nan"), float("nan"), "1",  # bs6 Zone # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), "1",  # bs6 Area # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs7 # noqa
                     float("nan"), float("nan"), float("nan"),  # bs8
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs9 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"),  # bs10
                     float("nan"), float("nan"), float("nan"), float("nan"),  # bs11
                     float("nan"), float("nan"), float("nan"),  # bs12
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),], name="bs6")  # bs13 # noqa
    return pd.concat([bs, bs6], axis=1)


@pytest.fixture
def bs7(bs) -> pd.DataFrame:
    bs7 = pd.Series([float("nan"), float("nan"), float("nan"),  # bs2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs3 Structure # noqa
                     float("nan"), float("nan"), float("nan"),  # bs3 Entire
                     float("nan"), float("nan"),  # bs3 Part
                     float("nan"), float("nan"), float("nan"),  # bs5
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Zone # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Area # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), "1",  # bs7
                     float("nan"), float("nan"), float("nan"),  # bs8
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs9 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"),  # bs10
                     float("nan"), float("nan"), float("nan"), float("nan"),  # bs11
                     float("nan"), float("nan"), float("nan"),  # bs12
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),], name="bs7")  # bs13 # noqa
    return pd.concat([bs, bs7], axis=1)


@pytest.fixture
def bs8(bs) -> pd.DataFrame:
    bs8 = pd.Series([float("nan"), float("nan"), float("nan"),  # bs2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs3 Structure # noqa
                     float("nan"), float("nan"), float("nan"),  # bs3 Entire
                     float("nan"), float("nan"),  # bs3 Part
                     float("nan"), float("nan"), float("nan"),  # bs5
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Zone # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Area # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs7 # noqa
                     float("nan"), float("nan"), "1",  # bs8
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs9 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"),  # bs10
                     float("nan"), float("nan"), float("nan"), float("nan"),  # bs11
                     float("nan"), float("nan"), float("nan"),  # bs12
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),], name="bs8")  # bs13 # noqa
    return pd.concat([bs, bs8], axis=1)


@pytest.fixture
def bs9(bs) -> pd.DataFrame:
    bs9 = pd.Series([float("nan"), float("nan"), float("nan"),  # bs2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs3 Structure # noqa
                     float("nan"), float("nan"), float("nan"),  # bs3 Entire
                     float("nan"), float("nan"),  # bs3 Part
                     float("nan"), float("nan"), float("nan"),  # bs5
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Zone # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Area # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs7 # noqa
                     float("nan"), float("nan"), float("nan"),  # bs8
                     float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan"), "1",  # bs9 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"),  # bs10
                     float("nan"), float("nan"), float("nan"), float("nan"),  # bs11
                     float("nan"), float("nan"), float("nan"),  # bs12
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),], name="bs9")  # bs13 # noqa
    return pd.concat([bs, bs9], axis=1)


@pytest.fixture
def bs10(bs) -> pd.DataFrame:
    bs10 = pd.Series([float("nan"), float("nan"), float("nan"),  # bs2
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs3 Structure # noqa
                      float("nan"), float("nan"), float("nan"),  # bs3 Entire
                      float("nan"), float("nan"),  # bs3 Part
                      float("nan"), float("nan"), float("nan"),  # bs5
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Zone # noqa
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Area # noqa
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs7 # noqa
                      float("nan"), float("nan"), float("nan"),  # bs8
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs9 # noqa
                      float("nan"), "1", float("nan"), "1",  # bs10
                      float("nan"), float("nan"), float("nan"), float("nan"),  # bs11
                      float("nan"), float("nan"), float("nan"),  # bs12
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),], name="bs10")  # bs13 # noqa
    return pd.concat([bs, bs10], axis=1)


@pytest.fixture
def bs11(bs) -> pd.DataFrame:
    bs11 = pd.Series([float("nan"), float("nan"), float("nan"),  # bs2
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs3 Structure # noqa
                      float("nan"), float("nan"), float("nan"),  # bs3 Entire
                      float("nan"), float("nan"),  # bs3 Part
                      float("nan"), float("nan"), float("nan"),  # bs5
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Zone # noqa
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Area # noqa
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs7 # noqa
                      float("nan"), float("nan"), float("nan"),  # bs8
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs9 # noqa
                      float("nan"), float("nan"), float("nan"), float("nan"),  # bs10
                      float("nan"), "1", float("nan"), "1",  # bs11
                      float("nan"), float("nan"), float("nan"),  # bs12
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),], name="bs11")  # bs13 # noqa
    return pd.concat([bs, bs11], axis=1)


@pytest.fixture
def bs12(bs) -> pd.DataFrame:
    bs12 = pd.Series([float("nan"), float("nan"), float("nan"),  # bs2
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs3 Structure # noqa
                      float("nan"), float("nan"), float("nan"),  # bs3 Entire
                      float("nan"), float("nan"),  # bs3 Part
                      float("nan"), float("nan"), float("nan"),  # bs5
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Zone # noqa
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Area # noqa
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs7 # noqa
                      float("nan"), float("nan"), float("nan"),  # bs8
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs9 # noqa
                      float("nan"), float("nan"), float("nan"), float("nan"),  # bs10
                      float("nan"), float("nan"), float("nan"), float("nan"),  # bs11
                      float("nan"), float("nan"), "1",  # bs12
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),], name="bs12")  # bs13 # noqa
    return pd.concat([bs, bs12], axis=1)


@pytest.fixture
def bs13(bs) -> pd.DataFrame:
    bs13 = pd.Series([float("nan"), float("nan"), float("nan"),  # bs2
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs3 Structure # noqa
                      float("nan"), float("nan"), float("nan"),  # bs3 Entire
                      float("nan"), float("nan"),  # bs3 Part
                      float("nan"), float("nan"), float("nan"),  # bs5
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Zone # noqa
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs6 Area # noqa
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs7 # noqa
                      float("nan"), float("nan"), float("nan"),  # bs8
                      float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # bs9 # noqa
                      float("nan"), float("nan"), float("nan"), float("nan"),  # bs10
                      float("nan"), float("nan"), float("nan"), float("nan"),  # bs11
                      float("nan"), float("nan"), float("nan"),  # bs12
                      float("nan"), float("nan"), "1", float("nan"), "1"], name="bs13")  # bs13 # noqa
    return pd.concat([bs, bs13], axis=1)


#########################################
# Fixtures pour règles Clinical Finding #
#########################################
@pytest.fixture
def co_pa() -> pd.DataFrame:
    return pd.DataFrame(
        {"conceptId": ["co2", "co2",
                       "co6_abv1", "co6_abv1", "co6_abv2", "co6_abv2", "co6_abv3", "co6_abv3", "co6_abv3",  # noqa
                       "co6_bel1", "co6_bel1", "co6_bel2", "co6_bel2", "co6_bel3", "co6_bel3", "co6_bel3",  # noqa
                       "co6_in1", "co6_in1", "co6_in2", "co6_in2", "co6_in3", "co6_in3", "co6_in3",  # noqa
                       "co6_out1", "co6_out1", "co6_out2", "co6_out2", "co6_out3", "co6_out3", "co6_out3",  # noqa
                       "pa2_trouble", "pa2_affection", "pa2_anomalie", "pa2_maladie", "pa2",  # noqa
                       "pa2_comp1", "pa2_comp1", "pa2_comp2", "pa2_comp2", "pa2_comp3", "pa2_comp3", "pa2_comp3",  # noqa
                       "pa3.1", "pa3.1",
                       "pa4_epi", "pa4_epi",
                       "pa4_sei", "pa4_sei", "pa4_sei", "pa4_sei",
                       "pa4_con", "pa4_con",
                       "pa6", "pa6",
                       "pa7_1", "pa7_2", "pa7_2",
                       "pa8_c", "pa8_c",
                       "pa8_f", "pa8_f",
                       "pa8_sf", "pa8_sf",
                       "pa9_c", "pa9_c",
                       "pa9_f", "pa9_f", "pa9_f", "pa9_b", "pa9_b",
                       "pa9_a", "pa9_a"],
         "FSN": ["Neurological finding", "Neurological finding",  # co2
                 "Iron above reference range", "Iron above reference range", "Iron above reference range", "Iron above reference range", "Protein above reference range", "Protein above reference range", "Protein above reference range",  # co6 above # noqa
                 "Iron below reference range", "Iron below reference range", "Iron below reference range", "Iron below reference range", "Protein below reference range", "Protein below reference range", "Protein below reference range",  # co6 below # noqa
                 "Iron within reference range", "Iron within reference range", "Iron within reference range", "Iron within reference range", "Protein within reference range", "Protein within reference range", "Protein within reference range",  # co6 within # noqa
                 "Iron outside reference range", "Iron outside reference range", "Iron outside reference range", "Iron outside reference range", "Protein outside reference range", "Protein outside reference range", "Protein outside reference range",  # co6 outside # noqa
                 "Eating disorder", "Disorder of skin", "Chromosomal disorder", "Iatrogenic disorder", "Sleep disorder",  # pa2 # noqa
                 "Disorder of pancreatic stent", "Disorder of pancreatic stent", "Disorder of pancreatic stent", "Disorder of pancreatic stent", "Disorder of pancreatic stent", "Disorder of pancreatic stent", "Disorder of pancreatic stent",  # pa2 Complication # noqa
                 "Pressure injury of hip", "Pressure injury of hip",  # pa3.1
                 "Reflex epilepsy", "Reflex epilepsy",  # pa4 Epilepsy
                 "Seizure issue", "Seizure issue", "Seizure issue", "Seizure issue",  # pa4 Seizure # noqa
                 "Uremic convulsion", "Uremic convulsion",  # pa4 Convulsion
                 "Visual impairment", "Visual impairment",  # pa6
                 "Primary osteoporosis", "Primary siphilis", "Primary siphilis",  # pa7
                 "Chilblain", "Chilblain",  # pa8 Chilblain
                 "Frostbite of left hand", "Frostbite of left hand",  # pa8 Frostbite
                 "Superficial frostbite of thorax", "Superficial frostbite of thorax",  # pa8 Superficial frostbite # noqa
                 "Carbuncle of breast", "Carbuncle of breast",  # pa9 Carbuncle
                 "Furuncle of hand", "Furuncle of hand", "Furuncle of hand", "Boil of hand", "Boil of hand",  # pa9 Furuncle Boil # noqa
                 "Anthrax", "Anthrax"],  # pa9 anthrax
         "term": ["constatation neurologique", "observation neurologique",  # co2
                  "fer supérieur à l'intervalle de référence", "fer supérieur à l'intervalle de référence", "fer supérieur aux valeurs de référence", "fer supérieur aux valeurs de référence", "protéine supérieure à l'intervalle de référence", "protéine supérieure à l'intervalle de référence", "protéine supérieure aux valeurs de référence",  # co6 above # noqa
                  "fer inférieur à l'intervalle de référence", "fer inférieur à l'intervalle de référence", "fer inférieur aux valeurs de référence", "fer inférieur aux valeurs de référence", "protéine inférieure à l'intervalle de référence", "protéine inférieure à l'intervalle de référence", "protéine inférieure aux valeurs de référence",  # co6 below # noqa
                  "fer dans l'intervalle de référence", "fer dans l'intervalle de référence", "fer dans les valeurs de référence", "fer dans les valeurs de référence", "protéine dans l'intervalle de référence", "protéine dans l'intervalle de référence", "protéine dans les valeurs de référence",  # co6 within # noqa
                  "fer en dehors de l'intervalle de référence", "fer en dehors de l'intervalle de référence", "fer en dehors des valeurs de référence", "fer en dehors des valeurs de référence", "protéine en dehors de l'intervalle de référence", "protéine en dehors de l'intervalle de référence", "protéine en dehors des valeurs de référence",  # co6 outside # noqa
                  "trouble de l'alimentation", "affection cutanée", "anomalie chromosomique", "maladie iatrogénique", "sommeil défaillant",  # pa2 # noqa
                  "complication d'endoprothèse pancréatique", "complication d'endoprothèse pancréatique", "problème de stent pancréatique", "problème de stent pancréatique", "complication d'endoprothèse pancréatique", "complication d'endoprothèse pancréatique", "problème de stent pancréatique",  # pa2 Complication # noqa
                  "escarre de la hanche", "blessure par pression de la hanche",  # pa3.1
                  "épilepsie réflexe", "crise réflexe",  # pa4 Epilepsy
                  "crise", "convulsion", "trouble convulsif", "épilepsie",  # pa4 Seizure # noqa
                  "convulsions urémiques", "crise urémique",  # pa4 Convulsion
                  "atteinte de la vision", "déficience visuelle",  # pa6
                  "ostéoporose primitive", "syphilis primaire", "syphilis primordiale",  # pa7 # noqa
                  "engelure", "gelure",  # pa8 Chilblain
                  "gelure de la main gauche", "engelure de la main gauche",  # pa8 Frostbite # noqa
                  "gelure superficielle du thorax", "engelure superficielle du thorax",  # pa8 Superficial frostbite # noqa
                  "anthrax du sein", "maladie du sein",  # pa9 Carbuncle
                  "furoncle de la main", "folliculite nécrotique de la main", "maladie de la main", "clou de la main", "maladie de la main",  # pa9 Furuncle Boil # noqa
                  "maladie du charbon", "anthrax"],  # pa9 anthrax
         "acceptabilityId": ["PREFERRED", "PREFERRED",  # co2
                             "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE",  # co6 above # noqa
                             "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE",  # co6 below # noqa
                             "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE",  # co6 within # noqa
                             "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE",  # co6 outside # noqa
                             "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "PREFERRED",  # pa2 # noqa
                             "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE",  # pa2 Complication # noqa
                             "PREFERRED", "PREFERRED",  # pa3.1
                             "PREFERRED", "PREFERRED",  # pa4 Epilepsy
                             "PREFERRED", "PREFERRED", "PREFERRED", "PREFERRED",  # pa4 Seizure # noqa
                             "PREFERRED", "PREFERRED",  # pa4 Convulsion
                             "PREFERRED", "PREFERRED",  # pa6
                             "PREFERRED", "PREFERRED", "PREFERRED",  # pa7
                             "PREFERRED", "PREFERRED",  # pa8 Chilblain
                             "PREFERRED", "PREFERRED",  # pa8 Frostbite
                             "PREFERRED", "PREFERRED",  # pa8 Superficial frostbite
                             "PREFERRED", "PREFERRED",  # pa9 Carbuncle
                             "PREFERRED", "PREFERRED", "PREFERRED", "PREFERRED", "PREFERRED",  # pa9 Furuncle Boil # noqa
                             "PREFERRED", "PREFERRED"]}  # pa9 anthrax
    )


@pytest.fixture
def co2(co_pa) -> pd.DataFrame:
    co2 = pd.Series([float("nan"), "1",  # co2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 above # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 below # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 within # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 outside # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 Complication # noqa
                     float("nan"), float("nan"),  # pa3.1
                     float("nan"), float("nan"),  # pa4 Epilepsy
                     float("nan"), float("nan"), float("nan"), float("nan"),  # pa4 Seizure # noqa
                     float("nan"), float("nan"),  # pa4 Convulsion
                     float("nan"), float("nan"),  # pa6
                     float("nan"), float("nan"), float("nan"),  # pa7
                     float("nan"), float("nan"),  # pa8 Chilblain
                     float("nan"), float("nan"),  # pa8 Frostbite
                     float("nan"), float("nan"),  # pa8 Superficial frostbite
                     float("nan"), float("nan"),  # pa9 Carbuncle
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa9 Furuncle Boil # noqa
                     float("nan"), float("nan")], name="co2")  # pa9 anthrax
    return pd.concat([co_pa, co2], axis=1)


@pytest.fixture
def co6(co_pa) -> pd.DataFrame:
    co6 = pd.Series([float("nan"), float("nan"),  # co2
                     float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan"),   # co6 above # noqa
                     float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan"),   # co6 below # noqa
                     float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan"),   # co6 within # noqa
                     float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan"),   # co6 outside # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 Complication # noqa
                     float("nan"), float("nan"),  # pa3.1
                     float("nan"), float("nan"),  # pa4 Epilepsy
                     float("nan"), float("nan"), float("nan"), float("nan"),  # pa4 Seizure # noqa
                     float("nan"), float("nan"),  # pa4 Convulsion
                     float("nan"), float("nan"),  # pa6
                     float("nan"), float("nan"), float("nan"),  # pa7
                     float("nan"), float("nan"),  # pa8 Chilblain
                     float("nan"), float("nan"),  # pa8 Frostbite
                     float("nan"), float("nan"),  # pa8 Superficial frostbite
                     float("nan"), float("nan"),  # pa9 Carbuncle
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa9 Furuncle Boil # noqa
                     float("nan"), float("nan")], name="co6")  # pa9 anthrax
    return pd.concat([co_pa, co6], axis=1)


@pytest.fixture
def pa2(co_pa) -> pd.DataFrame:
    pa2 = pd.Series([float("nan"), float("nan"),  # co2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 above # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 below # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 within # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 outside # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), "1",  # pa2 # noqa
                     float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 Complication # noqa
                     float("nan"), float("nan"),  # pa3.1
                     float("nan"), float("nan"),  # pa4 Epilepsy
                     float("nan"), float("nan"), float("nan"), float("nan"),  # pa4 Seizure # noqa
                     float("nan"), float("nan"),  # pa4 Convulsion
                     float("nan"), float("nan"),  # pa6
                     float("nan"), float("nan"), float("nan"),  # pa7
                     float("nan"), float("nan"),  # pa8 Chilblain
                     float("nan"), float("nan"),  # pa8 Frostbite
                     float("nan"), float("nan"),  # pa8 Superficial frostbite
                     float("nan"), float("nan"),  # pa9 Carbuncle
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa9 Furuncle Boil # noqa
                     float("nan"), float("nan")], name="pa2")  # pa9 anthrax
    return pd.concat([co_pa, pa2], axis=1)


@pytest.fixture
def pa3_1(co_pa) -> pd.DataFrame:
    pa3_1 = pd.Series([float("nan"), float("nan"),  # co2
                       float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 above # noqa
                       float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 below # noqa
                       float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 within # noqa
                       float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 outside # noqa
                       float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 # noqa
                       float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 Complication # noqa
                       float("nan"), "1",  # pa3.1
                       float("nan"), float("nan"),  # pa4 Epilepsy
                       float("nan"), float("nan"), float("nan"), float("nan"),  # pa4 Seizure # noqa
                       float("nan"), float("nan"),  # pa4 Convulsion
                       float("nan"), float("nan"),  # pa6
                       float("nan"), float("nan"), float("nan"),  # pa7
                       float("nan"), float("nan"),  # pa8 Chilblain
                       float("nan"), float("nan"),  # pa8 Frostbite
                       float("nan"), float("nan"),  # pa8 Superficial frostbite
                       float("nan"), float("nan"),  # pa9 Carbuncle
                       float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa9 Furuncle Boil # noqa
                       float("nan"), float("nan")], name="pa3.1")  # pa9 anthrax
    return pd.concat([co_pa, pa3_1], axis=1)


@pytest.fixture
def pa4(co_pa) -> pd.DataFrame:
    pa4 = pd.Series([float("nan"), float("nan"),  # co2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 above # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 below # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 within # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 outside # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 Complication # noqa
                     float("nan"), float("nan"),  # pa3.1
                     float("nan"), "1",  # pa4 Epilepsy
                     float("nan"), float("nan"), float("nan"), "1",  # pa4 Seizure # noqa
                     float("nan"), "1",  # pa4 Convulsion
                     float("nan"), float("nan"),  # pa6
                     float("nan"), float("nan"), float("nan"),  # pa7
                     float("nan"), float("nan"),  # pa8 Chilblain
                     float("nan"), float("nan"),  # pa8 Frostbite
                     float("nan"), float("nan"),  # pa8 Superficial frostbite
                     float("nan"), float("nan"),  # pa9 Carbuncle
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa9 Furuncle Boil # noqa
                     float("nan"), float("nan")], name="pa4")  # pa9 anthrax
    return pd.concat([co_pa, pa4], axis=1)


@pytest.fixture
def pa6(co_pa) -> pd.DataFrame:
    pa6 = pd.Series([float("nan"), float("nan"),  # co2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 above # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 below # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 within # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 outside # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 Complication # noqa
                     float("nan"), float("nan"),  # pa3.1
                     float("nan"), float("nan"),  # pa4 Epilepsy
                     float("nan"), float("nan"), float("nan"), float("nan"),  # pa4 Seizure # noqa
                     float("nan"), float("nan"),  # pa4 Convulsion
                     float("nan"), "1",  # pa6
                     float("nan"), float("nan"), float("nan"),  # pa7
                     float("nan"), float("nan"),  # pa8 Chilblain
                     float("nan"), float("nan"),  # pa8 Frostbite
                     float("nan"), float("nan"),  # pa8 Superficial frostbite
                     float("nan"), float("nan"),  # pa9 Carbuncle
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa9 Furuncle Boil # noqa
                     float("nan"), float("nan")], name="pa6")  # pa9 anthrax
    return pd.concat([co_pa, pa6], axis=1)


@pytest.fixture
def pa7(co_pa) -> pd.DataFrame:
    pa7 = pd.Series([float("nan"), float("nan"),  # co2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 above # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 below # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 within # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 outside # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 Complication # noqa
                     float("nan"), float("nan"),  # pa3.1
                     float("nan"), float("nan"),  # pa4 Epilepsy
                     float("nan"), float("nan"), float("nan"), float("nan"),  # pa4 Seizure # noqa
                     float("nan"), float("nan"),  # pa4 Convulsion
                     float("nan"), float("nan"),  # pa6
                     float("nan"), float("nan"), "1",  # pa7
                     float("nan"), float("nan"),  # pa8 Chilblain
                     float("nan"), float("nan"),  # pa8 Frostbite
                     float("nan"), float("nan"),  # pa8 Superficial frostbite
                     float("nan"), float("nan"),  # pa9 Carbuncle
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa9 Furuncle Boil # noqa
                     float("nan"), float("nan")], name="pa7")  # pa9 anthrax
    return pd.concat([co_pa, pa7], axis=1)


@pytest.fixture
def pa8(co_pa) -> pd.DataFrame:
    pa8 = pd.Series([float("nan"), float("nan"),  # co2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 above # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 below # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 within # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 outside # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 Complication # noqa
                     float("nan"), float("nan"),  # pa3.1
                     float("nan"), float("nan"),  # pa4 Epilepsy
                     float("nan"), float("nan"), float("nan"), float("nan"),  # pa4 Seizure # noqa
                     float("nan"), float("nan"),  # pa4 Convulsion
                     float("nan"), float("nan"),  # pa6
                     float("nan"), float("nan"), float("nan"),  # pa7
                     float("nan"), "1",  # pa8 Chilblain
                     float("nan"), "1",  # pa8 Frostbite
                     float("nan"), "1",  # pa8 Superficial frostbite
                     float("nan"), float("nan"),  # pa9 Carbuncle
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa9 Furuncle Boil # noqa
                     float("nan"), float("nan")], name="pa8")  # pa9 anthrax
    return pd.concat([co_pa, pa8], axis=1)


@pytest.fixture
def pa9(co_pa) -> pd.DataFrame:
    pa9 = pd.Series([float("nan"), float("nan"),  # co2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 above # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 below # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 within # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),   # co6 outside # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pa2 Complication # noqa
                     float("nan"), float("nan"),  # pa3.1
                     float("nan"), float("nan"),  # pa4 Epilepsy
                     float("nan"), float("nan"), float("nan"), float("nan"),  # pa4 Seizure # noqa
                     float("nan"), float("nan"),  # pa4 Convulsion
                     float("nan"), float("nan"),  # pa6
                     float("nan"), float("nan"), float("nan"),  # pa7
                     float("nan"), float("nan"),  # pa8 Chilblain
                     float("nan"), float("nan"),  # pa8 Frostbite
                     float("nan"), float("nan"),  # pa8 Superficial frostbite
                     float("nan"), "1",  # pa9 Carbuncle
                     float("nan"), float("nan"), "1", float("nan"), "1",  # pa9 Furuncle Boil # noqa
                     float("nan"), "1"], name="pa9")  # pa9 anthrax
    return pd.concat([co_pa, pa9], axis=1)


############################################################
# Fixtures pour règles Pharmaceutical / biological product #
############################################################
@pytest.fixture
def me() -> pd.DataFrame:
    return pd.DataFrame(
        {"conceptId": ["me1_p", "me1_p", "me1_p",
                       "me1_v", "me1_v", "me1_v",
                       "me2_p", "me2_p", "me2_p",
                       "me2_v", "me2_v", "me2_v",
                       "me3", "me3", "me3",
                       "me4", "me4", "me4"],
         "FSN": ["Product containing amoxicilline", "Product containing amoxicilline", "Product containing amoxicilline",  # me1 Product # noqa
                 "Vaccine product containing Dengue virus antigen", "Vaccine product containing Dengue virus antigen", "Vaccine product containing Dengue virus antigen",  # me1 Vaccin # noqa
                 "Product containing only amoxicilline", "Product containing only amoxicilline", "Product containing only amoxicilline",  # me2 Product # noqa
                 "Vaccine product containing only Dengue virus antigen", "Vaccine product containing only Dengue virus antigen", "Vaccine product containing only Dengue virus antigen",  # me2 Vaccin # noqa
                 "Product containing precisely amoxicilline (clinical drug)", "Product containing precisely amoxicilline (clinical drug)", "Product containing precisely amoxicilline (clinical drug)",  # me3 # noqa
                 "Product containing precisely amoxicilline conventional release oral tablet", "Product containing precisely amoxicilline conventional release oral tablet", "Product containing precisely amoxicilline conventional release oral tablet"],  # me4 # noqa
         "term": ["produit contenant amoxicilline", "amoxicilline", "amoxicilline",  # me1 Product # noqa
                  "vaccin contenant des antigènes du virus de la dengue", "vaccin contre la dengue", "vaccin contre la dengue",  # me1 Vaccin # noqa
                  "produit contenant uniquement amoxicilline", "amoxicilline", "amoxicilline",  # me2 Product # noqa
                  "vaccin contenant uniquement des antigènes du virus de la dengue", "vaccin contre la dengue", "vaccin contre la dengue",  # me2 Vaccin # noqa
                  "produit contenant précisément amoxicilline", "amoxicilline", "amoxicilline",  # me3 # noqa
                  "amoxicilline, comprimé oral", "amoxicilline, libération conventionnelle, comprimé oral", "amoxicilline, libération conventionnelle, comprimé oral"],  # me4 # noqa
         "acceptabilityId": ["PREFERRED", "ACCEPTABLE", "PREFERRED",  # me1 Product
                             "PREFERRED", "ACCEPTABLE", "PREFERRED",  # me1 Vaccin
                             "PREFERRED", "ACCEPTABLE", "PREFERRED",  # me2 Product
                             "PREFERRED", "ACCEPTABLE", "PREFERRED",  # me2 Vaccin
                             "PREFERRED", "ACCEPTABLE", "PREFERRED",  # me3
                             "PREFERRED", "ACCEPTABLE", "PREFERRED"]}  # me4
    )


@pytest.fixture
def me1(me) -> pd.DataFrame:
    me1 = pd.Series([float("nan"), float("nan"), "1",  # me1 Product
                     float("nan"), float("nan"), "1",  # me1 Vaccin
                     float("nan"), float("nan"), float("nan"),  # me2 Product
                     float("nan"), float("nan"), float("nan"),  # me2 Vaccin
                     float("nan"), float("nan"), float("nan"),  # me3
                     float("nan"), float("nan"), float("nan")], name="me1")  # me4
    return pd.concat([me, me1], axis=1)


@pytest.fixture
def me2(me) -> pd.DataFrame:
    me2 = pd.Series([float("nan"), float("nan"), float("nan"),  # me1 Product
                     float("nan"), float("nan"), float("nan"),  # me1 Vaccin
                     float("nan"), float("nan"), "1",  # me2 Product
                     float("nan"), float("nan"), "1",  # me2 Vaccin
                     float("nan"), float("nan"), float("nan"),  # me3
                     float("nan"), float("nan"), float("nan")], name="me2")  # me4
    return pd.concat([me, me2], axis=1)


@pytest.fixture
def me3(me) -> pd.DataFrame:
    me3 = pd.Series([float("nan"), float("nan"), float("nan"),  # me1 Product
                     float("nan"), float("nan"), float("nan"),  # me1 Vaccin
                     float("nan"), float("nan"), float("nan"),  # me2 Product
                     float("nan"), float("nan"), float("nan"),  # me2 Vaccin
                     float("nan"), float("nan"), "1",  # me3
                     float("nan"), float("nan"), float("nan")], name="me3")  # me4
    return pd.concat([me, me3], axis=1)


@pytest.fixture
def me4(me) -> pd.DataFrame:
    me4 = pd.Series([float("nan"), float("nan"), float("nan"),  # me1 Product
                     float("nan"), float("nan"), float("nan"),  # me1 Vaccin
                     float("nan"), float("nan"), float("nan"),  # me2 Product
                     float("nan"), float("nan"), float("nan"),  # me2 Vaccin
                     float("nan"), float("nan"), float("nan"),  # me3
                     float("nan"), float("nan"), "1"], name="me4")  # me4
    return pd.concat([me, me4], axis=1)


########################################
# Fixtures pour règles Physical object #
########################################
@pytest.fixture
def sb() -> pd.DataFrame:
    return pd.DataFrame(
        {"conceptId": ["sb1", "sb1", "sb1",
                       "sb2", "sb2", "sb2",
                       "sb3_1", "sb3_1", "sb3_2", "sb3_2", "sb3_3", "sb3_3", "sb3_3"],
         "FSN": ["Evacuated blood collection tube, K2EDTA/aprotinin", "Evacuated blood collection tube, K2EDTA/aprotinin", "Evacuated blood collection tube, K2EDTA/aprotinin",  # sb1 # noqa
                 "Evacuated urine specimen container, boric acid (H3BO3)", "Evacuated urine specimen container, boric acid (H3BO3)", "Evacuated urine specimen container, boric acid (H3BO3)",  # sb2 # noqa
                 "Metal stent", "Metal stent", "Metal stent", "Metal stent", "Metal stent", "Metal stent", "Metal stent"],  # sb3 # noqa
         "term": ["tube sous vide EDTA avec anticoagulant irréversible-K2/aprotinine pour prélèvement sanguin", "tube sous vide EDTA avec anticoagulant irréversible-K2/aprotinine", "tube sous vide EDTA avec anticoagulant irréversible-K2/aprotinine",  # sb1 # noqa
                  "support sous vide boraté pour prélèvement urinaire", "acide borique pour prélèvement urinaire", "acide borique pour prélèvement urinaire",  # sb2 # noqa
                  "endoprothèse métallique", "endoprothèse métallique", "stent métallique", "stent métallique", "endoprothèse métallique", "endoprothèse métallique", "stent métallique"],  # sb3 # noqa
         "acceptabilityId": ["PREFERRED", "ACCEPTABLE", "PREFERRED",  # sb1
                             "PREFERRED", "ACCEPTABLE", "PREFERRED",  # sb2
                             "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE"]}  # sb3 # noqa
    )


@pytest.fixture
def sb1(sb) -> pd.DataFrame:
    sb1 = pd.Series([float("nan"), float("nan"), "1",  # sb1
                     float("nan"), float("nan"), float("nan"),  # sb2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan")], name="sb1")  # sb3 # noqa
    return pd.concat([sb, sb1], axis=1)


@pytest.fixture
def sb2(sb) -> pd.DataFrame:
    sb2 = pd.Series([float("nan"), float("nan"), float("nan"),  # sb1
                     float("nan"), float("nan"), "1",  # sb2
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan")], name="sb2")  # sb3 # noqa
    return pd.concat([sb, sb2], axis=1)


@pytest.fixture
def sb3(sb) -> pd.DataFrame:
    sb3 = pd.Series([float("nan"), float("nan"), float("nan"),  # sb1
                     float("nan"), float("nan"), float("nan"),  # sb2
                     float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan")], name="sb3")  # sb3 # noqa
    return pd.concat([sb, sb3], axis=1)


##################################
# Fixtures pour règles Procedure #
##################################
@pytest.fixture
def pr() -> pd.DataFrame:
    return pd.DataFrame(
        {"conceptId": ["pr2_1", "pr2_1", "pr2_2", "pr2_2", "pr2_3", "pr2_3", "pr2_3",
                       "pr2_chir1", "pr2_chir1", "pr2_chir2", "pr2_chir2", "pr2_chir2", "pr2_chir3", "pr2_chir3", "pr2_chir3", "pr2_chir3",  # noqa
                       "pr3", "pr3",
                       "pr4", "pr4",
                       "pr4_magne", "pr4_magne",
                       "pr9_1", "pr9_1", "pr9_2", "pr9_2", "pr9_3", "pr9_3", "pr9_3",
                       "pr10", "pr10",
                       "pr12_1", "pr12_1", "pr12_2", "pr12_2", "pr12_3", "pr12_3", "pr12_3",  # noqa
                       "pr13_1", "pr13_1", "pr13_2", "pr13_2", "pr13_3", "pr13_3", "pr13_3",  # noqa
                       "pr14_1", "pr14_1", "pr14_2", "pr14_2", "pr14_3", "pr14_3", "pr14_3",  # noqa
                       "pr15", "pr15"],
         "FSN": ["Head procedure", "Head procedure", "Head procedure", "Head procedure", "Head procedure", "Head procedure", "Head procedure",  # pr2 # noqa
                 "Head surgical procedure", "Head surgical procedure", "Head operation", "Head operation", "Head operation", "Head operation", "Head operation", "Head operation", "Head operation",  # pr2 Chirurgie # noqa
                 "Telephone consultation", "Telephone consultation",  # pr3
                 "Removal of foreign body from head", "Removal of foreign body from head",  # pr4 # noqa
                 "Magnet extraction of foreign body from head", "Magnet extraction of foreign body from head",  # pr4 Magnétique # noqa
                 "Excisional biopsy of mass", "Excisional biopsy of mass", "Excisional biopsy of mass", "Excisional biopsy of mass", "Excisional biopsy of mass", "Excisional biopsy of mass", "Excisional biopsy of mass",  # pr9 # noqa
                 "Incisional biopsy of brain", "Incisional biopsy of brain",  # pr10
                 "Chest MRI", "Chest MRI", "Chest magnetic resonance imaging", "Chest magnetic resonance imaging", "Magnetic resonance angiography of chest", "Magnetic resonance angiography of chest", "Magnetic resonance angiography of chest",  # pr12 # noqa
                 "Excision using imaging guidance", "Excision using imaging guidance", "Excision using imaging guidance", "Excision using imaging guidance", "Excision using imaging guidance", "Excision using imaging guidance", "Excision using imaging guidance",  # pr13 # noqa
                 "Fluoroscopy of trachea", "Fluoroscopy of trachea", "Fluoroscopic imaging of trachea", "Fluoroscopic imaging of trachea", "Fluoroscopy of trachea", "Fluoroscopy of trachea", "Fluoroscopy of trachea",  # pr14 # noqa
                 "Hepatitis education", "Hepatitis education"],  # pr15
         "term": ["procédure de la tête", "procédure de la tête", "intervention de la tête", "intervention de la tête", "procédure de la tête", "procédure de la tête", "intervention de la tête",  # pr2 # noqa
                  "intervention chirurgicale de la tête", "opération de la tête", "opération de la tête", "opération de la tête", "chirurgie de la tête", "intervention chirurgicale de la tête", "intervention chirurgicale de la tête", "opération de la tête", "chirurgie de la tête",  # pr2 Chirurgie # noqa
                  "consultation téléphonique", "rendez-vous téléphonique",  # pr3
                  "retrait d'un corps étranger de la tête", "extraction d'un corps étranger de la tête",  # pr4 # noqa
                  "extraction avec un aimant d'un corps étranger de la tête", "retrait d'un corps étranger de la tête à l'aide d'un aimant",  # pr4 Magnétique # noqa
                  "biopsie-exérèse d'une masse", "biopsie-exérèse d'une masse", "biopsie excisionnelle d'une masse", "biopsie excisionnelle d'une masse", "biopsie-exérèse d'une masse", "biopsie-exérèse d'une masse", "biopsie excisionnelle d'une masse",  # pr9 # noqa
                  "biopsie incisionnelle de l'encéphale", "biopsie de l'encéphale",  # pr10 # noqa
                  "IRM du thorax", "IRM du thorax", "imagerie par résonance magnétique du thorax", "imagerie par résonance magnétique du thorax", "angiographie par IRM du thorax", "angiographie par IRM du thorax", "angiographie par imagerie par résonance magnétique du thorax",  # pr12 # noqa
                  "excision de la trachée guidée par imagerie", "excision de la trachée guidée par imagerie", "excision de la trachée sous guidage par imagerie", "excision de la trachée sous guidage par imagerie", "excision de la trachée guidée par imagerie", "excision de la trachée guidée par imagerie", "excision de la trachée sous guidage par imagerie",  # pr13 # noqa
                  "radioscopie de la trachée", "radioscopie de la trachée", "examen fluoroscopique de la trachée", "examen fluoroscopique de la trachée", "radioscopie de la trachée", "radioscopie de la trachée", "fluoroscopie de la trachée",  # pr14 # noqa
                  "éducation concernant l'hépatite", "formation concernant l'hépatite"],  # pr15 # noqa
         "acceptabilityId": ["PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE",  # pr2 # noqa
                             "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE", "ACCEPTABLE",  # pr2 Chirurgie # noqa
                             "PREFERRED", "PREFERRED",  # pr3
                             "PREFERRED", "PREFERRED",  # pr4
                             "PREFERRED", "PREFERRED",  # pr4 Magnétique
                             "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE",  # pr9 # noqa
                             "PREFERRED", "PREFERRED",  # pr10
                             "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE",  # pr12 # noqa
                             "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE",  # pr13 # noqa
                             "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE",  # pr14 # noqa
                             "PREFERRED", "PREFERRED"]}  # pr15
    )


@pytest.fixture
def pr2(pr) -> pd.DataFrame:
    pr2 = pd.Series([float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 # noqa
                     float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 Chirurgie # noqa
                     float("nan"), float("nan"),  # pr3
                     float("nan"), float("nan"),  # pr4
                     float("nan"), float("nan"),  # pr4 Magnétique
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr9 # noqa
                     float("nan"), float("nan"),  # pr10
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr12 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr13 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr14 # noqa
                     float("nan"), float("nan")], name="pr2")  # pr15
    return pd.concat([pr, pr2], axis=1)


@pytest.fixture
def pr3(pr) -> pd.DataFrame:
    pr3 = pd.Series([float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 Chirurgie # noqa
                     float("nan"), "1",  # pr3
                     float("nan"), float("nan"),  # pr4
                     float("nan"), float("nan"),  # pr4 Magnétique
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr9 # noqa
                     float("nan"), float("nan"),  # pr10
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr12 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr13 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr14 # noqa
                     float("nan"), float("nan")], name="pr3")  # pr15
    return pd.concat([pr, pr3], axis=1)


@pytest.fixture
def pr4(pr) -> pd.DataFrame:
    pr4 = pd.Series([float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 Chirurgie # noqa
                     float("nan"), float("nan"),  # pr3
                     float("nan"), "1",  # pr4
                     float("nan"), "1",  # pr4 Magnétique
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr9 # noqa
                     float("nan"), float("nan"),  # pr10
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr12 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr13 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr14 # noqa
                     float("nan"), float("nan")], name="pr4")  # pr15
    return pd.concat([pr, pr4], axis=1)


@pytest.fixture
def pr9(pr) -> pd.DataFrame:
    pr9 = pd.Series([float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 Chirurgie # noqa
                     float("nan"), float("nan"),  # pr3
                     float("nan"), float("nan"),  # pr4
                     float("nan"), float("nan"),  # pr4 Magnétique
                     float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan"),  # pr9 # noqa
                     float("nan"), float("nan"),  # pr10
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr12 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr13 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr14 # noqa
                     float("nan"), float("nan")], name="pr9")  # pr15
    return pd.concat([pr, pr9], axis=1)


@pytest.fixture
def pr10(pr) -> pd.DataFrame:
    pr10 = pd.Series([float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 Chirurgie # noqa
                     float("nan"), float("nan"),  # pr3
                     float("nan"), float("nan"),  # pr4
                     float("nan"), float("nan"),  # pr4 Magnétique
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr9 # noqa
                     float("nan"), "1",   # pr10
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr12 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr13 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr14 # noqa
                     float("nan"), float("nan")], name="pr10")  # pr15
    return pd.concat([pr, pr10], axis=1)


@pytest.fixture
def pr12(pr) -> pd.DataFrame:
    pr12 = pd.Series([float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 Chirurgie # noqa
                     float("nan"), float("nan"),  # pr3
                     float("nan"), float("nan"),  # pr4
                     float("nan"), float("nan"),  # pr4 Magnétique
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr9 # noqa
                     float("nan"), float("nan"),  # pr10
                     float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan"),  # pr12 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr13 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr14 # noqa
                     float("nan"), float("nan")], name="pr12")  # pr15
    return pd.concat([pr, pr12], axis=1)


@pytest.fixture
def pr13(pr) -> pd.DataFrame:
    pr13 = pd.Series([float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 Chirurgie # noqa
                     float("nan"), float("nan"),  # pr3
                     float("nan"), float("nan"),  # pr4
                     float("nan"), float("nan"),  # pr4 Magnétique
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr9 # noqa
                     float("nan"), float("nan"),  # pr10
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr12 # noqa
                     float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan"),  # pr13 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr14 # noqa
                     float("nan"), float("nan")], name="pr13")  # pr15
    return pd.concat([pr, pr13], axis=1)


@pytest.fixture
def pr14(pr) -> pd.DataFrame:
    pr14 = pd.Series([float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 Chirurgie # noqa
                     float("nan"), float("nan"),  # pr3
                     float("nan"), float("nan"),  # pr4
                     float("nan"), float("nan"),  # pr4 Magnétique
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr9 # noqa
                     float("nan"), float("nan"),  # pr10
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr12 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr13 # noqa
                     float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan"),  # pr14 # noqa
                     float("nan"), float("nan")], name="pr14")  # pr15
    return pd.concat([pr, pr14], axis=1)


@pytest.fixture
def pr15(pr) -> pd.DataFrame:
    pr15 = pd.Series([float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr2 Chirurgie # noqa
                     float("nan"), float("nan"),  # pr3
                     float("nan"), float("nan"),  # pr4
                     float("nan"), float("nan"),  # pr4 Magnétique
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr9 # noqa
                     float("nan"), float("nan"),  # pr10
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr12 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr13 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # pr14 # noqa
                     float("nan"), "1"], name="pr15")  # pr15
    return pd.concat([pr, pr15], axis=1)


########################################################
# Fixtures pour règles Situation with explicit context #
########################################################
@pytest.fixture
def hs() -> pd.DataFrame:
    return pd.DataFrame(
        {"conceptId": ["hs1"] * 2,
         "FSN": ["Asthma familial history"] * 2,
         "term": ["antécédent familial d'asthme", "antécédents familiaux d'asthme"]}
    )


@pytest.fixture
def hs1(hs) -> pd.DataFrame:
    hs1 = pd.Series([float("nan"), "1"], name="hs1")
    return pd.concat([hs, hs1], axis=1)


#################################
# Fixtures pour règles Specimen #
#################################
@pytest.fixture
def ec() -> pd.DataFrame:
    return pd.DataFrame(
        {"conceptId": ["ec2_sub", "ec2_sub",
                       "ec2_wash", "ec2_wash",
                       "ec2_cyto", "ec2_cyto",
                       "ec4", "ec4"],
         "FSN": ["Implant submitted as specimen", "Implant submitted as specimen",  # ec2 Submitted # noqa
                 "Pharyngeal washings", "Pharyngeal washings",  # ec2 Washings
                 "Cervix cytologic material", "Cervix cytologic material",  # ec2 Cytologic # noqa
                 "Intravenous infusion fluid sample", "Intravenous infusion fluid sample"],  # ec4 # noqa
         "term": ["implant présenté comme échantillon", "échantillon d'implant",  # ec2 Submitted # noqa
                  "liquide de lavage pharyngien", "lavage pharyngien",  # ec2 Washings
                  "matériel cytologique du col utérin", "matériel cervical",  # ec2 Cytologic # noqa
                  "échantillon de liquide de perfusion intraveineuse", "échantillon de perfusion intraveineuse"]}  # ec4 # noqa
    )


@pytest.fixture
def ec2(ec) -> pd.DataFrame:
    ec2 = pd.Series([float("nan"), "1",  # ec2 Submitted
                     float("nan"), "1",  # ec2 Washings
                     float("nan"), "1",  # ec2 Cytologic
                     float("nan"), float("nan")], name="ec2")  # ec4
    return pd.concat([ec, ec2], axis=1)


@pytest.fixture
def ec4(ec) -> pd.DataFrame:
    ec4 = pd.Series([float("nan"), float("nan"),  # ec2 Submitted
                     float("nan"), float("nan"),  # ec2 Washings
                     float("nan"), float("nan"),  # ec2 Cytologic
                     float("nan"), "1"], name="ec4")  # ec4
    return pd.concat([ec, ec4], axis=1)


##################################
# Fixtures pour règles Substance #
##################################
@pytest.fixture
def su() -> pd.DataFrame:
    return pd.DataFrame(
        {"conceptId": ["su1_1", "su1_1", "su1_2", "su1_2", "su1_2", "su1_3", "su1_3", "su1_3", "su1_3",  # noqa
                       "su3_o", "su3_o", "su3_m", "su3_m", "su3_p", "su3_p",
                       "su8", "su8"],
         "FSN": ["rabies virus antibody", "rabies virus antibody", "rabies virus antibody", "rabies virus antibody", "rabies virus antibody", "rabies virus immunoglobulin", "rabies virus immunoglobulin", "rabies virus immunoglobulin", "rabies virus immunoglobulin",  # su1 # noqa
                 "ortho-hydroxybenzoate", "ortho-hydroxybenzoate", "meta-hydroxybenzoate", "meta-hydroxybenzoate", "para-hydroxybenzoate", "para-hydroxybenzoate",  # su3 # noqa
                 "moenomycin B>1<", "moenomycin B>1<"],  # su8
         "term": ["immunoglobuline antirabique", "immunoglobuline antirabique", "Ig antirabique", "Ig antirabique", "anticorps antirabique", "anticorps antirabique", "anticorps antirabique", "Ig antirabique", "immunoglobuline antirabique",  # su1 # noqa
                  "o-hydroxybenzoate", "ortho-hydroxybenzoate", "m-hydroxybenzoate", "méta-hydroxybenzoate", "p-hydroxybenzoate", "para-hydroxybenzoate",  # su3 # noqa
                  "moénomycine B1", "moénomycine B>1<",],  # su8
         "acceptabilityId": ["PREFERRED", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE", "PREFERRED", "ACCEPTABLE", "ACCEPTABLE", "ACCEPTABLE",  # su1 # noqa
                             "PREFERRED", "PREFERRED", "PREFERRED", "PREFERRED", "PREFERRED", "PREFERRED",  # su3 # noqa
                             "PREFERRED", "PREFERRED"]}  # su8
    )


@pytest.fixture
def su1(su) -> pd.DataFrame:
    su1 = pd.Series([float("nan"), "1", "1", float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # su1 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # su3 # noqa
                     float("nan"), float("nan")], name="su1")  # su8
    return pd.concat([su, su1], axis=1)


@pytest.fixture
def su3(su) -> pd.DataFrame:
    su3 = pd.Series([float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # su1 # noqa
                     float("nan"), "1", float("nan"), "1", float("nan"), "1",  # su3 # noqa
                     float("nan"), float("nan")], name="su3")
    return pd.concat([su, su3], axis=1)


@pytest.fixture
def su8(su) -> pd.DataFrame:
    su8 = pd.Series([float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # su1 # noqa
                     float("nan"), float("nan"), float("nan"), float("nan"), float("nan"), float("nan"),  # su3 # noqa
                     float("nan"), "1"], name="su8")
    return pd.concat([su, su8], axis=1)
