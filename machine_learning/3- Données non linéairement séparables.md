---
titre: 3 - Données non linéairement séparables
cours: "[[Entrypoint]]"
partie: 3
statut: draft
Contexte: |-
  4e année post-bac, 18h au total.
  Suite de [[03 - Classification et séparations linéaires]].
  Partie 4 : comprendre l'échec du linéaire, introduire l'idée de projection
  non linéaire, et préparer les parties 5 (MLP) et 6 (RBF).
---
²> [!abstract] Objectif de cette partie
> Montrer que le perceptron échoue dès que les données ne sont pas linéairement séparables, introduire l'idée centrale du cours : **projeter avec $\Phi(x)$ dans un espace plus grand où ça le devient**. Voir le prix à payer : **complexification et surapprentissage**.

# 1. Limite du modèle linéaire

Rappel [[03 - Classification et séparations linéaires]] :

- Théorème du perceptron : si séparable, Rosenblatt converge. Sinon, il **oscille indéfiniment**.
- Classer linéaire = couper l'espace en deux avec un hyperplan $w^T x + b = 0$.

Or beaucoup de problèmes ne ressemblent pas à ça :

![[assets/04-non-separables-exemples.png]]

> [!example] Deux échecs canoniques
> - **XOR** : $(0,0) \to -1$, $(1,1) \to -1$, $(0,1) \to +1$, $(1,0) \to +1$. Aucune droite ne sépare les $+1$ des $-1$ (voir `03-exemple-XOR`).
> - **Cercles concentriques** : centre $-1$, anneau $+1$. Il faudrait un cercle, pas une droite.


> [!note] À retenir
> L'échec n'est pas un bug d'optimisation. C'est le **modèle** qui est trop pauvre. Il faut enrichir la représentation, pas changer $\eta$.

# 2. Travail dans un espace de plus grande dimension

## 2.1 Idée générale

Au lieu de classer $x \in \mathbb{R}^d$ directement, on le transforme :

$$\Phi : \mathbb{R}^d \to \mathbb{R}^D, \quad D > d$$

puis on applique un modèle linéaire dessus :

$$f(x) = \text{sign}(w^T \Phi(x) + b)$$

La frontière est linéaire **dans l'espace d'arrivée**, mais non linéaire **dans l'espace de départ**.

> [!info] Théorème de Cover (admis, intuitif)
> Plus la dimension d'arrivée $D$ est grande, plus un jeu de $n$ points a de chances de devenir linéairement séparable par une projection non linéaire aléatoire ou bien choisie. En contrepartie, voir section 4.

Exemples de $\Phi$ : ajouter des monômes ($x_1^2$, $x_1 x_2$), des distances ($||x - c||$), des seuils.

## 2.2 Ce qui change pour l'apprentissage

- Une fois $\Phi$ fixé, on retombe sur [[03 - Classification et séparations linéaires]] : Rosenblatt sur les $\Phi(x_i)$ converge si séparable dans l'arrivée.
- Toute la difficulté est déplacée : **qui choisit $\Phi$ ?**
  - à la main (cette partie),
  - apprise en supervisé (partie 5, MLP),
  - à base de prototypes non supervisés (partie 6, RBF),
  - implicite via noyau (parties 8-9, SVM).

# 3. Exemples

## 3.1 XOR relevé avec $x_3 = (x_1 - x_2)^2$

Posons $\Phi(x_1, x_2) = (x_1, x_2, (x_1-x_2)^2)$ :

| $x$ | $y$ | $\Phi(x)$ |
|---|---|---|
| $(0,0)$ | $-1$ | $(0,0,0)$ |
| $(1,1)$ | $-1$ | $(1,1,0)$ |
| $(0,1)$ | $+1$ | $(0,1,1)$ |
| $(1,0)$ | $+1$ | $(1,0,1)$ |

Les $-1$ ont $x_3 = 0$, les $+1$ ont $x_3 = 1$. Le plan horizontal $x_3 = 0.5$ sépare, soit $w = (0,0,1)$, $b = -0.5$.

![[assets/04-phi-XOR-3D.png]]

