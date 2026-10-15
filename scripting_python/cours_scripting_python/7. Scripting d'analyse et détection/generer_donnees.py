#!/usr/bin/env python3
"""Génère `logs_reseau.csv` : journaux simulés de connexions sortantes.

Le dataset mélange du trafic légitime et trois hôtes compromis, un par
difficulté de détection (cf. notebook `detection_beacon.ipynb`) :

1. **Beaconing statique** (`10.0.0.66`) — un domaine C2 fixe, contacté à
   intervalle régulier (~60 s) avec jitter. Noyé dans des mises à jour
   légitimes elles aussi périodiques (piège).
2. **Fast-flux / DGA** (`10.0.0.67`) — le rythme est régulier mais la
   destination *tourne* (domaine et IP changent à chaque connexion) : grouper
   par domaine ne suffit plus.
3. **Timing aléatoire** (`10.0.0.68`) — aucun rythme exploitable ; l'indice
   est dans la plage d'IP contactée (un /24 que personne d'autre ne touche).

Le générateur est déterministe (graine fixe) : relancer produit exactement le
même CSV. Les données générées sont stockées dans le repo, à côté de ce script.

Usage :
    python3 generer_donnees.py            # écrit logs_reseau.csv dans ce dossier
    python3 generer_donnees.py --out /tmp/logs.csv

Cadre légal : tout ceci est un jeu de données **simulé**, aucune cible réelle.
Art. 323-1 Code pénal : accès frauduleux = délit, même « juste pour voir ».
"""

import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

GRAINE = 42

# --- Hôtes internes (sources) ------------------------------------------------
HOTES_LEGITIMES = [f"10.0.0.{i}" for i in range(1, 13)]
VICTIME_A = "10.0.0.66"  # ex 1 : beaconing statique
VICTIME_B = "10.0.0.67"  # ex 2 : fast-flux / DGA
VICTIME_C = "10.0.0.68"  # ex 3 : timing aléatoire + plage d'IP rare

# --- Destinations légitimes (partagées entre plusieurs hôtes) ----------------
# (domaine, ip, port, « périodique ? »)
DESTINATIONS_LEGITIMES = {
    "google.com": ("142.250.75.14", 443, False),
    "microsoft.com": ("20.112.52.29", 443, False),
    "github.com": ("140.82.112.3", 443, False),
    "wikipedia.org": ("208.80.154.224", 443, False),
    "amazon.com": ("52.94.236.248", 443, False),
    "cloudflare.com": ("104.16.132.229", 443, False),
    # Mises à jour légitimes, périodiques : le piège de l'exercice 1.
    "windowsupdate.com": ("23.216.55.10", 443, True),
    "ntp.org": ("162.159.200.123", 123, True),
    "av-updates.example.net": ("45.63.10.20", 443, True),
}

# --- C2 des victimes ---------------------------------------------------------
C2_A = ("c2-sync.xyz", "185.165.29.10", 443)   # statique
C2_C = ("vpn-relay.xyz", None, 443)             # timing aléatoire (IPs dans un /24 rare)
PREFIXE_C = "91.240.118"                         # /24 rare, touché par C uniquement

# Fast-flux : pool d'IP dispersées dans plusieurs /24, pool de domaines DGA.
# Graine dédiée pour rester déterministe indépendamment du reste du script.
_rng_b = random.Random(GRAINE)
IP_POOL_B = [f"193.29.{_rng_b.randint(1, 220)}.{_rng_b.randint(2, 250)}" for _ in range(40)]
DOMAINES_B = [f"flux-{_rng_b.randrange(1000, 9999)}.xyz" for _ in range(480)]

DEBUT = datetime(2026, 10, 14, 8, 0, 0)   # fenêtre d'observation : 08:00 -> 20:00
FIN = datetime(2026, 10, 14, 20, 0, 0)
DUREE_S = int((FIN - DEBUT).total_seconds())


