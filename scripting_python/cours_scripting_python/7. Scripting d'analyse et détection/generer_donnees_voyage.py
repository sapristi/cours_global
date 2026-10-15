#!/usr/bin/env python3
"""Génère les trois jeux de données du TP « voyage impossible ».

Le TP demande de détecter les **déplacements impossibles** (> 900 km/h) dans des
connexions utilisateur géolocalisées, puis d'éliminer les faux positifs.

Trois fichiers sont produits :

1. `connexions.csv` — journal **minimal** des connexions : `timestamp`,
   `username`, `ip`. Ni géolocalisation ni information sur les VPN : ces
   colonnes se **reconstruisent** en joignant les deux autres fichiers (comme
   une vraie base GeoIP).
2. `ip_geo.csv` — mini-base GeoIP : `ip`, `latitude`, `longitude`, `city`,
   `country`. Associe chaque IP à sa position géographique.
3. `vpn_ips.csv` — liste d'IP de **sortie VPN/datacenter** connues (le *flag*).

Le dataset injecte volontairement plusieurs classes d'événements :

- **Utilisateurs légitimes** (résidentiels) : se connectent toujours depuis le
  même lieu, aucune alerte.
- **Télétravailleurs derrière un VPN** (faux positif n°1) : un utilisateur
  « saute » de sa ville vers un nœud de sortie VPN dans un autre pays en
  quelques minutes. Ces IP sont **listées** dans `vpn_ips.csv`.
- **Employés d'une entreprise** (faux positif n°2) : un **même IP de sortie**
  d'entreprise (proxy/NAT) est partagé par de nombreux utilisateurs, et sa
  géolocalisation (Paris) est loin du domicile des employés. Cet IP n'est dans
  **aucune** liste : il se détecte par *heuristique* (un IP vu par beaucoup
  d'utilisateurs = infrastructure partagée).
- **Un compte compromis** (`alice.dupont`, vrai positif) : un attaquant se
  connecte depuis New York 20 minutes après une connexion légitime à Paris.

Les deux méthodes de filtrage sont **complémentaires** :
- le VPN mono-utilisateur n'est pas « partagé » → seule la **liste** l'attrape ;
- l'IP d'entreprise n'est dans aucune liste → seule l'**heuristique** l'attrape.

Les adresses IP utilisées appartiennent aux plages **réservées à la
documentation** (RFC 5737 : 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24) :
aucune IP réelle n'est visée.

Le générateur est **déterministe** (graine fixe) : relancer produit exactement
les mêmes fichiers.

Usage :
    python3 generer_donnees_voyage.py            # écrit les 3 CSV dans ce dossier
    python3 generer_donnees_voyage.py --out-dir /tmp/tp

Cadre légal : données **entièrement simulées**, aucune cible réelle.
Art. 323-1 Code pénal : accès frauduleux = délit, même « juste pour voir ».
"""

import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

GRAINE = 42

# Seuil de « déplacement impossible » : au-delà, un humain ne peut pas voyager.
SEUIL_KMH = 900

# --- Géographie (lat, lon) ----------------------------------------------------
VILLES = {
    "Paris": (48.8566, 2.3522),
    "Lyon": (45.7640, 4.8357),
    "Marseille": (43.2965, 5.3698),
    "Toulouse": (43.6047, 1.4442),
    "Bordeaux": (44.8378, -0.5792),
    "Lille": (50.6292, 3.0573),
    "Nantes": (47.2184, -1.5536),
    "Strasbourg": (48.5734, 7.7521),
    "Rennes": (48.1173, -1.6778),
    "Nice": (43.7102, 7.2620),
    "Grenoble": (45.1885, 5.7245),
    "Dijon": (47.3220, 5.0415),
}

VILLES_VPN = {
    "Frankfurt": (50.1109, 8.6821),
    "Amsterdam": (52.3676, 4.9041),
    "London": (51.5074, -0.1278),
    "Zuerich": (47.3769, 8.5417),
}

VILLES_AUTRES = {
    "New York": (40.7128, -74.0060),
}

PAYS = {
    "Paris": "France", "Lyon": "France", "Marseille": "France",
    "Toulouse": "France", "Bordeaux": "France", "Lille": "France",
    "Nantes": "France", "Strasbourg": "France", "Rennes": "France",
    "Nice": "France", "Grenoble": "France", "Dijon": "France",
    "Frankfurt": "Allemagne", "Amsterdam": "Pays-Bas",
    "London": "Royaume-Uni", "Zuerich": "Suisse",
    "New York": "États-Unis",
}

# --- Plages d'IP réservées à la documentation (RFC 5737) ----------------------
RESID_PREFIX = "192.0.2"     # utilisateurs résidentiels + IP de l'attaquant
VPN_PREFIX = "198.51.100"    # nœuds de sortie VPN
ENTREPRISE_IP = "203.0.113.10"  # proxy/NAT de sortie de l'entreprise (partagé)


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    """Distance du grand cercle (km) entre deux points (loi de haversine)."""
    import math
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


