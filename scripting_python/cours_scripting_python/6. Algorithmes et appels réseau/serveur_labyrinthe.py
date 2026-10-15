#!/usr/bin/env python3
# /// script
# dependencies = [
#   "flask",
# ]
# ///
"""Serveur « labyrinthe web » — TP spidering (LABO ISOLÉ UNIQUEMENT).

Un site web local dont les pages sont reliées par des liens. Sept flags
(`FLAG{1}` à `FLAG{7}`) sont cachés ; chacun exige une technique de spidering
particulière pour être trouvé :

- FLAG{1} : parsing HTML classique (liens absolus) ;
- FLAG{2} : résolution de liens relatifs (`urljoin`) ;
- FLAG{3} : lecture d'un payload JSON (pas de <a href>) ;
- FLAG{4} : inspection du corps d'une page en erreur 404 ;
- FLAG{5} : suivi d'une redirection 302 ;
- FLAG{6} : traversée d'un grand graphe généré (200 nœuds, `graphe_labyrinthe.json`) ;
- FLAG{7} : lecture d'un en-tête HTTP (header `X-Flag`).

Le graphe contient en plus un leurre (faux flag) et des pièges : cycles,
pagination infinie, normalisation d'URL, boucle de redirection, routes lentes.

Usage (prof uniquement — les étudiants ne lancent pas le serveur) :
    uv run serveur_labyrinthe.py --port 8000
    # ou : pip install flask && python3 serveur_labyrinthe.py --port 8000

Cadre légal : labo isolé uniquement, autorisation écrite hors labo.
Art. 323-1 Code pénal : accès frauduleux = délit, même « juste pour voir ».
"""
import argparse
import json
import time
from pathlib import Path

from flask import Flask, Response, redirect, request

FLAG_1 = "FLAG{1}"
FLAG_2 = "FLAG{2}"
FLAG_3 = "FLAG{3}"
FLAG_4 = "FLAG{4}"
FLAG_5 = "FLAG{5}"
FLAG_6 = "FLAG{6}"
FLAG_7 = "FLAG{7}"

FLAG_LEURRE_MOT = "FLAG{ceci_est_un_leurre}"

DELAI_LENT_1 = 4.0
DELAI_LENT_2 = 3.0
HOST_DEFAUT = "127.0.0.1"
PORT_DEFAUT = 8000

CHEMIN_GRAPHE = Path(__file__).with_name("graphe_labyrinthe.json")


def charger_graphe(chemin: Path) -> tuple[dict[int, list[int]], int, int]:
    """Charge le graphe généré : (adjacence, nœud d'entrée, nœud du flag)."""
    donnees = json.loads(chemin.read_text(encoding="utf-8"))
    graphe = {int(n): [int(v) for v in voisins] for n, voisins in donnees["graphe"].items()}
    return graphe, int(donnees["entree"]), int(donnees["flag"])


def pages_generees(graphe: dict[int, list[int]], noeud_flag: int) -> dict[str, dict]:
    """Construit les pages `/gene/<n>` à partir du graphe chargé."""
    pages: dict[str, dict] = {}
    for n, voisins in graphe.items():
        pages[f"/gene/{n}"] = {
            "titre": f"Salle générée {n}",
            "liens": [f"/gene/{v}" for v in voisins],
        }
    pages[f"/gene/{noeud_flag}"]["texte"] = f"Bravo ! Flag : {FLAG_6}"
    return pages


GRAPHE, NOEUD_ENTREE, NOEUD_FLAG = charger_graphe(CHEMIN_GRAPHE)

