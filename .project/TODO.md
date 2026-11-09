# TODO

## T-001 — machine_learning TD04 : traiter les TODO de l'auteur
created: 2026-11-09 15:07

Le notebook `machine_learning/td/04_evaluation_elan.ipynb` contient des notes `TODO` laissées par l'auteur, à appliquer puis supprimer :

- cellule de la classe `MLP` (préambule) : commentaire `# TODO: lr en dernier paramètre` au-dessus de `fit` — passer `lr` après `X_test`/`t_test` dans la signature de `fit` (et adapter tous les appels qui passent `lr` en positionnel, ex. bonus C `fit(..., lr=k * LR, ...)`, ainsi que `MLPMomentum`).
- docstring de `sweep_threshold` (exercice 5) : `TODO: considérer retourner des listes plutot que np.array` — trancher, puis adapter `check_sweep`, le tracé et `check_sweep_moons` (bonus E).
- énoncé de l'exercice bonus A : `TODO: reprendre l'exo, on ne comprends pas bien pourquoi X_new / t_new ne sont pas utilisés ici alors qu'ils sont introduits juste au dessus` — clarifier l'énoncé (X_new/t_new ne servent qu'à la cellule suivante, test final consulté une fois) ; cette note est actuellement visible des étudiants.

Respecter le skill `notebook_exercises` (`.claude/skills/notebook_exercises/SKILL.md`) et revérifier avec `uv run scripts/check_notebooks.py machine_learning/td/04_evaluation_elan.ipynb`.

## T-002 — Remplacer le marqueur `# TOCLEAR` par un encart « réponse »
created: 2026-11-09 15:07

Problème : les cellules de réponse du corrigé commencent par `# TOCLEAR`, qui s'affiche comme un titre markdown de niveau 1 quand on lit le corrigé (confusion avec la structure du notebook).

À faire : afficher la réponse dans un encart `fieldset` similaire à celui des exercices (voir skill `notebook_exercises`, styles inline uniquement, lignes vides après `</legend>` et avant `</fieldset>`), avec une couleur différente (ex. vert) et une légende du type « 💡 Réponse ». Choisir le marqueur de suppression le plus simple, par exemple un commentaire HTML `<!-- TOCLEAR -->` en première ligne (invisible au rendu) ou la détection de la légende de l'encart.

Fichiers concernés :
- `scripts/nb_common.py` (`is_toclear_cell`, `drop_toclear_cells`, docstrings) — utilisé par `scripts/prepare_notebooks.py` et `scripts/collect_lite_content.py` ;
- documentation : `AGENTS.md` (racine), `.claude/skills/notebook_exercises/SKILL.md` (section « Cellule de réponse `# TOCLEAR` ») ;
- migrer toutes les cellules `# TOCLEAR` existantes de `machine_learning/td/*.ipynb` (et `scripting_python/td/` s'il y en a).

Vérifier ensuite avec `prepare_notebooks.py` qu'aucune réponse ne subsiste dans l'aperçu, et avec `check_notebooks.py`.
