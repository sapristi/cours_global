# AGENTS.md — scripting_python

Cours de scripting Python pour la cybersécurité (3e année). Les fichiers de cours
sont à la racine de `scripting_python/` (vault Obsidian = racine du dépôt).
Conventions générales (Obsidian, export, Python) : voir `AGENTS.md` à la racine.

## Structure

- `Entrypoint.md` : objectifs + plan.
- `N. <Titre>.md` = un module de cours. Frontmatter requis : `durée (h)` (nombre) + `Contexte` (texte, source du plan).
- `assets/` = images et autres ressources des modules ; `Exercices/` = énoncés complémentaires.
- `td/` = notebooks des TD, nommés `NN_<theme>.ipynb` (à plat, préfixe numéroté). Ce sont les **corrigés** (solutions incluses), avec leurs fichiers de données (`.csv`) à côté.
- `Cours.base` = config Bases/Dataview du tableau de bord (`file.folder == "/"`, `file.ext == "md"`). Ne pas éditer comme du contenu.
- Images : `![[Pasted image ....png|largeur]]` (embed Obsidian + resize). Stocker dans `assets/`.
- Slides : source `.typ` (Typst), compilée en `.pdf` à côté. Éditer le `.typ`, jamais le `.pdf` ; recompiler : `typst compile "<fichier>.typ"`.

## Conventions

- Liens/embeds wiki `[[...]]` / `![[...]]`, callouts `[!abstract]`, `[!info]`, `[!danger]`, `[!example]`, `[!note]`.
- Frontmatter YAML strict (`---` blocs). `Contexte` multiligne avec `|-`.
- Rédiger en français. Vocabulaire suggéré du module 1 : CIA, AAA, vulnérabilité/exploit/payload/IOC/TTP, Kill Chain, Red/Blue team.

## Garde-fou contenu

- Tout exemple offensif (scan `socket`, brute-force `requests`/`paramiko`, injection) doit rappeler : **labo isolé uniquement, autorisation écrite, art. 323-1 Code pénal**. Ne jamais proposer de cible réelle.
- Libs de référence du cours : `socket`, `requests`, `hashlib`, `re`, `paramiko`, `pandas` (module 7).
