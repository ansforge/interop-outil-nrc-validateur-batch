import pandas as pd

from typing import Literal, TYPE_CHECKING
from validateur_batch.control import format_check

if TYPE_CHECKING:
    from validateur_batch.object import server

BATCH_TYPE = Literal["VAL", "ADD", "CHG", "REP", "INA"]
COL = {
    "VAL": ["Concept ID", "FSN"],
    "ADD": ["Concept ID", "GB/US FSN Term (For reference only)",
            "Preferred Term (For reference only)", "Translated Term", "Language Code",
            "Case significance", "Type", "Language reference set", "Acceptability",
            "Notes"],
    "CHG": ["Description ID", "Preferred Term (For reference only)",
            "Term (For reference only)", "Case significance", "Type",
            "Language reference set", "Acceptability", "Notes"],
    "REP": ["Concept ID", "Description ID", "Preferred Term (For reference only)",
            "Term (For reference only)", "Inactivation Reason",
            "Association Target ID1", "Association Target ID2",
            "Association Target ID3", "Association Target ID4",
            "New Replacement Description ID", "Replacement term (For reference only)",
            "New Translated Term", "Language Code", "Case significance", "Type",
            "Language reference set", "Acceptability", "Notes"],
    "INA": ["Description ID Or Term",
            "Language Code (require if the term is specified)", "Concept ID (Optional)",
            "Preferred Term (For reference only)", "Term (For reference only)",
            "Inactivation Reason", "Association Target ID1", "Association Target ID2",
            "Association Target ID3", "Association Target ID4", "Notes"]
}


