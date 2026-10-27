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

Dépistage d'un cancer : sur 1000 personnes testées, 10 sont malades. Un « test » qui répond **toujours « sain »** donne :

| | prédit malade | prédit sain |
|---|---|---|
| **malade** | TP = 0 | FN = 10 |
| **sain** | FP = 0 | TN = 990 |

Accuracy $= 990/1000 = 99\,\%$… et rappel $= 0$ : il ne détecte **aucun** cancer. Un vrai test, qui détecte 8 malades sur 10 au prix de 30 fausses alertes, a une accuracy *plus basse* ($968/1000 = 96.8\,\%$) mais il est infiniment plus utile (rappel $0.8$).

Le même phénomène sur des données synthétiques (celles du TD07, 8 % de positifs) :

![[06-eval-confusion.png]]

> [!danger] Ne pas se fier à l'accuracy seule
> Quand une classe est rare, il faut regarder la matrice de confusion en entier, ou au moins précision et rappel.

> [!info] Le seuil
> Le seuil $0.5$ est un choix. Le baisser fait prédire « positif » plus souvent : le rappel monte, la précision baisse. Pour un dépistage de cancer, rater un malade (FN) est bien plus grave qu'une fausse alerte (FP), qui coûte seulement un examen complémentaire : on choisit un seuil bas, pour un rappel élevé.

> [!example] Exercice : quel modèle choisir ?
> Pour chaque cas d'usage, on compare deux modèles testés sur le même jeu de test de 1000 exemples. Papier-crayon, pas de code.
>
> **Cas A : détection d'intrusion réseau.** La classe positive est « connexion malveillante » (20 sur 1000). Une intrusion non détectée peut compromettre tout le réseau ; une fausse alerte coûte seulement quelques minutes d'analyse.
>
> | Modèle A1 | prédit intrusion | prédit normal |
> |---|---|---|
> | **intrusion** | TP = 10 | FN = 10 |
> | **normal** | FP = 0 | TN = 980 |
>
> | Modèle A2 | prédit intrusion | prédit normal |
> |---|---|---|
> | **intrusion** | TP = 18 | FN = 2 |
> | **normal** | FP = 30 | TN = 950 |
>
> **Cas B : filtre anti-spam avec quarantaine.** La classe positive est « spam » (100 sur 1000). Les mails prédits spam sont mis en quarantaine, que personne ne relit : un vrai mail y est perdu. Laisser passer un spam est seulement agaçant.
>
> | Modèle B1 | prédit spam | prédit légitime |
> |---|---|---|
> | **spam** | TP = 90 | FN = 10 |
> | **légitime** | FP = 60 | TN = 840 |
>
> | Modèle B2 | prédit spam | prédit légitime |
> |---|---|---|
> | **spam** | TP = 60 | FN = 40 |
> | **légitime** | FP = 15 | TN = 885 |
>
> 1. Calculer l'accuracy, la précision et le rappel des quatre modèles.
> 2. Pour chaque cas, quel modèle choisir ? Justifier en s'appuyant sur le coût de chaque type d'erreur.
> 3. Dans l'un des deux cas, le modèle qui a la meilleure accuracy n'est pas le bon choix. Lequel, et pourquoi ?

> [!example]- Correction
> **1. Mesures**
>
> | Modèle | accuracy | précision | rappel |
> |---|---|---|---|
> | A1 | $990/1000 = 99\,\%$ | $10/10 = 1$ | $10/20 = 0.5$ |
> | A2 | $968/1000 = 96.8\,\%$ | $18/48 = 0.375$ | $18/20 = 0.9$ |
> | B1 | $930/1000 = 93\,\%$ | $90/150 = 0.6$ | $90/100 = 0.9$ |
> | B2 | $945/1000 = 94.5\,\%$ | $60/75 = 0.8$ | $60/100 = 0.6$ |
>
> **2. Choix**
>
> - **Cas A : A2.** Ici rater une intrusion (FN) est le coût principal, donc on veut un rappel élevé. A2 en détecte 18 sur 20 (rappel $0.9$), A1 seulement la moitié. A2 fait 30 fausses alertes, ce qui se paie en temps d'analyse mais reste supportable.
> - **Cas B : B2.** Ici le coût principal est le vrai mail mis en quarantaine (FP), donc on veut une précision élevée. Dans B2, 80 % des mails mis en quarantaine sont bien des spams (B1 : 60 %, soit 60 mails légitimes perdus contre 15). B2 laisse passer plus de spams (40 contre 10), ce qui est le moindre mal.
>
> **3.** C'est le cas A : A1 a la meilleure accuracy ($99\,\%$ contre $96.8\,\%$) mais détecte une intrusion sur deux seulement. Avec 98 % de connexions normales, l'accuracy récompense surtout le fait de bien classer les cas normaux ; elle cache les FN. Dans le cas B, B2 est meilleur à la fois en accuracy et en précision : l'accuracy ne contredit pas le bon choix, mais l'écart entre B1 et B2 ($1.5$ point) ne rend pas compte de la différence de 45 mails légitimes perdus.
>
> Le « bon » modèle dépend donc du coût des erreurs : rappel pour A, précision pour B.

