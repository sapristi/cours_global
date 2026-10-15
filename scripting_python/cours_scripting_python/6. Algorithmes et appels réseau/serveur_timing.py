#!/usr/bin/env python3
"""Serveur vulnérable à une attaque temporelle (LABO ISOLÉ UNIQUEMENT).

Compare un `guess` au `secret` caractère par caractère, en dormant
`sleep + jitter` à chaque caractère correct. Le temps de réponse fuit
donc la longueur du préfixe correct — c'est ce qu'on fait découvrir aux
élèves en mesurant les temps.

Deux endpoints :
    GET /check   -> comportement « fuyant » : délai proportionnel au
                    préfixe correct, tel quel.
    GET /check2  -> identique, mais ajoute en plus un délai aléatoire
                    `betavariate(0.5, 0.5) * sleep * 2` sur *toutes* les
                    requêtes : le signal est noyé dans un bruit plus large.

Usage :
    python3 serveur_timing.py --secret "a1b2c3" --sleep 0.05 --jitter 0.02

Réponse :
    200 "ACCES AUTORISE" si guess == secret, 403 "ACCES REFUSE" sinon.

Cadre légal : labo isolé uniquement, autorisation écrite hors labo.
Art. 323-1 Code pénal : accès frauduleux = délit, même « juste pour voir ».
"""
import argparse
import random
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"


def verifier(guess: str, secret: str, sleep: float, jitter: float,
             bruit_beta: bool = False) -> bool:
    """Compare guess au secret et dort à chaque caractère correct.

    Le nombre de `sleep` effectués vaut la longueur du préfixe commun
    (bornée par la longueur du secret). Le temps passé ici est donc
    proportionnel au nombre de caractères corrects.

    Si `bruit_beta` est vrai, on ajoute d'abord un délai aléatoire
    `betavariate(0.5, 0.5) * sleep * 2` indépendant du guess : la fuite
    reste présente mais noyée dans un bruit large (endpoint /check2).
    """
    if bruit_beta:
        time.sleep(random.betavariate(0.5, 0.5) * sleep * 2)
    time.sleep(random.uniform(0, jitter))
    for i, caractere in enumerate(secret):
        if i >= len(guess) or guess[i] != caractere:
            return False
        time.sleep(sleep + random.uniform(0, jitter))
    return len(guess) == len(secret)


class Gestionnaire(BaseHTTPRequestHandler):
    """Répond à GET /check et /check2 (attributs de classe configurés par main())."""

    secret: str = ""
    sleep: float = 0.05
    jitter: float = 0.02

    def do_GET(self) -> None:
        chemin = urlparse(self.path)
        if chemin.path == "/check":
            bruit_beta = False
        elif chemin.path == "/check2":
            bruit_beta = True
        else:
            self.send_error(404)
            return

        guess = parse_qs(chemin.query).get("guess", [""])[0]

        debut = time.perf_counter()
        autorise = verifier(guess, self.secret, self.sleep, self.jitter, bruit_beta)
        duree = time.perf_counter() - debut

        code = 200 if autorise else 403
        corps = "ACCES AUTORISE\n" if autorise else "ACCES REFUSE\n"
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        try:
            self.wfile.write(corps.encode())
        except OSError:
            pass

        print(f"route={chemin.path} guess={guess!r} code={code} "
              f"duree={duree * 1000:.1f}ms")

    def log_message(self, format: str, *args) -> None:
        pass  # on logue déjà le détail dans do_GET


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--secret", default=None,
                   help="secret à protéger (0-9a-z) ; aléatoire si omis")
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--sleep", type=float, default=0.05,
                   help="sommeil (s) par caractère correct")
    p.add_argument("--jitter", type=float, default=0.02,
                   help="bruit max (s) ajouté à chaque caractère correct")
    args = p.parse_args()

    secret = args.secret or "".join(random.choices(ALPHABET, k=8))
    hors_alphabet = [c for c in secret if c not in ALPHABET]
    if hors_alphabet:
        sys.exit(f"secret : caractères hors alphabet {''.join(hors_alphabet)!r} "
                 f"(alphabet = {ALPHABET})")

    Gestionnaire.secret = secret
    Gestionnaire.sleep = args.sleep
    Gestionnaire.jitter = args.jitter

    serveur = ThreadingHTTPServer((args.host, args.port), Gestionnaire)
    print(f"Écoute sur http://{args.host}:{args.port} "
          f"(secret de {len(secret)} caractères, caché)")
    print(f"sleep={args.sleep * 1000:.1f}ms jitter={args.jitter * 1000:.1f}ms "
          f"(Ctrl+C pour arrêter)")
    print("/check  : délai proportionnel au préfixe correct")
    print("/check2 : idem + délai aléatoire betavariate(0.5,0.5)*sleep*2 "
          "sur chaque requête")
    try:
        serveur.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt demandé.")
    finally:
        serveur.server_close()


if __name__ == "__main__":
    main()
