---
titre: 6 - Réseaux RBF
cours: "[[Entrypoint]]"
partie: 6
statut: draft
Contexte: |-
  4e année post-bac, 18h au total.
  Suite de [[4 - Réseaux de neurones à plusieurs couches]] et [[5 - Évaluer un modèle]].
  Séance de 1h30 au plus : ~20 min de cours, ~60 min de TD (TD05).
  k-means (algorithme de Lloyd) : principe expliqué, sans formalisation, pas codé.
---
> [!abstract] Objectif de cette partie
> Découvrir deux modèles qui raisonnent par **proximité** : les **k plus proches voisins** (k-NN) et les **réseaux à fonctions de base radiales** (RBF). Comprendre ce qui distingue un neurone RBF (réponse **locale**) d'un neurone sigmoïde (réponse **globale**), et pourquoi un réseau RBF s'entraîne simplement, en combinant apprentissage **non supervisé** (placement des centres) et **supervisé** (couche de sortie).

Les cibles sont à nouveau $t \in \{0, 1\}$ et la sortie $y \in [0, 1]$ est une probabilité, comme au [[4 - Réseaux de neurones à plusieurs couches|chapitre 4]].

# 1. Du k-NN au RBF

## 1.1 Les k plus proches voisins

Pour classer un nouveau point $x$ :
1. calculer sa distance $\|x - x_i\|$ à **tous** les points d'entraînement ;
2. garder les $k$ plus proches ;
3. répondre l'étiquette **majoritaire** parmi eux.

Il n'y a **pas d'entraînement** : on garde les données, tout le travail se fait à la prédiction (modèle *paresseux*).

![[assets/07-rbf-knn.png]]

> [!info] Lecture
> Avec $k = 1$, la frontière suit chaque point, y compris les points bruités : surapprentissage. Avec $k = 15$, le vote lisse la frontière. $k$ règle la complexité du modèle.

## 1.2 Vers une influence « douce »

Le vote du k-NN est **dur** : les $k$ voisins comptent autant, les autres pas du tout. Idée : faire compter **tous** les points, avec une influence qui **décroît avec la distance**. Il faut pour cela une fonction « en cloche » de la distance : c'est la fonction à base radiale.

# 2. La fonction à base radiale

Une fonction à base radiale ne dépend que de la **distance** à un centre $c$. On utilise la gaussienne :

$$\varphi(x) = \exp\left(-\frac{\|x - c\|^2}{2\sigma^2}\right)$$

- $\varphi(c) = 1$ : activation maximale au centre ;
- $\varphi(x) \to 0$ quand $x$ s'éloigne de $c$ ;
- la **largeur** $\sigma$ règle la portée de la bosse.

![[assets/07-rbf-bosses-1d.png]]

En 2D, c'est une bosse circulaire autour du centre :

![[assets/07-rbf-bosse-2d.png]]

# 3. Neurone sigmoïde ou neurone RBF

|                   | Neurone sigmoïde (chapitre 4)                  | Neurone RBF                       |
| ----------------- | ---------------------------------------------- | --------------------------------- |
| Calcul            | $\text{sigmoid}(w \cdot x + b)$                | $\varphi(\|x - c\|)$              |
| Paramètres        | poids $w$, biais $b$                           | centre $c$, largeur $\sigma$      |
| Zone d'activation | un **demi-plan**                               | une **bosse** autour de $c$       |
| Réponse           | **globale** : forte jusqu'à l'infini d'un côté | **locale** : nulle loin du centre |

![[assets/07-rbf-sigmoide-vs-rbf.png]]

> [!info] Lecture
> Le neurone sigmoïde découpe le plan par une droite (trait blanc, activation 0.5) et reste actif sur tout un demi-plan. Le neurone RBF ne répond qu'au voisinage de son centre (croix) ; le cercle blanc est la ligne où son activation vaut 0.5.

# 4. Architecture d'un réseau RBF

Un réseau RBF a **une seule couche cachée** :
- **couche cachée** : $K$ neurones RBF, de centres $c_1, \dots, c_K$ et de même largeur $\sigma$ ; ils calculent $\varphi_k(x) = \exp\left(-\|x - c_k\|^2 / 2\sigma^2\right)$ ;
- **sortie** : un neurone classique (linéaire puis sigmoïde) sur ces activations :

$$y = \text{sigmoid}\left(\sum_{k=1}^{K} w_k\, \varphi_k(x) + b\right)$$

![[assets/07-rbf-architecture.png]]

Chaque neurone caché « couvre » une région de l'espace ; la sortie combine ces régions. Une somme pondérée de bosses suffit à approcher n'importe quelle fonction régulière, pourvu qu'on ait assez de centres :

![[assets/07-rbf-somme-bosses.png]]

> [!example] Lien avec le k-NN
> Un point $x$ proche des centres de classe 1 active surtout des bosses de poids $w_k > 0$, d'où $y$ proche de 1. Comme un k-NN, le réseau répond selon les **voisins** de $x$, mais avec une pondération douce plutôt qu'un vote.

# 5. Apprentissage : non supervisé, puis supervisé

Contrairement au perceptron multicouche, on n'apprend **pas** tout par rétropropagation. L'apprentissage d'un réseau RBF enchaîne deux familles d'apprentissage :
- **non supervisé** : on n'utilise que les entrées $X$, **sans les cibles** $t$ ; on cherche la structure des données (où sont-elles ? comment se regroupent-elles ?) ;
- **supervisé** : on utilise les couples $(x, t)$ ; on apprend à prédire $t$ à partir de $x$, comme depuis le début du cours.

