#!/usr/bin/env python3
"""Corrigé — labyrinthe web (spidering en BFS).

Parcourt le site en largeur depuis l'accueil, en :
- gardant un ensemble des pages déjà visitées (URL **normalisées**) ;
- limitant le nombre de pages explorées (la pagination est infinie) ;
- posant un timeout sur chaque requête (routes lentes) ;
- ne s'arrêtant pas sur les pages d'erreur ni sur les contenus non-HTML ;
- lisant les flags dans le corps **et** dans les en-têtes de réponse ;
- collectant tous les flags valides (`FLAG{1}` à `FLAG{7}`) et en ignorant
  le leurre (`FLAG{ceci_est_un_leurre}`).

Usage :
    python3 labyrinthe_corrige.py --url http://127.0.0.1:8000/ --max-pages 500

Cadre légal : labo isolé uniquement, autorisation écrite hors labo.
Art. 323-1 Code pénal : accès frauduleux = délit, même « juste pour voir ».
"""
import argparse
import re
import sys
from collections import deque
from urllib.parse import urljoin, urlparse, urlunparse

import requests

FLAG_RE = re.compile(r"FLAG\{[^}]+\}")
VALIDES = {f"FLAG{{{i}}}" for i in range(1, 8)}
LEURRES = {"FLAG{ceci_est_un_leurre}"}
LIEN_RE = re.compile(r'href="([^"]+)"')
CHEMIN_RE = re.compile(r"/[A-Za-z0-9_./-]+")


def normaliser(url: str) -> str:
    """Normalise une URL : sans fragment, sans slash final, params triés.

    Permet de reconnaître /page, /page/ et /page#ancre comme la même page,
    et de casser les boucles de normalisation (ex. /miroir <-> /miroir/).
    """
    p = urlparse(url)
    chemin = p.path.rstrip("/") or "/"
    params = sorted(p.query.split("&")) if p.query else []
    return urlunparse((p.scheme, p.netloc, chemin, "", "&".join(params), ""))


def extraire_liens(html: str) -> list[str]:
    """Renvoie les href des balises <a href="..."> du HTML."""
    return LIEN_RE.findall(html)


def crawler(depart: str, max_pages: int, timeout: float) -> set[str]:
    """Explore le site en BFS et renvoie tous les flags valides trouvés."""
    visites: set[str] = set()
    file: deque[str] = deque([depart])
    trouves: set[str] = set()

    while file and len(visites) < max_pages:
        url = file.popleft()
        cle = normaliser(url)
        if cle in visites:
            continue
        visites.add(cle)

        try:
            r = requests.get(url, timeout=timeout)
        except requests.RequestException:
            continue

        texte = r.text
        trouves.update(FLAG_RE.findall(texte))
        entetes = " ".join(f"{k}: {v}" for k, v in r.headers.items())
        trouves.update(FLAG_RE.findall(entetes))

        if "text/html" in r.headers.get("content-type", ""):
            for lien in extraire_liens(texte):
                file.append(urljoin(r.url, lien))
        else:
            for chemin in CHEMIN_RE.findall(texte):
                file.append(urljoin(r.url, chemin))

    return trouves


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--url", default="http://127.0.0.1:8000/")
    p.add_argument("--max-pages", type=int, default=500,
                   help="nombre maximal de pages explorées (pagination infinie)")
    p.add_argument("--timeout", type=float, default=5.0,
                   help="timeout (s) de chaque requête")
    args = p.parse_args()

    trouves = crawler(args.url, args.max_pages, args.timeout)
    valides = sorted(trouves & VALIDES)
    leurres = sorted(trouves & LEURRES)

    if not valides:
        print("Aucun flag valide trouvé (limite atteinte ?).")
    else:
        print("\n".join(valides))

    if leurres:
        print(f"(leurre(s) ignoré(s) : {', '.join(leurres)})", file=sys.stderr)


if __name__ == "__main__":
    main()
