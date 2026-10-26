# Design — Partie 8 du cours ML : Support Vector Machines (2h, cours + TD)

## Intention et contexte

Cours de machine learning, 4ᵉ année post-bac, 18h au total (voir `machine_learning/Entrypoint.md`).
La partie 8 du plan est « Support Vector Machines » (a. meilleure séparation linéaire, b. brèves notions
de programmation quadratique, c. considérations théoriques, d. projection dans un espace de dimension
infinie), suivie de la partie 9 « Machines à noyau ».

L'enseignant souhaite préparer **2 heures** consacrées aux SVM : définir les attendus, préparer le
module de cours et le TD d'application. La ligne directrice du cours : **léger sur le formalisme,
intuition d'abord**.

Pourquoi les SVM arrivent-ils à ce moment du cours : les parties précédentes ont tout préparé —

- partie 3 / TD01 : le perceptron trouve *un* séparateur, n'importe lequel, sans contrôle ;
- partie 4 : données non linéairement séparables, idée de projection $\Phi(x)$ ;
- partie 7 : surapprentissage, généralisation, régularisation.

Le problème que les SVM résolvent n'est donc pas « trouver un hyperplan séparateur » (déjà acquis),
mais « **choisir le bon** parmi tous les séparateurs qui marchent » : celui qui généralise le mieux.

## Objectifs (attendus) — ce que l'étudiant doit savoir faire à la fin

1. Expliquer en mots pourquoi un séparateur quelconque ne suffit pas (deux perceptrons valides,
   erreurs de test différentes) et sur quoi repose le critère du SVM (la marge).
2. Définir la marge, donner la distance d'un point à l'hyperplan, et **identifier les vecteurs supports
   sur un dessin** (et sur des données 2D concrètes).
3. Écrire et **commenter** le problème d'optimisation du SVM à marge dure
   $\min \frac12\|w\|^2$ sous contrainte $t_i(w^T x_i + b) \geq 1$ — le comprendre comme
   « marge maximale ⇔ $\|w\|$ minimal », pas le résoudre à la main.
4. Expliquer le rôle du solveur (programmation quadratique = boîte noire assumée) et lire sa sortie :
   $w$, $b$, et quels points déterminent la solution.
5. Expliquer en mots la marge souple : quand elle est nécessaire (bruit, point mal placé), l'idée du
   prix payé par point fautif (paramètre $C$), l'équilibre régularisation/erreurs.
6. Relier le tout à la partie 7 (train/test) : grande marge = bonne généralisation (énoncé admis
   et argumenté par intuition).
7. En application : implémenter un SVM approché (descente de gradient, hinge loss + régularisation),
   l'appliquer sur jeux linéaires et non linéaires (via $\Phi$ de la partie 4), et situer l'astuce
   noyau comme ouverture vers la partie 9.

## Ce qui a été décidé avec l'enseignant

- **Trois temps** : (1) l'intérêt / le problème du SVM, (2) comment ça marche, (3) une application TD.
- **Pas de multiplicateurs de Lagrange, pas de dual, pas de KKT** : jugés trop compliqués pour le
  public. Le solveur QP est présenté comme boîte noire (« il existe des solveurs qui rendent
  $(w, b)$ ») ; pas de dérivation.
- **Le TD implémente quand même un SVM**, mais version approximée : descente de gradient
  **échantillon par échantillon** (SGD, style TD01 — mise à jour par point, pas par lot) sur
  « hinge loss + $\lambda\|w\|^2$ » (régularisation). Validé par l'enseignant, avec la clause : la
  solution approchée peut différer légèrement de la solution exacte du QP — le cours le dit
  explicitement (le solveur exact existe, l'implémentation en approche l'idéal).
  **Parenté à souligner dans le TD** : en cibles $\pm 1$, la mise à jour du perceptron
  ($w \mathrel{+}= t_i x_i$) et celle du SVM partagent la même forme ; le SVM étend au-delà des
  points mal classés (tous les points fautifs au sens de la marge : $t_i(w^T x_i + b) < 1$) et
  ajoute le tir régularisant $-\lambda w$ (aspect « mémoire » du SVM : corriger mais ne pas
  charger $w$).
  **Convention fixée (appel du concepteur)** : dans le TD, $\lambda$ est la force de régularisation
  (objectif = hinge + $\frac{\lambda}{2}\|w\|^2$, gradient pris échantillon par échantillon) :
  $\lambda$ grand ⇒ marge large ⇒ tolérant au bruit ; $\lambda$ petit ⇒ la frontière se plie au
  point fautif. Le cours, lui, ne manipule que le paramètre $C$ du standard (« prix payé par point
  fautif », qualitatif, sans formule) en le décrivant comme jouant un rôle symétrique inverse de
  $\lambda$ ($\lambda \approx 1/C$) ; jamais les deux conventions dans le même calcul.
