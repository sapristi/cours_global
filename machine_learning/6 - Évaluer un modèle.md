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
> Mesurer la qualité d'un classifieur **sans se mentir** : matrice de confusion et métriques adaptées aux classes déséquilibrées, protocole train / validation / test, lecture des courbes d'apprentissage (surapprentissage, arrêt précoce), et effet de l'élan vu à travers ces courbes.

---
# 1. Évaluer un classifieur binaire

## 1.1 La matrice de confusion

On appelle classe **positive** la classe d'intérêt (la fraude, la maladie, l'intrusion…). La sortie sigmoïde $y$ est seuillée à $0.5$ : on prédit « positif » si $y \ge 0.5$. En comparant prédictions et cibles $t$, on obtient quatre comptes :

| | prédit positif | prédit négatif |
|---|---|---|
| **réel positif** | TP (vrais positifs) | FN (faux négatifs) |
| **réel négatif** | FP (faux positifs) | TN (vrais négatifs) |

## 1.2 Accuracy, précision, rappel

Avec $N = \mathrm{TP}+\mathrm{FP}+\mathrm{TN}+\mathrm{FN}$ :

$$\text{accuracy} = \frac{\mathrm{TP}+\mathrm{TN}}{N} \qquad \text{précision} = \frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FP}} \qquad \text{rappel} = \frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}}$$

- **accuracy** (taux de bonne classification) : part des exemples bien classés ;
- **précision** : parmi les exemples *prédits* positifs, la part qui l'est vraiment ;
- **rappel** : parmi les vrais positifs, la part détectée.

## 1.3 Le piège des classes déséquilibrées

Exemple : deux nuages gaussiens dont la classe positive ne représente que 10 % des points. Sur 1000 points de validation (80 positifs), comparons « toujours négatif » et un MLP `[2, 16, 1]` entraîné sur 100 points :

![[06-eval-confusion.png]]

« Toujours négatif » ne détecte aucun positif, et pourtant son accuracy vaut $0.920$. Le MLP fait $0.948$ : à peine 2,8 points de mieux, alors qu'il détecte 46 positifs sur 80. L'accuracy ne distingue pas un classifieur inutile d'un classifieur utile.

> [!danger] Accuracy seule = piège
> Sur des classes déséquilibrées, un classifieur trivial a une très bonne accuracy. Il faut lire **précision et rappel** (donc la matrice de confusion en entier).

## 1.4 Le seuil arbitre entre précision et rappel

Le seuil $0.5$ est un réglage, pas une fatalité. Baisser le seuil prédit plus de positifs : le rappel monte, la précision baisse. Pour le MLP ci-dessus, passer le seuil de $0.5$ à $0.1$ fait monter le rappel de $0.575$ à $0.888$, mais la précision tombe de $0.719$ à $0.438$.

> [!info] Que privilégier ?
> Détecteur de fraude : un faux négatif coûte bien plus cher qu'une fausse alerte, on privilégie le **rappel** (seuil bas). Filtre qui bloque des comptes : on privilégie la **précision**. Le choix dépend du coût relatif d'un FN et d'un FP.

---
# 2. Le protocole train / validation / test

Dans [[1 - Qu'est-ce qu'apprendre ?]] (hold-out), on gardait un jeu de test de côté. Mais on veut aussi **régler** le modèle (pas d'apprentissage $\eta$, élan $\mu$, nombre d'époques, seuil) : si on règle sur le test, il devient du train déguisé. On découpe donc en trois jeux.

![[06-eval-train-val-test.png]]

- **train** : calcule les gradients, modifie les poids ;
- **validation** : sert à *régler*, on peut la consulter autant de fois que nécessaire ;
- **test** : sert à *juger* le réglage final, **une seule fois**, à la fin.

> [!danger] Le test reste verrouillé
> Dès que le test a servi à choisir quelque chose, il devient une validation de plus : son score est optimiste et ne dit plus rien sur des données vraiment nouvelles.