# --- Utilisateurs -------------------------------------------------------------
UTILISATEURS_LEGITIMES = [
    ("jean.durand", "Paris"), ("marie.martin", "Lyon"),
    ("pierre.bernard", "Marseille"), ("luc.petit", "Toulouse"),
    ("claire.robert", "Bordeaux"), ("thomas.richard", "Lille"),
    ("nicolas.dubois", "Nantes"), ("julie.moreau", "Strasbourg"),
    ("antoine.laurent", "Rennes"), ("manon.simon", "Nice"),
    ("marc.michel", "Grenoble"), ("camille.lefebvre", "Dijon"),
    ("david.garcia", "Paris"), ("celine.fournier", "Lyon"),
    ("olivier.girard", "Marseille"), ("emma.lambert", "Toulouse"),
    ("eric.rousseau", "Bordeaux"), ("chloe.vincent", "Lille"),
    ("paul.muller", "Nantes"), ("lea.faure", "Strasbourg"),
    ("vincent.andre", "Rennes"), ("sarah.mercier", "Nice"),
    ("mathieu.carre", "Grenoble"), ("elise.guerin", "Dijon"),
    ("francois.boyer", "Paris"), ("lucie.garnier", "Lyon"),
    ("julien.chevalier", "Marseille"), ("anais.francois", "Toulouse"),
    ("romain.leger", "Bordeaux"), ("elsa.renard", "Lille"),
]

# (utilisateur, ville de domicile, ville du nœud VPN)
UTILISATEURS_VPN = [
    ("remi.giraud", "Lyon", "Frankfurt"),
    ("sophie.dumont", "Strasbourg", "Amsterdam"),
    ("thomas.olivier", "Nice", "London"),
    ("emma.payet", "Bordeaux", "London"),
    ("lucas.nguyen", "Lille", "Frankfurt"),
]

# (utilisateur, ville de domicile) — tous sortent par ENTREPRISE_IP (Paris).
UTILISATEURS_ENTREPRISE = [
    ("sophie.martin", "Lyon"), ("olivier.richard", "Marseille"),
    ("camille.petit", "Toulouse"), ("vincent.dubois", "Bordeaux"),
    ("julie.lacroix", "Strasbourg"), ("mathieu.blanc", "Nantes"),
    ("chloe.guerin", "Rennes"), ("david.renard", "Nice"),
    ("celine.legrand", "Grenoble"), ("nicolas.herve", "Dijon"),
    ("laura.bonnet", "Lyon"), ("antoine.rousseau", "Marseille"),
]

COMPROMIS = "alice.dupont"
COMPROMIS_VILLE = "Paris"        # connexions légitimes
COMPROMIS_ATTAQUE = "New York"   # connexion de l'attaquant

DEBUT = datetime(2026, 10, 7, 0, 0, 0)
NB_JOURS = 7


def ts(jour: int, heure: int, minute: int) -> datetime:
    """Instant du `jour`-ième jour (0-indexé) à `heure`:`minute`."""
    return DEBUT + timedelta(days=jour, hours=heure, minutes=minute)


