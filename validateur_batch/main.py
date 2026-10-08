#!/usr/bin/env python3

import argparse
import os.path as op
import pandas as pd

from typing import Optional
from validateur_batch import io
from validateur_batch.object import server
from validateur_batch.control import editorial_check, format_check


def run(input_dir: str, output_dir: str, import_mode: bool = False,
        endpoint: Optional[str] = None, snapshot: Optional[str] = None) -> None:
    """Lance la vérification ou le formatage pour l'import des batchs

    Args:
        input_dir: Dossier contenant les batchs
        output_dir: Dossier où sauvegarder les rapports
        import_mode: Formate pour l'import si vrai, sinon lance la vérification
        endpoint: Endpoint du FTS à utiliser (mode vérification)
        snapshot: Chemin vers la snapshot de l'édition FR (mode vérification)
    """
    # Initialisation de la classe de gestion du FTS
    fts = server.Server(endpoint)

    # Création de la liste des fichiers
    print("\n## Imports batch ##")
    print("Lecture des imports batch...", end="\r")
    list_b = io.read_excel_dir(input_dir)
    print("Lecture des imports batch - OK")

    # Formater pour l'import dans l'Authoring Platform
    if import_mode:
        print("Formatage et sauvegarde des batchs...", end="\r")
        _ = [io.save_for_import(b, output_dir) for b in list_b if b.type != "VAL"]
        print("Formatage et sauvegarde des batchs - OK")
    # Sinon lancer la vérification des fichiers
    else:
        # Initialiser la preview de la snapshot de l'édition FR
        print("\n## Snapshot FR ##")
        preview = io.read_snapshot(snapshot, list_b)

        print("\n\n## Respect du format ##")
        for b in list_b:
            # Vérification du respect du format
            b.check_format(fts)
            # Appliquer les changements des batchs sur `data`
            if b.type != "VAL":
                preview.set_index("id", inplace=True)
                preview = b.apply_modif(preview)
                preview.reset_index(inplace=True)

        # Ajouter les FSN de l'édition INT à la preview
        fsn = preview.loc[:, ["conceptId"]].drop_duplicates("conceptId",
                                                            ignore_index=True)
        fsn.loc[:, "FSN"] = fsn.loc[:, "conceptId"].map(
            fts.batch_get_fsn(list(fsn.loc[:, "conceptId"])))
        preview = pd.merge(preview, fsn, how="left", on="conceptId")
        preview = preview[["id", "active", "_type_", "conceptId", "FSN", "term",
                           "caseSignificanceId", "acceptabilityId", "notes"]]

        # Vérification du respect des règles éditoriales
        print("\n## Respect des règles éditoriales ##")
        preview = editorial_check.run_editorial_check(preview, fts)
        # Vérification du respect 1 concept = 1 PT
        preview = format_check.check_pt(preview)
        # Sauvegarde du fichier
        filepath = op.join(output_dir, "check_results.csv")
        preview.to_csv(filepath, sep=";", index=False)
        print(f"\nAnalyse terminée et sauvegardée : {filepath}")


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("input", type=str, help="Dossier contenant les batchs")
    cli.add_argument("output", type=str, help="Dossier où sauvegarder les rapports")
    cli.add_argument("-i", "--import_mode", action="store_true",
                     help="Formate pour l'import, si absent lance la vérification")
    cli.add_argument("-e", "--endpoint", type=str, help="Endpoint du FTS à utiliser")
    cli.add_argument("-s", "--snapshot", type=str,
                     help="Chemin vers la snapshot de l'édition FR")

    args = cli.parse_args()

    if not args.import_mode and (args.snapshot is None or args.endpoint is None):
        cli.error("--endpoint et --snapshot sont nécessaires en mode vérification")

    run(args.input, args.output, args.import_mode, args.endpoint, args.snapshot)
