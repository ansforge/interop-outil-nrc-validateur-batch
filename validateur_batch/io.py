import os
import os.path as op
import pandas as pd

from typing import List
from validateur_batch.object import batch


CASE = {
    "900000000000448009": "ci",
    "900000000000017005": "CS",
    "900000000000020002": "cI"
}

ACCEPT = {
    "900000000000548007": "PREFERRED",
    "900000000000549004": "ACCEPTABLE"
}


def read_excel_dir(directory: str) -> List[batch.Batch]:
    """Lecture de l'ensemble des fichiers Excel d'un dossier

    Args:
        directory: Chemin vers le dossier contenant les fichiers Excel

    Returns:
        Dictionnaire {nom du fichier: {nom de l'onglet: DataFrame de l'onglet}}
    """
    list_b = {}
    files_list = sorted(f for f in os.listdir(directory)
                        if f.endswith(".xlsx") and not f.startswith("~$"))

    for file in files_list:
        sheets = pd.read_excel(op.join(directory, file), sheet_name=None, dtype=str)

        # Les fichiers VAL et ADD ne doivent contenir qu'un seul onglet
        if (file.startswith(("LstConcRevusNonModif", "ModEdtNatAddDesc"))
                and len(sheets) > 1):
            raise ValueError(f"Le fichier contient plusieurs onglets : {file} "
                             f"({', '.join(sheets)})")

        if file.startswith("LstConcRevusNonModif"):
            df = next(iter(sheets.values()))
            list_b["VAL"] = df
        elif file.startswith("ModEdtNatAddDesc"):
            df = next(iter(sheets.values()))
            list_b["ADD"] = df
        elif file.startswith("ModEdtNatSnomed"):
            if not sheets["Description Additions"].empty and "ADD" in list_b.keys():
                list_b["ADD"] = pd.concat([list_b["ADD"],
                                          sheets["Description Additions"]],
                                          ignore_index=True)
            elif not sheets["Description Additions"].empty and "ADD" not in list_b.keys():  # noqa
                list_b["ADD"] = sheets["Description Additions"]

            if not sheets["Description Changes"].empty:
                list_b["CHG"] = sheets["Description Changes"]

            if not sheets["Description Inactivations"].empty:
                list_b["INA"] = sheets["Description Inactivations"]

            if not sheets["Description Replacements"].empty:
                col = "New Replacement Description ID"
                if not all(sheets["Description Replacements"].loc[:, col].isnull()):
                    raise ValueError(f"Remplacement : '{col}' n'est pas vide")
                list_b["REP"] = sheets["Description Replacements"]

        else:
            raise ValueError(f"Fichier inconnu : {file}")

    return [batch.Batch(k, v) for k, v in list_b.items()]


def read_snapshot(snapshot: str,
                  list_batch: List[batch.Batch]) -> pd.DataFrame:
    """Lecture de la Snapshot de l'édition française

    Args:
        snapshot: Chemin vers le dossier de la snapshot
        list_batch: Liste des batchs à valider

    Returns:
        DataFrame représentant les concepts de l'édition FR inclus dans le périmètre
        des batchs
    """
    # Vérification du dossier Snapshot
    if op.basename(op.normpath(snapshot)) != "Snapshot":
        raise ValueError("Le chemin ne pointe pas vers le dossier Snapshot")
    # Récupération et vérification de la date
    date = op.dirname(op.normpath(snapshot)).split("_")[-1].split("T")[0]
    if not date.startswith("20") or not date.endswith("0621"):
        raise ValueError("Le dossier Snapshot n'appartient pas au RF2 de l'édition FR")

    p = {
        "concept": op.join(snapshot, f"Terminology/sct2_Concept_Snapshot_FR1000315_{date}.txt"), # noqa
        "desc_fr": op.join(snapshot, f"Terminology/sct2_Description_Snapshot-fr_FR1000315_{date}.txt"), # noqa
        "desc_en": op.join(snapshot, f"Terminology/sct2_Description_Snapshot-en_FR1000315_{date}.txt"), # noqa
        "lang": op.join(snapshot, f"Refset/Language/der2_cRefset_LanguageSnapshot-fr_FR1000315_{date}.txt") # noqa
    }

    print("Lecture des concepts...", end="\r")
    # Lecture des concepts
    concept = pd.read_csv(p["concept"], sep="\t", usecols=["id", "active"],
                          dtype={"id": str, "active": pd.CategoricalDtype(["1", "0"])})
    concept = concept.loc[concept.loc[:, "active"] == "1"]
    print("Lecture des concepts - OK")

    print("Lecture des descriptions...", end="\r")
    # Lecture des descriptions françaises
    desc = pd.read_csv(p["desc_fr"], sep="\t", quoting=3, na_filter=False,
                       usecols=["id", "active", "conceptId", "typeId", "term",
                                "caseSignificanceId"],
                       dtype={"id": str, "active": pd.CategoricalDtype(["1", "0"]),
                              "conceptId": str, "typeId": str, "term": str},
                       converters={"caseSignificanceId": lambda x: CASE.get(x)})
    desc = desc.loc[(desc.loc[:, "conceptId"].isin(concept.loc[:, "id"]))
                    & (desc.loc[:, "typeId"] == "900000000000013009")
                    & (desc.loc[:, "active"] == "1")]
    print("Lecture des descriptions - OK")

    # Lecture des acceptabilités
    print("Lecture des language refset...", end="\r")
    lang = pd.read_csv(p["lang"], sep="\t", na_filter=False,
                       usecols=["referencedComponentId", "acceptabilityId"],
                       dtype={"referencedComponentId": str},
                       converters={"acceptabilityId": lambda x: ACCEPT.get(x)})
    print("Lecture des language refset - OK")

    print("Préparation du DataFrame...", end="\r")
    # Fusion & filtre par rapport au périmètre des batchs
    desc = pd.merge(desc, lang, how="left", left_on="id",
                    right_on="referencedComponentId")
    desc.drop(["typeId", "referencedComponentId"], axis=1, inplace=True)

    # Récupérer les concepts ID du non modifié + batchs d'addition et remplacement
    scope = set().union(*[
        b.df.loc[:, "Concept ID"] for b in list_batch if b.type in ["ADD", "REP", "VAL"]
    ])
    # Récupérer les concepts ID des batchs de changement et inactivation + les concepts
    # ID des descriptions de remplacements d'un batch de remplacement
    scope_d = set().union(*[
        b.df.loc[:, "Description ID"] for b in list_batch if b.type == "CHG"
    ])
    scope_d = scope_d.union(*[
        b.df.loc[:, "Description ID Or Term"] for b in list_batch if b.type == "INA"
    ])
    scope = scope.union(desc.loc[desc.loc[:, "id"].isin(scope_d), "conceptId"])
    print("Préparation du DataFrame - OK", end="\r")

    return desc.loc[desc.loc[:, "conceptId"].isin(scope)]


