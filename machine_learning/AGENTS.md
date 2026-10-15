# AGENTS.md — machine_learning

Cours de machine learning (4e année). Vault Obsidian : `cours_ml/`.
Conventions générales (Obsidian, export, Python) : voir `AGENTS.md` à la racine.

## Standards de notation (notebooks)

On distingue soigneusement la **cible** (ce qu'il faut prédire) de la **sortie** (ce que le modèle prédit). Conventions alignées sur le cours :

| Concept | Minuscule (scalaire/vecteur) | Majuscule (matrice) |
|---|---|---|
| Entrée | `x` | `X` (un échantillon par ligne, forme (N, d)) |
| **Cible (target)** | `t` | `T` (cibles one-hot, notation mathématique) |
| **Sortie / prédiction** | `y` | `Y` (activations d'une couche, sortie du réseau) |
| Pré-activation | `z` | `Z` |
| Poids / biais | `w`, `b` | `W`, `b` |
| Activation | `a` | `A` |
| Coût / erreur rétropropagée | `E`, `δ` | — |
| Taux d'apprentissage | `r` (perceptron), `η` (multi-couche) | `lr` en code |

Règle clé : la **cible** se note toujours `t` (jamais `y`) ; `y` est réservé à la **sortie** du modèle.

## Organisation

- `cours_ml/` : cours au format markdown (interprété par Obsidian). Fichiers `*.md` à la racine, figures dans `cours_ml/assets/`, scripts de génération de figures dans `cours_ml/scripts/`.
- `td/` : notebooks des travaux dirigés, nommés `NN_<theme>.ipynb` (à plat). Ce sont les **corrigés** (solutions incluses).
- `td/assets/` : images extraites des notebooks (via `scripts/notebooks.py --td machine_learning/td extract`).

## Maintenance des images de notebooks

```bash
uv run python scripts/notebooks.py --td machine_learning/td extract   # attachments -> assets/
uv run python scripts/notebooks.py --td machine_learning/td clear     # vider les sorties
uv run python scripts/notebooks.py --td machine_learning/td prune     # supprimer les orphelines
```
