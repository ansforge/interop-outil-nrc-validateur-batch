from validateur_batch.scope import Scope
import pandas as pd

def check_scope_completeness(scope: Scope, preview: pd.DataFrame) -> pd.DataFrame:
    """
    Vérifie que tous les concepts présents dans le périmètre d'analyse sont présents dans le DataFrame de prévisualisation.

    Args:
        scope (Scope): Objet Scope contenant le périmètre d'analyse.
        preview (pd.DataFrame): DataFrame de prévisualisation contenant les concepts à vérifier, avec une colonne "conceptId".

    Returns:
        pd.DataFrame: DataFrame du scope enrichi d'une colonne "in_delivery" indiquant si chaque concept du périmètre d'analyse est présent dans le DataFrame de prévisualisation.
    """
    if scope is None:
        raise ValueError("Le périmètre d'analyse doit être défini pour effectuer la vérification de complétude.")
    
    scope_df = scope.full_scope_df.copy()
    scope_df["in_delivery"] = scope_df["conceptId"].isin(preview["conceptId"])
    return scope_df

def check_scope_exclusivity(scope: Scope, preview: pd.DataFrame) -> pd.DataFrame:
    """
    Vérifie que tous les concepts présents dans le DataFrame de prévisualisation sont présents dans le périmètre d'analyse.

    Args:
        scope (Scope): Objet Scope contenant le périmètre d'analyse.
        preview (pd.DataFrame): DataFrame de prévisualisation contenant les concepts à vérifier, avec une colonne "conceptId".

    Returns:
        pd.DataFrame: DataFrame de prévisualisation enrichi d'une colonne "in_scope" indiquant si chaque concept de la prévisualisation est présent dans le périmètre d'analyse.
    """
    if scope is None:
        raise ValueError("Le périmètre d'analyse doit être défini pour effectuer la vérification d'exclusivité.")
    
    scope_concept_ids = set(scope.full_scope_df["conceptId"])
    preview = preview.copy()
    preview["in_scope"] = preview["conceptId"].isin(scope_concept_ids)
    return preview