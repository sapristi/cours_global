# DONE

## T-004 — scripting_python : mettre les notebooks TD aux normes du skill
created: 2026-11-09 15:36
done: 2026-11-09 20:53

Les notebooks `scripting_python/td/*.ipynb` ne suivent pas le skill `notebook_exercises` (`.claude/skills/notebook_exercises/SKILL.md`). Par exemple, `05_voyage_impossible.ipynb` n'a pas d'encart `fieldset` « ✏️ Exercice N », ses sections ne suivent pas la structure `##`/`###` numérotée, sa consigne d'intro mentionne `#BEGIN`/`#END`, et ses fonctions n'ont pas de `# raise NotImplementedError` après `# BEGIN`. Les notebooks ML (commit « machine_learning: notebooks TD conformes au skill notebook_exercises ») servent de référence.

Le corrigé de TD05 est commité (f63727a).

Revérifier avec `uv run scripts/check_notebooks.py` et des aperçus `prepare_notebooks.py` dans un dossier temporaire.

Outcome: les 6 notebooks de `scripting_python/td/` sont conformes (encarts « ✏️ Exercice N », structure `##`/`###` numérotée, `# raise NotImplementedError`, vérification autonome après chaque exercice, sorties vidées, ids de cellules). TD02 et TD03 n'avaient ni corrigé ni vérifications : ils ont été écrits (TD03 : fonctions qui renvoient la figure en `str` ; motif « rayures » redéfini par `(c+ligne)%4==0` car le dessin d'origine était irrégulier, à valider). `bases_pandas.ipynb` non renommé (URL déployée). Commits b59df08..5203f66, plus les corrections de revue finale incluses dans c56749b. `check_notebooks.py` : 12/12 OK.

## T-005 — Vérifier le déploiement JupyterLite sur GitHub Pages
created: 2026-11-09 15:36
done: 2026-11-09 20:26

Déployé le 2026-11-09 sur https://sapristi.github.io/cours_global/ : Pages activé (source GitHub Actions), fix plotly commité (735a844), run CI 42639806188 vert. Le premier déploiement est resté bloqué en « syncing_files » jusqu'au timeout, juste après l'activation de Pages ; il est passé en relançant le job. Contrôlé par curl : les deux dossiers de cours, tous les notebooks, les CSV, plotly dans `pyodide-lock.json`, et TD04 en ligne sans solutions ni réponses, avec la cellule Clear notebook.

Reste (manuel, dans un navigateur) : ouvrir un notebook ML qui importe plotly (01 ou 03) et un notebook scripting_python qui lit un CSV (05), puis les exécuter en entier dans JupyterLite. Si tout passe, fermer la tâche.

Outcome: vérification manuelle faite par l'auteur dans un navigateur : notebooks ML avec plotly et scripting_python TD05 (CSV) exécutés en entier dans JupyterLite, tout passe.

## T-003 — scripting_python TD05 : corrigé de `fusionner` manquant
created: 2026-11-09 15:20
done: 2026-11-09 15:28

`uv run scripts/check_notebooks.py` échoue sur `scripting_python/td/05_voyage_impossible.ipynb` : dans le corrigé, la cellule `fusionner` ne contient que `# TODO` + `pass` (pas de solution entre `# BEGIN`/`# END`). La fonction renvoie None et la cellule suivante lève `AttributeError: 'NoneType' object has no attribute 'columns'`. Échec antérieur à T-002 (notebook identique à HEAD au 2026-11-09). Écrire la solution entre marqueurs `# BEGIN`/`# END` en suivant le skill `notebook_exercises`, puis revérifier avec `check_notebooks.py`.

