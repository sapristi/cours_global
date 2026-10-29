---
titre: 6 - Support Vector Machines
cours: "[[Entrypoint]]"
partie: 6
statut: draft
Contexte: |-
  4e année post-bac, 18h au total.
  Suite de [[2 - Perceptron]] et [[3- Données non linéairement séparables]].
  Séance de 1h15 : ~25 min de cours, ~50 min de TD (TD05).
  Pas de résolution formelle (Lagrangien, dual, KKT hors programme).
---
> [!abstract] Objectif de cette partie
> Comprendre **pourquoi** le SVM choisit une séparation particulière, la **marge maximale** ; **comment** on l'écrit comme un problème d'optimisation ; et pourquoi c'est, au fond, un **perceptron amélioré** que l'on entraîne par descente de gradient.

> [!danger] Changement de convention : cibles $\pm 1$
> Dans tout ce chapitre (et au TD05), les cibles valent $t \in \{-1, +1\}$, et non plus $\{0, 1\}$ comme au [[2 - Perceptron|chapitre 2]] et au TD01. Avec le score $z = w \cdot x + b$, la sortie est $y = \text{sign}(z)$.
> Intérêt : un point est **bien classé** si et seulement si $t\,z > 0$. 

# 1. Intuition : quelle droite choisir ?

Sur un jeu linéairement séparable, il existe une **infinité** de droites qui séparent parfaitement les données.

![[assets/05-svm-separateurs.png]]

Le perceptron s'arrête sur la première qu'il trouve : elle dépend de l'initialisation et de l'ordre de présentation des points, et elle **frôle** souvent un point (droite « limite » en pointillés). Un nouveau point légèrement bruité de ce côté-là sera mal classé.

Intuitivement, on préfère la droite qui laisse **le plus de place possible de chaque côté** (en vert) : un point un peu déplacé reste du bon côté.

> [!info] Définitions (informelles)
> - **Marge** : distance entre la droite séparatrice et le point d'entraînement le plus proche.
> - **SVM** (*Support Vector Machine*) : choisit la droite de **marge maximale**. Elle est **unique**.
> - **Vecteurs de support** : les points les plus proches, ceux qui « touchent » la marge. Eux seuls déterminent la droite : déplacer un autre point (sans franchir la marge) ne change rien.

# 2. Formalisation : marge dure

## 2.1 Distance à l'hyperplan

L'hyperplan séparateur est $\{x : w \cdot x + b = 0\}$ ; $w$ lui est **normal**. La distance (admise) d'un point $x_i$ à cet hyperplan vaut :

$$d(x_i) = \frac{|w \cdot x_i + b|}{\|w\|}$$

Si le point est bien classé, $|w \cdot x_i + b| = t_i (w \cdot x_i + b)$. La marge d'un séparateur est donc :

$$\text{marge}(w, b) = \min_i \frac{t_i (w \cdot x_i + b)}{\|w\|}$$

(négative si un point est mal classé : c'est la fonction que l'on code en premier au TD).

## 2.2 Normalisation

Multiplier $(w, b)$ par $\alpha > 0$ ne change **pas** l'hyperplan. On peut donc fixer l'échelle en imposant que les points les plus proches vérifient :

$$\min_i t_i (w \cdot x_i + b) = 1$$

Alors les points les plus proches sont à distance $1/\|w\|$, et la bande vide entre les deux classes, délimitée par $z = -1$ et $z = +1$, a pour largeur $2/\|w\|$.

![[assets/05-svm-marge.png]]

> [!info] Lecture
> Trait plein : frontière $z = 0$. Pointillés : $z = \pm 1$. Les trois points entourés sont les vecteurs de support : ils sont exactement sur $z = \pm 1$. Aucun point d'entraînement n'est dans la bande.

## 2.3 Le problème d'optimisation

Maximiser la marge $1/\|w\|$ revient à minimiser $\|w\|^2$ (plus commode) :

$$\min_{w,\,b} \ \frac{1}{2}\|w\|^2 \quad \text{sous les contraintes} \quad t_i (w \cdot x_i + b) \ge 1, \quad i = 1, \dots, N$$

C'est un problème de **programmation quadratique** : objectif quadratique, contraintes linéaires. Il a une **solution unique** (si les données sont séparables) et des **solveurs dédiés** le résolvent efficacement. On l'admet : sa résolution est hors programme.

# 3. Marge souple

## 3.1 Variables d'écart

Si les données ne sont pas séparables (bruit, point aberrant), les contraintes $t_i z_i \ge 1$ sont impossibles à satisfaire toutes. On autorise chaque point à violer sa contrainte d'une quantité $\xi_i \ge 0$ (variable d'écart), que l'on fait payer :

$$\min_{w,\,b,\,\xi} \ \frac{1}{2}\|w\|^2 + C \sum_{i=1}^N \xi_i \quad \text{s.c.} \quad t_i (w \cdot x_i + b) \ge 1 - \xi_i, \quad \xi_i \ge 0$$

![[assets/05-svm-marge-souple.png]]

> [!info] Lecture de $\xi_i$
> - $\xi_i = 0$ : point hors de la bande, du bon côté (aucune pénalité).
> - $0 < \xi_i \le 1$ : point **dans la bande** mais encore bien classé ($\xi_1$ sur la figure).
> - $\xi_i > 1$ : point **mal classé** ($\xi_2$, $\xi_3$).
>
> Seules les violations les plus nettes sont annotées : d'autres points (par exemple un $+1$ légèrement à l'intérieur de sa marge) ont aussi un petit $\xi_i > 0$.
>
> Les **vecteurs de support** sont alors tous les points tels que $t_i z_i \le 1$ (sur la marge, dans la bande ou mal classés) : ce sont eux qui fixent la frontière.