def save_for_import(data: batch.Batch, directory: str) -> None:
    """Sauvegarde un batch au format TSV et renomme les colonnes pour permettre
    l'import dans l'Authoring Platform.

    Args:
        data: Batch data to format and save
        directory: Chemin vers le dossier où sauvegarder les fichiers
    """
    if data.type == "ADD":
        data.df.columns = ["conceptId", "termRef", "preferredTerm", "term", "lang",
                           "caseSignificanceId", "typeId", "langRefset1",
                           "acceptability1", "notes"]
        data.df.insert(9, "langRefset2", [""] * len(data.df))
        data.df.insert(10, "acceptability2", [""] * len(data.df))
        data.df.insert(11, "langRefset3", [""] * len(data.df))
        data.df.insert(12, "acceptability3", [""] * len(data.df))
        data.df.insert(13, "langRefset4", [""] * len(data.df))
        data.df.insert(14, "acceptability4", [""] * len(data.df))
        data.df.insert(15, "langRefset5", [""] * len(data.df))
        data.df.insert(16, "acceptability5", [""] * len(data.df))
    elif data.type == "CHG":
        data.df.insert(7, "Language reference set", [""] * len(data.df),
                       allow_duplicates=True)
        data.df.insert(8, "Acceptability", [""] * len(data.df), allow_duplicates=True)
        data.df.insert(9, "Language reference set", [""] * len(data.df),
                       allow_duplicates=True)
        data.df.insert(10, "Acceptability", [""] * len(data.df), allow_duplicates=True)
        data.df.insert(11, "Language reference set", [""] * len(data.df),
                       allow_duplicates=True)
        data.df.insert(12, "Acceptability", [""] * len(data.df), allow_duplicates=True)
        data.df.insert(13, "Language reference set", [""] * len(data.df),
                       allow_duplicates=True)
        data.df.insert(14, "Acceptability", [""] * len(data.df), allow_duplicates=True)
    elif data.type == "INA":
        data.df.columns = ["descriptionID Or Term",
                           "Language Code (require if the term is specified)",
                           "Concept ID (Optional)",
                           "Preferred Term (For reference only)",
                           "Term (For reference only)", "Inactivation Reason",
                           "Association Target ID1", "Association Target ID2",
                           "Association Target ID3", "Association Target ID4", "Notes"]
    else:
        data.df.columns = ["conceptId", "descriptionId", "preferredTerm", "term",
                           "inactivationReason", "associationTargetId1",
                           "associationTargetId2", "associationTargetId3",
                           "associationTargetId4", "newReplacementDescriptionId",
                           "replacementTerm", "newTranslatedTerm", "languageCode",
                           "caseSignificance", "type", "languageRefset1",
                           "acceptability1", "Notes"]
        data.df.insert(17, "languageRefset2", [""] * len(data.df))
        data.df.insert(18, "acceptability2", [""] * len(data.df))
        data.df.insert(19, "languageRefset3", [""] * len(data.df))
        data.df.insert(20, "acceptability3", [""] * len(data.df))
        data.df.insert(21, "languageRefset4", [""] * len(data.df))
        data.df.insert(22, "acceptability4", [""] * len(data.df))
        data.df.insert(23, "languageRefset5", [""] * len(data.df))
        data.df.insert(24, "acceptability5", [""] * len(data.df))

    data.df.to_csv(op.join(directory, f"{data.type.lower()}.tsv"), sep="\t",
                   index=False)
