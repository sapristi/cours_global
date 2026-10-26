# Cours + TD « Support Vector Machines » — conception

Date : 2026-10-26. Cours : `machine_learning/`.

## Intention

Une première version (cours `5 - Support Vector Machines.md`, TD
`td/05_svm.ipynb`, plan et spec associés) a été produite puis jugée
insatisfaisante par l'enseignant : elle est supprimée et **on repart de zéro**.
Ne pas s'en inspirer (ne pas la relire via `git show`).

Objectif : faire comprendre **pourquoi** le SVM choisit une séparation
particulière (la marge maximale), **comment** on l'écrit comme un problème
d'optimisation, et le relier à ce que les étudiants connaissent déjà
(perceptron, descente de gradient). La résolution formelle (Lagrangien, dual,
KKT) est **hors programme** : le problème quadratique est posé et « admis
résolu par des solveurs dédiés ».

## Ce que les étudiants doivent retenir (validé par l'enseignant)

1. **Données séparables** : le perceptron s'arrête sur *une* droite séparatrice
   quelconque, qui dépend de l'ordre de présentation et de l'initialisation, et
   frôle souvent des points. Le SVM donne *la* droite de marge maximale, unique,
   qui généralise mieux.
2. **Données bruitées** (quelques points du mauvais côté) : le perceptron ne
   converge pas et oscille ; le SVM à marge souple reste stable.
3. **Régularisation** : `λ` (ou `C`) arbitre entre marge large et erreurs
   d'entraînement.

## Livrables

1. Chapitre de cours : `machine_learning/5 - Support Vector Machines.md`
   (vault Obsidian ; conventions du `AGENTS.md` racine : frontmatter YAML au
   même format que `3- Données non linéairement séparables.md`, callouts,
   embeds `![[assets/...]]`).
2. Notebook corrigé : `machine_learning/td/05_svm.ipynb`. Blocs solution
   `# BEGIN` / `# END`, doit passer `uv run scripts/check_notebooks.py`.
   Utiliser le skill `notebook_exercises` pour la rédaction.
3. Figures du chapitre, générées par un script versionné
   `machine_learning/scripts/figures_svm.py` (choix de Claude ; aucun dossier de
   scripts de figures n'existe aujourd'hui), sortie dans
   `machine_learning/assets/05-svm-*.png`.
4. Les anciennes figures `machine_learning/assets/08-*.png` (issues de la
   version supprimée) sont retirées si plus aucun fichier ne les référence
   (choix de Claude).

## Contraintes

- Séance de **1 h 15** : ~25 min de cours (projeté / tableau), ~50 min de TD.
  Le TD doit tenir en ~45 min pour un étudiant moyen ; le reste en bonus.
- 4e année post-bac. Python / numpy / matplotlib uniquement (pas de sklearn).
- Contenu en français.
- Notations (`machine_learning/AGENTS.md`) : cible `t`, sortie `y`, score
  `z = w·x + b`, poids `w`, biais `b`, pas `lr` en code / `η` au tableau.
  **Cibles ±1** pour tout le chapitre et le TD (à signaler explicitement : le
  TD01 utilisait 0/1). Biais en `+b` comme au TD02.
- Pas de résolution formelle ; pas de noyaux en exercice.

## Cours (~25 min)

Plan imposé, contenu détaillé laissé au rédacteur :

1. **Intuition** — Sur un jeu séparable, plusieurs droites séparent
   parfaitement (figure : 2-3 séparateurs dont un « limite » qui frôle un
   point). Laquelle préférer ? Celle qui laisse le plus de place de chaque côté :
   un nouveau point un peu bruité reste bien classé. Définition informelle de la
   **marge** et des **vecteurs de support**.
2. **Formalisation** — Distance d'un point à l'hyperplan
   `|w·x + b| / ‖w‖` (donnée, avec un dessin). Classement correct ⇔
   `t_i (w·x_i + b) > 0`. Normalisation `min_i t_i (w·x_i + b) = 1` ⇒ marge
   `1/‖w‖`. Problème :
   `min ½‖w‖²` s.c. `t_i (w·x_i + b) ≥ 1`. C'est un problème de programmation
   quadratique (objectif quadratique, contraintes linéaires) : on dit qu'il a
   une solution unique et que des solveurs existent, **sans** les détailler.
