# TD « Évaluer un modèle » + élan — conception

Date : 2026-10-26. Cours : `machine_learning/`.

## Intention

L'évaluation d'un modèle n'a quasiment pas été traitée en cours : seuls erreur
train / erreur test et le hold-out sont posés (partie 1, §3). L'élan (momentum)
a été présenté de façon non formelle (partie 4, §4) mais jamais pratiqué : la
section 8 du TD 03 n'a pas été faite et sera remplacée par ce nouveau TD. La
section 6 du TD 03 (split train/test, courbe train/test, early stopping) n'a pas
non plus été faite : ce TD en reprend la substance.

Objectif : donner aux étudiants les outils de base pour **évaluer** un
classifieur et **lire des courbes d'apprentissage**, puis mettre cette lecture en
pratique en comparant un entraînement **avec / sans élan**.

Ce travail est indépendant du TD 06 (`06_momentum_surapprentissage.ipynb`) en
cours de rédaction par ailleurs : ne pas le lire, ne pas le modifier. Ce
nouveau TD **remplacera** le TD 06 (décision de l'enseignant) : les étudiants
ne feront pas le TD 06, l'élan est donc bien pratiqué ici pour la première fois.
Le retrait du TD 06 et un éventuel renumérotage se feront à part.

## Livrables

1. Un chapitre de cours court : `machine_learning/6 - Évaluer un modèle.md`
   (vault Obsidian, conventions du `AGENTS.md` racine : frontmatter YAML,
   callouts, embeds `![[...]]`).
2. Un notebook corrigé : `machine_learning/td/07_evaluation_elan.ipynb`
   (numéro 07 : choix de Claude, pour ne pas entrer en collision avec le TD 06).
   Blocs solution `# BEGIN` / `# END` ; doit passer `uv run scripts/check_notebooks.py`.
3. Les figures du chapitre, générées par un script (dans `machine_learning/assets/`),
   à partir des mêmes données / du même MLP que le TD.

## Contraintes

- Séance de **3 h** au total : ~30 min de cours, ~2 h 30 de TD (exercices
  principaux tenant en ~2 h 15, le reste en bonus).
- 4e année post-bac, python / numpy / matplotlib uniquement (pas de sklearn
  pour les modèles ni les métriques ; générer les jeux de données en numpy).
- Notations du cours (`machine_learning/AGENTS.md`) : cible `t`/`T`, sortie
  `y`/`Y`, pas `η` = `lr`, élan `μ`, vitesse `v`. Règle d'élan exactement celle
  du cours : `v ← μ v + η ∂E/∂W`, `W ← W − v`.
- Les étudiants ont un MLP fonctionnel (TD 03 jusqu'à la section 5). On ne leur
  fait pas réécrire forward/backward.
- Contenu en français.

## Notions à retenir (validées)

1. **Évaluer un classifieur binaire**
   - classe « positive » = classe d'intérêt ; sortie sigmoïde seuillée à 0.5 ;
   - matrice de confusion **TP, FP, TN, FN** ;
   - taux de bonne classification (accuracy) = (TP+TN)/N, et son piège sur
     classes déséquilibrées (« toujours non » fait 90 %+) ;
   - **précision** = TP/(TP+FP), **rappel** = TP/(TP+FN) ; le seuil arbitre
     entre les deux.
2. **Protocole train / validation / test** : extension du hold-out déjà vu. La
   validation sert à régler (η, μ, epoch d'arrêt) ; le test reste verrouillé et
   n'est utilisé qu'une fois, à la fin.
3. **Courbes d'apprentissage** = erreur en fonction des epochs, train et
   validation sur le même graphe.
   - profils : sous-apprentissage (les deux hautes), bon régime,
     **surapprentissage** (l'écart se creuse, la validation remonte),
     instabilité (oscillations / divergence, pas trop grand ou μ trop grand) ;
   - coût (MSE) et taux d'erreur de classement ne racontent pas toujours la
     même chose ;
   - **early stopping** : s'arrêter au minimum de la courbe de validation.
4. **L'élan lu à travers les courbes**
   - comparer à conditions égales (même graine, même η, mêmes données) ;
   - l'élan atteint plus vite un niveau d'erreur donné → atteint aussi **plus
     tôt** la zone de surapprentissage, l'epoch d'arrêt se déplace ;
   - il change la vitesse, pas la capacité : le minimum de validation est du
     même ordre ;
   - il aide à traverser les plateaux ;
   - μ trop grand → oscillations visibles.

## Chapitre de cours (~30 min)

Quatre sections, une par notion ci-dessus, au même niveau de concision que
`1 - Qu'est-ce qu'apprendre ?.md` (callouts courts, une figure par section).
Figures :
- une matrice de confusion annotée (exemple chiffré sur les gaussiennes
  déséquilibrées : MLP vs « toujours non ») ;
- un schéma du découpage train / validation / test ;
- une courbe d'apprentissage annotée (zones sous-apprentissage / bon régime /
  surapprentissage, epoch d'arrêt) ;
- la comparaison μ = 0 / 0.9 sur les lunes (minimum atteint ~8× plus tôt).

Le chapitre peut renvoyer au TD pour la pratique ; il ne contient pas de code
au-delà de quelques formules.

## TD (~2 h 30)

Structure (le détail des énoncés, questions de lecture et corrigés est laissé
au rédacteur, en suivant le skill `notebook_exercises`) :

0. **Fourni** (pas d'exercice) : une classe `MLP` équivalente à celle du TD 03
   (tanh caché, sortie sigmoïde, coût MSE `0.5 · mean`), dont `fit` prend
   optionnellement un jeu de validation et renvoie un historique
   `{"train": [...], "val": [...]}` (MSE), plus le taux d'erreur de classement
   train/val. Générateurs de données numpy fournis. Fonction de tracé des
   courbes fournie.
1. **Matrice de confusion** (~35 min), gaussiennes déséquilibrées (~10 % de
   positifs) :
   - implémenter `confusion(t, y)` → (TP, FP, TN, FN), puis `accuracy`,
     `precision`, `recall` ; cellule de vérification avec valeurs de référence ;
   - comparer le classifieur « toujours négatif » et le MLP entraîné :
     accuracy proche, rappel très différent ;
   - faire varier le seuil et observer précision / rappel.
2. **Courbes d’apprentissage** (~30 min), lunes :
   - split train / validation / test (petit train pour provoquer le
     surapprentissage) ;
   - entraîner sans élan, tracer, identifier sur la courbe les zones et
     l'epoch du minimum de validation ; comparer avec la courbe du taux
     d'erreur.
3. **Élan** (~50 min), lunes :
   - sous-classe `MLPMomentum(MLP)` qui surcharge `step` avec la règle du
     cours (vitesses `vWs` / `vbs` nulles au départ) ; vérification sur une
     étape avec valeurs de référence ;
   - comparer μ = 0 / 0.9 / 0.99 à conditions égales : epoch et valeur du
     minimum de validation, surapprentissage plus précoce, oscillations ;
   - early stopping (ou simple choix de l'epoch au minimum de validation),
     puis évaluation **unique** sur le test (matrice de confusion de
     l'exercice 1).
4. **Spirales** (~20 min) : sans élan la descente reste sur un plateau
   longtemps ; avec élan elle en sort bien plus tôt.

**Bonus** : pas d'apprentissage trop grand → divergence / oscillations ; autres
valeurs de μ ; seuil de décision sur les lunes.

## Données et réglages (issus d'un essai préalable)

Essai réalisé avec MLP `[2, 32, 32, 1]`, tanh, sortie sigmoïde, MSE, descente
par lot complet, η = 0.5, 5000 epochs, init `N(0, 0.5)`, graine 0 pour les
poids, graine 1 pour les données, validation = 1000 points :

| Jeu | Génération | Train | Résultat observé |
|---|---|---|---|
| Lunes | deux demi-cercles, bruit gaussien 0.3 | 60 | min val ≈ 0.032 à l'epoch 503 (μ=0) vs 63 (μ=0.9) ; surapprentissage ensuite ; oscillations au début pour μ=0.99 |
| Spirales | 2 spirales, r ∈ [0.2, 1], θ = 3πr (+π), bruit 0.08 | 120 | μ=0 sur un plateau jusqu'à ~800 epochs ; μ=0.9 en sort vers ~100 |
| Gaussiennes déséquilibrées | centres (0,0) et (1,1), σ = 0.6, 10 % de positifs | 100 | μ=0.99 reste coincé sur « toujours négatif » (accuracy 91 %, rappel 0) |
| Cercles (écarté) | — | — | bruit trop fort, non retenu |

Ces réglages sont un point de départ : le rédacteur les ajuste pour que chaque
phénomène soit lisible (courbes nettes, temps d'exécution raisonnable dans
JupyterLite — viser quelques secondes par entraînement), et vérifie que les
chiffres cités dans les énoncés et le cours correspondent aux sorties réelles.
L'axe des epochs en échelle log a rendu les comparaisons lisibles dans l'essai.

## Non-objectifs

- Courbes d'apprentissage en fonction de la taille du jeu d'entraînement.
- Courbe ROC / AUC, F1, validation croisée, régularisation.
- Classification multi-classes.
- Retoucher le TD 03 (la suppression de sa section 8 sera faite à part).

## Anti-objectifs

- Laisser croire que l'élan « améliore » le modèle : le message est vitesse,
  pas qualité.
- Utiliser le test pour régler quoi que ce soit.
- Des courbes trop bruitées ou ambiguës pour que la lecture demandée soit
  évidente.

## Laissé au rédacteur

- Formulation exacte des énoncés et questions de lecture.
- Réglages fins des jeux (bruit, tailles, η, nombre d'epochs).
- Emplacement et nom du script de génération des figures du cours.

## Décisions de Claude (à vérifier)

- Numéro de notebook 07.
- Ex. 4 (spirales) reste un exercice principal (seule illustration pratique du plateau) ; durées : 35 + 30 + 50 + 20 = 2 h 15.
- Aucun autre fichier du cours n’est modifié (ni `Entrypoint.md`, ni liens depuis les chapitres existants).
