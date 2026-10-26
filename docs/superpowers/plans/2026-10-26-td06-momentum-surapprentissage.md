# TD 06 ML — Élan et surapprentissage : plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Créer un nouveau TD autonome `machine_learning/td/06_momentum_surapprentissage.ipynb` (≈3h) qui analyse, sur des cas concrets et via des courbes d'apprentissage train/test, ce que l'élan (momentum) apporte — et ne apporte pas — à la généralisation.

**Architecture:** Un nouveau fichier notebook, autonome (imports + définitions d'outils fouries en tête : `MLP`, `MLPMomentum`, `gen_2d`, `plot_history` — copies fidèles de TD 03, sans blocs `# BEGIN`). Quatre exercices (Ex. 1 à 4) + bilan. `03_backpropagation.ipynb` n'est **pas** modifié.

**Tech Stack:** numpy, matplotlib (aucune nouvelle dépendance ; pas de plotly).

**Spec:** conversation 2026-10-26 (attendus A1–A3 / B1–B3, révisés après spike `/tmp/opencode/spike/`) ; chiffres épinglés ci-dessous issus du spike.

## Global Constraints

- Notebook = **corrigé** : solutions entre `# BEGIN` / `# END`. Outils fournis (classes, générateurs, split) en code libre, SANS `# BEGIN`, pour rester dans la version étudiante.
- Autonomie : version étudiante (build JupyterLite, solutions retirées) doit être exécutable sans aucun notebook précédent — tout ce dont un exercice a besoin est défini en tête ou dans son propre énoncé.
- Notation (AGENTS.md machine_learning) : cible `t`/`T`, sortie `y`/`Y` — jamais `y` pour la cible.
- Grain identique entre variantes μ (comparaisons appariées) ; graines figées pour que les étudiants retrouvent les courbes du corrigé.
- Ne pas toucher à `03_backpropagation.ipynb` ni aux dossiers `.obsidian/`. **Hors périmètre de cette session mais à faire plus tard : la section 8 / Ex. 9 (« Élan ») du TD 03 sera supprimée** (déplacée/absorbée par le TD 06).
- Runtime total du notebook (check) : cible < ~10 min.

## Review Focus

- **Divergence affichable** : le cas `lr=1.3e-3` sans élan diverge vers inf/nan ; le code corrigé doit produire une figure lisible (échelle linéaire, valeurs > 50 remplacées par nan), jamais un plot cassé par NaN sur échelle log.
- **Version étudiante** : les blocs `# BEGIN` ne contiennent que des instructions que l'étudiant peut écrire ; les définitions réutilisables (`gen_vallee`, `fit_mini`...) sont soit fournies en tête, soit demandées dans l'énoncé avec signature exacte.
- **Taille des runs** : Ex. 3 = 2 runs de 12000 epochs obligatoires + 3 configs de mini-challenge ; l'indiquer explicitement pour ne pas balayer 10 configs.
- **Parité des graines** : `seed=0` modélé et split seed `2` pour Ex. 3, `seed=3` pour la génération vallée.
- **Ne pas nuancer à moitié** : les énoncés des Ex. 3-4 ne donnent jamais la conclusion d'avance — les corrigés constatent après coup ce que les courbes montrent.

## Valeurs épinglées (issues du spike)

| Cas | Dataset | Réseau | lr | epochs | Résultat attendu (μ=0 vs μ=0.9) |
|---|---|---|---|---|---|
| Ex. 1 | `gen_2d(noise=0.1)`, split 400/100 (perm. seed 1) | `[2,16,16,1]` tanh | 0.2 | 20000 | train fin 0.0050 → 0.0042 ; te_min 0.0068 @19998 → 0.0078 @3549, te_fin 0.0068 → 0.0109 |
| Ex. 2 | `gen_vallee(n=200, scale=80, noise=0.05, seed=3)` linéaire : `t = 0.5·x1 + 0.02·x2 + ε` | `[2,1]` | 7e-4 | 6000 | seuil 0.005 atteunt ep. 4858 → 485 |
| Ex. 2 (divergence) | idem | `[2,1]` | 1.3e-3 | 2000 | sans élan loss → inf/nan ; avec élan converge ep. 261 |
| Ex. 2 (trajectoire) | idem | `[2,1]` | 7e-4 | 2500 (pas d'échantillonnage : 20) | départ (0.02, −0.065) → optimum (0.5, 0.02) ; dépassement bref sur l'axe raide avec élan |
| Ex. 3 | `gen_2d(noise=0.4)`, split 100/400 (perm. seed 2) | `[2,16,16,1]` tanh | 0.05 | 12000 | train fin 0.0444 → 0.0024 ; te_min 0.0947 @168 → 0.1099 @95 ; te_fin 0.1546 → 1.2204 |
| Ex. 3 (challenge) | idem — μ=0.5/lr=0.02 égalise te_min 0.0949 @215 ; μ=0.9/lr=0.02: 0.1033 @126 ; μ=0.9/lr=0.01: 0.0996 @216. AUCUNE config μ=0.9 ne bat 0.0947 | | | | |
| Ex. 4 | `gen_2d(noise=0.1)`, split 100/400 | `[2,16,16,1]` tanh | 0.1, batch=16 | 300 | per-batch tardif : std ~0.005 → ~0.017 avec élan (bruit AMPLIFIÉ) ; te par epoch : μ=0.9 plafonne plus haut |

## Tasks

### Task 1: Squelette et outils du nouveau TD

**Files:**
- Create: `machine_learning/td/06_momentum_surapprentissage.ipynb`

**Interfaces:**
- Produces : pour les tasks suivantes — `MLP(sizes, activation, output_activation, seed)`, `MLPMomentum(..., momentum)`, `gen_2d(n, noise, seed)`, `plot_history(history, ax)`, alias `Vec`/`Mat`, `split(X, t, n_train, seed) -> (Xtr, ttr, Xte, tte)`.

- [ ] **Step 1: Md titre + objectifs + plan.** Titre `# TD 6 — Élan et surapprentissage : lire les courbes d'apprentissage`. Objectifs (attendus A1–A3, B1–B3 reformulés : distinguer optimisation/généralisation, reconnaître les régimes d'une courbe test, prédire-avant-de-mesurer l'effet de μ, distinguer zigzag systématique et bruit de batch) ; plan de séance (4 exercices + bilan, ≈3h) ; rappel `v_l ← μ v_l + η ∂E/∂W_l`.
- [ ] **Step 2: Code imports** : `numpy`, `matplotlib.pyplot`, alias `Vec`/`Mat`.
- [ ] **Step 3: Code outils** (copie fidèle de TD 03, sans `# BEGIN`) : `sigmoid`, `sigmoid_prime`, `tanh_prime`, `ACTIVATIONS`, `MLP` (avec `forward`, `backward`, `step`, `fit_batch`, `loss`, `predict`), `MLPMomentum` (héritage + `step` avec élan), `gen_2d`, `plot_history`, plus un helper `split(X, t, n_train, seed)` (permutation + slicing).
- [ ] **Step 4:** Commit.

### Task 2: Ex. 1 — premier contact avec/sans élan (lecture guidée)

**Files:**
- Modify: `machine_learning/td/06_momentum_surapprentissage.ipynb` — insertion md/code/md

**Interfaces:**
- Consumes: outils Task 1.
- Produces: rien.

- [ ] **Step 1: Md énoncé.** Jeu 2D `sin(x1)·cos(x2)` (bruit 0.1, 400 train / 100 test), réseau `[2,16,16,1]` tanh, `lr=0.2`, `epochs=20000`. AVANT tout entraînement, deux questions de pronostic (a) tempo train, (b) forme de la courbe test. Puis entraîner μ=0 (`MLP`) et μ=0.9 (`MLPMomentum`), même graines, même lr.
- [ ] **Step 2: Code corrigé** (BEGIN) : split (seed 1) en image de l'outil `split`, les 2 runs, `plot_history(h)` côte à côte (2 subplots, y log).
- [ ] **Step 3: Md lecture guidée (corrigé).** Constats : train ≈ pareil ; te_min 0.0068 @19998 vs 0.0078 @ ep.3549 avec remontée à 0.0109. «Sur ce jeu peu bruité et riche (400 exemples), l'élan ne dégrade pas grand-chose, mais il fait BOUGER la courbe test — les exercices suivants amplifient ce phénomène.»
- [ ] **Step 4: Vérification** (helper td03_core : hist finies, valeurs du tableau Review Focus). Commit.

### Task 3: Ex. 2 — la vallée mal conditionnée

**Files:**
- Modify: `machine_learning/td/06_momentum_surapprentissage.ipynb` — insertion md/code/md

**Interfaces:**
- Consumes: outils Task 1.
- Produces: `gen_vallee(n=200, scale=80.0, noise=0.05, seed=3) -> (X, t)`.

- [ ] **Step 1: Md énoncé.** Décrire `gen_vallee` (dans le corrigé) : deux entrées d'échelles très différentes, aucune normalisation ; réseau linéaire `[2,1]` (un poids par axe, pas d'activation). Questions : (a) prédire sans lancer ce que fait lr=7e-4 avec/sans élan ; (b) mesurer l'accélération **par les epochs jusqu'à un seuil** (fonction à écrire : premier index où train < 0.005) ; (c) monter lr à 1.3e-3 et observer le sans-élan ; (d) option corrigée : trajectoire des poids sur le paysage de perte ; (e) discussion : que change la standardisation des entrées (test rapide : l'effet s'évanouit).
- [ ] **Step 2: Code corrigé comparaison (BEGIN).** `gen_vallee` (signature ci-dessus, `t = 0.5·x1 + 0.02·x2 + ε(0, 0.05)`), runs `lr=7e-4, epochs=6000, seed=0`, fonction `epochs_to_threshold(hist, thr=0.005)` ; figure 2 subplots log, annotations des epochs-seuils (4858 / 485).
- [ ] **Step 3: Code corrigé divergence (BEGIN).** `lr=1.3e-3, epochs=2000` : sans élan la loss diverge → échelle **linéaire**, valeurs > 50 remplacées par `np.nan` (courbe sort du cadre = lisible) ; avec élan converge. Titre annoté du résultat de chaque côté.
- [ ] **Step 4: Code corrigé trajectoire (BEGIN, option fournie).** Paysage `E(w) = 0.5·mean((X·w − t)²)` sur grille (-0.65..0.65 × -0.09..0.09), contourf, trajectoire (poids tous les 20 epochs, lr=7e-4, μ=0 vs 0.9), 2 subplots.
- [ ] **Step 5: Md réponses attendues (corrigé).** Zigzag systématique sur l'axe raide ; l'élan MoyENNE les gradients → accélère le long de l'axe facile, amortit le dépassement (cf. dart issu du dépassement bref sur w2) ; standardiser supprime le malconditionnement (et l'intérêt de l'élan pour ce cas).
- [ ] **Step 6: Vérification** (helper td03_core : seuils 4858/485 ; divergence : loss > 50 sinon nan pour μ=0 ; trajectoire : fin à ±0.02 de l'optimum). Commit.

### Task 4: Ex. 3 — le bruit mémorisé (cœur de l'analyse)

**Files:**
- Modify: `machine_learning/td/06_momentum_surapprentissage.ipynb` — insertion md/code/md

**Interfaces:**
- Consumes: `gen_2d`, `MLP`, `MLPMomentum`, `split`.
- Produces: rien.

- [ ] **Step 1: Md énoncé.** Même fonction 2D, bruit ×4 (0.4), seulement 100 exemples d'entraînement, réseau `[2,16,16,1]` tanh, `lr=0.05`, `epochs=12000`, avec/sans élan. AVANT les courbes : (a) pronostic sur l'écart train/test pour chaque variante ; (b) définir ce qu'une courbe de généralisation idéale devrait faire au point bas de test.
- [ ] **Step 2: Code corrigé (BEGIN).** split (perm. seed 2), 100 train / 400 test, les 2 runs (seed modèlee 0), figure 2 subplots `plot_history`.
- [ ] **Step 3: Md corrigé-lecture.** Constats chiffrés (te_min 0.0947 @168 vs 0.1099 @95 ; te_fin 0.1546 vs 1.2204 ; train fin 0.0444 vs 0.0024) + formulation ouverte : « l'élan accélère l'optimisation de TOUT, y compris l'apprentissage du bruit — sur ce cas il aggrave le surapprentissage terminal sans améliorer le point bas test ».
- [ ] **Step 4: Md + code mini-challenge.** « Trouvez une config avec élan qui batte te_min=0.0947 du sans-élan, ou expliquez pourquoi vous abandonnez. » Corrigé : 3 essais (μ=0.9, lr∈{0.02, 0.01} et μ=0.5, lr=0.02, 12000 epochs), conclusion : te_min ∈ [0.0949, 0.1033], jamais mieux ; c'est le résultat.
- [ ] **Step 5: Vérification** (helper : te_min/te_fin des 3 configs ≈ valeurs épinglées). Commit.

### Task 5: Ex. 4 (optionnel) — mini-batchs : l'élan lisse-t-il vraiment ?

**Files:**
- Modify: `machine_learning/td/06_momentum_surapprentissage.ipynb` — insertion md/code/md

**Interfaces:**
- Consumes: `gen_2d`, `MLP`, `MLPMomentum`, `split`.
- Produces: `fit_mini(model, X, t, Xte, tte, batch_size, lr, epochs, seed=0)` écrit par l'étudiant.

- [ ] **Step 1: Md énoncé.** Le folklore : « l'élan lisse les oscillations ». À vérifier : écrire `fit_mini` (mélange des indices à chaque epoch, sous-blocs de `batch_size`, `model.step` sur chaque bloc, historique : loss du bloc + loss epoch train/test — signature fournie), puis entraîner μ=0 vs μ=0.9 (`batch=16, lr=0.1, epochs=300`, split 100/400 du jeu bruit=0.1) et dire si le folklore est vérifié.
- [ ] **Step 2: Code corrigé (BEGIN).** Référence de `fit_mini` ; les 2 runs ; figure 2×2 (perte par mini-batch μ=0/0.9 ; courbes par epoch μ=0/0.9).
- [ ] **Step 3: Md corrigé-lecture.** Contre-exemple : à μ=0.9 le bruit de batch est **amplifié** (std tardif ~0.017 vs ~0.005), la courbe test plafonne plus haut. Nuance : l'élan accumule les gradients systématiques (Ex. 2, zigzag déterministe) mais retient aussi chaque composante aléatoire — le folklore est vrai pour le zigzag, faux pour le bruit de SGD à ce régime.
- [ ] **Step 4: Vérification** (helper : les 4 hist finies, std tardif ordre 0.005 vs 0.017). Commit.

### Task 6: Bilan

**Files:**
- Modify: `machine_learning/td/06_momentum_surapprentissage.ipynb` — md bilan en fin de notebook

**Interfaces:**
- Consumes: les 4 exercices.
- Produces: rien.

- [ ] **Step 1: Md « Bilan ».** Tableau constats (train / test / interprétation, une ligne par exercice, valeurs du corrigé) + deux questions de synthèse à rédiger : (a) « En une phrase chacun : ce que l'élan garantit, ce qu'il ne garantit pas » ; (b) « À quelles conditions un couple de courbes train/test permet-il de conclure à un effet de l'élan sur la généralisation ? » (graine unique ? pas unique ? plusieurs graines ?) + mention `μ ∈ {0.3, 0.5, 0.99}` sur la vallée comme ouverture bonus.
- [ ] **Step 2:** Commit.

### Task 7: Vérification finale et nettoyage

- [ ] **Step 1:** `uv run scripts/check_notebooks.py machine_learning/td/06_momentum_surapprentissage.ipynb --timeout 1800` — aucune cellule ne lève ; noter le runtime.
- [ ] **Step 2:** `uv run python scripts/notebooks.py --td machine_learning/td extract` puis `--td machine_learning/td clear` (sorties vidées, assets extraits — état du dépôt).
- [ ] **Step 3:** Commit final.