# Graphe déclaratif : chemin -> page.
# Champs possibles : titre, texte, liens (list[str]), delai (float),
# redirect (str), status (int), content_type (str), corps (str brut),
# entetes (dict[str, str] ajoutés à la réponse).
PAGES: dict[str, dict] = {
    "/": {
        "titre": "Accueil du labyrinthe",
        "texte": "Bienvenue. Explorez les salles pour trouver les flags.",
        "liens": [
            # Flags et pièges « sûrs » (aucune exception) — explorés en premier :
            "/aile-nord", "/secteur/sud", "/api/status.json",
            "/salle-abandonnee", "/porte", "/vitrine", "/salle-a",
            "/miroir", "/normale", "/leurre",
            # Routes qui bloquent / font crasher un spider naïf — à la fin :
            "/archives", "/redir-a", "/lent",
        ],
    },
    # FLAG{1} — parsing HTML classique : chaîne de liens absolus.
    "/aile-nord": {"titre": "Aile nord", "liens": ["/aile-nord/salle-1"]},
    "/aile-nord/salle-1": {
        "titre": "Salle 1",
        "texte": f"Bravo ! Flag : {FLAG_1}",
        "liens": [],
    },
    # FLAG{2} — lien relatif sans slash initial : seul urljoin résout
    # « salle-2 » depuis /secteur/sud vers /secteur/salle-2. Une concaténation
    # naïve (base + lien) aboutirait à la mauvaise URL.
    "/secteur/sud": {"titre": "Couloir sud", "liens": ["salle-2"]},
    "/secteur/salle-2": {
        "titre": "Salle 2",
        "texte": f"Bravo ! Flag : {FLAG_2}",
        "liens": [],
    },
    # FLAG{3} — payload JSON : pas de balise <a href>, le flag est dans le
    # corps. Un spider qui ignore le contenu non-HTML ne le verra jamais.
    "/api/status.json": {
        "content_type": "application/json",
        "corps": f'{{"statut": "ok", "flag": "{FLAG_3}"}}\n',
    },
    # FLAG{4} — page en erreur 404 : le corps contient quand même le flag.
    # Un spider qui saute les status 4xx/5xx ne le trouvera jamais.
    "/salle-abandonnee": {
        "titre": "Salle abandonnée",
        "status": 404,
        "texte": f"Cette salle est condamnée, mais un flag traîne : {FLAG_4}",
        "liens": [],
    },
    # FLAG{5} — redirection 302 : le flag est sur la page d'arrivée. Il faut
    # suivre la redirection (ou travailler avec l'URL finale).
    "/porte": {"redirect": "/salle-fond"},
    "/salle-fond": {
        "titre": "Salle du fond",
        "texte": f"Bravo ! Flag : {FLAG_5}",
        "liens": [],
    },
    # FLAG{7} — en-tête HTTP : le flag n'est PAS dans le corps de la page mais
    # dans le header `X-Flag`. Un spider qui ne lit que `r.text` le rate.
    "/vitrine": {
        "titre": "Vitrine",
        "texte": "Rien à voir dans le corps de cette page…",
        "entetes": {"X-Flag": FLAG_7},
        "liens": [],
    },
    # Leurre : un faux flag pour apprendre à ne pas s'arrêter trop tôt.
    "/leurre": {
        "titre": "Leurre",
        "texte": f"Indice trompeur : {FLAG_LEURRE_MOT} (ce n'est pas un vrai flag).",
        "liens": ["/salle-a"],
    },
    # Pièges (aucun flag) : robustesse du spider.
    # Cycle : /salle-a <-> /salle-b — oblige à mémoriser les pages visitées.
    "/salle-a": {"titre": "Salle A", "liens": ["/salle-b"]},
    "/salle-b": {"titre": "Salle B", "liens": ["/salle-a", "/impasse"]},
    "/impasse": {"titre": "Impasse", "texte": "Rien ici.", "liens": []},
    # Boucle de normalisation : /miroir <-> /miroir/ (trailing slash).
    "/miroir": {"titre": "Miroir", "liens": ["/miroir/"]},
    "/miroir/": {"titre": "Miroir (slash)", "liens": ["/miroir"]},
    # Même page atteignable avec un paramètre : normalisation des query params.
    "/normale": {"titre": "Page normale", "liens": ["/normale?utm=1", "/salle-a"]},
    # Boucle de redirection 302 : à gérer via r.history / URL finale.
    "/redir-a": {"redirect": "/redir-b"},
    "/redir-b": {"redirect": "/redir-a"},
    # Zone lente : force un timeout côté client.
    "/lent": {"titre": "Zone lente", "liens": ["/lent-1", "/lent-2"]},
    "/lent-1": {"titre": "Lent 1", "delai": DELAI_LENT_1, "liens": []},
    "/lent-2": {"titre": "Lent 2", "delai": DELAI_LENT_2, "liens": []},
}

# FLAG{6} — grand graphe généré : 200 nœuds chargés depuis graphe_labyrinthe.json.
PAGES.update(pages_generees(GRAPHE, NOEUD_FLAG))
# Inséré juste avant /archives : FLAG{6} reste atteignable sans qu'un spider
# naïf ne se fasse d'abord crasher par la pagination infinie ou la redirection.
PAGES["/"]["liens"].insert(
    PAGES["/"]["liens"].index("/archives"), f"/gene/{NOEUD_ENTREE}"
)

app = Flask(__name__)
app.url_map.strict_slashes = False


def construire_html(titre: str, texte: str, liens: list[str]) -> str:
    """Construit une page HTML minimale listant les liens."""
    items = "".join(f'<li><a href="{lien}">{lien}</a></li>' for lien in liens)
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{titre}</title></head><body>"
        f"<h1>{titre}</h1><p>{texte}</p><ul>{items}</ul>"
        "</body></html>"
    )


def rendre(cle: str) -> Response:
    """Renvoie la page associée à `cle`, ou une 404 générique."""
    page = PAGES.get(cle)
    if page is None:
        corps = construire_html("404", "Page inconnue.", [])
        return Response(corps, status=404, mimetype="text/html")

    if "delai" in page:
        time.sleep(page["delai"])
    if "redirect" in page:
        return redirect(page["redirect"], code=302)

    corps = page.get("corps") or construire_html(
        page["titre"], page.get("texte", ""), page.get("liens", [])
    )
    reponse = Response(
        corps,
        status=page.get("status", 200),
        mimetype=page.get("content_type", "text/html"),
    )
    for nom, valeur in page.get("entetes", {}).items():
        reponse.headers[nom] = valeur
    return reponse


def rendre_archives(n: int) -> Response:
    """Pagination infinie : chaque page pointe vers la suivante (?page=n+1)."""
    liens = [f"/archives?page={n + 1}", "/"]
    corps = construire_html(
        f"Archives — page {n}",
        f"Vous êtes sur la page {n} des archives.",
        liens,
    )
    return Response(corps, status=200, mimetype="text/html")


@app.before_request
def journaliser() -> None:
    print(f"{request.method} {request.full_path}", flush=True)


@app.route("/")
def accueil() -> Response:
    return rendre("/")


@app.route("/archives")
def archives() -> Response:
    brut: str = request.args.get("page", "1")
    try:
        n: int = int(brut)
    except ValueError:
        n = 1
    return rendre_archives(n)


@app.route("/<path:chemin>")
def page(chemin: str) -> Response:
    return rendre("/" + chemin)


def main() -> None:
    p = argparse.ArgumentParser(description="Serveur labyrinthe web (TP spidering)")
    p.add_argument("--host", default=HOST_DEFAUT)
    p.add_argument("--port", type=int, default=PORT_DEFAUT)
    args = p.parse_args()
    print(f"Serveur labyrinthe sur http://{args.host}:{args.port} (Ctrl+C pour arrêter)")
    app.run(host=args.host, port=args.port, threaded=True)


if __name__ == "__main__":
    main()