- Le TD reste dans la philosophie du dépôt : **numpy pur** (aucune dépendance sklearn/scipy),
  exercices + corrigés.
- **Encodage** (décision enseignant) : tout le TD05 bascule en cibles $t \in \{-1, +1\}$ et biais
  $b$ (l'écriture marge $= 1/\|w\|$ ne tient qu'ainsi), avec une cellule de rappel/conversion
  $0/1 \to \pm 1$ plutôt que va-et-vient entre conventions.
- **Démo numérique du cours** (décision enseignant) : les $(w, b)$ affichés en section 3
  proviennent de l'implémentation approchée (préparée à part), présentés explicitement comme une
  **approximation** de ce que rendrait un solveur exact — cohérent avec ce que les étudiants
  construiront en TD.
- **Écho partie 7** (décision enseignant) : la partie 7 n'a traité que le découpage
  apprentissage/test, pas de théorie. Le renvoi reste donc simple (« au train/test de la partie 7 »)
  et la bonne généralisation de la marge est présentée comme un énoncé admis, argumentée par
  intuition ; aucune référence fantôme à la théorie de Vapnik déjà vue.
- **Publication** (décision enseignant) : travail direct sur `main`, pas de branche/PR ; le push
  reste à la main de l'enseignant ; ne pas toucher ni committer les fichiers en cours d'édition
  ailleurs (TD04, modules 2 et 3, `devoir/`).
- Même la partie sur la marge dure reste **géométrique et visuelle** : dessins, distances,
  vecteurs supports identifiés à l'œil ; une formule fondatrice seulement (minimisation de
  $\|w\|^2$ sous contraintes), lue et commentée, jamais dérivée.

## Périmètre des livrables

1. **Module de cours** `machine_learning/5 - Support Vector Machines.md`
   (numéro suivant les modules existants 1–4 ; c'est la partie 8 de l'Entrypoint).
2. **Notebook TD corrigé** `machine_learning/td/05_svm.ipynb` (numérotation continue 01–04).
3. **Figures du cours** dans `machine_learning/assets/`, nommées `08-<sujet>.png`
   (convention existante : les figures de la partie 4 sont `04-*.png`).

## Plan du cours (~70 min, ordre et minutage indicatifs)

1. **Le problème : quel séparateur choisir ?** (~20 min)
   Deux perceptrons entraînés sur les mêmes données (deux runs / deux ordres de présentation) donnent
   deux hyperplanes différents, avec des erreurs de test différentes. Conclusion : « un séparateur qui
   marche » ne suffit pas ; il manque un critère. Teaser dessiné : parmi les séparateurs infinis, les
   marges sont toutes différentes.
2. **La marge et les vecteurs supports** (~25 min)
   Distance d'un point à l'hyperplan $\frac{|w^T x + b|}{\|w\|}$ ; définition de la marge (distance du
   séparateur au point le plus proche) ; les vecteurs supports = les points qui s'appuient sur les
   sommets de la bande ; tous les autres points ne changent rien. Convention d'écriture
   $t_i(w^T x_i + b) \geq 1$ expliquée comme une normalisation (dans cette écriture la marge vaut
   $1/\|w\|$). Figure clé : deux séparateurs sur les mêmes données, le nôtre avec une marge minuscule,
   le meilleur avec une marge large.
3. **Le meilleur séparateur = un problème d'optimisation** (~15 min)
   Maximiser la marge ⇔ minimiser $\frac12\|w\|^2$ sous les contraintes ci-dessus. Rappel express de
   la programmation linéaire (prérequis), par analogie : « optimiser un objectif sous des
   contraintes » ; puis la programmation quadratique : « même exercice, mais la courbe à minimiser
   est une parabole » (résolution par une boîte noire, illustrée par une courbe 1D avec
   contraintes). Lecture de la solution du « solveur » : $(w, b)$ et la bande ; les points avec
   $t_i(w^T x_i + b) = 1$ sont les vecteurs supports. La démo numérique est produite par
   l'implémentation approchée (préparée hors séance) et présentée comme approximation de ce que
   rendrait un solveur exact.
