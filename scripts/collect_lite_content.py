#!/usr/bin/env python3
"""Rassemble les notebooks des cours dans ``content/`` pour ``jupyter lite build``.

Les notebooks vivent dans les dossiers de chaque cours (source de vérité, jamais
modifiés ici) :

- ``machine_learning/td/*.ipynb`` (corrigés à plat)
- ``scripting_python/td/*.ipynb`` (corrigés à plat, préfixe numéroté)

Ce script les copie dans ``content/<cours>/…`` en conservant l'arborescence
relative à la source du cours, pour les retrouver sous leur dossier dans
JupyterLite. À la copie, chaque notebook :

1. perd ses solutions : les blocs ``# BEGIN``/``# END`` (ou ``#BEGIN``/``#END``)
   sont remplacés par ``# TODO`` + corps/hint dérivé des commentaires, les
   cellules de code dont la 1ère ligne est un commentaire contenant ``DELETE``
   sont supprimées, les cellules markdown dont la 1ère ligne non vide est
   exactement ``# TOCLEAR`` (réponses du corrigé) sont supprimées, et les
   sorties sont vidées (la version déployée est un énoncé à trous) ;
2. reçoit en première cellule un bouton « Clear notebook » qui purge son état du
   stockage local du navigateur (IndexedDB) ;
3. voit ses images markdown ``assets/*`` ré-embarquées en base64 (data URI).

Les fichiers de données (CSV, JSON, …) chargés par les notebooks sont aussi
copiés tels quels.

Usage :
    uv run scripts/collect_lite_content.py [--cours machine_learning]
"""

import argparse
import shutil
import sys
from pathlib import Path

from nb_common import inject_clear_button, inline_images, load_notebook, dump_notebook, strip_solutions

RACINE = Path(__file__).resolve().parent.parent
CONTENT = RACINE / "content"

# Cours -> dossiers sources des notebooks (source de vérité).
COURS: dict[str, list[Path]] = {
    "machine_learning": [RACINE / "machine_learning" / "td"],
    "scripting_python": [RACINE / "scripting_python" / "td"],
}

EXCLUS = (".git", "dist", "content", "node_modules", ".venv", ".obsidian", ".ipynb_checkpoints", "__pycache__")

DONNEES_EXTENSIONS = {".csv", ".json", ".txt", ".tsv", ".parquet", ".pcap", ".pcapng"}


def est_exclu(chemin: Path) -> bool:
    return any(part in EXCLUS for part in chemin.parts)


def trouver_notebooks(sources: list[Path]) -> list[tuple[Path, Path]]:
    """Renvoie les couples ``(source, rel)`` des notebooks d'un cours."""
    out: list[tuple[Path, Path]] = []
    for source in sources:
        for p in source.rglob("*.ipynb"):
            rel = p.relative_to(source)
            if est_exclu(rel) or "checkpoint" in p.name:
                continue
            out.append((p, rel))
    return sorted(out, key=lambda t: t[1].as_posix())


def trouver_donnees(sources: list[Path]) -> list[tuple[Path, Path]]:
    out: list[tuple[Path, Path]] = []
    for source in sources:
        for p in source.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in DONNEES_EXTENSIONS:
                continue
            rel = p.relative_to(source)
            if est_exclu(rel):
                continue
            out.append((p, rel))
    return sorted(out, key=lambda t: t[1].as_posix())


def collecter_notebooks(cours: str, sources: list[Path]) -> None:
    for src, rel in trouver_notebooks(sources):
        dst = CONTENT / cours / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

        cle = (Path(cours) / rel).as_posix()
        nb = load_notebook(dst)
        nb_retires = strip_solutions(nb)
        inline_images(nb, assets_dir=src.parent / "assets")
        inject_clear_button(nb, cle)
        dump_notebook(nb, dst)

        suffixes = ["+ clear cell"]
        if nb_retires:
            suffixes.append(f"+ {nb_retires} solution(s) retirée(s)")
        print(f"{cours}/{rel} -> content/{cours}/{rel} [{', '.join(suffixes)}]")


def collecter_donnees(cours: str, sources: list[Path]) -> None:
    for src, rel in trouver_donnees(sources):
        dst = CONTENT / cours / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"{cours}/{rel} -> content/{cours}/{rel} [données]")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cours", choices=sorted(COURS), help="ne traiter que ce cours")
    args = parser.parse_args()

    cours_a_traiter = [args.cours] if args.cours else sorted(COURS)

    shutil.rmtree(CONTENT, ignore_errors=True)
    CONTENT.mkdir(parents=True, exist_ok=True)

    for cours in cours_a_traiter:
        sources = COURS[cours]
        missing = [s for s in sources if not s.is_dir()]
        if missing:
            print(f"dossier source introuvable : {', '.join(map(str, missing))}", file=sys.stderr)
            return 1
        collecter_notebooks(cours, sources)
        collecter_donnees(cours, sources)
    return 0


if __name__ == "__main__":
    sys.exit(main())