def horodatage(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def generer() -> tuple[list[dict], dict[str, dict]]:
    """Retourne (événements de connexion, géolocalisation par IP)."""
    connexions: list[dict] = []
    geo: dict[str, dict] = {}

    rng = random.Random(GRAINE)
    compteur_ip = {"resid": 1, "vpn": 1}

    def ip_residentiel() -> str:
        ip = f"{RESID_PREFIX}.{compteur_ip['resid']}"
        compteur_ip["resid"] += 1
        return ip

    def ip_vpn() -> str:
        ip = f"{VPN_PREFIX}.{compteur_ip['vpn']}"
        compteur_ip["vpn"] += 1
        return ip

    def enregistrer_geo(ip: str, ville: str) -> None:
        lat, lon = VILLES.get(ville) or VILLES_VPN.get(ville) or VILLES_AUTRES[ville]
        geo[ip] = {
            "ip": ip, "latitude": lat, "longitude": lon,
            "city": ville, "country": PAYS[ville],
        }

    # --- Utilisateurs légitimes (toujours le même IP) ------------------------
    for nom, ville in UTILISATEURS_LEGITIMES:
        ip = ip_residentiel()
        enregistrer_geo(ip, ville)
        for jour in range(NB_JOURS):
            for heure in (8, 13, 19):
                jitter = rng.randint(0, 25)
                connexions.append({
                    "timestamp": horodatage(ts(jour, heure, jitter)),
                    "username": nom, "ip": ip,
                })

    # --- Télétravailleurs VPN (domicile -> VPN, faux positif liste) ----------
    for nom, ville, ville_vpn in UTILISATEURS_VPN:
        ip_dom = ip_residentiel()
        ip_sortie = ip_vpn()
        enregistrer_geo(ip_dom, ville)
        enregistrer_geo(ip_sortie, ville_vpn)
        for jour in range(NB_JOURS):
            # 09:00 domicile -> 09:10 VPN (10 min) : saut apparent.
            connexions.append({"timestamp": horodatage(ts(jour, 9, 0)),
                               "username": nom, "ip": ip_dom})
            connexions.append({"timestamp": horodatage(ts(jour, 9, 10)),
                               "username": nom, "ip": ip_sortie})
            connexions.append({"timestamp": horodatage(ts(jour, 20, 0)),
                               "username": nom, "ip": ip_dom})

    # --- Employés (domicile -> proxy d'entreprise, faux positif heuristique) --
    enregistrer_geo(ENTREPRISE_IP, "Paris")
    for nom, ville in UTILISATEURS_ENTREPRISE:
        ip_dom = ip_residentiel()
        enregistrer_geo(ip_dom, ville)
        for jour in range(NB_JOURS):
            # 08:00 domicile -> 08:15 proxy (15 min) : saut apparent.
            connexions.append({"timestamp": horodatage(ts(jour, 8, 0)),
                               "username": nom, "ip": ip_dom})
            connexions.append({"timestamp": horodatage(ts(jour, 8, 15)),
                               "username": nom, "ip": ENTREPRISE_IP})
            connexions.append({"timestamp": horodatage(ts(jour, 18, 0)),
                               "username": nom, "ip": ip_dom})

    # --- Compte compromis (Paris -> New York en 20 min, vrai positif) ---------
    ip_paris = ip_residentiel()
    ip_newyork = ip_residentiel()
    enregistrer_geo(ip_paris, COMPROMIS_VILLE)
    enregistrer_geo(ip_newyork, COMPROMIS_ATTAQUE)
    for jour in range(NB_JOURS):
        connexions.append({"timestamp": horodatage(ts(jour, 8, 0)),
                           "username": COMPROMIS, "ip": ip_paris})
        connexions.append({"timestamp": horodatage(ts(jour, 18, 0)),
                           "username": COMPROMIS, "ip": ip_paris})
    # L'attaque : jour 3, l'attaquant se connecte depuis New York à 08:20,
    # 20 minutes après la connexion légitime de Paris à 08:00.
    connexions.append({"timestamp": horodatage(ts(3, 8, 20)),
                       "username": COMPROMIS, "ip": ip_newyork})

    connexions.sort(key=lambda c: (c["username"], c["timestamp"]))
    return connexions, geo


def ecrire_csv(lignes: list[dict], chemin: Path, colonnes: list[str]) -> None:
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(",".join(colonnes) + "\n")
        for l in lignes:
            f.write(",".join(str(l[c]) for c in colonnes) + "\n")


def resumer(connexions: list[dict], geo: dict[str, dict]) -> None:
    vpn_ips = {ip for ip, g in geo.items() if g["ip"].startswith(VPN_PREFIX)}
    par_utilisateur: dict[str, int] = {}
    for c in connexions:
        par_utilisateur[c["username"]] = par_utilisateur.get(c["username"], 0) + 1

    print(f"{len(connexions)} connexions, {len(par_utilisateur)} utilisateurs, "
          f"{len(geo)} IP géolocalisées, {len(vpn_ips)} IP VPN.")
    # Contrôle de cohérence : chaque IP de connexion a bien une géoloc.
    ips_connus = set(geo)
    ips_inconnus = {c["ip"] for c in connexions} - ips_connus
    assert not ips_inconnus, f"IP sans géoloc : {ips_inconnus}"
    # Contrôle : usernames uniques.
    assert len({u for u, _ in UTILISATEURS_LEGITIMES}) == len(UTILISATEURS_LEGITIMES)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-dir", default=None,
                   help="dossier de sortie (défaut : à côté du script)")
    args = p.parse_args()

    sortie = Path(args.out_dir) if args.out_dir else Path(__file__).parent
    sortie.mkdir(parents=True, exist_ok=True)

    connexions, geo = generer()

    ecrire_csv(connexions, sortie / "connexions.csv",
               ["timestamp", "username", "ip"])
    ip_geo_triee = sorted(geo.values(), key=lambda g: g["ip"])
    ecrire_csv(ip_geo_triee, sortie / "ip_geo.csv",
               ["ip", "latitude", "longitude", "city", "country"])
    vpn_ips_triees = sorted(ip for ip, g in geo.items() if g["ip"].startswith(VPN_PREFIX))
    ecrire_csv([{"ip": ip} for ip in vpn_ips_triees], sortie / "vpn_ips.csv", ["ip"])

    print(f"Écrit dans {sortie}")
    resumer(connexions, geo)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
