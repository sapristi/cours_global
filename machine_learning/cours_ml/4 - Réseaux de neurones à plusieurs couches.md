# 1. Contexte

On se place dans le cas d'un réseau de neurones à plusieurs couches (chaque couche peut elle-même avoir plusieurs neurones):
![[Pasted image 20261011215258.png]]

Note: les neurones de couches successives sont bien tous reliés entre eux; on utilise une seule grosse flèche pour garder le schéma lisible. Un schéma plus détaillé ressemblerait à cela:
![[Pasted image 20261011215637.png|196]]

# 2. Couches à un unique neurone

Afin de simplifier les calculs, supposons pour l'instant que
- l'entrée $x$ est de dimension $1$
- chaque couche $l$ a un unique neurone, de poids $w_l$; on ignore le biais
- la fonction d'activation (partagée par toutes les couches) est notée $a$, et $a'$ sa dérivée.

Ainsi, tout se passe en dimension 1, et l'on évite les considérations matricielles.

## 2.1 Valeur de sortie du réseau
On peut alors calculer la sortie de chaque couche du réseau avec la formule:
$$\begin{eqnarray}z_{l+1} &=& y_l \cdot w_{l+1}\\
y_{l+1} &=& a(z_{l+1})\end{eqnarray}$$
( on pose $y_0 = x$: entrée du réseau).

La sortie du réseau s'obtient avec la valeur de $y_L$ (sortie de la dernière couche).

> [!info] Le calcul des sorties s'effectue de la couche $1$ à la couche $L$, d'où le nom de « passe avant » ( *forward* en anglais)

## 2.2 Mise à jour des poids

### 2.2.1 Principe

La mise à jour des poids fonctionne avec une méthode de descente de gradient.
![[Pasted image 20261002144236.png]]

Soient
- $x$ un échantillon d'entrée
- $t$ la valeur attendue
- $y$ la valeur de sortie

On définit la fonction d'erreur $E$ comme:
$$E= \frac{1}{2}(y-t)^2$$
On va alors appliquer la méthode de descente de gradient à $E$, vue comme étant une fonction des poids. Une étape d'apprentissage correspond à une application de la formule de descente de gradient, pour chacun des poids:
$$\begin{eqnarray}
w_{l} ← w_{l} - \eta\cdot \frac{\partial E}{\partial w_l}(w_l) \\
\end{eqnarray}$$
où 
- $\frac{\partial E}{\partial w_l}$ est la dérivée partielle de $E$ par rapport à son $l^{ème}$ paramètre $w_l$
- $\eta$ est un paramètre appelé *taux d'apprentissage* ($0 < \eta \le 1$).

Nous allons donc devoir calculer ces dérivées partielles. Voir [[Annexe 1 - Calcul des dérivées partielles]] pour le détail des calculs.

### 2.2.2 Suppléments


> [!tip] Définition de la dérivée partielle
> $E$ est ici une fonction à $L$ paramètres; on pourrait l'écrire $E(w_1, ..., w_L)$. 
Supposons tous les $w_k, k \neq l$ constants; on peut alors considérer $E$ comme fonction de l'unique paramètre $w_l$. Appelons $E_l$ cette fonction.
>
> La dérivée partielle de $E$ par rapport à (son $l^{ème}$ paramètre) $w_l$ correspond alors à $E_l'$, dérivée de la fonction $E_l$: pour toute valeur de $w_l$, $\frac{\partial E}{\partial w_l}(w_l) = E_l'(w_l)$.

> [!danger] Quand on écrit $\frac{\partial E}{\partial w_l}(w_l)$, $w_l$ prends deux sens différents:
> ![[Pasted image 20261011224535.png]]
> En pratique, on omet même parfois le 2nd $w_l$, ce qui donne $\frac{\partial E}{\partial w_l}$ au lieu de $\frac{\partial E}{\partial w_l}(w_l)$.

### 2.2.3 Conclusion

On pose
$$\begin{eqnarray}
\delta_L &=& (y_L - t)\cdot a'(z_L)\\
\delta_{l-1} &=& \delta_l \cdot w_l \cdot  a'(z_{l-1}) 
\end{eqnarray}$$
on peut calculer chacune des dérivées partielles avec 
$$\frac{\partial E}{\partial w_l}(w_l) = \delta_l \cdot y_{l-1}$$
La mise à jour des poids s'obtient enfin en appliquant pour chaque couche $l$ (où $\eta$ est le taux d'apprentissage):
$$\begin{eqnarray}
w_{l} ← w_{l} - \eta\cdot \frac{\partial E}{\partial w_l}(w_l) \\
\end{eqnarray}$$

> [!info] Le calcul des $\delta_l$ s'effectue de la couche $L$ à la couche $1$, d'où le nom de « passe arrière » ( *backward* en anglais)


# 3. Couches à plusieurs neurones
## 3.1 Conventions matricielles

Afin d'accélérer les calculs avec `numpy`, nous utiliserons les conventions suivantes:
- On dispose de $N$ vecteurs d'entrée sous forme de ligne, que nous regroupons en une matrice $X$. $d$ est la dimension de l'entrée.
   ![[Pasted image 20261002120039.png|center|183]]
- Chaque ligne de la matrice de poids $W$ contient les poids d'un neurone 
  ![[Pasted image 20261002105419.png|center|198]]