4. **La marge souple (bruit et points mal placés) (~10 min)**
   L'image : un point mal placé dans la marge ne doit pas conditionner toute la frontière — on le
   tolère, mais chaque point fautif paie un prix (paramètre $C$, qualitatif, sans formule ; rôle
   inverse de la $\lambda$ du TD). Lien direct partie 7 : régularisation, équilibre entre largeur
   de marge et points fautifs.
5. **Considérations théoriques et ouverture (parties 8c, 8d, ~10 min)**
   Énoncé admis et argumenté par intuition : le séparateur à marge maximale généralise mieux —
   imposer une marge ≥ m rend bien plus rare l'ensemble des séparateurs possibles, donc moins de
   chance d'en coller un qui épouse le hasard de l'échantillon. Renvoi simple au découpage
   train/test vu en partie 7 (pas de théorie de fond). Ouverture : on peut projeter avec $\Phi$
   (partie 4) avant le SVM, et magie — des noyaux permettront de faire ça sans jamais calculer
   $\Phi$, encore mieux avec une dimension infinie (partie 9, teaser 2 min).
6. **Callout « À la fin, vous devez savoir faire »** en tête ou en pied du module, reprenant les
   attendus ci-dessus.

## Plan du TD (~50 min)

Format : suite logique d'exercices `> **Exercice n**` avec vérifications visuelles, corrigé inline
entouré des marqueurs `# BEGIN` / `# END`, numpy pur. Datasets réutilisés du TD01 (ET logique,
droite oblique, jeu séparable) et du TD04 (`anneau`, `XOR`), avec des jeux de test pour observer la
généralisation.

1. **Marge à la main** : sur quelques points 2D + un séparateur donné, calculer la marge ; classer
   visuellement des séparateurs par marge décroissante. Exercice « identifiez les vecteurs
   supports » sur des données 2D.
2. **Marge et généralisation** : entraîner le perceptron (reprise de TD01, code redonné,
   re-encodé $\pm 1$/biais $b$) sur un jeu séparable avec différents ordres/runs ; regarder les
   séparateurs obtenus et leurs **erreurs de test** ; constater que la marge prédit mieux la
   généralisation que l'erreur d'entraînement.
3. **Implémentation du SVM approché** : classe `SVM`, mise à jour **échantillon par échantillon**
   (style TD01, prolongement direct de la règle du perceptron : mêmes points fautifs au sens de la
   marge $t_i(w^T x_i + b) < 1$ + tir régularisant $-\lambda w$ ; cibles $\pm 1$, biais $b$).
   Écrire la mise à jour d'un point pas à pas, boucler sur les époques, vérifier la convergence.
   Affichage de la marge et des « quasi vecteurs supports » définis comme
   $0 < t_i(w^T x_i + b) < 1$ (ou équivalente, à définir proprement dans le notebook).
4. **Marge dure contre marge souple (bruit)** : injecter un point mal placé ou du bruit ; comparer
   $\lambda$ grand (frontière stable, le point fautif est ignoré, marge large) contre $\lambda$
   petit (la frontière se plie au point fautif) ; constater le compromis tolérance/rigueur.
5. **Application non linéaire** : sur le dataset `anneau` du TD04, projeter avec $\Phi$ à la main
   (cf. partie 4 puis TD04), puis sur le SVM linéaire dans l'espace transformé ; affichage de la
   frontière dans le plan d'origine. Constat final : si on veut éviter le calcul de $\Phi$, il y a
   l'astuce noyau (piste partie 9).

Aucune cellule du notebook ne doit lever d'exception : `uv run scripts/check_notebooks.py` doit
traverser.

## Hypothèses (résolues après relecture)

- **Séparation des 2h** : ~70 min de cours + ~50 min de TD, les temps par section sont indicatifs
  (appel du concepteur) ; le déroulé exact en séance (tout le cours puis le TD, ou entremêlé) reste
  à la main de l'enseignant.
- Prévu pour être enseigné le 30/10 (après l'évaluation du 29/10, portant sur les parties
  précédentes) — hypothèse non bloquante pour les livrables.