| Étape | Paramètres | Utilise les cibles $t$ ? | Méthode |
|---|---|---|---|
| 1 | centres $c_1, \dots, c_K$ | **non** | k-means : apprentissage **non supervisé** |
| 2 | largeur $\sigma$ | — | hyper-paramètre, choisi à la main |
| 3 | poids $w$, biais $b$ | **oui** | descente de gradient : apprentissage **supervisé** |

## 5.1 Placer les centres : k-means (non supervisé)

On veut $K$ centres qui **résument** les données : $K$ points représentatifs, répartis là où se trouvent les exemples d'entraînement. C'est ce que fait l'algorithme **k-means** (algorithme de **Lloyd**), qui regroupe les points en $K$ paquets (*clusters*) et place un centre au milieu de chacun.

Principe :
1. **Départ** : on prend $K$ points d'entraînement comme centres initiaux.
2. **Affectation** : chaque point d'entraînement est rattaché au centre **le plus proche**. On obtient $K$ paquets.
3. **Mise à jour** : chaque centre est déplacé à la **moyenne** des points de son paquet (le « milieu » du paquet).
4. On **répète** 2 et 3 jusqu'à ce que les centres ne bougent plus.

À chaque tour, les centres glissent vers le cœur des groupes de points ; en quelques itérations, ils se stabilisent. Résultat : une zone dense en données reçoit plusieurs centres, une zone vide n'en reçoit aucun, et deux centres ne se retrouvent pas l'un sur l'autre.

> [!info] Les étiquettes ne servent pas
> k-means ne regarde que les positions des points, pas leur classe. Un centre peut donc tomber dans une zone où les deux classes se mélangent : ce n'est pas un problème, c'est la couche de sortie (étape 3) qui apprendra quel poids donner à chaque bosse.

## 5.2 Fixer la largeur $\sigma$

$\sigma$ est un **hyper-paramètre** : on le choisit, on ne l'apprend pas. Ordre de grandeur : la distance typique entre centres voisins, pour que les bosses se recouvrent un peu (voir section 6).

## 5.3 Apprendre $w$ et $b$ (supervisé)

Une fois les centres et $\sigma$ fixés, $\Phi(X)$ (les activations, de forme $(N, K)$) est une **nouvelle représentation** des données. Il ne reste qu'**une seule couche** à apprendre, sur l'entrée $\Phi(X)$ et avec les cibles $t$ : c'est la descente de gradient du [[4 - Réseaux de neurones à plusieurs couches|chapitre 4]], sans rétropropagation.

> [!info] Moindres carrés
> Avec une sortie **linéaire** (sans sigmoïde), trouver $w$ est un problème de moindres carrés : on obtient la solution directement, en une seule résolution d'un système linéaire, sans itérer.

## 5.4 Bilan

On retrouve l'idée du [[3- Données non linéairement séparables|chapitre 3]] : $\Phi$ envoie les données dans un espace (de dimension $K$) où elles deviennent linéairement séparables. La différence : $\Phi$ n'est pas choisie à la main, elle est **apprise à partir des données, sans les étiquettes**. Le réseau RBF combine donc :
- une partie **non supervisée** (k-means) qui construit la représentation $\Phi$ ;
- une partie **supervisée** (le neurone de sortie) qui classe dans cette représentation.

> [!note] Et si on apprenait tout par gradient ?
> C'est possible : centres et largeurs peuvent aussi être ajustés par rétropropagation, comme un MLP. Mais on perd ce qui fait l'intérêt du RBF : le problème devient plus difficile (minima locaux) et plus lent. En pratique, on garde l'apprentissage en deux temps.

# 6. Ce qu'il faut régler, ce qu'il faut savoir

- **$\sigma$ trop petit** : chaque bosse ne couvre que son centre, le réseau apprend par cœur (surapprentissage). **$\sigma$ trop grand** : toutes les bosses se ressemblent, la frontière est trop lisse (sous-apprentissage).
- **$K$** joue le même rôle : avec un centre par point d'entraînement ($K = N$), le réseau peut interpoler exactement les données d'entraînement.
- **Loin des données**, toutes les activations $\varphi_k(x)$ tombent à 0 : la sortie se fige sur la constante $\text{sigmoid}(b)$, qui ne dépend plus de $x$. Attention : ce n'est pas un vrai « je ne sais pas », cette constante peut être au-dessus de 0.5 et classer tout le plan lointain dans une même classe. Un MLP, lui, prolonge ses demi-plans et répond 0 ou 1 avec assurance, même là où il n'a jamais vu de données.
- La même gaussienne servira de **noyau** au SVM non linéaire ([[7 - Support Vector Machines|chapitre 7]], section 5) : même fonction, autre usage.

---

> [!note] À retenir
> 1. **k-NN** : pas d'entraînement, vote des $k$ plus proches voisins ; $k$ règle le lissage.
> 2. **Neurone RBF** : $\varphi(x) = \exp(-\|x - c\|^2 / 2\sigma^2)$, réponse **locale** ; le neurone sigmoïde a une réponse **globale**.
> 3. **Réseau RBF** : $y = \text{sigmoid}(\sum_k w_k \varphi_k(x) + b)$, un « k-NN adouci ».
> 4. **Apprentissage en deux temps** : d'abord les centres par k-means (**non supervisé**, sans les cibles) et $\sigma$ à la main, puis seulement $w, b$ (**supervisé**) : une seule couche, apprentissage rapide.
> 5. $\sigma$ et $K$ règlent la complexité ; loin des données, la sortie est constante.
