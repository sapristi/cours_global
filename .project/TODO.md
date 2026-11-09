# TODO

## T-004 — scripting_python : mettre les notebooks TD aux normes du skill
created: 2026-11-09 15:36

Les notebooks `scripting_python/td/*.ipynb` ne suivent pas le skill `notebook_exercises` (`.claude/skills/notebook_exercises/SKILL.md`). Par exemple, `05_voyage_impossible.ipynb` n'a pas d'encart `fieldset` « ✏️ Exercice N », ses sections ne suivent pas la structure `##`/`###` numérotée, sa consigne d'intro mentionne `#BEGIN`/`#END`, et ses fonctions n'ont pas de `# raise NotImplementedError` après `# BEGIN`. Les notebooks ML (commit « machine_learning: notebooks TD conformes au skill notebook_exercises ») servent de référence.

Le corrigé de TD05 (solutions des 5 fonctions, T-003) est fait mais n'est **pas encore commité** : à commiter avec cette mise à jour, ou avant. Sans lui, `check_notebooks.py` échoue sur TD05, et donc la CI aussi.

Revérifier avec `uv run scripts/check_notebooks.py` et des aperçus `prepare_notebooks.py` dans un dossier temporaire.

## T-005 — Vérifier le déploiement JupyterLite sur GitHub Pages
created: 2026-11-09 15:36

S'assurer que les notebooks (des deux cours) sont bien déployés sur GitHub Pages via JupyterLite. Workflow : `.github/workflows/deploy.yml` (check_snippets → check_notebooks → `collect_lite_content.py` → `jupyter lite build` → upload `dist/` → deploy, uniquement sur `main`). URL cible indiquée dans le workflow : `https://<owner>.github.io/cours_global/`.

À vérifier :
- le remote GitHub, que Pages est activé avec la source « GitHub Actions » (`gh api repos/<owner>/<repo>/pages`) ;
- le dernier run du workflow (`gh run list --workflow deploy.yml`), et qu'il passe ;
- sur le site déployé, que les notebooks sont présents dans `machine_learning/` et `scripting_python/`, sans solutions ni cellules `<!-- TOCLEAR -->`, avec le bouton « Clear notebook » et leurs fichiers de données (CSV) ;
- qu'un notebook s'exécute dans le navigateur (dépendances pyodide disponibles : pandas, numpy, matplotlib…).

Attention : `check_notebooks.py` échoue sur `scripting_python/td/05_voyage_impossible.ipynb` tant que son corrigé (T-003, voir T-004) n'est pas commité ; la CI échouera donc avant le build.