def horodatage(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def generer_lignes(rng: random.Random) -> list[dict]:
    lignes: list[dict] = []

    def ajouter(ts: datetime, src: str, dst_ip: str, domaine: str, port: int, octets: int) -> None:
        lignes.append({
            "timestamp": horodatage(ts),
            "src_ip": src,
            "dst_ip": dst_ip,
            "domain": domaine,
            "dst_port": port,
            "bytes_out": octets,
        })

    # --- Trafic légitime -----------------------------------------------------
    for hote in HOTES_LEGITIMES:
        # Navigation web : destinations partagées, timing irrégulier (Poisson).
        for _ in range(rng.randint(90, 140)):
            domaine, (ip, port, _) = rng.choice(
                [(d, v) for d, v in DESTINATIONS_LEGITIMES.items() if not v[2]]
            )
            ts = DEBUT + timedelta(seconds=rng.randint(0, DUREE_S))
            ajouter(ts, hote, ip, domaine, port, rng.randint(200, 60_000))

        # Mises à jour périodiques : intervalle quasi constant (le piège ex 1).
        for domaine, (ip, port, _) in DESTINATIONS_LEGITIMES.items():
            intervalle = {"windowsupdate.com": 1800, "ntp.org": 3600,
                          "av-updates.example.net": 1200}.get(domaine)
            if intervalle is None or rng.random() < 0.4:
                continue
            t = DEBUT + timedelta(seconds=rng.randint(0, intervalle))
            while t <= FIN:
                # Payload variable (un téléchargement de màj n'est pas constant).
                ajouter(t, hote, ip, domaine, port, rng.randint(500, 200_000))
                t += timedelta(seconds=intervalle)

    # --- Victime A : beaconing statique --------------------------------------
    domaine_a, ip_a, port_a = C2_A
    t = DEBUT + timedelta(seconds=10)
    while t <= FIN:
        jitter = rng.randint(-5, 5)
        ajouter(t + timedelta(seconds=jitter), VICTIME_A, ip_a, domaine_a, port_a, 512)
        t += timedelta(seconds=60)

    # --- Victime B : fast-flux / DGA (destination qui tourne) -----------------
    t = DEBUT + timedelta(seconds=20)
    i = 0
    while t <= FIN:
        domaine = DOMAINES_B[i % len(DOMAINES_B)]
        ip = IP_POOL_B[i % len(IP_POOL_B)]
        jitter = rng.randint(-3, 3)
        ajouter(t + timedelta(seconds=jitter), VICTIME_B, ip, domaine, 443, 256)
        t += timedelta(seconds=90)
        i += 1

    # --- Victime C : timing aléatoire, /24 rare ------------------------------
    domaine_c, _, port_c = C2_C
    t = DEBUT + timedelta(seconds=30)
    while t <= FIN:
        ip = f"{PREFIXE_C}.{rng.randint(101, 105)}"
        ajouter(t, VICTIME_C, ip, domaine_c, port_c, 128)
        # Intervalle exponentiel (pas de rythme) : moyenne ~300 s.
        t += timedelta(seconds=rng.expovariate(1 / 300.0))

    lignes.sort(key=lambda l: l["timestamp"])
    return lignes


def ecrire_csv(lignes: list[dict], chemin: Path) -> None:
    colonnes = ["timestamp", "src_ip", "dst_ip", "domain", "dst_port", "bytes_out"]
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(",".join(colonnes) + "\n")
        for l in lignes:
            f.write(",".join(str(l[c]) for c in colonnes) + "\n")


def resumer(lignes: list[dict]) -> None:
    par_hote: dict[str, int] = {}
    for l in lignes:
        par_hote[l["src_ip"]] = par_hote.get(l["src_ip"], 0) + 1
    print(f"{len(lignes)} connexions générées.")
    print("Connexions par hôte (top 5) :")
    for hote, n in sorted(par_hote.items(), key=lambda kv: -kv[1])[:5]:
        print(f"  {hote:>12} : {n}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", default=None, help="chemin du CSV (défaut : à côté du script)")
    args = p.parse_args()

    sortie = Path(args.out) if args.out else Path(__file__).parent / "logs_reseau.csv"
    rng = random.Random(GRAINE)
    lignes = generer_lignes(rng)
    ecrire_csv(lignes, sortie)
    print(f"Écrit dans {sortie}")
    resumer(lignes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