Outcome: le notebook avait été commité sans aucune solution : les 5 fonctions (`fusionner`, `detecter_voyages_impossibles`, `retirer_vpn`, `ip_partagees`, `utilisateurs_compromis`) ont reçu leur corrigé entre `# BEGIN`/`# END` (indices de l'ex. 2 passés en `##`). Version étudiant identique à l'ancien notebook ; `check_notebooks.py` : 12/12 OK. Non commité.

## T-002 — Remplacer le marqueur `# TOCLEAR` par un encart « réponse »
created: 2026-11-09 15:07
done: 2026-11-09 15:20

Problème : les cellules de réponse du corrigé commencent par `# TOCLEAR`, qui s'affiche comme un titre markdown de niveau 1 quand on lit le corrigé (confusion avec la structure du notebook).

À faire : afficher la réponse dans un encart `fieldset` similaire à celui des exercices (voir skill `notebook_exercises`, styles inline uniquement, lignes vides après `</legend>` et avant `</fieldset>`), avec une couleur différente (ex. vert) et une légende du type « 💡 Réponse ». Choisir le marqueur de suppression le plus simple, par exemple un commentaire HTML `<!-- TOCLEAR -->` en première ligne (invisible au rendu) ou la détection de la légende de l'encart.

Fichiers concernés :
- `scripts/nb_common.py` (`is_toclear_cell`, `drop_toclear_cells`, docstrings) — utilisé par `scripts/prepare_notebooks.py` et `scripts/collect_lite_content.py` ;
- documentation : `AGENTS.md` (racine), `.claude/skills/notebook_exercises/SKILL.md` (section « Cellule de réponse `# TOCLEAR` ») ;
- migrer toutes les cellules `# TOCLEAR` existantes de `machine_learning/td/*.ipynb` (et `scripting_python/td/` s'il y en a).

Vérifier ensuite avec `prepare_notebooks.py` qu'aucune réponse ne subsiste dans l'aperçu, et avec `check_notebooks.py`.

Outcome: marqueur `<!-- TOCLEAR -->` (1re ligne non vide, invisible au rendu ; ancienne forme `# TOCLEAR` abandonnée) + encart `fieldset` vert #2e7d32 « 💡 Réponse ». `scripts/nb_common.py`, docstrings de prepare/collect, `AGENTS.md` et skill notebook_exercises mis à jour ; 31 cellules migrées (ML TD01–06, aucune dans scripting_python). Aperçus vérifiés sans réponse. Non commité.

## T-001 — machine_learning TD04 : traiter les TODO de l'auteur
created: 2026-11-09 15:07
done: 2026-11-09 15:12

Le notebook `machine_learning/td/04_evaluation_elan.ipynb` contient des notes `TODO` laissées par l'auteur, à appliquer puis supprimer :

- cellule de la classe `MLP` (préambule) : commentaire `# TODO: lr en dernier paramètre` au-dessus de `fit` — passer `lr` après `X_test`/`t_test` dans la signature de `fit` (et adapter tous les appels qui passent `lr` en positionnel, ex. bonus C `fit(..., lr=k * LR, ...)`, ainsi que `MLPMomentum`).
- docstring de `sweep_threshold` (exercice 5) : `TODO: considérer retourner des listes plutot que np.array` — trancher, puis adapter `check_sweep`, le tracé et `check_sweep_moons` (bonus E).
- énoncé de l'exercice bonus A : `TODO: reprendre l'exo, on ne comprends pas bien pourquoi X_new / t_new ne sont pas utilisés ici alors qu'ils sont introduits juste au dessus` — clarifier l'énoncé (X_new/t_new ne servent qu'à la cellule suivante, test final consulté une fois) ; cette note est actuellement visible des étudiants.

Respecter le skill `notebook_exercises` (`.claude/skills/notebook_exercises/SKILL.md`) et revérifier avec `uv run scripts/check_notebooks.py machine_learning/td/04_evaluation_elan.ipynb`.

Outcome: `fit(self, X, t, epochs, X_test=None, t_test=None, lr=LR)` (appels bonus C réordonnés, MLPMomentum inchangé) ; `sweep_threshold` renvoie des listes Python (check_sweep / check_sweep_moons adaptés) ; énoncé bonus A réécrit (validation = courbes de §3, X_new/t_new consultés une seule fois après). check_notebooks OK. Non commité.