> [!info] Lecture
> À gauche en 2D : impossible. À droite en 3D : les $+1$ sont « soulevés ». Un plan horizontal suffit. La frontière reprojetée en 2D vaut $(x_1-x_2)^2 = 0.5$, soit deux droites parallèles.

Variante équivalente : $\Phi(x) = (x_1, x_2, x_1 x_2)$ avec $w = (1,1,-2)$, $b = -0.5$. Vérification : $h = x_1 + x_2 - 2x_1x_2 - 0.5$ donne $-0.5$ sur $(0,0)$ et $(1,1)$, $+0.5$ sur $(0,1)$ et $(1,0)$.

## 3.2 Cercles concentriques relevés avec $r = x_1^2 + x_2^2$

Posons $\Phi(x_1, x_2) = (x_1, x_2, x_1^2+x_2^2)$. Les points du centre ont $r \approx 0$, ceux de l'anneau $r \approx 1$. Le plan $r = 0.35$ sépare.

![[assets/04-phi-cercles-3D.png]]

> [!info] Lecture
> Le paraboloïde $r = x_1^2+x_2^2$ « soulève » l'anneau. Un plan horizontal coupe le paraboloïde en un cercle : reprojeté en 2D, on obtient une frontière circulaire avec un modèle linéaire en 3D.

C'est exactement le même mécanisme que XOR : **rendre linéaire ailleurs ce qui est courbe ici**.

> [!example] À tester en Python / Octave
> Reprendre la boucle Rosenblatt de la partie 3, mais entraîner sur $\Phi(x)$ au lieu de $x$. Constater : 0 erreur sur XOR relevé et sur cercles relevés. Tracer la frontière reprojetée en 2D.

# 4. Complexification des modèles et impact sur la généralisation

Ajouter des dimensions marche toujours sur le train — et c'est le piège.

![[assets/04-complexite-generalisation.png]]

- Erreur train : décroît avec la complexité (dimension de $\Phi$, degré polynomial, nombre de neurones). Avec assez de features, on sépare toujours $n$ points.
- Erreur test : courbe en **U**. D'abord elle baisse (on corrige le sous-apprentissage), puis elle remonte (on mémorise, voir [[1 - Qu'est-ce qu'apprendre ?]]).
- À droite de la courbe : **surapprentissage**, détaillé en partie 7.

> [!danger] Ne pas confondre
> Séparable sur le train $\neq$ bon en généralisation. Un $\Phi$ trop riche donne une frontière tordue qui colle au bruit. Choisir la complexité = compromis biais-variance, jamais sur la seule erreur train. Toujours valider sur du non-vu (train / test).

Conséquence pratique : le feature engineering manuel ne passe pas à l'échelle. On veut des $\Phi$ dont la complexité est **contrôlée** ou **apprise** — d'où la suite.

# 5. Vers les parties 5 et 6

Les deux modèles suivants sont deux façons d'obtenir $\Phi$ automatiquement :

| Modèle | $\Phi(x)$ | Comment on l'obtient ? | Lecture |
|---|---|---|---|
| **Partie 5 : MLP** | sortie de la couche cachée | apprise en **supervisé** par rétropropagation du gradient | globale, frontières composées de morceaux d'hyperplans |
| **Partie 6 : RBF** | distances aux prototypes $\exp(-\|x-c_k\|^2/\sigma^2)$ | centres $c_k$ en **non supervisé** (Lloyd / k-means), puis couche linéaire | locale, lien avec k plus proches voisins |
| Parties 8-9 : SVM/noyau | implicite, dimension infinie | noyau $K(x,x')$, pas de $\Phi$ explicite | marge maximale |

Même équation finale $w^T \Phi(x) + b$ dans les trois cas. Seule change la façon de construire $\Phi$.

---

## À retenir pour la suite

1. Non séparable = aucune droite/plan ne suffit, Rosenblatt oscille.
2. Solution : $\Phi(x)$ vers plus grande dimension, puis modèle linéaire.
3. XOR avec $(x_1-x_2)^2$, cercles avec $x_1^2+x_2^2$ : calculs à savoir refaire.
4. Plus de complexité = train à 0 mais risque de surapprentissage (courbe en U).
5. Suite : $\Phi$ apprise (MLP, partie 5) vs $\Phi$ à prototypes (RBF, partie 6).
