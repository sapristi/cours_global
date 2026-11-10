# AGENTS.md — cours_global

@README.md

# Instructions

## Avant de travailler sur un cours ou un TD

**Lire `<cours>/Readme.md`** (`machine_learning/Readme.md` ou
`scripting_python/Readme.md`) : contexte (niveau, prérequis), objectifs,
plan, compétences évaluées et section **Conventions** du cours (notations du
cours de ML, cadre légal des exemples offensifs en scripting python…). Ces
conventions s'appliquent aussi aux notebooks de TD.

## Structure du dépôt

- `machine_learning/` : cours de machine learning.
  - Les cours en markdown (`N - <Titre>.md`) sont directement à la racine du dossier ; figures dans `assets/`, scripts de génération de figures dans `scripts/`.
  - `td/` = notebooks des TD (les **corrigés**, solutions incluses), à plat `NN_<theme>.ipynb` ; images extraites des notebooks dans `td/assets/` (gérées par `scripts/notebooks.py`, lancé par le hook pre-commit).
  - `Readme.md` = contexte, objectifs, plan, conventions.
- `scripting_python/` : cours de scripting Python (cybersécurité).
  - Les modules de cours (`N. <Titre>.md`) sont directement à la racine du dossier ; `assets/` = assets des modules ; `Exercices/` = énoncés complémentaires.
  - `td/` = notebooks des TD (les **corrigés**, solutions incluses), à plat `NN_<theme>.ipynb` + fichiers de données.
  - `Readme.md` = contexte, objectifs, plan (via `Cours.base`), compétences évaluées, conventions.
- `devoirs/` = **sous-module Git privé** (sujets, corrigés, notes des devoirs) ; voir la section « Devoirs » plus bas.
- `scripts/` = scripts mutualisés (voir plus bas).
- `content/` = staging généré par `collect_lite_content.py` (gitignoré, ne pas éditer à la main).
- `dist/` = sortie du build JupyterLite (gitignorée).
- `.github/workflows/deploy.yml` = CI (vérifications + build + déploiement Pages).

## Devoirs (sous-module privé)

Le dépôt `cours_global` est **public**. Les devoirs (sujets, corrigés, grilles
de notes) vivent dans un dépôt **privé** séparé,
`git@github.com:sapristi/cours_devoirs.git`, monté comme sous-module dans
`devoirs/` :

```
devoirs/                 ← sous-module (dépôt privé cours_devoirs)
├── machine_learning/
└── scripting_python/
    ├── DST_30min_sujet.{md,typ,pdf}
    ├── DST_30min_corrige.{typ,pdf}
    └── DST_30min_notes.ods
```

Un seul dépôt privé pour tous les cours, un sous-dossier par cours (même nom
que le dossier du cours).

Règles :

- **Ne jamais** placer de devoir, corrigé ou fichier de notes ailleurs que
  dans `devoirs/`.
- Le CI (`actions/checkout` sans `submodules`) ne clone pas `devoirs/` ; ne
  pas l'y ajouter.

Workflow :

```bash
# récupérer les devoirs (clone neuf ou autre machine ; accès au dépôt privé requis)
git submodule update --init

# modifier un devoir : committer et pousser d'abord DANS le sous-module…
cd devoirs
git add scripting_python/… && git commit -m "…" && git push
cd ..
# …puis committer le nouveau pointeur dans cours_global
git add devoirs && git commit -m "devoirs : <résumé>"
```


Sujets et corrigés sont rédigés en Typst : éditer le `.typ`, jamais le `.pdf`,
puis recompiler avec `typst compile "<fichier>.typ"` (le `.pdf` est versionné à
côté).

## Conventions Obsidian

**À appliquer uniquement quand un fichier markdown est édité, pas un notebook .ipynb**

- Liens/embeds wiki `[[...]]` / `![[...]]`, callouts `[!abstract]`, `[!info]`, `[!danger]`, `[!example]`, `[!note]`.
- Frontmatter YAML strict (`---` blocs). `Contexte` multiligne avec `|-`.
- Images : stockées dans `<cours>/assets/`, embarquées avec `![[<image>.png|largeur]]`.
- Les fichiers `*.base` (ex. `scripting_python/Cours.base`, tableau du plan) sont de la configuration Bases.

## Environnement Python

Toujours lancer Python via `uv run` (jamais `python` directement) :

```bash
uv run python <script>.py
```

## Préparation des notebooks pour la diffusion

Les notebooks du repo sont les **corrigés** (solutions incluses). Au build
JupyterLite, `scripts/collect_lite_content.py` les copie dans `content/` en
retirant les solutions (blocs `# BEGIN`/`# END`, les deux formes `# BEGIN` et
`#BEGIN` sont acceptées) et en injectant un bouton « Clear notebook ». Les cellules markdown dont la
première ligne non vide est exactement `<!-- TOCLEAR -->` (réponses du corrigé,
affichées dans un encart vert « 💡 Réponse », voir le skill `notebook_exercises`)
sont supprimées.

### Aperçu local (fichier → fichier)

```bash
uv run python scripts/prepare_notebooks.py <corrige>.ipynb <apercu>.ipynb
```

Sert à prévisualiser ce que verra l'étudiant. Écrire l'aperçu hors du repo
(ex. `/tmp/`) : ne jamais écraser le corrigé, ne pas versionner l'aperçu.

### Vérifications

- `uv run scripts/check_notebooks.py` : exécute tous les corrigés (échec si une cellule lève).
- `uv run scripts/check_snippets.py` : syntaxe des snippets Python des `.md`.

### Images des notebooks (machine_learning)

Le hook pre-commit le fait automatiquement ; à la main :

```bash
uv run python scripts/notebooks.py --td machine_learning/td extract   # attachments -> td/assets/
uv run python scripts/notebooks.py --td machine_learning/td clear     # vider les sorties
uv run python scripts/notebooks.py --td machine_learning/td prune     # supprimer les images orphelines
```
