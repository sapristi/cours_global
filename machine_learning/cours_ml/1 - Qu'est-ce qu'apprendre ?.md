---
titre: 02 - Qu'est-ce qu'apprendre ?
cours: "[[Entrypoint]]"
partie: 1
statut: draft
Contexte: |-
  4e année post-bac, 18h au total.
  Pas de prérequis ML. Python et Octave utilisés plus tard.
  Partie 2 : poser le vocabulaire et l'intuition avant les modèles.
---

> [!abstract] Objectif de cette partie
> Distinguer les formes d'apprentissage, comprendre la différence entre **mémoriser** et **généraliser**, et distinguer **classification** vs **régression**.

---
# 1. Introduction - Apprentissage automatique

## 1.1 L'apprentissage automatique: qu'est ce que c'est ?


> [!info] Idée centrale
> Apprendre = exploiter des données (passées), pour construire un modèle réutilisable (sur de futures données)


![[Pasted image 20260928144728.png]]


- On dispose d'un *modèle* (algorithme ou réseau de neurone)
- On dispose de *données d'entrainement*
- On va *entraîner* le modèle sur les données d'entraînement
- On obtient un *modèle "entraîné"*, qui va être capable d'exprimer une sortie sur des données d'entrée "nouvelles".

![[Pasted image 20260928173641.png|301]]

## 1.2 Applications


- reconnaissance de caractères / d'images
- reconnaissance de spam
- détection de fraude
- traduction
- prédiction (de vente, de croissance, etc)
- météo

## 1.3 Quel type de données ?

**En entrée:**
- texte
- valeurs numériques

**En sortie:**
- valeurs numériques / valeur quantitative→ **régression**
- catégories / valeur qualitative→ **classification**
- texte

> [!info] Dans tous les cas, on peut ramener les différents types de données à des valeurs numériques.

> [!question] Classifier les exemples précédents entre régression et classification.

# 2. Deux formes d'apprentissage automatique
## 2.1 Apprentissage supervisé

![[Pasted image 20260928183350.png]]


On entraîne le modèle sur des données dont on sait déjà quelle est la sortie attendue.

## 2.2 Apprentissage non supervisé

![[Pasted image 20260928183440.png]]

On entraîne le modèle sur des données pour lesquelles on ne sait pas quelle est la sortie attendue; on espère que l'entraînement va permettre de "découvrir" une structure dans les données d'entrée.

> [!note]
> - Globalement moins performant que l'apprentissage supervisé
> - Ne nécessite pas de données labellisées (qui coûtent cher)

# 3. Apprentissage supervisé : tentative de généralisation



![[Pasted image 20260928145826.png|398]]

## 3.1 Apprendre par cœur VS généraliser

> [!example] Par cœur vs tendance (régression polynomiale)
> - Mêmes points bruités autour d'une courbe douce.
> - Degré 1 : rate partout (sous-apprentissage).
> - Degré 4 environ : capte la tendance, petite erreur train stable.
> - Degré 15 : passe par tous les points, erreur train = 0 mais zigzague au moindre bruit = par cœur.
> Retenir : erreur train 0 ne prouve rien, c'est même suspect.

## 3.2 Qu'est-ce que généraliser ?

> [!info] Généraliser = être bon sur du non-vu
> Généraliser = erreur faible sur des données **non vues** à l'entraînement.
> Vocabulaire : **erreur train** (sur données d'entraînement) vs **erreur test** (sur données gardées de côté, split train/test).
> Schéma : train -> entraîne, test verrouillé -> juge.

## 3.3 Comment valider sans se mentir ? (hold-out)

> [!danger] Ne jamais juger sur le train seul
> Protocole hold-out : 1) couper le jeu en train/test, 2) entraîner sur train seul, 3) mesurer une fois sur test verrouillé.
> Le test ne sert pas à régler le modèle, sinon il devient du train déguisé.

---

