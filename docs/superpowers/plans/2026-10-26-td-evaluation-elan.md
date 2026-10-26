# TD « Évaluer un modèle » + élan — plan de réalisation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Écrire le notebook corrigé `machine_learning/td/07_evaluation_elan.ipynb` (matrice de confusion, courbes d'apprentissage, élan) et le chapitre `machine_learning/6 - Évaluer un modèle.md` avec ses figures.

**Architecture:** Notebook autonome (JupyterLite) : code fourni en tête (générateurs, `MLP`, tracés), puis 4 sections d'exercices avec blocs `# BEGIN`/`# END` et cellules de vérification. Un script séparé régénère les figures du chapitre en dupliquant le minimum de code (générateurs + MLP) : le notebook doit rester autonome, la duplication est assumée.

**Tech Stack:** python, numpy, matplotlib, Jupyter ; `uv run`.

**Spec:** `docs/superpowers/specs/2026-10-26-td-evaluation-elan-design.md` (à lire en entier avant toute tâche).

## Global Constraints

- Ne **pas** lire ni modifier `machine_learning/td/06_momentum_surapprentissage.ipynb`, ni les specs/plans du TD 06.
- Ne pas modifier d'autres fichiers du cours (`Entrypoint.md`, autres chapitres, TD 03).
- Python toujours via `uv run`. numpy / matplotlib seulement (pas de sklearn).
- Notations : cible `t`/`T`, sortie `y`/`Y`, `lr` = η, élan `μ` (`momentum` en code), vitesses `vWs`/`vbs`.
- Règle d'élan : `v ← μ v + lr ∂E/∂W`, `W ← W − v` (idem biais).
- Conventions notebook : skill `notebook_exercises` (`.opencode/skills/notebook_exercises/SKILL.md`) — à lire avant la tâche 1 : sections `##` numérotées, `###` sous-sections, `> **Exercice N** — …`, fonctions à compléter typées (alias `Vec`, `Mat`), chaque exercice de code suivi d'une cellule de vérification hors `# BEGIN`/`# END` qui imprime `… — OK`, cellules « à exécuter » sans impératif.
- Conventions markdown : `AGENTS.md` racine (frontmatter YAML, callouts, `![[...]]`).
- Français partout. Messages de commit au format du repo (`td07: …`, `cours(eval): …`).
- Temps d'exécution : chaque entraînement du notebook ≲ 5 s en local (JupyterLite est plus lent) ; `uv run scripts/check_notebooks.py machine_learning/td/07_evaluation_elan.ipynb` doit passer.
- Réponses aux questions de lecture : dans une **cellule markdown** juste après la question, dont la **première ligne non vide est exactement `# TOCLEAR`** (puis le texte du corrigé). Ces cellules sont supprimées à la préparation (tâche 0). Pour les cellules où l'étudiant doit écrire sa réponse, laisser avant la cellule `# TOCLEAR` une cellule markdown « *Votre réponse :* » (visible des deux côtés).
- Tout chiffre cité dans un énoncé, une lecture guidée ou le chapitre doit être recopié depuis une sortie réelle (graines fixées).

## Review Focus

