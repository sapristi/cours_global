#!/usr/bin/env python3
"""Génère `logs_reseau.csv` et `logs_reseau_grand.csv` : journaux simulés de
connexions sortantes.

Le dataset principal mélange du trafic légitime et trois hôtes compromis, un
par difficulté de détection (cf. notebook `detection_beacon.ipynb`) :

1. **Beaconing statique** (`10.0.0.66`) — un domaine C2 fixe, contacté à
   intervalle régulier (~7 min) avec jitter (~une centaine de connexions sur
   la fenêtre). Noyé dans des mises à jour légitimes elles aussi périodiques
   (piège).
2. **Fast-flux / DGA** (`10.0.0.67`) — le rythme est régulier mais la
   destination *tourne* (domaine et IP changent à chaque connexion) : grouper
   par domaine ne suffit plus.
3. **Timing aléatoire** (`10.0.0.68`) — aucun rythme exploitable ; l'indice
   est dans la plage d'IP contactée (un /24 que personne d'autre ne touche).

Un **second jeu de données** (`logs_reseau_grand.csv`) illustre le cas où le
simple comptage de destinations ne suffit plus : une centaine d'hôtes légitimes
contactent chacun des centaines d'IP de CDN partagées, et un seul implant
fast-flux (`10.0.0.167`) ne touche que des IP « rares » (contactées par lui
seul).

Le générateur est déterministe (graine fixe) : relancer produit exactement les
mêmes CSV. Les données générées sont stockées dans le repo, à côté de ce script.

Usage :
    python3 generer_donnees.py                            # écrit les deux CSV
    python3 generer_donnees.py --out /tmp/logs.csv \
                                --out-grand /tmp/logs_grand.csv

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
    # Sosies du C2 ex 1 : mêmes motifs (sync / updates, même zone),
    # eux aussi périodiques, pour noyer le beacon dans le tri par CV.
    "sync-backup.example.net": ("45.63.10.21", 443, True),
    "metrics-updates.example.net": ("45.63.10.22", 443, True),
}

# --- Leurres "suspects" à CV élevé -------------------------------------------
# Noms shady (DGA, `.top`) mais timing humain irrégulier : ils apparaissent
# dans le tri par CV avec un CV élevé, au milieu du trafic légitime. On ne
# doit pas pouvoir les confondre avec le beacon au seul nom de domaine.
# (domaine, ip, port, hôtes légitimes qui le contactent)
LEURRES_SUSPECTS = {
    "free-prize-claim.top": ("91.121.45.67", 443, ["10.0.0.4", "10.0.0.9"]),
    "x9f2k7q4m1z.xyz": ("45.155.204.31", 443, ["10.0.0.5", "10.0.0.8"]),
}
NB_LEURRE_SUSPECT = 25  # connexions par hôte (≥ 20 pour figurer dans le tri par CV)

# --- C2 des victimes ---------------------------------------------------------
C2_A = ("sync-updates.example.net", "185.165.29.10", 443)   # statique, discret
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

# --- Grand réseau (exercice 4) : le comptage de destinations ne suffit plus ---
GRAINE_GRAND = 1337
NB_HOTES_GRAND = 100
VICTIME_GRAND = "10.0.0.167"  # fast-flux : toutes ses IP de destination sont « rares »

# IP « CDN » partagées : contactées par de très nombreux hôtes légitimes.
CDN_POOL = [(f"198.18.{i // 256}.{i % 256}", f"cdn-{i}.example.net") for i in range(600)]

# Télémétrie : service légitime périodique (le faux positif de l'exercice 1).
TELEMETRIE_IP = "198.51.100.10"
TELEMETRIE_DOMAINE = "telemetry.analytics.example.net"

# Fast-flux « grand » : pool d'IP rares + pool de domaines DGA, uniques et
# mélangés de façon déterministe.
_rng_grand = random.Random(GRAINE_GRAND)
IP_RARES_GRAND = [f"193.29.{i // 256}.{i % 256}" for i in range(400)]
_rng_grand.shuffle(IP_RARES_GRAND)
DOMAINES_GRAND = [f"flux-{i}.xyz" for i in range(400)]
_rng_grand.shuffle(DOMAINES_GRAND)


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
    # Les sosies du C2 ex 1 utilisent un flux aléatoire dédié : le générateur
    # principal `rng` garde exactement la même séquence qu'avant leur ajout
    # (mêmes volumes pour les autres domaines, même jitter du beacon).
    # Même logique pour le jitter des mises à jour périodiques : un flux
    # dédié, pour ne changer que les timestamps (pas les volumes).
    rng_sosies = random.Random(GRAINE + 1000)
    rng_jitter = random.Random(GRAINE + 2000)
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
                          "av-updates.example.net": 1200,
                          "sync-backup.example.net": 1500,
                          "metrics-updates.example.net": 1800}.get(domaine)
            tirage = rng_sosies if domaine in ("sync-backup.example.net",
                                               "metrics-updates.example.net") else rng
            if intervalle is None or tirage.random() < 0.4:
                continue
            t = DEBUT + timedelta(seconds=tirage.randint(0, intervalle))
            while t <= FIN:
                # Payload variable (un téléchargement de màj n'est pas constant).
                # Jitter de ±5 s, même ordre que celui du beacon malicieux :
                # les mises à jour légitimes restent quasi périodiques (CV faible)
                # sans être parfaitement régulières (CV == 0.0 irréaliste).
                jitter = rng_jitter.randint(-5, 5)
                ajouter(t + timedelta(seconds=jitter), hote, ip, domaine, port,
                        tirage.randint(500, 200_000))
                t += timedelta(seconds=intervalle)

    # --- Leurres suspects à CV élevé -----------------------------------------
    # Quelques hôtes légitimes contactent des domaines au nom shady, mais à des
    # instants uniformément aléatoires (CV élevé) : dans le tri par CV, ils se
    # retrouvent au milieu du trafic humain, pas en tête avec le beacon.
    for domaine, (ip, port, hotes) in LEURRES_SUSPECTS.items():
        for hote in hotes:
            for _ in range(NB_LEURRE_SUSPECT):
                ts = DEBUT + timedelta(seconds=rng_sosies.randint(0, DUREE_S))
                ajouter(ts, hote, ip, domaine, port, rng_sosies.randint(200, 60_000))

    # --- Victime A : beaconing statique --------------------------------------
    # Intervalle de ~7 min (et non ~1 min) : le beacon ne doit pas dominer le
    # volume du dataset, sinon l'exercice 3 (plage d'IP rare + volume) devient
    # trivial — l'IP du C2 serait repérable au seul tri par volume.
    domaine_a, ip_a, port_a = C2_A
    t = DEBUT + timedelta(seconds=10)
    while t <= FIN:
        jitter = rng.randint(-5, 5)
        ajouter(t + timedelta(seconds=jitter), VICTIME_A, ip_a, domaine_a, port_a, 512)
        t += timedelta(seconds=420)

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


def generer_lignes_grand(rng: random.Random) -> list[dict]:
    """Grand réseau : beaucoup d'hôtes légitimes + une victime fast-flux.

    Sur ce réseau, compter les IP de destination distinctes (exercice 2) ne
    suffit plus : les hôtes légitimes en contactent autant, voire plus, que
    l'implant. Ce qui distingue la victime, c'est que toutes ses destinations
    sont « rares » (contactées par une seule source).
    """
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

    # --- Hôtes légitimes -----------------------------------------------------
    # Jitter de la télémétrie : flux dédié pour ne changer que les timestamps.
    rng_jitter_tel = random.Random(GRAINE_GRAND + 2000)
    for i in range(1, NB_HOTES_GRAND + 1):
        hote = f"10.0.0.{i}"
        # Navigation dense sur des IP de CDN partagées : chaque hôte en touche
        # plusieurs centaines, ce qui noie le signal « nombre de destinations ».
        nb_cdn = rng.randint(200, 600)
        for ip, domaine in rng.sample(CDN_POOL, nb_cdn):
            ts = DEBUT + timedelta(seconds=rng.randint(0, DUREE_S))
            ajouter(ts, hote, ip, domaine, 443, rng.randint(200, 60_000))
        # Longue traîne : quelques destinations obscures, vues par ce seul hôte.
        for _ in range(rng.randint(0, 10)):
            ip = f"185.220.{rng.randint(0, 255)}.{rng.randint(1, 254)}"
            ts = DEBUT + timedelta(seconds=rng.randint(0, DUREE_S))
            ajouter(ts, hote, ip, f"obscur-{ip.replace('.', '-')}.example", 443, rng.randint(100, 20_000))
        # Télémétrie périodique : un faux positif qui trompe l'exercice 1.
        # Même jitter (±5 s) que les mises à jour du petit réseau.
        t = DEBUT + timedelta(seconds=rng.randint(0, 900))
        while t <= FIN:
            ajouter(t + timedelta(seconds=rng_jitter_tel.randint(-5, 5)), hote,
                    TELEMETRIE_IP, TELEMETRIE_DOMAINE, 443, rng.randint(500, 2_000))
            t += timedelta(seconds=900)

    # --- Victime fast-flux : des IP rares qui tournent -----------------------
    t = DEBUT + timedelta(seconds=20)
    for ip, domaine in zip(IP_RARES_GRAND, DOMAINES_GRAND):
        ajouter(t, VICTIME_GRAND, ip, domaine, 443, 256)
        t += timedelta(seconds=90)

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


def resumer_grand(lignes: list[dict]) -> None:
    print(f"{len(lignes)} connexions générées (grand réseau).")
    sources_par_ip: dict[str, set[str]] = {}
    for l in lignes:
        sources_par_ip.setdefault(l["dst_ip"], set()).add(l["src_ip"])
    ip_rares = [ip for ip, srcs in sources_par_ip.items() if len(srcs) == 1]
    print(f"{len(ip_rares)} IP de destination « rares » (une seule source).")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", default=None, help="chemin du petit CSV (défaut : logs_reseau.csv)")
    p.add_argument("--out-grand", default=None, help="chemin du grand CSV (défaut : logs_reseau_grand.csv)")
    args = p.parse_args()

    base = Path(__file__).parent
    sortie = Path(args.out) if args.out else base / "logs_reseau.csv"
    sortie_grand = Path(args.out_grand) if args.out_grand else base / "logs_reseau_grand.csv"

    rng = random.Random(GRAINE)
    lignes = generer_lignes(rng)
    ecrire_csv(lignes, sortie)
    print(f"Écrit dans {sortie}")
    resumer(lignes)

    rng_grand = random.Random(GRAINE_GRAND)
    lignes_grand = generer_lignes_grand(rng_grand)
    ecrire_csv(lignes_grand, sortie_grand)
    print(f"Écrit dans {sortie_grand}")
    resumer_grand(lignes_grand)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
