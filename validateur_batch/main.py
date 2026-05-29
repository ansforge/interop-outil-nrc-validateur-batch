#!/usr/bin/env python3

import argparse
import os.path as op
import pandas as pd

from validateur_batch import io
from validateur_batch.object import batch, server
from validateur_batch.control import editorial_check, format_check

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("endpoint", type=str, help="Endpoint du FTS à utiliser")
    cli.add_argument("snapshot", type=str,
                     help="Chemin vers la snapshot de l'édition FR")
    cli.add_argument("date", type=str, help="Date de publication de l'édition FR")
    cli.add_argument("output", type=str, help="Dossier où sauvegarder les rapports")
    cli.add_argument("--val", type=str,
                     help="Chemin vers le CSV des concepts non modifiés")
    cli.add_argument("--add", type=str,
                     help="Chemin vers le CSV de l'onglet 'Description Additions'")
    cli.add_argument("--chg", type=str,
                     help="Chemin vers le CSV de l'onglet 'Description Changes'")
    cli.add_argument("--rep", type=str,
                     help="Chemin vers le CSV de l'onglet 'Description Replacement'")
    cli.add_argument("--ina", type=str,
                     help="Chemin vers le CSV de l'onglet 'Description Inactivations'")
    args = cli.parse_args()

    # Initialisation de la classe de gestion du FTS
    fts = server.Server(args.endpoint)

    # Création de la liste des fichiers
    print("\n## Imports batch ##")
    print("Lecture des imports batch...", end="\r")
    input = zip(
        [args.val, args.add, args.chg, args.rep, args.ina],
        ["VAL", "ADD", "CHG", "REP", "INA"]
    )
    list_b = [batch.Batch(f, t) for f, t in input if f is not None]
    print("Lecture des imports batch - OK")

    # Initialiser la preview de la snapshot de l'édition FR
    print("\n## Snapshot FR ##")
    preview = io.read_snapshot(args.snapshot, args.date, list_b)

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
    fsn = preview.loc[:, ["conceptId"]].drop_duplicates("conceptId", ignore_index=True)
    fsn.loc[:, "FSN"] = [fts.get_fsn(sctid) for sctid in fsn.loc[:, "conceptId"]]
    preview = pd.merge(preview, fsn, how="left", on="conceptId")
    preview = preview[["id", "active", "_type_", "conceptId", "FSN", "term",
                       "caseSignificanceId", "acceptabilityId", "notes"]]

    # Vérification du respect des règles éditoriales
    print("\n## Respect des règles éditoriales ##")
    preview = editorial_check.run_editorial_check(preview, fts)
    # Vérification du respect 1 concept = 1 PT
    preview = format_check.check_pt(preview)
    # Sauvegarde du fichier
    filepath = op.join(args.output, "check_results.csv")
    preview.to_csv(filepath, sep=";", index=False)
    print(f"\nAnalyse terminée et sauvegardée : {filepath}")