> [!note] Dans le TD07
> Lunes : 60 points d'entraînement (volontairement peu), 500 de validation, 500 de test. Une fois le réglage figé sur la validation, le test donne une accuracy de $0.902$ (taux d'erreur $0.098$), proche du taux d'erreur de validation ($0.094$) : la validation estimait bien la performance sur des données nouvelles.

---
# 3. Courbes d'apprentissage

## 3.1 Principe

Une **courbe d'apprentissage** trace l'erreur (le coût $E$, ou le taux d'erreur de classement) en fonction des époques, **train et validation sur le même graphe**.

![[06-eval-courbe-apprentissage.png]]

## 3.2 Les profils

- **sous-apprentissage** : coûts d'entraînement et de validation tous deux élevés, le réseau n'a pas encore appris ;
- **bon régime** : les deux baissent ensemble, avec un écart faible ;
- **surapprentissage** : le coût d'entraînement continue de baisser mais celui de validation **remonte**, l'écart se creuse : le réseau apprend le bruit des points d'entraînement ;
- **instabilité** : oscillations ou divergence (pas $\eta$ trop grand, ou, on le verra, élan $\mu$ trop grand).

Sur la figure (lunes, 60 points d'entraînement, réseau `[2, 32, 32, 1]`, $\eta = 0.5$, sans élan), le coût de validation passe par un minimum de $0.0389$ après 680 étapes. À la fin (4000 époques), le coût d'entraînement est tombé à $0.0135$ mais celui de validation est remonté à $0.0568$.

## 3.3 Arrêt précoce (early stopping)

> [!info] Early stopping
> S'arrêter à l'époque du **minimum de la courbe de validation**. On choisit l'époque sur la validation, jamais sur le test.

> [!note] Coût et taux d'erreur ne racontent pas toujours la même chose
> Le coût mesure aussi la *confiance* des sorties (une sortie trop sûre d'elle et fausse coûte cher), le taux d'erreur seulement le côté du seuil. Ici le coût de validation est minimal après 680 étapes, mais le taux d'erreur de validation reste sur un long plateau et atteint son minimum plus tard : l'époque d'arrêt dépend de la mesure choisie.

---
# 4. L'élan lu à travers les courbes

Rappel de la règle ([[4 - Réseaux de neurones à plusieurs couches#4. Élan]]) :

$$v \leftarrow \mu\, v + \eta\,\frac{\partial E}{\partial W}, \qquad W \leftarrow W - v$$

Pour juger l'élan, on compare **à conditions égales** : mêmes données, même initialisation (graine), même $\eta$, même nombre d'époques ; seul $\mu$ change.

![[06-eval-elan-lunes.png]]

- L'élan atteint **plus vite** un niveau d'erreur donné : sur les lunes, le minimum de validation est atteint après 173 étapes avec $\mu = 0.9$ contre 680 sans élan, soit environ 4 fois plus tôt.
- Il entre donc **aussi plus tôt** dans la zone de surapprentissage : l'époque d'arrêt se déplace. À 4000 époques, le coût de validation vaut $0.0762$ avec élan contre $0.0568$ sans.
- Il change la **vitesse**, pas la **capacité** : le minimum de validation est du même ordre ($0.0415$ contre $0.0389$, pas plus bas).
- Il aide à traverser les **plateaux** : sur les spirales (TD07, §4), le coût d'entraînement passe sous $0.05$ après 138 étapes avec $\mu = 0.9$ contre 987 sans élan, environ 7 fois plus vite.
- Un $\mu$ **trop grand** rend la descente instable : sur les lunes, $\mu = 0.99$ oscille au début et son minimum de validation est le moins bon des trois ($0.0497$).

> [!danger] L'élan n'améliore pas le modèle
> Il ne rend pas le modèle meilleur : il le fait arriver plus vite au même endroit. Son intérêt est d'économiser des étapes de calcul, à condition d'arrêter au bon moment (sur la validation).

> [!example] Pour la pratique
> Le **TD07** reprend ces quatre notions : matrice de confusion et métriques à implémenter, courbes d'apprentissage sur les lunes, classe `MLPMomentum`, early stopping, évaluation unique sur le test, puis spirales.
