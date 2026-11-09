# Contexte
Cours pour des étudiants de 3e année. On suppose des bases en programmation, et une connaissance superficielle de python.

**Objectifs Matière :**

- Réaliser des algorithmes en Python pour résoudre des problèmes de cybersécurité.
- Apprendre à utiliser les bibliothèques de Python (requests, socket) pour interagir avec le réseau.
- Développer des scripts d'analyse et de détection de menaces.
- Rédiger du code Python lisible, professionnel et documenté.

# Plan du cours
![[Cours.base]]


 
# Évaluation

## Compétences évaluées

1. **Connaissances en cybersécurité :** maîtriser le vocabulaire et les cadres (CIA, AAA, kill chain, IOC). Associer une menace à une phase d'attaque et à une défense adaptée, et connaître le cadre légal.
2. **Lecture et compréhension de code Python :** prédire le résultat d'un extrait de code, repérer et expliquer une erreur, décrire en français ce que fait un traitement (dont une chaîne d'opérations pandas).
3. **Compréhension des échanges réseau :** analyser une requête et une réponse HTTP, connaître le rôle du timeout et les risques liés aux bibliothèques tierces.
4. **Raisonnement algorithmique :** dérouler un algorithme à la main (parcours BFS/DFS, attaque temporelle). Estimer et comparer la complexité de plusieurs approches (force brute ou attaque par canal latéral).
5. **Analyse et détection de menaces :** calculer et interpréter des indicateurs sur des journaux (coefficient de variation, vitesse de déplacement, comptage de destinations). Poser un diagnostic, puis identifier et traiter les faux positifs.
6. **Esprit critique :** justifier un choix, expliquer les limites d'une méthode de détection et la contre-mesure qu'un attaquant pourrait lui opposer.

# Conventions

## Modules de cours

Chaque module (`N. <Titre>.md`) a un frontmatter avec `durée (h)` (nombre) et `Contexte` (texte, source du plan affiché ci-dessus via `Cours.base`).

Vocabulaire de référence (module 1) : CIA, AAA, vulnérabilité / exploit / payload / IOC / TTP, Kill Chain, Red / Blue team.

## Bibliothèques de référence

`socket`, `requests`, `hashlib`, `re`, `paramiko`, `pandas` (module 7).

## Cadre légal des exemples offensifs

> [!danger] Labo isolé uniquement
> Tout exemple offensif (scan avec `socket`, brute-force avec `requests` / `paramiko`, injection…) doit rappeler : **labo isolé uniquement, autorisation écrite préalable, art. 323-1 du Code pénal**. Ne jamais proposer ni utiliser de cible réelle.
