---
name: review_td
description: Use when asked to review, test or get student feedback on a TD notebook (`<cours>/td/NN_<theme>.ipynb`) — a simulated student does the whole TD on the distributed version (solutions removed) and writes a feedback report (difficulty and tries per exercise, useless or too hard exercises, unclear instructions, favorite exercises, overall impression, general suggestions).
---

# Review d'un TD par un élève simulé

Un « élève » fait le TD **comme un étudiant** : sur la version diffusée (sans
solutions), sans voir le corrigé, puis rédige un retour.

## 1. Direct ou sous-agent ?

L'élève ne doit **rien savoir** du corrigé ni des choix de conception du TD.

- **Session vide** (le skill est la première chose demandée) : faire la review
  directement, dans la session.
- **Session déjà utilisée** (le corrigé, le notebook ou la discussion du TD sont
  déjà dans le contexte) : lancer un **sous-agent** (`general-purpose`) avec le
  prompt de l'élève (section 3), en lui passant les chemins préparés à
  l'étape 2. Ne pas le faire soi-même : on connaîtrait déjà les réponses.

## 2. Préparation (faite par la session principale)

1. Lire `<cours>/Readme.md` (section Contexte : niveau, prérequis) pour fixer
   le profil de l'élève.
2. Générer la version élève **hors du dépôt**, dans un dossier de travail
   (`$CLAUDE_JOB_DIR/tmp/review_<td>/` ou le scratchpad, sinon `/tmp/review_<td>/`) :
   ```bash
   uv run python scripts/prepare_notebooks.py <cours>/td/NN_<theme>.ipynb <travail>/NN_<theme>_eleve.ipynb
   ```
3. Copier dans ce dossier les fichiers de données lus par le notebook (CSV…,
   repérer les `read_csv` / `open(...)`).

## 3. Consignes de l'élève (prompt du sous-agent, ou à suivre en direct)

- Profil : étudiant·e du niveau indiqué dans le Readme du cours ; ne connaît
  que les prérequis annoncés et ce que le notebook lui-même présente
  (préambules, rappels, indices).
- **Ne pas lire** le dépôt (corrigé, cours, scripts) : uniquement le notebook
  élève et les données du dossier de travail.
- Faire le TD **dans l'ordre**, honnêtement : compléter chaque cellule
  `# TODO`, rédiger les réponses dans les cellules « *Votre réponse :* »,
  exécuter les cellules de vérification. Exécuter de haut en bas avec, en cwd
  le dossier de travail :
  ```bash
  uv run --with nbclient --with ipykernel --with pandas python -c "..."   # nbclient
  ```
  (ajouter les `--with` nécessaires aux imports du notebook ; toujours `uv run`).
- Noter en chemin, pour chaque exercice : nombre d'essais avant que la
  vérification passe, blocages, consignes ambiguës, ce qu'il a fallu deviner,
  notions utilisées mais jamais introduites, vérifications trop strictes,
  trop permissives ou qui dévoilent la réponse, et redondances avec un autre
  exercice.

## 4. Rapport

Markdown en français, écrit dans `<cours>/td/NN_<theme>_retour_eleve.md`
(non versionné, sauf demande). Si le sous-agent ne peut pas écrire dans le
dépôt, il l'écrit dans le dossier de travail et la session principale le copie.

```markdown
# Retour élève — TD NN <titre>

Profil simulé : … — date.

## Déroulé par exercice
| exercice | difficulté ressentie (1–5) | essais | remarques courtes |

## Exercices peu utiles ou trop difficiles
(lesquels, pourquoi, suggestion concrète : reformulation, indice, découpage, fusion)

## Consignes ambiguës
(citation exacte de l'énoncé → ce qui était ambigu → reformulation proposée ;
inclure messages d'erreur peu clairs et vérifications mal calibrées)

## Exercices préférés
(lesquels et pourquoi)

## Sentiment global
(paragraphe à la 1re personne : durée estimée, charge, progression de la
difficulté, ce que j'ai appris)

## Suggestions générales
(si pertinent : structure, préambule, ordre des parties, cohérence d'ensemble)
```

## 5. Restitution

Résumer à l'utilisateur les points principaux (une ligne par rubrique) et le
chemin du rapport. Ne pas modifier le corrigé sans demande : proposer les
corrections, appliquer si l'utilisateur valide (skill `notebook_exercises`).
