# TODO


## T-006 — Unifier et simplifier assets et scripts des cours
created: 2026-11-09 21:58

Contexte : depuis la fusion, il n'y a plus qu'un seul vault Obsidian (racine du
dépôt), mais l'organisation des assets et des scripts diffère encore entre
`machine_learning/` et `scripting_python/`. Objectif : une convention commune,
la plus simple possible, puis mettre à jour `AGENTS.md` (sections « Structure
du dépôt », « Conventions Obsidian », « Images des notebooks »).

Points à traiter :
- Pièces jointes Obsidian : `.obsidian/app.json` ne définit pas
  `attachmentFolderPath`, les images collées atterrissent à la racine du vault
  et non dans `<cours>/assets/`. Choisir un réglage (ex. sous-dossier `assets`
  relatif au fichier courant).
- Noms d'images : mélange de figures nommées (`05-svm-marge.png`) et de
  `Pasted image <date>.png` dans les deux `assets/` ; renommer ou non
  (Obsidian met les liens à jour, `alwaysUpdateLinks: true`).
- Images des notebooks : `td/assets/` + `scripts/notebooks.py`
  (extract/clear/prune) et les hooks `.pre-commit-config.yaml` ne couvrent que
  `machine_learning/td` ; étendre à `scripting_python/td` (ou à tous les `td/`).
- Scripts : `machine_learning/scripts/` (génération de figures
  `figures_*.py`) à côté de `scripts/` racine (outillage notebooks/build) ;
  décider s'il faut fusionner, renommer, ou garder séparé et documenter.
- `scripting_python/Exercices/` (énoncés `.md`) vs énoncés `.md` déjà dans
  `scripting_python/td/` : regrouper ?
- Vérifier ensuite `collect_lite_content.py`, `check_*.py` et le CI
  (`.github/workflows/deploy.yml`) avec la nouvelle arborescence.
