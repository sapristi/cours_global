# TD — Attaque temporelle

## Le coffre

Le serveur https://scripting_python_td1.mmill.eu/ protège un **secret** : une chaîne de 6 caractères, uniquement composés de `0-9` et de `a-z`. À chaque tentative, il répond poliment :

```text
ACCES REFUSE
```

Toujours la même réponse, quel que soit ce que vous proposez. Sauf que… certains refus semblent *plus longs* que d'autres. Comme si le serveur hésitait.

Votre mission : ouvrir le coffre.

Dans un second terminal (ou un shell Python), testez une requête :

```python
import requests

r = requests.get("https://scripting_python_td1.mmill.eu/check", params={"guess": "xxxxxx"})
print(r.status_code, r.text)
```

> [!todo] Prise en main
> 1. Quel est le **code de statut** quand le guess est faux ?
> 2. Que renvoie le serveur si vous oubliez le paramètre `guess` ? Et sur une autre route (`/` par exemple) ?

## Étape 1 — Force brute : le mur

Première idée, naturelle : essayer **toutes** les combinaisons possibles.

> [!todo] Écrire le brute-force
> Écrivez un script qui énumère toutes les chaînes de 6 caractères sur l'alphabet `0-9a-z`, les envoie une par une, et s'arrête dès qu'une réponse `200` arrive.

> [!note] L'alphabet
> ```python
> ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"   # 36 caractères
> ```

> [!todo] Faire le calcul
> 1. Combien de combinaisons de longueur 6 sur 36 caractères existe-t-il ? Combien de temps prendrait l'énumération complète ?
> 2. Conclusion : peut-on raisonnablement compter là-dessus ?

Ce mur, c'est le quotidien de l'attaquant : forcer brutalement est rarement viable… sauf s'il existe un moyen de réduire drastiquement l'espace de recherche. C'est exactement ce que ce TD va vous faire trouver.

## Étape 2 — Remarquez-vous quelque chose ?

Oublions la force brute un instant. Le serveur répond toujours la même chose, mais **met-il le même temps** ?

> [!note] Mesurer un temps en Python
> On utilise `time.perf_counter()` (résolution sub-milliseconde), pas `time.time()`.

> [!tip] Astuce ipython / jupyter : `%time` et `%%time`
> Dans un shell ipython ou un notebook, vous pouvez mesurer le temps d'exécution sans écrire le code `perf_counter` vous-même, grâce à deux *magic commands* d'IPython :
>
> - **`%time`** (une seule ligne) : mesure l'exécution d'une instruction, par ex. `%time temps_reponse("axxxxx")`.
> - **`%%time`** (toute une cellule) : se place en **première ligne** d'une cellule et mesure l'ensemble du code de cette cellule. On l'écrit avec **deux** `%` car il s'applique à un bloc (comme `%%timeit`), contrairement à `%time` qui ne prend qu'une seule expression.
>
> Dans les deux cas, le résultat est affiché directement sous la cellule, sans polluer votre code ni votre sortie. Attention : ces magies sont propres à IPython/Jupyter — elles ne fonctionnent **pas** dans un script `.py` lancé par `python3`. Pour un script, on garde `time.perf_counter()`.
>
> Doc : https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-time

```python
import requests
import time

URL = "http://127.0.0.1:8000/check"

def temps_reponse(guess: str) -> float:
    """Durée (secondes) d'un appel /check avec ce guess."""
    debut = time.perf_counter()
    requests.get(URL, params={"guess": guess})
    return time.perf_counter() - debut
```

> [!todo] Observer, sans a priori
> Mesurez `temps_reponse`, sur des chaînes avec différents préfixes (`axxxxx`, `bxxxx`, ...). Que remarquez-vous ?


## Étape 3 — Formuler l'hypothèse

> [!todo] Nommer le phénomène
> Écrivez en une phrase ce que vous venez de découvrir : à quoi correspond la durée de la réponse ?

Vous venez de mettre le doigt sur une **attaque temporelle** (*timing attack*) : une **fuite d'information par canal latéral** (*side-channel*). Le serveur ne vous dit rien… mais le *temps qu'il met à le dire* en dit long.

> [!info] Canal latéral
> Un side-channel, c'est une information qui fuit par un canal *autre* que la réponse elle-même : le temps, la consommation d'énergie, le rayonnement électromagnétique, le cache… Ici : le temps de réponse.

## Étape 4 — Ça existe dans la vraie vie

L'attaque temporelle n'est pas un exercice d'école. Quelques jalons :

| Année       | Affaire             | En deux mots                                                                                                                                                            |
| ----------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| années 1970 | **TENEX**           | Première attaque temporelle documentée : la vérification de mot de passe fuyait via le temps de *page fault*, caractère par caractère.                                  |
| 1996        | **Kocher**          | *« Timing Attacks on Implementations of Diffie-Hellman, RSA, DSS »* : mesurer le temps d'exécution pour extraire une clé privée. L'article fondateur des side-channels. |
| 2003        | **Boneh & Brumley** | Attaque temporelle **à distance** contre OpenSSL : une clé RSA 1024 bits extraite par le réseau, depuis une autre machine.                                              |
| 2013        | **Lucky Thirteen**  | Attaque temporelle sur le padding de TLS, démontrée en pratique sur des implémentations réelles.                                                                        |

Le principe est toujours le même que le nôtre : le temps de réponse dépend d'un secret, et cette dépendance suffit à le reconstruire.

## Étape 5 — L'attaque, caractère par caractère

Vous savez que le temps fuit quelque chose à propos de votre guess. Reste à l'exploiter.

> [!todo] Implémenter
> Écrivez une fonction `trouver_secret()` qui :
> - part d'un préfixe vide ;
> - à chaque étape, teste `préfixe + c` pour chaque `c` de l'alphabet ;
> - garde le candidat le plus lent ;
> - s'arrête dès qu'un guess renvoie `200`.


> [!todo] Un peu de maths
> Comparer le nombre d'essais nécessaires entre le brute-force classique et la méthode d'attaque temporelle.

## Étape 6 — Données bruitées


> [!todo] Attaquer `/check2`
> 1. Attaquez `https://scripting_python_td1.mmill.eu/check2` avec votre script (changez juste l'URL).
> 2. Que remarquez-vous ? Comment faire pour y remédier ?

# Annexe - fonctions utilitaires

- `time.perf_counter`: https://docs.python.org/3/library/time.html#time.perf_counter
- `statistics.median`: https://docs.python.org/3/library/statistics.html#statistics.median
- `itertools.product`: https://docs.python.org/3/library/itertools.html#itertools.product
