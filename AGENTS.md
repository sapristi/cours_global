# AGENTS.md — cours_global

Dépôt fusionné regroupant plusieurs cours (actuellement machine learning et
scripting python), chacun dans son propre sous-dossier et son propre vault
Obsidian. Contenu pédagogique en français.

## Structure du dépôt

- `machine_learning/` : cours de machine learning.
  - `cours_ml/` = vault Obsidian (cours en markdown ; figures dans `cours_ml/assets/`, scripts de génération de figures dans `cours_ml/scripts/`).
  - `td/` = notebooks des TD (les **corrigés**, solutions incluses), à plat `NN_<theme>.ipynb`.
  - `Entrypoint.md` = objectifs + plan.
- `scripting_python/` : cours de scripting Python (cybersécurité).
  - `cours scripting python/` = vault Obsidian (`N. <Titre>.md` = module de cours, `N. <Titre>/` = assets du module).
  - `td/` = notebooks des TD (les **corrigés**, solutions incluses), à plat `NN_<theme>.ipynb` + fichiers de données.
  - `Entrypoint.md` = objectifs + plan.
- `scripts/` = scripts mutualisés (voir plus bas).
- `content/` = staging généré par `collect_lite_content.py` (gitignoré, ne pas éditer à la main).
- `dist/` = sortie du build JupyterLite (gitignorée).
- `.github/workflows/deploy.yml` = CI (vérifications + build + déploiement Pages).

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
`#BEGIN` sont acceptées) et en injectant un bouton « Clear notebook ».

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