3. **Marge souple** — Données non séparables / bruitées : variables d'écart
   `ξ_i ≥ 0`, `t_i (w·x_i + b) ≥ 1 − ξ_i`, objectif `½‖w‖² + C Σ ξ_i`. Lecture
   du rôle de `C`. Réécriture sans contraintes avec la **perte hinge**
   `max(0, 1 − t_i z_i)` :
   `E(w, b) = λ/2 ‖w‖² + 1/N Σ max(0, 1 − t_i (w·x_i + b))`
   (λ ≈ 1/(NC), à mentionner sans démonstration). Cette forme se minimise par
   **descente de gradient** : donner le (sous-)gradient, c'est ce qu'on code en TD.
4. **Lien avec le perceptron** — La règle de Rosenblatt revient à une descente
   de gradient stochastique sur `max(0, −t z)`. Le SVM = perceptron + « 1 »
   (on exige une marge) + régularisation `‖w‖²` (on maximise la marge). Figure
   des deux pertes en fonction de `t z`.
5. **Ouverture** — Une phrase : remplacer `x` par `Φ(x)` (cours 3) donne un SVM
   non linéaire ; l'« astuce du noyau » permet de le faire efficacement (partie 9).

Callouts `[!abstract]` objectif en tête, `[!note] À retenir` en fin.

## TD (~50 min)

Fil conducteur : un même jeu 2D, deux classes gaussiennes **séparables avec un
écart étroit**, peu de points d'entraînement (≈ 20-30) et un gros jeu de test
(≈ 500), pour que la différence de généralisation soit visible. Le
constructeur choisit graines et paramètres pour que les effets ci-dessous
soient nets et reproductibles.

**Fourni (non à coder)** : imports, générateur de données (cibles ±1),
fonction d'affichage (points, frontière `z = 0`, marges `z = ±1` en
pointillés, vecteurs de support entourés en option), et une classe
`Perceptron` vectorielle (cibles ±1, biais `+b`, ordre des points mélangé selon
une graine, renvoie le nombre d'époques et l'historique d'erreurs par époque).
Les étudiants ont déjà codé le perceptron au TD01 : on ne le refait pas.

Exercices (ordre imposé, durées indicatives) :

1. **Marge géométrique** (~5 min) — coder
   `marge(w, b, X, t) = min_i t_i (w·x_i + b) / ‖w‖` (négative si un point est
   mal classé). Check sur un cas calculable à la main.
2. **Perceptron, plusieurs runs** (~7 min) — entraîner le perceptron fourni
   avec 4-5 graines différentes, afficher les droites, la marge et l'accuracy
   test de chacune. Question d'observation.
3. **SVM par descente de gradient** (~15 min, cœur du TD) — classe `SVM`
   avec `scores(X)`, `predict(X)`, `loss(X, t)`, `gradient(X, t)` (renvoie
   `(dw, db)`), `fit(X, t, lr, epochs)` (descente de gradient **batch**,
   vectorisée numpy, historique de la perte). Checks : valeur de `loss` sur un
   cas à la main, `gradient` comparé à des différences finies, `fit` qui fait
   baisser la perte.
4. **Comparaison sur données séparables** (~8 min) — SVM vs les runs du
   perceptron : marge, accuracy test, figure avec marges et vecteurs de support
   (points tels que `t z ≤ 1 + ε`). La descente de gradient approche la marge
   maximale sans l'atteindre exactement : le dire.
5. **Données bruitées** (~7 min) — quelques étiquettes d'entraînement
   inversées. Tracer l'erreur par époque du perceptron (oscille, ne converge
   pas) et la perte du SVM (décroît et se stabilise) ; comparer les frontières
   et l'accuracy test.
6. **Effet de λ** (~5 min) — 3 valeurs de `λ` sur les données bruitées, figure
   côte à côte ; question : que devient la marge, combien de vecteurs de support ?

**Bonus** : cercles concentriques (cours 3) + `Φ(x) = (x1, x2, x1² + x2²)` +
le même `SVM` linéaire ; frontière affichée dans le plan d'origine.

Questions d'observation : réponse du corrigé dans une cellule markdown `# TOCLEAR`.

## Non-objectifs / anti-objectifs

- Pas de Lagrangien, dual, KKT, SMO, solveur QP.
- Pas de noyaux en exercice (bonus Φ explicite seulement).
- Pas de multi-classes.
- Ne pas modifier les autres chapitres ni les autres TD.
- Échec même si ça tourne : un TD qui dépasse nettement 50 min, ou dont les
  figures ne montrent pas clairement les trois points à retenir.

## Laissé au constructeur

Graines, tailles de jeux, `lr`, nombre d'époques, valeurs de `λ` ; style
précis des figures ; formulation des questions et indices ; découpage fin des
cellules.