- Renvoi vers la partie 7 (Surapprentissage) : cette partie n'a pas encore de module markdown ; la
  partie 7 a été traitée avec le simple découpage apprentissage/test (pas de théorie) : le cours
  SVM fait donc des renvois textuels limités (« train/test », « partie 7 ») sans lien Obsidian
  mort, et présente la généralisation de la marge comme énoncé admis de ce module (décision
  enseignant).
- D'où viennent les nombres de la démo « sortie du solveur » (décision enseignant) : ils proviennent
  de l'implémentation approchée construite en TD, qualifiés expressément d'approximation du
  résultat d'un solveur exact.
- Encodage des cibles (décision enseignant) : tout le TD05 en $\{-1, +1\}$, cellule de raccord
  $0/1 \to \pm 1$.

## Contraintes du dépôt (non négociables)

- **Notations** (voir `machine_learning/AGENTS.md`) : la cible est toujours $t$ (jamais $y$) — pour
  le SVM, $t_i \in \{-1, +1\}$ ; $y$ = sortie du modèle ; entrées $x$ / matrice $X$ (un échantillon
  par ligne) ; pré-activation $z$ ; taux d'apprentissage `lr`/$\eta$ en code.
- Markdown Obsidian : wiki-links `[[...]]`, callouts `[!abstract]` / `[!info]` / `[!example]`,
  math $\LaTeX$ ; figures en `![[assets/08-<sujet>.png]]`. Ne pas toucher aux dossiers `.obsidian/`.
- Python toujours lancé via `uv run python ...` (jamais `python` direct), numpy/matplotlib.
- Notebook TD : corrigé avec solutions inline ; les blocs de solution encadrés par `# BEGIN` / `# END`
  (comme TD01) pour que la version étudiante puisse être dé-stripée par
  `scripts/collect_lite_content.py` ; aperçu étudiant via
  `uv run python scripts/prepare_notebooks.py <corrige>.ipynb /tmp/apercu.ipynb` (jamais écraser le
  corrigé, jamais versionner l'aperçu).
- Après rédaction du TD : `uv run python scripts/notebooks.py --td machine_learning/td clear` puis
  `extract` pour mettre à jour `td/assets/`, et s'assurer que `uv run scripts/check_notebooks.py`
  et `uv run scripts/check_snippets.py` passent.
- Rédaction en français, vocabulaire assumé du cours (marge, vecteurs supports, hyperplan...).

## Anti-objectifs (ce qui serait un échec)

- Un cours qui dérive en démonstration mathématique ou qui donne l'impression que la solution sort
  de la magie sans explication intuitive.
- Un TD qui utilise une bibliothèque toute faite (sklearn) : les étudiants doivent implémenter.
- Incohérences de notation ($y$ au lieu de $t$ pour la cible), mélange des conventions $0/1$ et
  $\pm 1$ dans un même calcul, incohérences avec les parties 3, 4 et 7 déjà enseignées.
- Un TD trop long pour 50 min (objectif : 4–5 exercices courts, pas un SMO complet).

## Laissé au concepteur (le builder)

- Rédaction complète des contenus (texte du module, cellules du notebook), du découpage exact en
  cellules et de la formulation des exercices, dans le style des modules 1–4 et du TD01.
- Choix de l'API exacte de la classe `SVM` (dataclass + méthode `fit`/`output`/`predict`, alignée
  sur les TD précédents) et des utilitaires d'affichage de la marge (réutiliser le style de
  `make_axis`/affichage du TD01).
- Génération des figures `08-*.png` via des scripts matplotlib jetables (scripts temporaires, pas
  nécessaire de les versionner ; suivre le contenu de la partie 4 comme référence de style).
- Numérotations et intitulés réels des datasets recyclés (copier/redéfinir les cellules de données
  nécessaires dans le TD05 ; les TDs sont autonomes).
- Vérification par les scripts maison, nettoyage des sorties, extraction des images du TD.

## Hors périmètre

- La partie 9 « Machines à noyau » (seulement le teaser de 2 min en clôture du cours).
- Le module « Surapprentissage » (partie 7) s'il manque encore — on ne le crée pas ici.
- L'évaluation du 29/10.
- L'implémentation d'un solveur exact (SMO, dual), même en annexe du TD.
