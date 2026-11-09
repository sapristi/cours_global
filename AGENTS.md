# AGENTS.md — cours_global

Dépôt fusionné regroupant plusieurs cours (actuellement machine learning et
scripting python), chacun dans son propre sous-dossier et son propre vault
Obsidian. Contenu pédagogique en français.

## Structure du dépôt

- `machine_learning/` : cours de machine learning.
  - Les cours en markdown (`N - <Titre>.md`) sont directement à la racine du dossier (vault Obsidian) ; figures dans `assets/`, scripts de génération de figures dans `scripts/`.
  - `td/` = notebooks des TD (les **corrigés**, solutions incluses), à plat `NN_<theme>.ipynb`.
  - `Entrypoint.md` = objectifs + plan.
- `scripting_python/` : cours de scripting Python (cybersécurité).
  - Les modules de cours (`N. <Titre>.md`) sont directement à la racine du dossier (vault Obsidian) ; `assets/` = assets des modules.
  - `td/` = notebooks des TD (les **corrigés**, solutions incluses), à plat `NN_<theme>.ipynb` + fichiers de données.
  - `Entrypoint.md` = objectifs + plan.
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
que le dossier du cours). Un sous-module ne peut pas pointer vers un
sous-répertoire, d'où ce dossier unique à la racine.

Règles :

- **Ne jamais** placer de devoir, corrigé ou fichier de notes ailleurs que
  dans `devoirs/` : tout le reste du dépôt est public. Les fichiers de notes
  contiennent des données personnelles d'étudiants (RGPD).
- Ne pas recréer de dossier `devoir/` dans les cours (l'ancien
  `scripting_python/devoir/` a été migré ; ses sujets restent dans
  l'historique public, ce qui est acceptable pour des sujets déjà distribués).
- Les devoirs ne sont pas dans les vaults Obsidian et ne sont pas parcourus
  par les scripts (`check_*`, `collect_lite_content.py` ne scannent que
  `machine_learning/` et `scripting_python/`).
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

Pousser `cours_global` avant `devoirs/` laisse un pointeur vers un commit
introuvable pour les autres clones.

## Conventions Obsidian

**À appliquer uniquement quand un fichier markdown est édité, pas un notebook .ipynb**

- Liens/embeds wiki `[[...]]` / `![[...]]`, callouts `[!abstract]`, `[!info]`, `[!danger]`, `[!example]`, `[!note]`.
- Frontmatter YAML strict (`---` blocs). `Contexte` multiligne avec `|-`.
- Ne pas toucher aux dossiers `.obsidian/` des vaults (workspace, `graph.json`, plugins).

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

## Par cours

Voir `machine_learning/AGENTS.md` et `scripting_python/AGENTS.md` pour les
conventions spécifiques à chaque cours.