class Batch:
    """Représente un batch de descriptions à ajouter, modifier, inactiver ou remplacer
    dans l'Authoring Platform ainsi que les résultats des contrôles associés"""
    def __init__(self, file: str, type: BATCH_TYPE):
        # Métadonnées du batch
        self.file = file
        self.type = type
        # Données du batch
        self.df = pd.read_csv(file, sep=";", quoting=3, na_filter=False, dtype=str)

        if not all(i == j for i, j in zip(self.df.columns, COL[type])):
            raise ValueError(f"Colonne(s) du fichier incorrecte(s) : {file}")

    def _apply_add(self, preview: pd.DataFrame) -> pd.DataFrame:
        """Applique les modifications d'un batch d'addition à `preview`

        args:
            preview: DataFrame contenant les descriptions d'intérêt de la snapshot dans
                le périmètre des travaux

        returns:
            DataFrame avec les nouvelles descriptions ajoutées par le batch
        """
        # Identifier l'addition de PT pour des concepts en ayant déjà
        pt = preview.loc[preview.loc[:, "conceptId"].isin(
            self.df.loc[self.df.loc[:, "Acceptability"] == "PREFERRED", "Concept ID"])]
        # Modifier l'acceptabilité des PT existants
        pt.loc[:, "acceptabilityId"] = ["ACCEPTABLE"] * len(pt)
        preview.update(pt)

        # Formatage du batch à ajouter
        add = self.df.loc[:, ["Concept ID", "Translated Term", "Case significance",
                              "Acceptability", "Notes"]]
        add.columns = ["conceptId", "term", "caseSignificanceId",
                       "acceptabilityId", "notes"]
        add.loc[:, "_type_"] = ["ADD"] * len(add)
        add.loc[:, "active"] = ["1"] * len(add)

        # Ajout des descriptions du batch
        preview.reset_index(inplace=True)
        preview = pd.concat([preview, add], ignore_index=True)
        preview.set_index("id", inplace=True)

        return preview

    def _apply_chg(self, preview: pd.DataFrame) -> pd.DataFrame:
        """Applique les modifications d'un batch de changement à `preview`

        args:
            preview: DataFrame contenant les descriptions d'intérêt de la snapshot dans
                le périmètre des travaux

        returns:
            DataFrame avec la mise à jour des métadonnées du batch
        """
        # Formatage des changements de métadonnées
        chg = self.df.loc[:, ["Description ID", "Case significance", "Acceptability",
                              "Notes"]]
        chg.set_index("Description ID", inplace=True)
        chg.columns = ["caseSignificanceId", "acceptabilityId", "notes"]
        chg.loc[:, "_type_"] = ["CHG"] * len(chg)

        # Changement des descriptions du batch
        preview.update(chg)

        return preview

    def _apply_rep(self, preview: pd.DataFrame) -> pd.DataFrame:
        """Applique les modifications d'un batch de remplacement à `preview`

        args:
            preview: DataFrame contenant les descriptions d'intérêt de la snapshot dans
                le périmètre des travaux

        returns:
            DataFrame avec le remplacement des descriptions du batch
        """
        rep = self.df.loc[:, ["Concept ID", "Description ID", "New Translated Term",
                              "Case significance", "Acceptability", "Notes"]]
        rep.set_index("Description ID", inplace=True)
        rep.columns = ["conceptId", "term", "caseSignificanceId",
                       "acceptabilityId", "notes"]
        rep.loc[:, "_type_"] = ["REP"] * len(rep)
        rep.loc[:, "active"] = ["1"] * len(rep)

        # Inactivation des descriptions à remplacer
        ina = rep.loc[:, ["active", "_type_"]]
        ina.loc[:, "active"] = ["0"] * len(ina)
        preview.update(ina)

        # Ajout des descriptions de remplacement
        add = rep.loc[:, ["active", "conceptId", "term", "caseSignificanceId",
                          "acceptabilityId", "notes", "_type_"]]
        preview.reset_index(inplace=True)
        preview = pd.concat([preview, add], ignore_index=True)
        preview.set_index("id", inplace=True)

        return preview

    def _apply_ina(self, preview: pd.DataFrame) -> pd.DataFrame:
        """Applique les modifications d'un batch d'inactivation à `preview`

        args:
            preview: DataFrame contenant les descriptions d'intérêt de la snapshot dans
                le périmètre des travaux

        returns:
            DataFrame avec l'inactivation des descriptions du batch
        """
        # Formatage des inactivations du batch
        ina = self.df.loc[:, ["Description ID Or Term", "Notes"]]
        ina.loc[:, "active"] = ["0"] * len(ina)
        ina.loc[:, "_type_"] = ["INA"] * len(ina)
        ina.set_index("Description ID Or Term", inplace=True)

        ina = ina.loc[:, ["active", "Notes", "_type_"]]
        ina.columns = ["active", "notes", "_type_"]

        # Inactivation des descriptions du batch
        preview.update(ina)

        return preview

    def apply_modif(self, preview: pd.DataFrame) -> None:
        """
        Applique les modifications du batch à `preview`

        args:
            preview: DataFrame contenant les descriptions d'intérêt de la snapshot
                FR dans le périmètre des travaux

        returns:
            DataFrame `preview` mis à jour avec les modifications des batchs
        """
        self.df.reset_index(inplace=True)
        self.df.loc[:, "_type_"] = [""] * len(self.df)
        print(f"{self.type} - Application des modifications à la Snapshot...",
              end="\r")
        match self.type:
            case "ADD":
                preview = self._apply_add(preview)
            case "CHG":
                preview = self._apply_chg(preview)
            case "REP":
                preview = self._apply_rep(preview)
            case "INA":
                preview = self._apply_ina(preview)
        print(f"{self.type} - Application des modifications à la Snapshot - OK")

        return preview

    def check_format(self, fts: "server.Server") -> None:
        """Lance les contrôles de format du fichier batch.

        args:
            fts: Serveur de Terminologies FHIR à utiliser
        """
        print(f"{self.type} - Vérification du format...", end="\r")
        nb = len(self.df.columns)
        self.df = format_check.run_format_check(self.df, self.type, fts)
        nb = len(self.df.columns) - nb
        status = "OK" if nb == 0 else "KO"
        print(f"{self.type} - {nb} règle(s) de format non respectées - {status}")
