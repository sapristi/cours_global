# TODO

## T-004 — scripting_python : mettre les notebooks TD aux normes du skill
created: 2026-11-09 15:36

Les notebooks `scripting_python/td/*.ipynb` ne suivent pas le skill `notebook_exercises` (`.claude/skills/notebook_exercises/SKILL.md`). Par exemple, `05_voyage_impossible.ipynb` n'a pas d'encart `fieldset` « ✏️ Exercice N », ses sections ne suivent pas la structure `##`/`###` numérotée, sa consigne d'intro mentionne `#BEGIN`/`#END`, et ses fonctions n'ont pas de `# raise NotImplementedError` après `# BEGIN`. Les notebooks ML (commit « machine_learning: notebooks TD conformes au skill notebook_exercises ») servent de référence.

Le corrigé de TD05 est commité (f63727a).

Revérifier avec `uv run scripts/check_notebooks.py` et des aperçus `prepare_notebooks.py` dans un dossier temporaire.
