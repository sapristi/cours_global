---
titre: 5 - Support Vector Machines
cours: "[[Entrypoint]]"
partie: 8
statut: draft
Contexte: |-
  4e année post-bac, 18h au total.
  Suite de [[4 - Réseaux de neurones à plusieurs couches]].
  Prérequis : perceptron ([[2 - Perceptron]]), projection Φ (partie 4),
  découpage train/test et régularisation (partie 7).
  Partie 8 : SVM — marge maximale, marge souple, programmation quadratique en boîte
  noire, considérations théoriques, ouverture vers les machines à noyau (partie 9).
  Durée : 2h (cours ~70 min + TD ~50 min, notebook 05_svm).
---

> [!abstract] Objectif de cette partie
> Le perceptron trouve **un** séparateur : n'importe lequel. La question devient : parmi tous
> les séparateurs qui « marchent », **choisir le meilleur** — celui qui généralisera le mieux.
> Le SVM (Support Vector Machine, Vapnik & Chervonenkis, 1963) répond : celui dont la **marge**
> est maximale. On verra la marge et ses **vecteurs supports**, comment la calculer
> (un solveur, sans faire les maths de la résolution), comment rester robuste quand les
> données sont bruitées (**marge souple**), et on ouvrira la voie aux **machines à noyau**
> (partie 9).

# 1. Un séparateur quelconque ne suffit pas

Souvenez-vous du TD01 (la [[2 - Perceptron|partie perceptron]]) :

- si les données sont linéairement séparables, l'algorithme de Rosenblatt **converge** ;
- mais rien ne dit *quelle* droite il choisit : cela dépend de l'ordre de présentation des
  points, du départ des poids...

Deux runs donnent alors des droites différentes, **toutes deux correctes** sur les données
d'entraînement.

![[assets/08-deux-separateurs.png]]

Or sur des données de test, ces deux séparateurs ne se valent pas : l'un se trompe, l'autre
non — **sans que rien dans l'erreur d'entraînement ne les distingue** (zéro erreur de
classement pour tous les deux).

> [!note] À retenir
> « Trouver un séparateur » était le problème facile. Il manque un **critère de choix**
> parmi les séparateurs possibles. Le SVM propose ce critère : la **marge**.

# 2. La marge et les vecteurs supports

On garde les conventions du cours : les cibles sont $t_i \in \{-1, +1\}$ (partie 4), le modèle
linéaire calcule la pré-activation $z(x) = w^\top x + b$ et prédit $\text{sign}(z(x))$.

Définitions (voir la figure) :

- **distance d'un point à l'hyperplan** : $\dfrac{|w^\top x + b|}{\|w\|}$ ;
- **marge** du séparateur : la plus petite de ces distances, c'est-à-dire la distance entre
  l'hyperplan et le point le plus proche ;
- **vecteurs supports** : les points les plus proches, ceux qui « bloquent » la bande.

![[assets/08-marge-def.png]]

Deux remarques qui rendent la marge attractive :

1. **Les autres points ne comptent pas.** Si on déplace un point sans franchir la bande de
   marge, le « meilleur » séparateur ne change pas d'un pouce. La solution ne dépend que des
   vecteurs supports : le reste des données est décoratif.
2. **La marge mesure l'épaisseur sous le séparateur.** Un séparateur collé aux données a une
   marge minuscule : la moindre variation de données le fait vaciller. Un séparateur large est
   « confortable ».

![[assets/08-marge-maximale.png]]

# 3. Le meilleur séparateur : un problème d'optimisation

On veut la marge maximale. Une petite astuce d'écriture simplifie tout : on peut toujours
**redimensionner** $(w, b)$ — le classeur signe($w^\top x + b$) ne dépend que du *signe* de
$w^\top x + b$, pas de son ampleur. On choisit donc l'échelle telle que

$$t_i \, (w^\top x_i + b) \geq 1 \quad \text{pour tout } i.$$

Dans cette écriture, la marge vaut exactement $\dfrac{1}{\|w\|}$ : agrandir la marge, c'est
**raccourcir** $w$. « Choisir le meilleur séparateur » devient le problème :

$$\boxed{\;\min_{w,b}\ \tfrac{1}{2}\|w\|^2 \quad \text{sous contrainte} \quad t_i\,(w^\top x_i + b) \geq 1\ \ \forall i\;}$$

On écrit le problème ; on ne le résout pas à la main : c'est un problème à
**objectif + contraintes**, de la même famille que la programmation linéaire vue dans les
prérequis (« maximiser le profit sous des contraintes de ressources »). La variante ici
s'appelle la **programmation quadratique** : même exercice, mais la courbe à minimiser est
une parabole au lieu d'un plan.

![[assets/08-prog-quadratique.png]]

