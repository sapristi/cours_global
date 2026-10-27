---
titre: 6 - Évaluer un modèle
cours: "[[Entrypoint]]"
partie: 6
statut: draft
Contexte: |-
  4e année post-bac, 18h au total.
  Suite de [[1 - Qu'est-ce qu'apprendre ?]] (hold-out) et de [[4 - Réseaux de neurones à plusieurs couches]] (élan).
  Séance : ~30 min de cours, puis TD07 (matrice de confusion, courbes d'apprentissage, élan).
---

> [!abstract] Objectif de cette partie
> Savoir dire si un classifieur est bon : compter ses erreurs (matrice de confusion), suivre l'apprentissage avec des courbes, y lire l'effet de l'élan. En fin de partie : comment régler les hyper-paramètres sans se tromper soi-même.

---
# 1. Compter les erreurs : la matrice de confusion

On appelle classe **positive** la classe qu'on cherche à détecter (la fraude, la maladie…). Le réseau prédit « positif » si sa sortie $y \ge 0.5$. En comparant prédictions et cibles $t$, chaque exemple tombe dans une des quatre cases :

| | prédit positif | prédit négatif |
|---|---|---|
| **réel positif** | TP (vrai positif) | FN (faux négatif) |
| **réel négatif** | FP (faux positif) | TN (vrai négatif) |

Trois mesures en découlent :

- **accuracy** (taux de bonne classification) $= \dfrac{\mathrm{TP}+\mathrm{TN}}{N}$ : la part des exemples bien classés ;
- **précision** $= \dfrac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FP}}$ : quand le modèle dit « positif », a-t-il raison ?
- **rappel** $= \dfrac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}}$ : parmi les vrais positifs, combien sont détectés ?

## Le piège des classes déséquilibrées

Si seulement 8 % des exemples sont positifs, le classifieur qui répond **toujours « négatif »** a une accuracy de 92 %… et ne détecte rien.

![[06-eval-confusion.png]]

> [!danger] Ne pas se fier à l'accuracy seule
> Quand une classe est rare, il faut regarder la matrice de confusion en entier, ou au moins précision et rappel.

> [!info] Le seuil
> Le seuil $0.5$ est un choix. Le baisser fait prédire « positif » plus souvent : le rappel monte, la précision baisse. Pour un détecteur de fraude, on préfère rater peu de fraudes (rappel élevé), quitte à avoir plus de fausses alertes.

---
# 2. Courbes d'apprentissage

Comme dans [[1 - Qu'est-ce qu'apprendre ?]], on garde une partie des données **de côté** : le réseau ne s'entraîne jamais dessus. On appelle ces données la **validation** (la raison de ce nom est en section 4).

Une **courbe d'apprentissage** trace l'erreur en fonction des époques, pour l'entraînement **et** la validation, sur le même graphe.

![[06-eval-courbe-apprentissage.png]]

On y lit trois phases :

- **sous-apprentissage** : les deux erreurs sont hautes, le réseau n'a pas encore appris ;
- **bon régime** : les deux baissent ensemble ;
- **surapprentissage** : l'erreur d'entraînement continue de baisser, mais celle de validation **remonte**. Le réseau apprend par cœur les points d'entraînement, y compris leur bruit.

Une courbe qui **oscille** ou qui **explose** signale une descente instable : pas $\eta$ trop grand.

> [!info] Ce qui compte, c'est la courbe de validation
> L'erreur d'entraînement baisse presque toujours. C'est l'erreur sur les données mises de côté qui dit si le réseau généralise.

---
# 3. L'élan vu sur les courbes

Rappel ([[4 - Réseaux de neurones à plusieurs couches#4. Élan]]) : $v \leftarrow \mu\, v + \eta\,\dfrac{\partial E}{\partial W}$, puis $W \leftarrow W - v$.

Pour voir l'effet de l'élan, on entraîne deux fois **dans les mêmes conditions** (mêmes données, même initialisation, même $\eta$) en ne changeant que $\mu$, et on superpose les courbes.

![[06-eval-elan-lunes.png]]

- Avec élan, les courbes descendent **plus vite** (ici environ 4 fois moins d'époques pour atteindre le minimum de validation).
- Le surapprentissage arrive donc **plus tôt**, lui aussi.
- Le minimum atteint est **à peu près le même** : l'élan va plus vite, il ne va pas plus loin.
- Il aide à sortir des **plateaux**, où la descente sans élan avance très lentement.
- Un $\mu$ **trop grand** (ex. $0.99$) fait osciller les courbes.

> [!danger] L'élan n'améliore pas le modèle
> Il fait arriver plus vite au même endroit : c'est un gain de temps de calcul, pas de qualité.

---
# 4. Régler les hyper-paramètres : train / validation / test

$\eta$, $\mu$, le nombre d'époques, le seuil sont des **hyper-paramètres** : on les choisit, la descente de gradient ne les apprend pas. On les choisit en regardant les courbes de validation.

Problème : à force de choisir ce qui marche le mieux sur la validation, on finit par s'adapter à elle. Son score devient optimiste. Pour avoir une mesure honnête, on garde donc un **troisième** jeu, le **test**.

![[06-eval-train-val-test.png]]

- **train** : sert à calculer les gradients ;
- **validation** : sert à **choisir** les hyper-paramètres, autant de fois qu'on veut ;
- **test** : sert à **juger** le modèle final, **une seule fois**, à la fin.

> [!danger] Le test reste verrouillé
> Si le test a servi à choisir quoi que ce soit, ce n'est plus un test : son score ne dit plus rien sur des données nouvelles.

> [!info] Arrêt précoce (early stopping)
> Le nombre d'époques est un hyper-paramètre comme les autres : on arrête l'entraînement au **minimum de la courbe de validation**, avant le surapprentissage.

> [!example] Pour la pratique
> Le **TD07** reprend tout cela : matrice de confusion, courbes d'apprentissage sur les lunes, classe `MLPMomentum`, arrêt précoce et évaluation unique sur le test, puis spirales.
