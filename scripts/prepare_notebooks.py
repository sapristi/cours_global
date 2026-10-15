#!/usr/bin/env python3
"""Aperçu local d'un notebook diffusé (fichier -> fichier).

Retire les solutions (blocs ``# BEGIN``/``# END``), supprime les cellules de
code dont la 1ère ligne est un commentaire contenant ``DELETE``, vide les
sorties et
ré-embarque les images ``assets/`` en base64, comme le ferait le pipeline CI
(``collect_lite_content.py``), mais **sans** bouton « Clear notebook » et sans
toucher au corrigé : le résultat est écrit dans un fichier séparé.

Usage :
    uv run scripts/prepare_notebooks.py <corrige>.ipynb <apercu>.ipynb

Écrire l'aperçu hors du repo (ex. ``/tmp/``) : ne jamais écraser le corrigé, ne
pas versionner l'aperçu.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from nb_common import inline_images, load_notebook, dump_notebook, strip_solutions


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("src", help="notebook corrigé (source)")
    p.add_argument("dst", help="notebook aperçu (destination)")
    args = p.parse_args(argv)

    src = Path(args.src)
    if not src.is_file():
        print(f"source introuvable: {src}", file=sys.stderr)
        return 2

    nb = load_notebook(src)
    nb_retires = strip_solutions(nb)
    inline_images(nb, assets_dir=src.parent / "assets")
    dump_notebook(nb, Path(args.dst))

    print(f"{src} -> {args.dst} ({nb_retires} solution(s) retirée(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