1. `precision` quand aucun positif n'est prédit (classifieur « toujours négatif ») : doit renvoyer `0.0`, sans `ZeroDivisionError` ni warning `nan` — testé tâche 2.
2. `confusion` reçoit `t` de forme `(N, 1)` et `y` de forme `(N,)` (ou l'inverse) : même résultat — testé tâche 2.
3. `MLPMomentum.fit` doit utiliser le `step` surchargé (sinon « avec élan » = « sans élan » silencieusement) — testé tâche 4 (μ=0 identique à `MLP`, μ=0.9 différent).
4. Réentraîner avec `epochs = best_epoch + 1` doit redonner exactement la perte de validation minimale (déterminisme de la descente par lot) — testé tâche 4.
5. Une cellule `# TOCLEAR` qui survivrait à la préparation livrerait le corrigé aux étudiants — vérifié tâche 6 (aperçu : aucune occurrence de `TOCLEAR`).
6. Chiffres des énoncés désynchronisés des sorties après réglage des jeux — vérifié tâche 6.

---

### Task 0: Supprimer les cellules markdown `# TOCLEAR` à la préparation

**Files:**
- Modify: `scripts/nb_common.py` (à côté de `is_delete_cell` / `drop_delete_cells`, appel dans `strip_solutions`)
- Modify: `scripts/prepare_notebooks.py` (docstring), `scripts/collect_lite_content.py` (docstring si elle liste les transformations)
- Modify: `.opencode/skills/notebook_exercises/SKILL.md` (nouvelle section « Cellule de réponse `# TOCLEAR` ») et `AGENTS.md` racine (§ Préparation des notebooks : une ligne)
- Test: script jetable dans le scratchpad (le repo n'a pas de suite de tests)

**Interfaces:**
- Produces : `TOCLEAR_MARQUEUR = "TOCLEAR"`, `is_toclear_cell(cell: dict) -> bool`, `drop_toclear_cells(nb: dict) -> int` ; `strip_solutions` appelle `drop_toclear_cells` (donc `prepare_notebooks.py` **et** `collect_lite_content.py` en profitent).
- Règle : cellule `markdown` dont la première ligne non vide, `.strip()`-ée, vaut exactement `# TOCLEAR`. Les cellules code ne sont pas concernées ; un `# TOCLEAR` ailleurs qu'en première ligne non vide ne déclenche rien.

- [ ] **Step 1: Test qui échoue** — script `<scratchpad>/test_toclear.py` (lancé avec `uv run python` depuis `scripts/`, ou en ajoutant `scripts/` à `sys.path`) :
  ```python
  from nb_common import strip_solutions
  md = lambda s: {"cell_type": "markdown", "metadata": {}, "source": s}
  code = lambda s: {"cell_type": "code", "metadata": {}, "source": s, "outputs": [], "execution_count": 1}
  nb = {"cells": [
      md("Question ?"),
      md("# TOCLEAR\nRéponse du corrigé"),
      md(["\n", "  # TOCLEAR  \n", "réponse\n"]),   # source en liste, ligne vide + espaces
      md("Texte\n# TOCLEAR"),                         # pas en 1re ligne -> gardée
      md("# TOCLEARX"),                                # pas exactement -> gardée
      code("# TOCLEAR\nx = 1"),                       # cellule code -> gardée
  ]}
  strip_solutions(nb)
  srcs = ["".join(c["source"]) if isinstance(c["source"], list) else c["source"] for c in nb["cells"]]
  assert srcs == ["Question ?", "Texte\n# TOCLEAR", "# TOCLEARX", "# TOCLEAR\nx = 1"], srcs
  print("toclear — OK")
  ```
- [ ] **Step 2:** Lancer → échoue (assertion, les cellules TOCLEAR sont encore là).
- [ ] **Step 3:** Implémenter `is_toclear_cell` / `drop_toclear_cells` sur le modèle de `is_delete_cell` / `drop_delete_cells`, appeler `drop_toclear_cells(nb)` dans `strip_solutions` à côté de `drop_delete_cells(nb)` ; mettre à jour la docstring de `strip_solutions`.
- [ ] **Step 4:** Relancer → `toclear — OK`. Non-régression : `uv run python scripts/prepare_notebooks.py machine_learning/td/03_backpropagation.ipynb <scratchpad>/03.ipynb` produit le même nombre de solutions retirées qu'avant la modification (le lancer aussi avant l'étape 3 pour comparer).
- [ ] **Step 5:** Docs (docstrings, SKILL.md, AGENTS.md racine) ; commit `scripts: retirer les cellules markdown # TOCLEAR à la préparation`.

### Task 1: Squelette du notebook + code fourni

**Files:**
- Create: `machine_learning/td/07_evaluation_elan.ipynb`

**Interfaces:**
- Produces (cellules fournies, hors `# BEGIN`) :
  - alias `Vec`, `Mat` ;
  - `make_blobs_imbalanced(n: int, noise: float = 0.6, pos_frac: float = 0.1, seed: int = 1) -> tuple[Mat, Mat]` — centres (0,0) / (1,1) ;
  - `make_moons(n: int, noise: float = 0.3, seed: int = 1) -> tuple[Mat, Mat]` ;
  - `make_spirals(n: int, noise: float = 0.08, seed: int = 1) -> tuple[Mat, Mat]` (r ∈ [0.2, 1], θ = 3πr, +π pour la classe 1) ;
  - tous renvoient `X (n, 2)` et `t (n, 1)` en float 0./1. ;
  - `class MLP(sizes: list[int], seed: int = 0)` : tanh caché, sortie sigmoïde, init `N(0, 0.5)`, biais nuls ; méthodes `forward(X) -> tuple[list[Mat], list[Mat]]`, `backward(X, t) -> list[tuple[Mat, Vec]]`, `step(X, t, lr) -> None`, `predict(X) -> Mat` (probabilités), `loss(X, t) -> float` (`0.5 · mean Σ_k (Y−T)²`), `error_rate(X, t, threshold=0.5) -> float`, `fit(X, t, lr, epochs, X_val=None, t_val=None) -> dict[str, list[float]]` avec clés `"train"`, `"val"`, `"err_train"`, `"err_val"` (listes vides côté val si pas de validation) ; `fit` appelle `self.step` ;
  - `plot_curves(histories: dict[str, dict[str, list[float]]], metric: str = "loss", logx: bool = True, ax=None)` : une couleur par entrée, train en pointillés, val en trait plein ; `metric="err"` trace les taux d'erreur ;
  - `plot_data(X, t, ax=None)` et `plot_decision(model, X, t, ax=None)`.

- [ ] **Step 1:** Créer le notebook : `# TD07 — Évaluer un modèle, courbes d'apprentissage et élan`, `## Objectif` (rappel de ce que l'on va faire, renvoi au chapitre « 6 - Évaluer un modèle »), `## Préambule` contenant le code fourni ci-dessus. `MLP` reprend la structure de `MLP` du TD 03 (`machine_learning/td/03_backpropagation.ipynb`, cellule 20) avec activations figées tanh/sigmoïde.
- [ ] **Step 2:** Ajouter une cellule de vérification fournie (`check_mlp`) : sur `MLP([2, 3, 1], seed=1)` et un petit batch fixé, gradient de `backward` comparé à un gradient numérique par différences finies (`np.allclose`, `atol=1e-6`), et `fit(..., epochs=3)` renvoie des listes de longueur 3. Imprime `MLP check — OK`.
- [ ] **Step 3:** `uv run scripts/check_notebooks.py machine_learning/td/07_evaluation_elan.ipynb` → succès.
- [ ] **Step 4:** Commit `td07: squelette + code fourni (données, MLP, tracés)`.

### Task 2: Section 1 — Matrice de confusion (gaussiennes déséquilibrées, ~35 min)

**Files:** Modify `machine_learning/td/07_evaluation_elan.ipynb`

**Interfaces:**
- Consumes : `make_blobs_imbalanced`, `MLP`, `plot_data`.
- Produces : `classify(Y: Mat, threshold: float = 0.5) -> Vec` (0./1., forme `(N,)`), `confusion(t, y) -> tuple[int, int, int, int]` ordre **(TP, FP, TN, FN)**, `accuracy(t, y) -> float`, `precision(t, y) -> float`, `recall(t, y) -> float`. `t` et `y` sont des étiquettes 0/1, acceptées en forme `(N,)` ou `(N, 1)` (aplatir).

- [ ] **Step 1:** `## 1. Évaluer un classifieur : la matrice de confusion` : markdown rappelant TP/FP/TN/FN (tableau 2×2), formules accuracy / précision / rappel, convention précision = 0 si aucun positif prédit. Cellule fournie : données (≈ 100 train, 1000 val), `plot_data`.
- [ ] **Step 2:** Exercice 1 — `classify` et `confusion`. Vérification `check_confusion` en égalité exacte :
  ```python
  t = np.array([1, 1, 1, 0, 0, 0, 0, 0.])
  y = np.array([1, 0, 0, 1, 0, 0, 0, 0.])
  assert confusion(t, y) == (1, 1, 5, 2)
  assert confusion(t.reshape(-1, 1), y) == (1, 1, 5, 2)
  assert np.array_equal(classify(np.array([[0.2], [0.5], [0.9]])), np.array([0., 1., 1.]))  # seuil inclusif : >= 0.5
  ```
- [ ] **Step 3:** Exercice 2 — `accuracy`, `precision`, `recall` (en s'appuyant sur `confusion`). Vérification exacte sur les mêmes `t`, `y` : `accuracy == 6/8`, `precision == 0.5`, `recall == 1/3`, et pour `y0 = np.zeros(8)` : `precision(t, y0) == 0.0`, `recall(t, y0) == 0.0`, `accuracy(t, y0) == 5/8`, sans warning (`with warnings.catch_warnings(): warnings.simplefilter("error")`).
- [ ] **Step 4:** Exercice 3 — comparer sur la validation le classifieur « toujours négatif » et un `MLP([2, 16, 1])` entraîné (réglages à choisir pour qu'il détecte une partie des positifs) : afficher les quatre comptes et les trois métriques. Lecture guidée : accuracy proche, rappel très différent. Corrigé dans `# BEGIN`/`# END`.
- [ ] **Step 5:** Exercice 4 — faire varier le seuil (ex. 0.1 → 0.9) et tracer précision et rappel en fonction du seuil ; question : lequel privilégier pour un détecteur de fraude ? Réponse en cellule `# TOCLEAR` (cf. Global Constraints).
- [ ] **Step 6:** `check_notebooks.py` sur le notebook → succès ; commit `td07: section 1 — matrice de confusion`.

### Task 3: Section 2 — Courbes d'apprentissage (lunes, sans élan, ~30 min)

**Files:** Modify `machine_learning/td/07_evaluation_elan.ipynb`

**Interfaces:**
- Consumes : `make_moons`, `MLP.fit`, `plot_curves`.
- Produces : `split_train_val_test(X: Mat, t: Mat, n_train: int, n_val: int, seed: int = 0) -> tuple[Mat, Mat, Mat, Mat, Mat, Mat]` (ordre `X_tr, t_tr, X_va, t_va, X_te, t_te`, permutation aléatoire puis découpage, le reste = test) ; variables globales `X_tr, t_tr, X_va, t_va, X_te, t_te` (lunes) et `hist_plain` réutilisées en section 3 ; constantes `SIZES = [2, 32, 32, 1]`, `LR = 0.5`, `EPOCHS` (≈ 5000, à régler).

- [ ] **Step 1:** `## 2. Courbes d'apprentissage` : markdown sur le protocole train / validation / test (validation = régler, test = juger une fois) et les quatre profils de courbes.
- [ ] **Step 2:** Exercice 5 — `split_train_val_test`. Vérification : sur `X = np.arange(20.).reshape(10, 2)`, `t = np.arange(10.).reshape(-1, 1)`, `n_train=5, n_val=3` → formes (5,2),(5,1),(3,2),(3,1),(2,2),(2,1) ; l'union des `t` triée vaut `np.arange(10.)` (aucun point perdu ni dupliqué) ; chaque `X` est aligné avec son `t` (`X[:, 0] / 2 == t.ravel()`).
- [ ] **Step 3:** Cellule fournie : lunes (60 train, ~500 val, ~500 test ; réglages de départ de la spec), entraînement `MLP(SIZES, seed=0).fit(..., lr=LR, epochs=EPOCHS, X_val=X_va, t_val=t_va)` → `hist_plain` ; `plot_curves({"μ=0": hist_plain})` en perte puis en taux d'erreur ; `plot_decision`.
- [ ] **Step 4:** Exercice 6 — lecture : calculer l'epoch du minimum de validation (`np.argmin`) et la valeur ; questions en markdown : où est le sous-apprentissage, où commence le surapprentissage, que fait le train pendant ce temps, perte et taux d'erreur racontent-ils la même chose ? Réponses (chiffrées, recopiées des sorties) en cellules `# TOCLEAR`.
- [ ] **Step 5:** `check_notebooks.py` → succès ; commit `td07: section 2 — courbes d'apprentissage`.

### Task 4: Section 3 — Élan (lunes, ~50 min)

**Files:** Modify `machine_learning/td/07_evaluation_elan.ipynb`

**Interfaces:**
- Consumes : `MLP`, `SIZES`, `LR`, `EPOCHS`, données lunes, `hist_plain`, `confusion`/`accuracy`/`precision`/`recall`, `classify`.
- Produces : `class MLPMomentum(MLP)` avec `__init__(self, sizes: list[int], seed: int = 0, momentum: float = 0.9)`, attributs `momentum`, `vWs`, `vbs` (zéros, mêmes formes que `Ws`/`bs`), `step(self, X: Mat, t: Mat, lr: float) -> None` surchargée ; `best_epoch(history: dict[str, list[float]]) -> int` (indice du minimum de `history["val"]`) ; `hists: dict[str, dict]` pour μ ∈ {0, 0.9, 0.99}.

- [ ] **Step 1:** `## 3. L'élan à travers les courbes` : rappel de la règle (formule du cours) et de l'image de la bille.
- [ ] **Step 2:** Exercice 7 — `MLPMomentum.step`. Vérification `check_momentum` :
  - `MLPMomentum([2, 3, 1], seed=1, momentum=0.0)` et `MLP([2, 3, 1], seed=1)` : après `fit(Xc, tc, lr=0.5, epochs=3)` sur un petit batch fixé, poids égaux (`np.allclose`, `atol=1e-12`) ;
  - avec `momentum=0.9` après 2 étapes : poids égaux à des tableaux de référence littéraux (générés une fois avec le corrigé, recopiés dans la cellule, `atol=1e-8`) **et** différents de ceux du `MLP` sans élan ;
  - `vWs[l].shape == Ws[l].shape` pour tout `l`.
- [ ] **Step 3:** Exercice 8 — entraîner μ = 0.9 et μ = 0.99 dans les mêmes conditions que `hist_plain` (même graine, `LR`, `EPOCHS`, données) ; `plot_curves(hists)` en perte et en erreur ; tableau imprimé : pour chaque μ, epoch et valeur du minimum de validation, perte val finale. Questions : facteur d'accélération, valeur du minimum, quand commence le surapprentissage, que se passe-t-il pour μ = 0.99. Réponses chiffrées en cellules `# TOCLEAR` ; message clé « l'élan change la vitesse, pas la destination ».
- [ ] **Step 4:** Exercice 9 — `best_epoch` puis early stopping : choisir le μ et l'epoch sur la validation, réentraîner un nouveau modèle avec `epochs = best_epoch(h) + 1`, évaluer **une seule fois** sur le test (matrice de confusion + 3 métriques). Vérification : `best_epoch({"val": [3., 1., 2.]}) == 1` ; la perte de validation du modèle réentraîné vaut exactement `min(h["val"])` (`==`, déterminisme).
- [ ] **Step 5:** `check_notebooks.py` → succès ; commit `td07: section 3 — élan et early stopping`.

### Task 5: Section 4 — Spirales, bonus, conclusion (~20 min)

**Files:** Modify `machine_learning/td/07_evaluation_elan.ipynb`

**Interfaces:**
- Consumes : `make_spirals`, `split_train_val_test`, `MLP`, `MLPMomentum`, `plot_curves`, `plot_decision`, `best_epoch`.

- [ ] **Step 1:** `## 4. Traverser un plateau : les spirales` — Exercice 10 : split (≈ 120 train), entraîner μ = 0 et μ = 0.9 (mêmes conditions), tracer ; question : combien d'epochs sur le plateau dans chaque cas, pourquoi l'élan aide (gradients faibles mais de même signe qui s'accumulent). Frontières de décision des deux modèles à `best_epoch`.
- [ ] **Step 2:** `## Bonus` (markdown + cellules libres, pas de vérification obligatoire) : `lr` trop grand (ex. ×4 / ×8) avec et sans élan → oscillations / divergence ; autres μ ; seuil de décision sur les lunes.
- [ ] **Step 3:** `## Conclusion` : 4–6 puces reprenant les notions de la spec (§ Notions à retenir).
- [ ] **Step 4:** `check_notebooks.py` → succès ; commit `td07: section 4 — spirales, bonus, conclusion`.

### Task 6: Vérification d'ensemble du notebook

**Files:** Modify `machine_learning/td/07_evaluation_elan.ipynb` (corrections seulement)

- [ ] **Step 1:** `uv run python scripts/prepare_notebooks.py machine_learning/td/07_evaluation_elan.ipynb <scratchpad>/07_apercu.ipynb` ; relire l'aperçu : chaque `# TODO` a un corps compréhensible, aucune solution ne fuit (`grep -c TOCLEAR` sur l'aperçu = 0), aucune cellule de vérification n'est masquée, les énoncés ne référencent pas d'état antérieur.
- [ ] **Step 2:** Exécuter le corrigé et confronter chaque chiffre cité (énoncés, réponses, conclusion) aux sorties ; corriger les écarts.
- [ ] **Step 3:** Mesurer la durée totale d'exécution (`time uv run scripts/check_notebooks.py machine_learning/td/07_evaluation_elan.ipynb`) ; si > ~60 s, réduire `EPOCHS` / taille de validation et revérifier l'étape 2.
- [ ] **Step 4:** Vider les sorties (`uv run python scripts/notebooks.py --td machine_learning/td clear` si c'est la pratique du repo pour les autres TD — vérifier sur `03_backpropagation.ipynb` si les sorties sont versionnées, et faire pareil) ; commit `td07: relecture et vérification`.

### Task 7: Figures et chapitre « 6 - Évaluer un modèle »

**Files:**
- Create: `machine_learning/scripts/figures_07_evaluation.py`
- Create: `machine_learning/assets/07-confusion.png`, `07-train-val-test.png`, `07-courbe-apprentissage.png`, `07-elan-lunes.png`
- Create: `machine_learning/6 - Évaluer un modèle.md`

**Interfaces:**
- Consumes : mêmes générateurs, MLP et réglages que le notebook (copiés, mêmes graines) pour que les chiffres du chapitre et du TD coïncident.

- [ ] **Step 1:** Écrire le script (exécutable par `uv run python machine_learning/scripts/figures_07_evaluation.py`, écrit les 4 PNG dans `machine_learning/assets/`) :
  - `07-confusion.png` : deux matrices 2×2 annotées côte à côte, « toujours négatif » vs MLP sur les gaussiennes déséquilibrées, avec accuracy / précision / rappel en titre ;
  - `07-train-val-test.png` : schéma en barre du découpage (train → entraîne, validation → règle, test verrouillé → juge) ;
  - `07-courbe-apprentissage.png` : courbe train/val des lunes μ = 0 avec zones annotées (sous-apprentissage, bon régime, surapprentissage) et epoch d'arrêt ;
  - `07-elan-lunes.png` : val + train pour μ = 0 et 0.9, minima marqués.
  Lancer le script, ouvrir chaque PNG pour vérifier la lisibilité.
- [ ] **Step 2:** Écrire le chapitre : frontmatter sur le modèle de `1 - Qu'est-ce qu'apprendre ?.md` (`titre`, `cours: "[[Entrypoint]]"`, `partie`, `statut: draft`, `Contexte: |-`), callout `[!abstract]` d'objectif, puis 4 sections (une par notion de la spec), chacune avec sa figure `![[07-....png]]` et un callout de synthèse ; renvois `[[1 - Qu'est-ce qu'apprendre ?]]` (hold-out) et `[[4 - Réseaux de neurones à plusieurs couches]]` (élan) ; mention du TD 07. Chiffres identiques à ceux du notebook.
- [ ] **Step 3:** `uv run scripts/check_snippets.py` → succès.
- [ ] **Step 4:** Commit `cours(eval): chapitre 6 - Évaluer un modèle + figures 07-*`.