- On peut alors calculer la sortie d'un neurone pour tous les vecteurs d'entrée en une seule opération:
$$\begin{eqnarray}Z &=& X \cdot W^T + b\\
Y &=& A(Z)\end{eqnarray} $$
Où $A$ est la fonction matricielle qui applique la fonction d'activation $a$ à chaque élément d'une matrice:
$$A(Z) = \begin{pmatrix}
a(z_{1,1}) & \dots & a(z_{1,d}) \\  
& \dots &\\ 
a(z_{n,1})  & \dots & a(z_{n,d}) \\ 
\end{pmatrix}$$
Note: le biais $b$ est un vecteur ligne; $X \cdot W^T + b$ signifie qu'on ajoute $b$ à chaque ligne de la matrice $X \cdot W^T$.
<!-- $$W = \begin{pmatrix}
w_{1,1} & w_{1,2} & \dots & w_{1,d} \\  
w_{2,1} & w_{2,2} & \dots & w_{2,d} \\ 
& &\dots \\ w_{n,1} & w_{n,2} & \dots & w_{n,d} \\ 
\end{pmatrix}$$ -->

## 3.2 Conventions de variables et notations

- On note $L$ le nombre de couches du réseau; on utilisera $l$ pour dénoter l'indice d'une couche quelconque.
- On note $U \odot V$ le produit de Hadamard entre les matrices $U$ et $V$ (produit terme à terme).
## 3.3 Calcul de la valeur de sortie du réseau

Pour calculer la valeur de sortie du réseau, on va calculer successivement la valeur des $Y_l$, avec les formules 
$$\begin{eqnarray}Z_{l+1} &=& Y_l \cdot W_{l+1}^T + b_{l+1}\\
Y_{l+1} &=& A(Z_{l+1})\end{eqnarray}$$
## 3.4 Mise à jour des poids du réseau

Dans le cas matriciel, on peut exprimer les $\delta_l$ comme:
$$\begin{eqnarray}
\delta_L &=& (Y - T) \odot A_o'(Z_L) \\
\delta_{l-1} &=& (\delta_{l} \, W_{l}) \odot A'(Z_{l-1})
\end{eqnarray}$$
Les dérivées partielles de $E$ par rapport aux $W_l$ / $b_l$ s'écrivent:
$$\begin{eqnarray}
\frac{\partial E}{\partial W_l} &=& \frac{1}{N} \delta_l^T \cdot Y_{l-1}\\
\frac{\partial E}{\partial b_l} &=& \frac{1}{N} \sum_{i=1}^N \delta_l^{(i)} \\
\end{eqnarray}$$

où 
- $N$ est le nombre d'échantillons d'entrainement (i.e. le nombre de lignes dans la matrice d'entrée $X$).
- $\delta_l^{(i)}$ est la $i^{\text{ème}}$ ligne de la matrice $\delta_l$; pour obtenir $\frac{\partial E}{\partial b_l}$ on additionne les lignes de $\delta_l$, afin d'obtenir une unique ligne.
- $A$ est la fonction qui applique la fonction d'activation $a$ à chaque élément d'une matrice; de même, $A'$ applique $a'$ à chaque élément.

La mise à jour des poids s'obtient enfin en appliquant pour chaque couche $l$:
$$\begin{eqnarray}
W_{l} &=&W_{l} - \eta \frac{\partial E}{\partial W_l} \\
b_l &=&b_l -  \eta\frac{\partial E}{\partial b_l}\\
\end{eqnarray}$$
# 4. Élan

## 4.1 Motivation

La règle de mise à jour ne prend en compte que le gradient **courant** : chaque poids est déplacé proportionnellement à $\frac{\partial E}{\partial W_l}$
Dans les « vallées » étroites de la surface d'erreur, le gradient oscille d'un bord à l'autre : la descente avance en **zigzag** et converge lentement. 

## 4.2 Principe

L'**élan** (momentum) consiste à accumuler une **vitesse** $v$ et à déplacer les poids selon cette vitesse plutôt que selon le gradient brut. Le gradient ne modifie plus directement $W$, il modifie la vitesse :

$$v \leftarrow \mu\, v + \eta\,\frac{\partial E}{\partial W}, \qquad W \leftarrow W - v$$

- $\eta$ : pas d'apprentissage
- $\mu \in [0,1)$ : coefficient d'élan, typiquement $0.9$
- $v$ : vitesse, même forme que $W$, initialisée à $0$

> [!note] Cas particulier
> $\mu = 0$ redonne exactement la descente de gradient classique : $v = \eta\,\frac{\partial E}{\partial W}$, donc $W \leftarrow W - \eta\,\frac{\partial E}{\partial W}$.

## 4.3 Pourquoi ça accélère

La vitesse est une moyenne pondérée des gradients passés :

$$v^{(t)} = \eta \sum_{k=0}^{t-1} \mu^{k}\, \frac{\partial E}{\partial W}^{(t-k)}$$

- Les composantes du gradient qui gardent le même signe **s'accumulent** : on accélère le long de la vallée.
- Les composantes qui oscillent d'un bord à l'autre **se compensent** : le zigzag est amorti.

Image : une bille qui roule. La gravité (le gradient) l'accélère, l'inertie ($\mu$) l'empêche de changer brusquement de direction.

## 4.4 En pratique

On garde en mémoire une vitesse par paramètre (en plus des poids) et, à chaque étape, on remplace la mise à jour directe par :

$$v \leftarrow \mu\, v + \eta\,\frac{\partial E}{\partial W}, \qquad W \leftarrow W - v$$

> [!info] Ce que ça ne change pas
> L'élan ne modifie **ni** le calcul du gradient (§2) **ni** sa forme : il change seulement la façon de l'utiliser pour mettre à jour les poids. C'est un hyperparamètre de plus ($\mu$) à régler.
 