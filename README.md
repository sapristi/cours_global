# cours_global

Supports de cours:

- **[`machine learning`](machine_learning/Readme.md)** ( perceptron,
  réseaux multi-couches, RBF, SVM, évaluation de modèles)
- **[`scripting python pour la cybersécurité`](scripting_python/Readme.md)**
  (bases de Python, réseau, analyse et détection avec `pandas`)

Chaque cours contient les cours rédigés en markdown et les notebooks de TD.
Le point d'entrée de chaque cours (contexte, objectifs, plan, conventions) est
son `Readme.md`.

## Lire les cours (Obsidian)

Les cours sont écrits pour [Obsidian](https://obsidian.md):

1. cloner le dépôt ;
2. dans Obsidian, *Ouvrir un dossier comme coffre* → choisir la **racine du
   dépôt**

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
TODO: mentionner que lorsqu'un notebook est sauvegardé, une nouvelle version 
déployée n'apparaît pas.


