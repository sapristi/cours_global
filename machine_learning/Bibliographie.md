---
titre: "Bibliographie"
cours: "[[Entrypoint]]"
statut: draft
Contexte: |-
  Livres de référence pour les 9 parties du cours.
  Critère de choix : accessibles pour des étudiants de 4e année, pas pointus.
  Priorité aux ouvrages qui couvrent perceptron, MLP, RBF/Lloyd, SVM et noyaux.
---

> [!abstract] Comment lire cette bibliographie
> Un seul livre couvre presque tout le programme : **Marsland**.
> Un seul livre court et français : **Azencott**.
> Pour la théorie de la généralisation (parties 2.b et 7) : **Learning from Data**.

# 1. Les trois livres à recommander en priorité

## 1.1 Marsland — référence principale

> [!note] Stephen Marsland, *Machine Learning: An Algorithmic Perspective*, 2e éd., CRC Press, 2014
> - Niveau L3/M1, écrit pour des étudiants **sans fortes bases statistiques**.
> - Chaque algorithme est implémenté en Python/NumPy, code librement téléchargeable sur le site de l'auteur.
> - Chapitres utiles :
>   - 3 *Neurons, Neural Networks, and Linear Discriminants* → perceptron, règles d'apprentissage
>   - 4 *The Multi-Layer Perceptron* → rétropropagation, dérivation complète, élan, arrêt de l'apprentissage
>   - 5 *Radial Basis Functions and Splines* → réseaux RBF
>   - 7 *Probabilistic Learning* → plus proches voisins
>   - 8 *Support Vector Machines* → marge, variables d'écart, noyaux
>   - 13 *Decision by Committee* → boosting, bagging
>   - 14 *Unsupervised Learning* → k-means (Lloyd)

## 1.2 Azencott — référence en français

> [!note] Chloé-Agathe Azencott, *Introduction au machine learning*, 3e éd., Dunod (coll. InfoSup), 2025
> - 288 pages, **85 exercices corrigés**. Niveau L3/M1 école d'ingénieur.
> - Chapitres utiles :
>   - 7 *Réseaux de neurones artificiels* → perceptron, perceptron multi-couches
>   - 8 *Méthodes des plus proches voisins*
>   - 10 *Machines à vecteurs de support et méthodes à noyaux* → marge rigide, marge souple, noyau
>   - chapitre *Clustering*
> - La version électronique de la 2e édition est disponible gratuitement sur le site de l'auteure.

## 1.3 Learning from Data — pour la théorie

> [!note] Y. Abu-Mostafa, M. Magdon-Ismail, H.-T. Lin, *Learning from Data: A Short Course*, AMLBook, 2012
> - ~200 pages, écrit « comme une histoire », se lit d'une traite.
> - Indispensable sur **généralisation / dimension VC / surapprentissage / régularisation / validation**.
> - Le MOOC Caltech associé (18 lectures) est gratuit ; les e-chapters couvrent *Neural Networks*, *Support Vector Machines*, *Radial Basis Functions*, *Similarity-Based Methods*.

# 2. Correspondance livres ↔ parties du cours

| Partie du cours | Marsland | Azencott | Learning from Data | Alpaydin |
|---|---|---|---|---|
| 2. Qu'est-ce qu'apprendre ? | ch. 1-2 | ch. 1-3 | ch. 1-2 | ch. 1-2 |
| 3. Séparations linéaires | ch. 3 | §7.1 | ch. 3, e-ch. 1 | §11.2-11.3 |
| 4. Données non séparables | ch. 3-4 | — | ch. 3 | §11.4 |
| 5. Perceptron multi-couches | ch. 4 | §7.2 | e-ch. 7 | ch. 11 |
| 6. RBF et Lloyd | ch. 5 | — | e-ch. 6, 8 | — |
| 7. Surapprentissage | ch. 4.3, 13 | ch. 3, 6 | ch. 4, 5 | ch. 11 |
| 8. SVM | ch. 8 | ch. 10 | e-ch. 8 | ch. 14 |
| 9. Machines à noyau | ch. 8 | ch. 10 | e-ch. 8 | ch. 14 |

# 3. Compléments

> [!note] Ethem Alpaydin, *Introduction to Machine Learning*, 4e éd., MIT Press, 2020
> Très clair, beaucoup d'exercices. Bon sur perceptron / MLP / rétropropagation (ch. 11) et sur les SVM + kernel trick (ch. 14). Ne traite pas les RBF ni Lloyd.

> [!example] Pour la mise en œuvre pratique
> Aurélien Géron, *Machine Learning avec Scikit-Learn* (3e éd., Dunod) — pour montrer l'équivalent « bibliothèque » des algorithmes implémentés à la main. Utile surtout pour la partie 1 (écosystème de travail).

# 4. Références plus denses (à feuilleter, pas à lire linéairement)

- **Simon Haykin**, *Neural Networks and Learning Machines*, 3e éd., Pearson. Suit le plan du cours presque chapitre par chapitre : perceptron de Rosenblatt → LMS → rétropropagation → RBF + k-means → SVM → régularisation → Hebb/PCA. Très complet mais ~900 pages.
- **Cornuéjols, Miclet, Barra**, *Apprentissage artificiel*, 4e éd., Eyrolles. La référence française, mais 990 pages et niveau M1/M2.

> [!danger] À éviter pour ce cours
> Christopher Bishop, *Pattern Recognition and Machine Learning*, et Hastie, Tibshirani, Friedman, *The Elements of Statistical Learning* : excellents mais trop pointus pour le niveau visé.