> [!info] Rôle de $C$
> - $C$ **grand** : chaque violation coûte cher, on colle aux données ; marge étroite (à la limite, marge dure).
> - $C$ **petit** : on accepte des violations pour avoir une marge large ; modèle plus simple, plus robuste au bruit.
>
> $C$ arbitre entre **marge large** et **erreurs d'entraînement** : c'est un hyperparamètre de régularisation, à choisir sur des données de validation.

## 3.2 Réécriture sans contraintes : la perte hinge

À l'optimum, chaque $\xi_i$ est le plus petit possible : $\xi_i = \max(0,\ 1 - t_i z_i)$. On remplace dans l'objectif, puis on divise tout par $NC$ (ce qui ne change pas le minimum) :

$$E(w, b) = \frac{\lambda}{2}\|w\|^2 + \frac{1}{N} \sum_{i=1}^N \max\big(0,\ 1 - t_i (w \cdot x_i + b)\big)$$

- $\max(0, 1 - t z)$ est la **perte hinge** (« charnière ») : nulle si le point est au-delà de sa marge ($t z \ge 1$), linéaire sinon.
- $\lambda = 1/(NC)$ : grand $\lambda$ ⇔ petit $C$ ⇔ marge large.
- Le biais $b$ n'est **pas** régularisé.

Plus de contraintes : on peut minimiser $E$ par **descente de gradient**, comme d'habitude.

## 3.3 Sous-gradient

La hinge n'est pas dérivable en $t z = 1$ ; on prend la dérivée 0 en ce point (sous-gradient). En notant $z_i = w \cdot x_i + b$ :

$$\frac{\partial E}{\partial w} = \lambda w - \frac{1}{N} \sum_{i \,:\, t_i z_i < 1} t_i\, x_i \qquad\qquad \frac{\partial E}{\partial b} = -\frac{1}{N} \sum_{i \,:\, t_i z_i < 1} t_i$$

puis $w \leftarrow w - \eta \frac{\partial E}{\partial w}$, $b \leftarrow b - \eta \frac{\partial E}{\partial b}$.

> [!example] Lecture (c'est ce qu'on code au TD)
> - Seuls les points qui **violent leur marge** ($t_i z_i < 1$) contribuent : chacun tire $w$ dans la direction $t_i x_i$, pour se repousser du bon côté.
> - Le terme $\lambda w$ fait **rétrécir** $w$ à chaque pas, donc élargit la marge $1/\|w\|$ (et la bande $2/\|w\|$).
> - Les points bien au-delà de leur marge n'interviennent pas.

# 4. Lien avec le perceptron

Le perceptron minimise lui aussi une perte, $\max(0, -t z)$ : nulle dès que le point est bien classé. Une descente de gradient **stochastique** (un point à la fois) sur cette perte donne, pour un point mal classé ($t z \le 0$) :

$$w \leftarrow w + \eta\, t\, x, \qquad b \leftarrow b + \eta\, t$$

C'est exactement la **règle de Rosenblatt** du [[2 - Perceptron|chapitre 2]] réécrite avec des cibles $\pm 1$ : $w \leftarrow w - r\,(y - t)\,x$ y devient $w \leftarrow w + 2r\,t\,x$ car $y - t = -2t$ ; le pas, noté $r$ au chapitre 2, absorbe ce facteur 2 ($\eta = 2r$).

![[assets/05-svm-pertes.png]]

| | Perceptron | SVM (marge souple) |
|---|---|---|
| Perte par point | $\max(0, -t z)$ | $\max(0, 1 - t z)$ |
| Point bien classé mais proche | ignoré | pénalisé (on exige $t z \ge 1$) |
| Régularisation | aucune | $\frac{\lambda}{2}\|w\|^2$ : maximise la marge |
| Données séparables | *une* droite, qui dépend de l'ordre et de l'initialisation | *la* droite de marge maximale |
| Données bruitées | ne converge pas, oscille | minimise $E$, se stabilise |

**SVM = perceptron + « 1 » (on exige une marge) + $\|w\|^2$ (on la maximise).**

# 5. Ouverture : SVM non linéaire

Comme au [[3- Données non linéairement séparables|chapitre 3]], remplacer $x$ par $\Phi(x)$ donne un SVM à frontière non linéaire (c'est le bonus du TD). L'**astuce du noyau** permet de le faire efficacement, même quand $\Phi$ est de très grande (voire infinie) dimension : partie 9.

---

> [!note] À retenir
> 1. Cibles $t \in \{-1, +1\}$ : bien classé ⇔ $t z > 0$.
> 2. Parmi tous les séparateurs, le SVM choisit celui de **marge maximale** ; il ne dépend que des **vecteurs de support**.
> 3. Marge dure : $\min \frac{1}{2}\|w\|^2$ s.c. $t_i z_i \ge 1$ (programmation quadratique, solveurs dédiés).
> 4. Marge souple : $E(w, b) = \frac{\lambda}{2}\|w\|^2 + \frac{1}{N}\sum \max(0, 1 - t_i z_i)$, minimisée par descente de (sous-)gradient.
> 5. $\lambda$ (ou $C$) arbitre entre marge large et erreurs d'entraînement.
> 6. Perceptron : une droite quelconque, oscille sur données bruitées. SVM : la droite de marge maximale, stable.
