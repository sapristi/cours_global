#!/usr/bin/env python3
"""Générateur du graphe du labyrinthe web — TP spidering (LABO ISOLÉ UNIQUEMENT).

Génère un graphe orienté aléatoire (200 nœuds, degré sortant 5 à 10, arêtes vers
l'avant pour rester acyclique), calcule la distance BFS depuis le nœud d'entrée,
repère le nœud le plus distant (qui portera le flag), puis sauvegarde le tout
dans `graphe_labyrinthe.json` (chargé par `serveur_labyrinthe.py`).

Le graphe est déterministe (graine fixe) : relancer ce script reproduit le même
graphe. Le résultat est stocké dans un fichier JSON séparé, pas dans le code
serveur — modifier le fichier JSON suffit à changer le labyrinthe.

Usage (prof uniquement) :
    python3 generer_graphe.py
"""
import json
import random
from collections import deque
from pathlib import Path

N_NOEUDS = 200
DEGRE_MIN = 5
DEGRE_MAX = 10
GRAINE = 20261013
SORTIE = Path(__file__).with_name("graphe_labyrinthe.json")


def generer_graphe(n: int, d_min: int, d_max: int, rng: random.Random) -> dict[int, list[int]]:
    """Graphe orienté acyclique : chaque nœud pointe vers d_min..d_max nœuds
    d'indice strictement supérieur (moins vers la fin, faute de cibles)."""
    graphe: dict[int, list[int]] = {}
    for i in range(n):
        cibles = [j for j in range(i + 1, n)]
        graphe[i] = rng.sample(cibles, min(rng.randint(d_min, d_max), len(cibles)))
    return graphe


def distances_bfs(graphe: dict[int, list[int]], depart: int) -> dict[int, int]:
    """Distance (en nombre d'arêtes) de `depart` vers chaque nœud atteignable."""
    dist: dict[int, int] = {depart: 0}
    file = deque([depart])
    while file:
        u = file.popleft()
        for v in graphe.get(u, []):
            if v not in dist:
                dist[v] = dist[u] + 1
                file.append(v)
    return dist


def main() -> None:
    rng = random.Random(GRAINE)
    graphe = generer_graphe(N_NOEUDS, DEGRE_MIN, DEGRE_MAX, rng)
    dist = distances_bfs(graphe, 0)
    noeud_flag, profondeur = max(dist.items(), key=lambda kv: kv[1])

    donnees = {
        "entree": 0,
        "flag": noeud_flag,
        "profondeur": profondeur,
        "graphe": {str(n): [int(v) for v in voisins] for n, voisins in graphe.items()},
    }

    SORTIE.write_text(json.dumps(donnees, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Graphe généré : {N_NOEUDS} nœuds, flag au nœud {noeud_flag} "
          f"(profondeur {profondeur} depuis l'entrée).")
    print(f"Écrit dans {SORTIE}")


if __name__ == "__main__":
    main()
