# TODO

## T-004 — scripting_python : mettre les notebooks TD aux normes du skill
created: 2026-11-09 15:36

Les notebooks `scripting_python/td/*.ipynb` ne suivent pas le skill `notebook_exercises` (`.claude/skills/notebook_exercises/SKILL.md`). Par exemple, `05_voyage_impossible.ipynb` n'a pas d'encart `fieldset` « ✏️ Exercice N », ses sections ne suivent pas la structure `##`/`###` numérotée, sa consigne d'intro mentionne `#BEGIN`/`#END`, et ses fonctions n'ont pas de `# raise NotImplementedError` après `# BEGIN`. Les notebooks ML (commit « machine_learning: notebooks TD conformes au skill notebook_exercises ») servent de référence.

Le corrigé de TD05 (solutions des 5 fonctions, T-003) est fait mais n'est **pas encore commité** : à commiter avec cette mise à jour, ou avant. Sans lui, `check_notebooks.py` échoue sur TD05, et donc la CI aussi.

Revérifier avec `uv run scripts/check_notebooks.py` et des aperçus `prepare_notebooks.py` dans un dossier temporaire.

## T-005 — Vérifier le déploiement JupyterLite sur GitHub Pages
created: 2026-11-09 15:36

S'assurer que les notebooks (des deux cours) sont bien déployés sur GitHub Pages via JupyterLite (`.github/workflows/deploy.yml`, URL `https://sapristi.github.io/cours_global/`).

État au 2026-11-09 (vérifié par un agent) :
- **Pages non activé** (`gh api repos/sapristi/cours_global/pages` → 404, `has_pages: false`) : à activer avec la source « GitHub Actions » (`gh api -X POST repos/sapristi/cours_global/pages -f build_type=workflow` ou Settings > Pages).
- **CI** : les 4 runs ont échoué à « Check notebooks execute » (TD05 sans corrigé). Corrigé par le commit local f63727a, non poussé. En local depuis HEAD, toute la chaîne passe (check_snippets, check_notebooks 12/12, collect, `jupyter lite build`), et `dist/` est correct : notebooks des deux cours, CSV, solutions et réponses retirées, cellule Clear notebook présente.
- **plotly absent de Pyodide** (0.8.6 / Pyodide 314.0.6) : `import plotly` échouera dans ML 01 et 03. `jupyter_lite_config.json` → `PyodideLockAddon` : remplacer `"prefetch": [...]` par `"specs": ["plotly"]` + `"prefetch_extra": ["numpy", "matplotlib", "pandas", "plotly"]`. Testé en build local : le build passe et la roue plotly 7.1.0 est incluse. `prefetch` remplace aussi la liste par défaut (ipykernel, comm…), d'où `prefetch_extra`.
- Mineur : les consignes de `05_voyage_impossible` et `bases_pandas` parlent de `#BEGIN`/`#END` (à traiter dans T-004).

Reste : appliquer le fix plotly, pousser, activer Pages, puis vérifier le site en ligne (contenus via `<site>/api/contents/all.json`, exécution d'un notebook ML avec plotly dans le navigateur).
