# 1. Introduction

Le perceptron (introduit en 1957) est un modèle d'apprentissage basé sur un neurone (simplifié) associé à une règle d'apprentissage.

## 1.1 Modèle de neurone

![[Pasted image 20260928193206.png]]

- L'entrée (*input*) varie à chaque "utilisation" du neurone)
- Les poids (*weight*) font partie du neurone. Ce sont eux qui seront modifiés lors de l'apprentissage. Les poids varient entre -1 et 1.
- On ajoute un poids $w_0$ relié à une constante (on verra plus tard la raison)
- Le neurone va d'abord calculer la somme $\Sigma_i x_i * w_i$
- Cette somme passe enfin à travers la fonction d'activation (*step function*), qui va normaliser la valeur de sortie (par exemple, la sortie pourra prendre pour valeur 0 ou 1)


> [!exemple] La fonction de Heaviside est une fonction d'activation classique:
> $$\ H(x)=\left\{\begin{matrix} 0 & \mathrm{si} & x < 0 \\ 1 & \mathrm{si} & x \ge 0. \end{matrix}\right.$$


## 1.2 Exercices

- On se place en dimension 2 (i.e. $n = 2$).
- On choisit la fonction de Heaviside comme fonction d'activation


![[Pasted image 20260928200223.png|225]]
On peut alors représenter l'action du neurone de la manière suivante: 
- le vecteur d'entrée $(x_1, x_2)$ est un point du plan
- le neurone sépare le plan en deux parties: la partie où le neurone est activé (la sortie vaut 1), et la partie où le neurone n'est pas activé



### [!faq] Exercice 1

Déterminer sur quelle partie du plan les neurones dotés des poids suivants sont activés:
1. $w_0 = 0; \hspace{0.5cm} w_1=1; \hspace{0.5cm} w_2=1$
2. $w_0 = 0; \hspace{0.5cm} w_1=-1; \hspace{0.5cm} w_2=2$
3. $w_0 = 0; \hspace{0.5cm} w_1=0; \hspace{0.5cm} w_2=1$
4. $w_0 = 1; \hspace{0.5cm} w_1=1; \hspace{0.5cm} w_2=1$
5. $w_0 = -1; \hspace{0.5cm} w_1=1; \hspace{0.5cm} w_2=1$

Indice: on pourra s'intéresser à la "frontière" (qui sépare les deux zones du plan), représentée par l'équation $x_1*w_1 + x_2*w_2 - w_0 = 0$.

### [!faq] Exercice 2
Quelle serait le problème si on n'avait pas introduit le *biais* (poids $w_0$) ?

### [!faq] Exercice 3
Implémenter en python un tel neurone, à l'aide d'une classe `Perceptron`.


# 2. Apprentissage

Afin de faire en sorte que le neurone puisse apprendre, nous allons utiliser un algorithme qui va faire évoluer les poids, à l'aide de données d'entrainement.

Le principe est le suivant:
- on choisit un pas d'apprentissage $r$ (typiquement $r = 0.1$)
- on initialise tous les poids à 0
- pour chacun des vecteurs d'entrainement $x^j$ , on compare le résultat attendu $t^j$ à la sortie du neurone $y^j$:
	- s'ils sont égaux, on ne fait rien
	- sinon, on modifie les poids:
		- On modifie chaque poids $w_i  ← w_i - r*(y^j - t^j)*x_i$ 
- Recommencer l'étape précédente tant que les poids ont changé


### [!faq] Exercice 4
Ajouter une méthode `learn` à la classe `Perceptron`, qui prends en entrée un vecteur d'apprentissage, la cible, et mets à jour les poids du perceptron (une étape d'apprentissage). On prendra une valeur fixe pour le pas d'apprentissage, par exemple $r=0.1$.

Vérifier que la méthode fonctionne correctement sur les entrées suivantes. On pourra utiliser les fonctions fournies pour afficher le perceptron et les données d'apprentissage (voir la page https://sapristi.github.io/cours_ml).

**Entrée 1**

| x1  | x2  | t   |
| --- | --- | --- |
| 1   | 1   | 1   |
| 1   | 0   | 0   |
| 0   | 1   | 0   |
| 0   | 0   | 0   |

**Entrée 2**

| x1  | x2  | t   |
| --- | --- | --- |
| -1  | -1  | 1   |
| 1   | 1   | 0   |

**Entrée 3**

| x1   | x2   | t   |
| ---- | ---- | --- |
| -1.5 | 0.2  | 1   |
| -1   | 0.5  | 1   |
| -0.5 | 1    | 1   |
| -1.5 | -1   | 0   |
| -1   | -0.6 | 0   |
| -0.5 | 0    | 0   |

**Entrée 4**

| x1  | x2  | t   |
| --- | --- | --- |
| 1   | 1   | 0   |
| 1   | 0   | 1   |
| 0   | 1   | 1   |
| 0   | 0   | 0   |
Que remarque-t-on sur cette entrée ?


### [!faq] Exercice 5
Implémenter une méthode `train`, qui prends un entrée un jeu de données d'entrainement, et entraîne le perceptron.

### [!faq] Exercice 6
Généraliser l'implémentation du perceptron à une dimension quelconque grace à numpy.