> [!info] Le solveur est une boîte noire (assumée)
> Résoudre un programme quadratique à la main serait fastidieux : des logiciels le font
> (c'est le même type d'outil qu'un solveur de programmation linéaire). On lui donne données
> et contraintes, il rend $(w, b)$ — et sa solution a une propriété précieuse : les points
> placés exactement sur les bords de la bande ($t_i(w^\top x_i + b) = 1$) sont **les vecteurs
> supports** ; les points remplis loin de la bande n'influencent même pas sa réponse.
>
> Dans le TD, nous approcherons cette solution par notre propre algorithme ; les chiffres
> affichés dans ce cours et ce TD sont issus de cette implémentation, **approximation** de ce
> que rendrait un solveur quadratique exact.

Le SVM linéaire est donc résumé par : *maximiser la marge* = *choisir le séparateur le plus
« éloigné des deux classes »*.

# 4. La marge souple : tolérer les points mal placés

La marge dure a une faiblesse : **un seul point mal placé compte pour toute
la solution**. Ajoutez un point aberrant profondément du mauvais côté, et le séparateur
« rigide » plonge : la marge s'effondre (bande grise minuscule, panneau de gauche).

![[assets/08-marge-souple.png]]

Idée du SVM dit **à marge souple** : tolérer quelques points fautifs, mais **les faire payer**
un prix. Un paramètre $C$ règle le tarif de la tricherie :

- $C$ grand : tricher coûte cher → la rigueur domine, la marge s'écrase pour servir chaque
  point (panneau de gauche) ;
- $C$ petit : tricher bon marché → la frontière garde sa marge et laisse le point fautif en
  erreur (panneau de droite).

C'est le même arbitrage que la régularisation vue en partie 7 : ne pas payer au prix fort une
exigence entière quand les données résistent. (Vocabulaire : dans le TD, on fera varier la
force de régularisation $\lambda$, qui joue un rôle symétrique inverse du $C$.)

> [!note] À retenir
> Marge dure : chaque point doit être bien servi. Marge souple : chaque point peut tricher,
> mais **paie**. Le bon équilibre se règle sur les données de test (partie 7) — pas en
> regardant l'erreur d'entraînement, qui est toujours propice à la rigueur extrême.

# 5. Résumé et ouverture : projeter, puis des noyaux

Retour sur la ligne principale du cours :

- Le **critère** du SVM est nouveau : non pas zéro erreur d'entraînement (partagé par une
  infinité de séparateurs), mais la **marge maximale**.
- **Pourquoi ça généralise** (énoncé admis) : imposer une grande marge rend bien plus rare
  l'ensemble des séparateurs « qui collent aux données » — qu'un hyperplan à large marge soit
  le fruit du hasard de l'échantillon est statistiquement bien moins plausible. C'est la même
  intuition que le découpage train/test vu en partie 7 : juger sur des données entièrement
  nouvelles, et préférer les modèles qui n'ont pas besoin de coller au détail.

Ensuite, la partie 4 nous a déjà appris à rendre séparable ce qui ne l'est pas : projeter avec
$\Phi$ (les [[3- Données non linéairement séparables|cercles concentriques]]) puis séparer
linéairement. Le TD05 fera exactement ça avec le SVM : **projeter, puis séparer à marge
maximale**.

Pour finir, un avant-goût de la partie 9 (machines à noyau) : le SVM a une propriété rare —
sa solution ne fait intervenir que des produits scalaires. Il sera donc
possible de remplacer $\Phi(x)^\top \Phi(x')$ par une simple fonction $k(x, x')$, **sans jamais
calculer $\Phi$**, ce qui ouvre la porte à des projections en dimension infinie. Mais nous
gardons cela pour la partie 9.

> [!abstract] À la fin de cette partie, vous devez savoir faire
> 1. Expliquer pourquoi un séparateur quelconque ne suffit pas (deux perceptrons valides,
>    erreurs de test différentes) et sur quoi repose le critère du SVM (la marge).
> 2. Définir la marge, donner la distance d'un point à l'hyperplan, et **identifier les
>    vecteurs supports sur un dessin**.
> 3. Écrire et commenter le problème d'optimisation du SVM à marge dure
>    ($\min \frac12\|w\|^2$ sous $t_i(w^\top x_i + b) \geq 1$) : marge maximale ⇔
>    $\|w\|$ minimal. (Le résoudre à la main : non.)
> 4. Expliquer le rôle du solveur (programmation quadratique, boîte noire) et lire sa
>    sortie : $(w, b)$ et quels points déterminent la solution.
> 5. Expliquer la marge souple en mots : point mal placé, prix payé par point fautif
>    (paramètre $C$), équilibre d'arbitrage.
> 6. Relier la marge à la généralisation vue en partie 7 (grande marge ⇒ bonne
>    généralisation, énoncé admis) et le tout au train/test.
> 7. En application : implémenter un SVM approché (descente de gradient, hinge +
>    régularisation), l'appliquer sur un jeu linéaire et sur le cercle via $\Phi$, et
>    situer l'astuce noyau pour la partie 9.

La suite logique est l'application : rendez-vous dans le TD05.
