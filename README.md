# cours_global

Supports de cours (en français) :

- **`machine_learning/`** : machine learning (4e année post-bac) — perceptron,
  réseaux multi-couches, RBF, SVM, évaluation de modèles ;
- **`scripting_python/`** : scripting Python pour la cybersécurité (3e année) —
  bases de Python, réseau (`socket`, `requests`), analyse et détection avec
  `pandas`.

Chaque cours contient les cours rédigés en markdown et les notebooks de TD.
Le point d'entrée de chaque cours (contexte, objectifs, plan, conventions) est
son `Entrypoint.md`.

## TD en ligne (JupyterLite)

👉 **<https://sapristi.github.io/cours_global/>**

Les notebooks de TD s'ouvrent directement dans le navigateur, sans rien
installer (JupyterLite : Python tourne dans le navigateur via Pyodide). Ils
sont rangés par cours (`machine_learning/`, `scripting_python/`).

- La version en ligne est un **énoncé à trous** : les solutions sont retirées
  au déploiement.
- Le travail est enregistré **dans le navigateur** (stockage local) : il reste
  disponible sur la même machine et le même navigateur, mais n'est pas
  synchronisé ailleurs. Pour le garder, le télécharger (*File → Download*).
- La première cellule de chaque notebook contient un bouton « Clear notebook »
  pour repartir de l'énoncé d'origine.

Le site est reconstruit et redéployé automatiquement à chaque push sur `main`
(GitHub Actions → GitHub Pages).

## Lire les cours (Obsidian)

Les cours sont écrits pour [Obsidian](https://obsidian.md) (liens `[[...]]`,
callouts, tableaux Bases) :

1. cloner le dépôt ;
2. dans Obsidian, *Ouvrir un dossier comme coffre* → choisir la **racine du
   dépôt** (un seul coffre pour tous les cours, configuration incluse dans
   `.obsidian/`) ;
3. commencer par `machine_learning/Entrypoint.md` ou
   `scripting_python/Entrypoint.md`.

Les fichiers restent lisibles dans n'importe quel éditeur markdown (ou sur
GitHub), au rendu des liens Obsidian près.

## Travailler sur le dépôt

Prérequis : [uv](https://docs.astral.sh/uv/).

```bash
uv sync                                  # dépendances
uv run scripts/check_notebooks.py        # exécute tous les notebooks corrigés
uv run scripts/check_snippets.py         # vérifie la syntaxe des snippets Python des .md
uv run scripts/preview_lite.py           # aperçu local du site JupyterLite (http://127.0.0.1:8000/lab)
```

Les notebooks du dépôt sont les **corrigés** (solutions incluses) ; les
solutions sont retirées par `scripts/collect_lite_content.py` au build. Les
conventions détaillées (format des exercices, structure, devoirs) sont dans
[`AGENTS.md`](AGENTS.md).

Le dossier `devoirs/` est un sous-module vers un dépôt privé (sujets, corrigés
et notes des évaluations) : il n'est pas accessible publiquement.