---
# 2. Courbes d'apprentissage

Comme dans [[1 - Qu'est-ce qu'apprendre ?]], on garde une partie des données **de côté**, le jeu de **test** : le réseau ne s'entraîne jamais dessus, on s'en sert seulement pour mesurer l'erreur sur des données nouvelles.

Une **courbe d'apprentissage** trace l'erreur en fonction des époques, pour l'entraînement **et** le test, sur le même graphe.

![[06-eval-courbe-apprentissage.png]]

On y lit trois phases :

- **sous-apprentissage** : les deux erreurs sont hautes, le réseau n'a pas encore appris ;
- **bon régime** : les deux baissent ensemble ;
- **surapprentissage** : l'erreur d'entraînement continue de baisser, mais celle de test **remonte**. Le réseau apprend par cœur les points d'entraînement, y compris leur bruit.

Une courbe qui **oscille** ou qui **explose** signale une descente instable : pas $\eta$ trop grand.

> [!info] Ce qui compte, c'est la courbe de test
> L'erreur d'entraînement baisse presque toujours. C'est l'erreur sur les données mises de côté qui dit si le réseau généralise.

---
# 3. L'élan vu sur les courbes

Rappel ([[4 - Réseaux de neurones à plusieurs couches#4. Élan]]) : $v \leftarrow \mu\, v + \eta\,\dfrac{\partial E}{\partial W}$, puis $W \leftarrow W - v$.

Pour voir l'effet de l'élan, on entraîne deux fois **dans les mêmes conditions** (mêmes données, même initialisation, même $\eta$) en ne changeant que $\mu$, et on superpose les courbes.

![[06-eval-elan-lunes.png]]

- Avec élan, les courbes descendent **plus vite** (ici environ 4 fois moins d'époques pour atteindre le minimum du coût de test).
- Le surapprentissage arrive donc **plus tôt**, lui aussi.
- Le minimum atteint est **à peu près le même** : l'élan va plus vite, il ne va pas plus loin.
- Il aide à sortir des **plateaux**, où la descente sans élan avance très lentement.
- Un $\mu$ **trop grand** (ex. $0.99$) fait osciller les courbes.

> [!danger] L'élan n'améliore pas le modèle
> Il fait arriver plus vite au même endroit : c'est un gain de temps de calcul, pas de qualité.

---
# 4. Régler les hyper-paramètres : train / validation / test

$\eta$, $\mu$, le nombre d'époques, le seuil sont des **hyper-paramètres** : on les choisit, la descente de gradient ne les apprend pas. On est tenté de les choisir en regardant les courbes de test.

Problème : à force de choisir ce qui marche le mieux sur le test, on finit par s'adapter à lui. Son score devient optimiste : ce n'est plus un test, c'est devenu un jeu de **validation**. Pour avoir une mesure honnête, on garde donc un **troisième** jeu, jamais regardé, qui sert de vrai test.

![[06-eval-train-val-test.png]]

- **train** : sert à calculer les gradients ;
- **validation** : sert à **choisir** les hyper-paramètres, autant de fois qu'on veut ;
- **test** : sert à **juger** le modèle final, **une seule fois**, à la fin.

> [!danger] Le test reste verrouillé
> Si le test a servi à choisir quoi que ce soit, ce n'est plus un test : son score ne dit plus rien sur des données nouvelles.

> [!info] Arrêt précoce (early stopping)
> Le nombre d'époques est un hyper-paramètre comme les autres : on arrête l'entraînement au **minimum de la courbe de validation**, avant le surapprentissage.

> [!example] Pour la pratique
> Le **TD07** reprend les sections 1 à 3 : matrice de confusion, courbes d'apprentissage sur les lunes, classe `MLPMomentum`, spirales. La section 4 (arrêt précoce, évaluation unique sur le test) y est en bonus.
