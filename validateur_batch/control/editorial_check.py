import pandas as pd

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from validateur_batch.object import server


def _get_correct_case(cs: pd.DataFrame) -> pd.DataFrame:
    """Corrige les descriptions labelisées 'CS' en 'cI'

    args:
        cs: Descriptions labelisées comme 'CS'`

    returns:
        DataFrame avec les identifiants de descriptions comme index et
        la correction de casse comme valeur
    """
    # Récupérer toutes les descriptions dont le premier mot contient une majuscule
    # et qui sont labelisées 'CS'
    cs = cs.loc[~cs.loc[:, "term"].str.islower()]
    upper = cs.loc[[any(w.isupper() for w in word)
                    for word in cs.loc[:, "term"].apply(lambda x: x.split()[0])]]
    incorrect_case = cs.iloc[~cs.index.isin(upper.index)]

    return pd.DataFrame(data={"caseSignificanceId": ["cI"] * len(incorrect_case)},
                        index=incorrect_case.index)


#####################
# Règles génériques #
#####################
def _check_ar2(df: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle ar2.

    args:
        df: DataFrame à valider

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle ar2.
    """
    idx = df.loc[df.loc[:, "term"].str.contains("^(?:les?|la|une?) ", case=False)].index
    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"ar2": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_ar6(df: pd.DataFrame, sb: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle ar6.

    args:
        df: DataFrame à valider
        sb: Filtre sur les Physical object de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle ar6.
    """
    idx = df.loc[sb
                 & (df.loc[:, "term"].str.contains(" (?:les?|la|une?|d'une?) ", case=False))].index # noqa
    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"ar6": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


#########################
# Règles Body structure #
#########################
def _check_bs2(df: pd.DataFrame, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs2.

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle bs2.
    """
    idx = df.loc[pt
                 & (df.loc[:, "FSN"].str.contains("joint", regex=False, case=False))
                 & (~df.loc[:, "term"].str.contains("(?:articulation|articulaire)", case=False))].index # noqa
    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"bs2": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")
    return df


def _check_bs3(df: pd.DataFrame, bs: pd.Series, pt: pd.Series,
               syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs3

    args:
        df: DataFrame à valider
        bs: Filtre sur les Body structure de `df`
        pt: Filtre sur les termes préférés de `df`
        syn: Filtre sur les synonymes acceptables de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle bs3
    """
    f_structure = df.loc[:, "FSN"].str.contains(r"structure(?!\))", case=False)

    has_invalid_syn = ~df.loc[f_structure, "conceptId"].isin(
        df.loc[syn
               & df.loc[:, "term"].str.endswith(", structure"), "conceptId"].unique()
    )

    idx = df.loc[bs & pt & f_structure
                 & (df.loc[:, "term"].str.contains("structure", regex=False, case=False))].index # noqa

    idx = idx.union(df.loc[bs & syn & has_invalid_syn].index)

    idx = idx.union(df.loc[bs
                           & (df.loc[:, "FSN"].str.contains("entire", regex=False, case=False)) # noqa
                           & (~df.loc[:, "term"].str.contains("(?:entiers?|entières?)", case=False))].index) # noqa

    idx = idx.union(df.loc[bs
                           & (df.loc[:, "FSN"].str.contains("part", regex=False, case=False)) # noqa
                           & (~df.loc[:, "term"].str.contains("partie", regex=False, case=False))].index) # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"bs3": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")
    return df


def _check_bs5(df: pd.DataFrame, bs: pd.Series, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs5

    args:
        df: DataFrame à valider
        bs: Filtre sur les Body structure de `df`
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle bs5.
    """
    idx = df.loc[bs & pt
                 & (df.loc[:, "FSN"].str.contains("region", regex=False, case=False))
                 & (~df.loc[:, "term"].str.contains("région", regex=False, case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"bs5": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_bs6(df: pd.DataFrame, bs: pd.Series, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs6

    args:
        df: DataFrame à valider
        bs: Filtre sur les Body structure de `df`
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle bs6.
    """
    idx = df.loc[bs & pt
                 & (df.loc[:, "FSN"].str.contains("(?:zone|area)", case=False))
                 & (~df.loc[:, "term"].str.contains("(?:zone|surface|aire)", case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"bs6": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_bs7(df: pd.DataFrame, bs: pd.Series, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs6

    args:
        df: DataFrame à valider
        bs: Filtre sur les Body structure de `df`
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle bs7.
    """
    idx = df.loc[bs & pt
                 & (df.loc[:, "FSN"].str.contains("proper", regex=False, case=False))
                 & (~df.loc[:, "term"].str.contains("(?:propre|proprement dite?)", case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"bs7": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_bs8(df: pd.DataFrame, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs8

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle bs8.
    """
    idx = df.loc[pt
                 & (df.loc[:, "FSN"].str.contains("apex", regex=False, case=False))
                 & (~df.loc[:, "term"].str.contains("apex", regex=False, case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"bs8": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_bs9(df: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs9.

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`
        syn: Filtre sur les synonymes acceptables de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle bs9.
    """
    f_lesser_toe = df.loc[:, "FSN"].str.contains("lesser toe", regex=False, case=False)

    has_invalid_syn = ~df.loc[f_lesser_toe, "conceptId"].isin(
        df.loc[syn
               & df.loc[:, "term"].str.contains("orteil latéral", regex=False), "conceptId"].unique() # noqa
    )

    idx = df.loc[pt & f_lesser_toe
                 & (~df.loc[:, "term"].str.contains("orteil excepté l'hallux", regex=False, case=False))].index # noqa

    idx = idx.union(df.loc[syn & has_invalid_syn].index)

    idx = idx.union(df.loc[f_lesser_toe
                           & (df.loc[:, "term"].str.contains("petit orteil", case=False))].index) # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"bs9": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_bs10(df: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs10-FR

    args:
        df: DataFrame à valider

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle bs10.
    """
    idx = df.loc[(df.loc[:, "FSN"].str.contains("lower limb", regex=False, case=False))
                 & (~df.loc[:, "term"].str.contains("membre inférieur", regex=False, case=False))].index # noqa

    idx = idx.union(df.loc[(df.loc[:, "FSN"].str.contains("lower leg", regex=False, case=False)) # noqa
                           & (~df.loc[:, "term"].str.contains("partie inférieure(?: entière)? de la jambe", case=False))].index) # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"bs10": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_bs11(df: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs11-FR

    args:
        df: DataFrame à valider

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle bs11-FR.
    """
    idx = df.loc[(df.loc[:, "FSN"].str.contains("upper limb", regex=False, case=False))
                 & (~df.loc[:, "term"].str.contains("membre supérieur", regex=False, case=False))].index # noqa

    idx = idx.union(df.loc[(df.loc[:, "FSN"].str.contains("upper arm", regex=False, case=False)) # noqa
                           & (~df.loc[:, "term"].str.contains("partie supérieure(?: entière)? du bras", case=False))].index) # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"bs11": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_bs12(df: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs12

    args:
        df: DataFrame à valider

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle bs12.
    """
    idx = df.loc[(df.loc[:, "FSN"].str.contains("cerebrum", regex=False, case=False))
                 & (~df.loc[:, "term"].str.contains("(?:cerveau|cérébral|cérébro)", case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"bs12": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_bs13(df: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle bs13

    args:
        df: DataFrame à valider

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle bs13.
    """
    idx = df.loc[(df.loc[:, "FSN"].str.contains("brain(?!stem)", case=False))
                 & (~df.loc[:, "term"].str.contains("encéphal", regex=False, case=False))].index # noqa

    idx = idx.union(df.loc[(df.loc[:, "FSN"].str.contains("brainstem", regex=False, case=False)) # noqa
                 & (~df.loc[:, "term"].str.contains("tronc cérébral", regex=False, case=False))].index) # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"bs13": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


###########################
# Règles Clinical finding #
###########################
def _check_co2(df: pd.DataFrame, co: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle co2

    args:
        df: DataFrame à valider
        co: Filtre sur les Clinical finding de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle co2.
    """
    idx = df.loc[co
                 & (df.loc[:, "FSN"].str.contains(r"(?<!\()finding(?!\))", case=False))
                 & (~df.loc[:, "term"].str.contains("constatation", regex=False, case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"co2": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_co6(df: pd.DataFrame, co: pd.Series, pt: pd.Series,
               syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle co6-FR

    args:
        df: DataFrame à valider
        co: Filtre sur les Clinical finding de `df`
        pt: Filtre sur les termes préférés de `df`
        syn: Filtre sur les synonymes acceptables de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle co6-FR.
    """
    # Filtre FSN
    f_above = df.loc[:, "FSN"].str.contains("above reference range", regex=False,
                                            case=False)
    f_below = df.loc[:, "FSN"].str.contains("below reference range", regex=False,
                                            case=False)
    f_within = df.loc[:, "FSN"].str.contains("within reference range", regex=False,
                                             case=False)
    f_outside = df.loc[:, "FSN"].str.contains("outside reference range", regex=False,
                                              case=False)

    # Identification des concepts ayant des synonymes invalides
    has_invalid_syn_abv = ~df.loc[f_above, "conceptId"].isin(
        df.loc[syn
               & df.loc[:, "term"].str.contains("supérieure? aux valeurs de référence"), "conceptId"].unique() # noqa
    )

    has_invalid_syn_bel = ~df.loc[f_below, "conceptId"].isin(
        df.loc[syn
               & df.loc[:, "term"].str.contains("inférieure? aux valeurs de référence"), "conceptId"].unique() # noqa
    )

    has_invalid_syn_in = ~df.loc[f_within, "conceptId"].isin(
        df.loc[syn
               & df.loc[:, "term"].str.contains("dans les valeurs de référence", regex=False), "conceptId"].unique() # noqa
    )

    has_invalid_syn_out = ~df.loc[f_outside, "conceptId"].isin(
        df.loc[syn
               & df.loc[:, "term"].str.contains("en dehors des valeurs de référence", regex=False), "conceptId"].unique() # noqa
    )

    # Identification des lignes ne respectant pas la règle
    idx = df.loc[co & pt & f_above
                 & (~df.loc[:, "term"].str.contains("supérieure? à l'intervalle de référence", case=False))].index # noqa

    idx = idx.union(df.loc[co & syn & has_invalid_syn_abv].index)

    idx = idx.union(df.loc[co & pt & f_below
                           & (~df.loc[:, "term"].str.contains("inférieure? à l'intervalle de référence", case=False))].index) # noqa

    idx = idx.union(df.loc[co & syn & has_invalid_syn_bel].index)

    idx = idx.union(df.loc[co & pt & f_within
                           & (~df.loc[:, "term"].str.contains("dans l'intervalle de référence", regex=False, case=False))].index) # noqa

    idx = idx.union(df.loc[co & syn & has_invalid_syn_in].index)

    idx = idx.union(df.loc[co & pt & f_outside
                           & (~df.loc[:, "term"].str.contains("en dehors de l'intervalle de référence", regex=False, case=False))].index) # noqa

    idx = idx.union(df.loc[co & syn & has_invalid_syn_out].index)

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"co6": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pa2(df: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa2

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`
        syn: Filtre sur les synonymes acceptables de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pa2.
    """
    sctid = df.loc[(df.loc[:, "FSN"].str.contains("disorder", regex=False, case=False))
                   & ((df.loc[:, "acceptabilityId"] == "PREFERRED")
                      & (df.loc[:, "term"].str.contains("complication", regex=False))),
                   "conceptId"].unique()

    f_complication = df.loc[:, "conceptId"].isin(sctid)

    has_invalid_syn = ~df.loc[f_complication, "conceptId"].isin(
        df.loc[syn
               & df.loc[:, "term"].str.contains("problème", regex=False), "conceptId"].unique() # noqa
    )

    idx = df.loc[pt
                 & (df.loc[:, "FSN"].str.contains("disorder", regex=False, case=False))
                 & (~df.loc[:, "term"].str.contains("(?:trouble|affection|anomalie|complication|maladie)", case=False))].index # noqa

    idx = idx.union(df.loc[syn & has_invalid_syn].index)

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pa2": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pa3_1(df: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa3.1

    args:
        df: DataFrame à valider

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pa3.1.
    """
    idx = df.loc[(df.loc[:, "FSN"].str.contains("pressure injury", regex=False, case=False)) # noqa
                 & (~df.loc[:, "term"].str.contains("escarre", regex=False, case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pa3.1": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pa4(df: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa4

    args:
        df: DataFrame à valider

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pa4.
    """
    idx = df.loc[(df.loc[:, "FSN"].str.contains("epilepsy", regex=False, case=False))
                 & (~df.loc[:, "term"].str.contains("épilepsie", regex=False, case=False))].index # noqa

    idx = idx.union(df.loc[(df.loc[:, "FSN"].str.contains("seizure", regex=False, case=False)) # noqa
                           & (~df.loc[:, "term"].str.contains("(?:crise|convulsion|convulsif|convulsive)", case=False))].index) # noqa

    idx = idx.union(df.loc[(df.loc[:, "FSN"].str.contains("convulsion", regex=False, case=False)) # noqa
                           & (~df.loc[:, "term"].str.contains("convulsion", regex=False, case=False))].index) # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pa4": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pa6(df: pd.DataFrame, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa6

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pa6.
    """
    idx = df.loc[pt
                 & (df.loc[:, "FSN"].str.contains("impairment", regex=False, case=False)) # noqa
                 & (~df.loc[:, "term"].str.contains("atteinte", regex=False, case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pa6": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pa7(df: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa7

    args:
        df: DataFrame à valider

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pa7.
    """
    idx = df.loc[(df.loc[:, "FSN"].str.contains("primary", regex=False, case=False))
                 & (~df.loc[:, "term"].str.contains("(?:primitif|primitive|primaire)", case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pa7": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pa8(df: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa8

    args:
        df: DataFrame à valider

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pa8.
    """
    idx = df.loc[(df.loc[:, "FSN"].str.contains("chilblain", regex=False, case=False))
                 & (~df.loc[:, "term"].str.contains("engelure", regex=False, case=False))].index # noqa

    idx = idx.union(df.loc[(df.loc[:, "FSN"].str.contains("(?<!superficial )frostbite", case=False)) # noqa
                           & (~df.loc[:, "term"].str.contains("(?:^| )gelure", case=False))].index) # noqa

    idx = idx.union(df.loc[(df.loc[:, "FSN"].str.contains("superficial frostbite", regex=False, case=False)) # noqa
                           & (~df.loc[:, "term"].str.contains("(?:^| )gelure superficielle", case=False))].index) # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pa8": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pa9(df: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pa9

    args:
        df: DataFrame à valider

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pa9.
    """
    idx = df.loc[(df.loc[:, "FSN"].str.contains("carbuncle", regex=False, case=False))
                 & (~df.loc[:, "term"].str.contains("anthrax", regex=False, case=False))].index # noqa

    idx = idx.union(df.loc[(df.loc[:, "FSN"].str.contains("(?:furuncle|boil)", case=False)) # noqa
                           & (~df.loc[:, "term"].str.contains("(?:furoncle|folliculite nécrotique|clou)", case=False))].index) # noqa

    idx = idx.union(df.loc[(df.loc[:, "FSN"].str.contains("anthrax", regex=False, case=False)) # noqa
                           & (~df.loc[:, "term"].str.contains("maladie du charbon", regex=False, case=False))].index) # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pa9": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


##############################################
# Règles Pharmaceutical / biological product #
##############################################
def _check_me1(df: pd.DataFrame, me: pd.Series, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle me1

    args:
        df: DataFrame à valider
        me: Filtre sur les Pharmaceutical / biological product de `df`
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle me1.
    """
    idx = df.loc[me & pt
                 & (df.loc[:, "FSN"].str.contains("product containing (?!only|precisely)", case=False)) # noqa
                 & (~df.loc[:, "term"].str.contains("(?:produit|vaccin) contenant (?!uniquement|précisément)", case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"me1": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")
    return df


def _check_me2(df: pd.DataFrame, me: pd.Series, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle me2

    args:
        df: DataFrame à valider
        me: Filtre sur les Pharmaceutical / biological product de `df`
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle me2.
    """
    idx = df.loc[me & pt
                 & (df.loc[:, "FSN"].str.contains("product containing only", regex=False, case=False)) # noqa
                 & (~df.loc[:, "term"].str.contains("(?:produit|vaccin) contenant uniquement", case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"me2": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_me3(df: pd.DataFrame, me: pd.Series, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle me3

    args:
        df: DataFrame à valider
        me: Filtre sur les Pharmaceutical / biological product de `df`
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle me3.
    """
    idx = df.loc[me & pt
                 & (df.loc[:, "FSN"].str.endswith("(clinical drug)"))
                 & (~df.loc[:, "term"].str.contains("produit contenant précisément", regex=False, case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"me3": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_me4(df: pd.DataFrame, me: pd.Series, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle me4

    args:
        df: DataFrame à valider
        me: Filtre sur les Pharmaceutical / biological product de `df`
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle me4.
    """
    idx = df.loc[me & pt
                 & (df.loc[:, "term"].str.contains("libération conventionnelle", regex=False, case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"me4": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


##########################
# Règles Physical object #
##########################
def _check_sb1(df: pd.DataFrame, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle sb1

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle sb1.
    """
    idx = df.loc[pt
                 & (df.loc[:, "FSN"].str.contains(r"evacuated [-\w\s\/\(\)':]+ collection tube", case=False)) # noqa
                 & (~df.loc[:, "term"].str.contains(r"tube sous vide [-\w\s\/\(\)':]+ pour prélèvement", case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"sb1": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_sb2(df: pd.DataFrame, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle sb2

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle sb2.
    """
    idx = df.loc[pt
                 & (df.loc[:, "FSN"].str.contains(r"evacuated [-\w\s\/\(\)':]+ specimen container", case=False)) # noqa
                 & (~df.loc[:, "term"].str.contains(r"support sous vide [-\w\s\/\(\)':]+ pour prélèvement", case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"sb2": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_sb3(df: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle sb3

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`
        syn: Filtre sur les synonymes acceptables de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle sb3.
    """
    f_stent = df.loc[:, "FSN"].str.contains("stent", regex=False, case=False)

    has_invalid_syn = ~df.loc[f_stent, "conceptId"].isin(
        df.loc[syn
               & df.loc[:, "term"].str.contains("stent", regex=False), "conceptId"].unique() # noqa
    )

    idx = df.loc[pt & f_stent
                 & (~df.loc[:, "term"].str.contains("endoprothèse", regex=False, case=False))].index # noqa

    idx = idx.union(df.loc[syn & has_invalid_syn].index)

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"sb3": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


####################
# Règles Procedure #
####################
def _check_pr2(df: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr2

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`
        syn: Filtre sur les synonymes acceptables de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pr2.
    """
    # Filtre FSN
    f_procedure = ((df.loc[:, "FSN"].str.contains("procedure", regex=False, case=False))
                   & (~df.loc[:, "FSN"].str.contains("surgical", regex=False, case=False)))  # noqa
    f_surgery = df.loc[:, "FSN"].str.contains("(?:operation|surgery|surgical)", case=False)  # noqa

    # Identification des concepts ayant des synonymes invalides
    has_invalid_syn = ~df.loc[f_procedure, "conceptId"].isin(
        df.loc[syn
               & (df.loc[:, "term"].str.contains("intervention", regex=False))
               & (~df.loc[:, "term"].str.contains("chirurgicale", regex=False)), "conceptId"].unique() # noqa
    )

    has_invalid_syn_ope = ~df.loc[f_surgery, "conceptId"].isin(
        df.loc[syn
               & (df.loc[:, "term"].str.contains("opération")), "conceptId"].unique()
    )

    has_invalid_syn_chir = ~df.loc[f_surgery, "conceptId"].isin(
        df.loc[syn
               & df.loc[:, "term"].str.contains("chirurgie"), "conceptId"].unique()
    )

    # Identification des lignes ne respectant pas la règle
    idx = df.loc[pt & f_procedure
                 & (~df.loc[:, "term"].str.contains("procédure", regex=False, case=False))].index # noqa

    idx = idx.union(df.loc[syn & has_invalid_syn].index)

    idx = idx.union(df.loc[pt & f_surgery
                           & (~df.loc[:, "term"].str.contains("intervention chirurgicale", regex=False, case=False))].index) # noqa

    idx = idx.union(df.loc[syn & has_invalid_syn_ope].index)
    idx = idx.union(df.loc[syn & has_invalid_syn_chir].index)

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pr2": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pr3(df: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr3

    args:
        df: DataFrame à valider

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pr3.
    """
    idx = df.loc[(df.loc[:, "FSN"].str.contains("consultation", regex=False, case=False)) # noqa
                 & (~df.loc[:, "term"].str.contains("consultation", regex=False, case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pr3": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pr4(df: pd.DataFrame, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr4

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pr4.
    """
    idx = df.loc[pt
                 & (df.loc[:, "FSN"].str.contains("removal of foreign body", regex=False, case=False)) # noqa
                 & (~df.loc[:, "term"].str.contains("retrait d'un corps étranger", regex=False, case=False))].index # noqa

    idx = idx.union(df.loc[pt
                           & (df.loc[:, "FSN"].str.contains("magnet extraction", regex=False, case=False)) # noqa
                           & (~df.loc[:, "term"].str.contains("extraction avec un aimant", regex=False, case=False))].index) # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pr4": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pr9(df: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr9

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`
        syn: Filtre sur les synonymes acceptables de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pr9.
    """
    f_excisional = df.loc[:, "FSN"].str.contains("excisional biopsy", regex=False, case=False)  # noqa

    has_invalid_syn = ~df.loc[f_excisional, "conceptId"].isin(
        df.loc[syn
               & df.loc[:, "term"].str.contains("biopsie excisionnelle", regex=False), "conceptId"].unique() # noqa
    )

    idx = df.loc[pt & f_excisional
                 & (~df.loc[:, "term"].str.contains("biopsie-exérèse", regex=False, case=False))].index # noqa

    idx = idx.union(df.loc[syn & has_invalid_syn].index)

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pr9": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pr10(df: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr10

    args:
        df: DataFrame à valider

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pr10.
    """
    idx = df.loc[(df.loc[:, "FSN"].str.contains("incisional biopsy", regex=False, case=False)) # noqa
                 & (~df.loc[:, "term"].str.contains("biopsie incisionnelle", regex=False, case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pr10": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pr12(df: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr12

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`
        syn: Filtre sur les synonymes acceptables de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pr12.
    """
    f_irm = df.loc[:, "FSN"].str.contains("(?:MRI|(?:m|M)agnetic resonance angiography|(?:m|M)agnetic resonance imaging)")  # noqa

    has_invalid_syn = ~df.loc[f_irm, "conceptId"].isin(
        df.loc[syn
               & df.loc[:, "term"].str.contains("imagerie par résonance magnétique", regex=False), "conceptId"].unique() # noqa
    )

    idx = df.loc[pt & f_irm
                 & (~df.loc[:, "term"].str.contains("IRM", regex=False, case=False))].index # noqa

    idx = idx.union(df.loc[syn & has_invalid_syn].index)

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pr12": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pr13(df: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr13

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`
        syn: Filtre sur les synonymes acceptables de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pr13.
    """
    f_guided = df.loc[:, "FSN"].str.contains("(?:guided|guidance)")  # noqa

    has_invalid_syn = ~df.loc[f_guided, "conceptId"].isin(
        df.loc[syn
               & df.loc[:, "term"].str.contains("sous guidage", regex=False), "conceptId"].unique() # noqa
    )

    idx = df.loc[pt & f_guided
                 & (~df.loc[:, "term"].str.contains("guidée? par", case=False))].index

    idx = idx.union(df.loc[syn & has_invalid_syn].index)

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pr13": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pr14(df: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr14

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`
        syn: Filtre sur les synonymes acceptables de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pr14.
    """
    f_fluo = df.loc[:, "FSN"].str.contains("(?:fluoroscopy|fluoroscopic)", case=False)  # noqa

    has_invalid_syn = ~df.loc[f_fluo, "conceptId"].isin(
        df.loc[syn
               & df.loc[:, "term"].str.contains("(?:fluoroscopie|fluoroscopique)"), "conceptId"].unique() # noqa
    )

    idx = df.loc[pt & f_fluo
                 & (~df.loc[:, "term"].str.contains("(?:radioscopie|radioscopique)", case=False))].index # noqa

    idx = idx.union(df.loc[syn & has_invalid_syn].index)

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pr14": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_pr15(df: pd.DataFrame, pr: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle pr15-FR

    Args:
        df: DataFrame à valider
        pr: Filtre sur les Procedure de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle pr15-FR.
    """
    idx = df.loc[pr
                 & (df.loc[:, "FSN"].str.contains("education", regex=False, case=False))
                 & (~df.loc[:, "term"].str.contains("éducation", case=False))].index

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"pr15": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


##########################################
# Règles Situation with explicit context #
##########################################
def _check_hs1(df: pd.DataFrame, hs: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle hs1

    args:
        df: DataFrame à valider
        hs: Filtre sur les Situation with explicit context de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle hs1.
    """
    idx = df.loc[hs
                 & (df.loc[:, "FSN"].str.contains("history", regex=False, case=False))
                 & (~df.loc[:, "term"].str.contains("antécédent(?!s)", case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"hs1": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


###################
# Règles Specimen #
###################
def _check_ec2(df: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle ec2

    args:
        df: DataFrame à valider

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle ec2.
    """
    idx = df.loc[(df.loc[:, "FSN"].str.contains("submitted as specimen", regex=False, case=False)) # noqa
                 & (~df.loc[:, "term"].str.contains("présentée? comme échantillon", case=False))].index # noqa

    idx = idx.union(df.loc[(df.loc[:, "FSN"].str.contains("washings", regex=False, case=False)) # noqa
                           & (~df.loc[:, "term"].str.contains("liquide de lavage", regex=False, case=False))].index) # noqa

    idx = idx.union(df.loc[(df.loc[:, "FSN"].str.contains("cytologic material", regex=False, case=False)) # noqa
                           & (~df.loc[:, "term"].str.contains("matériel cytologique", regex=False, case=False))].index) # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"ec2": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_ec4(df: pd.DataFrame) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle ec4

    args:
        df: DataFrame à valider

    returns:
        DataFrame du fichier avec une colonne identifiant les
        descriptions ne respectant pas la règle ec4.
    """
    idx = df.loc[(df.loc[:, "FSN"].str.contains("fluid sample", regex=False, case=False)) # noqa
                 & (~df.loc[:, "term"].str.contains("échantillon de liquide", regex=False, case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"ec4": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


####################
# Règles Substance #
####################
def _check_su1(df: pd.DataFrame, pt: pd.Series, syn: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle su1-FR.

    args:
        df: DataFrame à valider
        pt: Filtre sur les termes préférés de `df`
        syn: Filtre sur les synonymes acceptables de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les descriptions ne respectant
        pas la règle su1-FR.
    """
    has_invalid_syn = ~df.loc[:, "conceptId"].isin(
        df.loc[syn
               & (df.loc[:, "FSN"].str.contains("(?:antibody|immunoglobulin)", case=False)) # noqa
               & df.loc[:, "term"].str.contains("(?:anticorps|immunoglobuline)"), "conceptId"].unique() # noqa
    )

    has_invalid_syn_ig = ~df.loc[:, "conceptId"].isin(
        df.loc[syn
               & (df.loc[:, "FSN"].str.contains("(?:antibody|immunoglobulin)", case=False)) # noqa
               & df.loc[:, "term"].str.contains("Ig"), "conceptId"].unique() # noqa
    )

    idx = df.loc[pt
                 & (df.loc[:, "FSN"].str.contains("(?:antibody|immunoglobulin)", case=False)) # noqa
                 & (~df.loc[:, "term"].str.contains("(?:anticorps|immunoglobuline)", case=False))].index # noqa

    idx = idx.union(df.loc[syn & has_invalid_syn].index)

    idx = idx.union(df.loc[syn & has_invalid_syn_ig].index)

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"su1": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_su3(df: pd.DataFrame, su: pd.Series, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle su3-FR.

    args:
        df: DataFrame à valider
        su: Filtre sur les Substance de `df`
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les descriptions ne respectant
        pas la règle su3-FR.
    """
    idx = df.loc[su & pt
                 & (df.loc[:, "term"].str.contains("(?:méta-|ortho-|para-)", case=False))].index # noqa

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"su3": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def _check_su8(df: pd.DataFrame, su: pd.Series, pt: pd.Series) -> pd.DataFrame:
    """Identifie les descriptions ne respectant pas la règle su8-FR.

    args:
        df: DataFrame à valider
        su: Filtre sur les Substance de `df`
        pt: Filtre sur les termes préférés de `df`

    returns:
        DataFrame du fichier avec une colonne identifiant les descriptions ne respectant
        pas la règle su8-FR.
    """
    idx = df.loc[su & pt
                 & (df.loc[:, "term"].str.contains("(?:>.*<)"))].index

    if not idx.empty:
        df = pd.merge(df, pd.DataFrame(data={"su8": ["1"] * len(idx)}, index=idx),
                      how="left", left_index=True, right_index=True, validate="1:1")

    return df


def run_editorial_check(df: pd.DataFrame, fts: "server.Server") -> pd.DataFrame:
    """Lance l'ensemble des contrôles sur le respect des règles éditoriales.

    args:
        df: DataFrame à valider
        fts: Serveur de Terminologies FHIR à utiliser

    returns:
        Fichier avec les résultats des contrôles
    """
    print("Vérification des règles éditoriales...", end="\r")
    nb = len(df.columns)

    # Précalcul des lignes PT et SYN
    pt = (df.loc[:, "acceptabilityId"] == "PREFERRED")
    syn = (df.loc[:, "acceptabilityId"] == "ACCEPTABLE")

    # Précalcul des hiérarchies
    # Body structure
    bs = ((df.loc[:, "FSN"].str.endswith(" (body structure)"))
          | (df.loc[:, "FSN"].str.endswith(" (cell)"))
          | (df.loc[:, "FSN"].str.endswith(" (cell structure)"))
          | (df.loc[:, "FSN"].str.endswith(" (morphologic abnormality)")))
    # Clinical finding
    co = (df.loc[:, "FSN"].str.endswith(" (finding)"))
    pa = (df.loc[:, "FSN"].str.endswith(" (disorder)"))
    # Pharmaceutical / biological product
    me = (df.loc[:, "conceptId"].isin(fts.ecl("<< 373873005")))
    # Physical object
    sb = (df.loc[:, "conceptId"].isin(fts.ecl("<< 260787004")))
    # Procedure
    pr = ((df.loc[:, "FSN"].str.endswith(" (procedure)"))
          | (df.loc[:, "FSN"].str.endswith(" (regime/therapy)")))
    # Situation with explicit context
    hs = (df.loc[:, "FSN"].str.endswith(" (situation)"))
    # Specimen
    ec = (df.loc[:, "FSN"].str.endswith(" (specimen)"))
    # Substance
    su = (df.loc[:, "FSN"].str.endswith(" (substance)"))

    # Correction des casses
    correction = _get_correct_case(df.loc[df.loc[:, "caseSignificanceId"] == "CS"])
    df.update(correction)

    # Contrôles des règles sur les articles
    df = _check_ar2(df)
    df = _check_ar6(df, sb)

    # Contrôles des règles de Body Structure
    if not df.loc[bs].empty:
        df = _check_bs2(df, pt)
        df = _check_bs3(df, bs, pt, syn)
        df = _check_bs5(df, bs, pt)
        df = _check_bs6(df, bs, pt)
        df = _check_bs7(df, bs, pt)
        df = _check_bs8(df, pt)
        df = _check_bs9(df, pt, syn)
        df = _check_bs10(df)
        df = _check_bs11(df)
        df = _check_bs12(df)
        df = _check_bs13(df)

    # Contrôles des règles de Clinical finding
    if not df.loc[co].empty:
        df = _check_co2(df, co)
        df = _check_co6(df, co, pt, syn)
    if not df.loc[pa].empty:
        df = _check_pa3_1(df)
        df = _check_pa4(df)
        df = _check_pa6(df, pt)
        df = _check_pa7(df)
        df = _check_pa8(df)
        df = _check_pa9(df)

    # Contrôles des règles de Pharmaceutical / biological product
    if not df.loc[me].empty:
        df = _check_me1(df, me, pt)
        df = _check_me2(df, me, pt)
        df = _check_me3(df, me, pt)
        df = _check_me4(df, me, pt)

    # Contrôles des règles de Physical object
    if not df.loc[sb].empty:
        df = _check_sb1(df)
        df = _check_sb2(df)
        df = _check_sb3(df, pt, syn)

    # Contrôles des règles de Procedure
    if not df.loc[pr].empty:
        df = _check_pr2(df, pt, syn)
        df = _check_pr3(df)
        df = _check_pr4(df, pt)
        df = _check_pr9(df, pt, syn)
        df = _check_pr10(df)
        df = _check_pr12(df, pt, syn)
        df = _check_pr13(df, pt, syn)
        df = _check_pr14(df, pt, syn)
        df = _check_pr15(df, pr)

    # Contrôles des règles de Situation with explicit context
    if not df.loc[hs].empty:
        df = _check_hs1(df, hs)

    # Contrôles des règles de Specimen
    if not df.loc[ec].empty:
        df = _check_ec2(df)
        df = _check_ec4(df)

    # Contrôles des règles de Substance
    if not df.loc[su].empty:
        df = _check_su1(df, pt, syn)
        df = _check_su3(df, su, pt)
        df = _check_su8(df, su, pt)

    nb = len(df.columns) - nb
    status = "OK" if nb == 0 else "KO"
    print(f"{nb} règle(s) éditoriales non respectées - {status}")

    return df
