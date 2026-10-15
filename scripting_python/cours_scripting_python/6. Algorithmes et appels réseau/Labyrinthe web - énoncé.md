# TD — Labyrinthe web (spidering)

> [!abstract] Objectif
> Un serveur local sert des pages reliées entre elles ; **sept flags** sont
> cachés dans le graphe. Vous écrivez un *spider* (robot d'exploration) qui
> parcourt les pages en **BFS** ou **DFS** jusqu'à les trouver **tous**. C'est
> la technique du *spidering*, phase de **reconnaissance** : cartographier un
> site pour y repérer des cibles intéressantes.
>
> Chaque flag met en œuvre une **technique de spidering** particulière (parsing
> HTML, liens relatifs, JSON, 404, redirection, grand graphe, en-têtes). À vous
> de les identifier.

> [!danger] Cadre légal — labo isolé uniquement
> La cible est uniquement le serveur de TP (`http://127.0.0.1:8000`), lancé par
> le prof. Pas de spidering sur un site réel sans **autorisation écrite** :
> marteler le web d'autrui sature son serveur et tombe sous l'**art. 323-1
> Code pénal** (accès frauduleux = délit), même « juste pour voir ».

## Contexte et pièges

Le graphe contient volontairement des obstacles que votre spider devra gérer :

**Les flags** sont des chaînes de la forme `FLAG{1}` à `FLAG{7}`, présentes dans
le corps de pages précises **ou dans un en-tête de réponse**. Votre spider doit
les **collecter tous** puis les afficher. Certains se trouvent dans des pages
HTML classiques, d'autres dans un payload JSON, une page `404`, derrière une
redirection, au bout d'un grand graphe généré ou dans un header HTTP.

## Serveur

Le serveur (Flask) est lancé par le prof — les flags restent donc cachés dans le
code serveur. Vous ne touchez qu'au client :


https://scripting_python_td2.mmill.eu/


Vérifiez l'accès :

```python
import requests

r = requests.get("https://scripting_python_td2.mmill.eu//", timeout=5)
print(r.status_code, r.text)
```

## Étape 1 — Extraire les liens d'une page

> [!info] Documentation
> - `re.findall` : https://docs.python.org/3/library/re.html#re.findall
> - `urllib.parse.urljoin` : https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urljoin

> [!todo] Fonctions d'extraction
> Écrire deux fonctions (type hints + docstring) :
>
> ```python
> def extraire_liens(html: str) -> list[str]:
>     """Renvoie les href des balises <a href="..."> du HTML."""
>     # TODO: Votre solution
>
>
> def liens_absolus(base: str, liens: list[str]) -> list[str]:
>     """Résout les liens relatifs en URL absolues via urljoin."""
>     # TODO: Votre solution
> ```
>
> - Les liens sont de la forme `<a href="...">`. Utiliser une expression
>   régulière (ex. `r'href="([^"]+)"'`). Ou la librairie beautiful-soup
> - Un lien peut être relatif (`/salle-b`) ou absolu (`http://...`) : `urljoin`
>   gère les deux. **Attention** aux liens relatifs *sans* slash initial
>   (`salle-2`) : `urljoin` les résout correctement, une concaténation naïve non.
>   Certains flags ne sont accessibles **que** de cette façon.

## Étape 3 — BFS avec ensemble des pages visitées

> [!info] Documentation
> - `collections.deque` : https://docs.python.org/3/library/collections.html#collections.deque

> [!todo] Parcours en largeur
> Écrire une fonction qui explore le graphe en largeur :
>
> ```python
> from collections import deque
>
>
> def crawler(depart: str) -> None:
>     """Parcourt le site en BFS, sans repasser par une page déjà vue."""
>     visites: set[str] = set()
>     file = deque([depart])
>     # TODO: Votre solution
> ```
>
> - Tant que la file n'est pas vide : dépiler une URL, la marquer visitée,
>   récupérer son HTML, extraire les liens, empiler ceux pas encore vus.
> - Tester sur `/`. Sans limite, le script ne s'arrête **toujours pas** (la
>   pagination `/archives` génère des pages à l'infini) — mais au moins il ne
>   tourne plus en rond. On règle ça à l'étape 5.

## Bonus

> [!todo] Aller plus loin
> - **Spider DFS** : réécrire le parcours avec une pile (`list`, `append`/`pop`)
>   au lieu de la file. Variante récursive possible (attention à la profondeur de
>   récursion sur le grand graphe). Comparer l'ordre d'exploration et le nombre
>   de pages visitées à celui du BFS.
> - **Politesse** : ajouter un petit délai (`time.sleep`) entre les requêtes.
>   C'est une vraie bonne pratique du spidering : ne pas saturer le serveur.
> - **Graphe** : compter les pages, les liens, détecter les pages « cul-de-sac »
>   (aucun lien sortant). Déduire la structure du site.
