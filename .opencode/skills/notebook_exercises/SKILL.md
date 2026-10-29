---
name: notebook_exercises
description: Use when creating or editing a Jupyter notebook containing exercices (typically a TD "Travaux dirigés" notebook), or preparing notebooks for distribution with scripts/collect_lite_content.py.
---

# TD Jupyter

## Vue d'ensemble

Un TD est un notebook Jupyter, source unique : le **corrigé** (solutions incluses), versionné dans le repo (dans le dossier du cours, ex. `machine_learning/td/NN_<theme>.ipynb`). Au build jupyterlite, `scripts/collect_lite_content.py` copie les corrigés dans `content/` et produit la version **diffusée** (sans solutions) : elle n'a pas vocation à être versionnée ailleurs.

## Structure du notebook

Le notebook se découpe en **sections** de niveau `##`, une par **cas d'étude** (ex. « 1. Étude en 2D », « 2. Étude en 25D »), chacune subdivisée en **sous-sections numérotées** de niveau `###` (`1.1`, `1.2`, …).

- **Intro / préambule** : sections `##` dédiées, non numérotées (ex. `## Objectif`, `## Préambule`).
- **Conclusion** : section `##` dédiée, non numérotée, en fin de notebook (si pertinent).
- Les blocs d'aide (vérification `#### Vérification de …`, figures) sont des sous-niveaux `####` rattachés à leur sous-section `###`.

## Interfacer avec `collect_lite_content.py`

Le script remplace chaque bloc `# BEGIN` … `# END` (ou `#BEGIN` … `#END`) par `# TODO` + `pass`, vide les outputs et remet `execution_count` à `None`. Les commentaires écrits juste après `# BEGIN` deviennent le corps du TODO (voir « Corps du TODO »).

### Aperçu local (fichier → fichier)

```bash
uv run python scripts/prepare_notebooks.py <corrige>.ipynb <apercu>.ipynb
```

Sert à prévisualiser ce que verra l'étudiant. Écrire l'aperçu hors du repo (ex. `/tmp/`) : ne jamais écraser le corrigé, ne pas versionner l'aperçu.

## Écrire un exercice

Chaque exercice est énoncé dans une **cellule markdown**, encadré par un `fieldset` dont la `legend` porte le numéro :

```markdown
<fieldset style="border: 3px solid #1976d2; border-radius: 8px; padding: 0 14px; margin: 12px 0">
<legend style="color: #1976d2; font-weight: bold; font-size: 1.5em; padding: 0 6px">✏️ Exercice 7</legend>

Complétez `forward` (renvoie X, Z1, Y1, Z2, Y2).

</fieldset>
```

- Recopier les deux balises ouvrantes **telles quelles** (styles identiques sur tout le notebook) ; seul le titre de la `legend` change.
- **Lignes vides obligatoires** après `</legend>` et avant `</fieldset>` : sans elles, JupyterLab n'interprète pas le markdown de l'énoncé (backticks, gras, listes, `$…$`).
- Le corps est du markdown normal (paragraphes, listes numérotées), **sans** préfixe `>`.
- Styles inline uniquement : JupyterLab supprime les balises `<style>` et refuse `var(--jp-…)` dans les styles inline (d'où la couleur codée en dur).
- Le texte d'introduction ou de contexte reste **hors** du `fieldset`, avant lui.
- Numérotation **séquentielle** sur tout le notebook (Exercice 1, 2, 3…), lettres pour les sous-étapes (`Exercice 7a`, `7b`, …).
- L'énoncé nomme précisément ce qu'il faut compléter (fonction/méthode), puis la tâche.
- Les **questions de lecture** (interpréter une courbe, un résultat — réponse rédigée, sans code) sont aussi des exercices : même encadré, même numérotation séquentielle, titre « Exercice N ». Pas de libellé « Question » ni de numérotation séparée.

## En cas d'édition, ne pas référencer un état antérieur

L'énoncé est écrit **à partir de zéro**, pour un étudiant qui n'a aucun souvenir
d'un état antérieur du notebook. Il ne référence jamais un état que seul l'auteur
connaît — une version précédente du code, un objet qu'on aurait « remplacé », une
étape intermédiaire jamais montrée :

- ❌ « *plutôt qu'un* objet `groupby` opaque » — l'étudiant n'a jamais vu cet objet ;
- ❌ « le groupby *devient* un DataFrame » — il n'a pas assisté à la transformation ;
- ❌ « *comme précédemment* / *comme avant* » — il ne connaît pas cet « avant ».

Décrire directement l'action et son résultat, au présent :

```markdown
<!-- ❌ -->
1. Matérialiser le groupby : plutôt qu'un objet `groupby` opaque, on fabrique
   un DataFrame inspectable.

<!-- ✅ -->
1. Regrouper en listes : fabriquer un DataFrame où chaque ligne est un couple
   (src_ip, domain) et où l'on range ses instants dans une liste triée.
```

## Typage des fonctions à compléter

Les fonctions et méthodes à compléter (celles dont le corps contient un bloc `# BEGIN`/`# END`) doivent être typées (annotation de type sur les paramètres et sur la valeur de retour).

```python
# ❌
def output(self, x1, x2):

# ✅
def output(self, x1: float, x2: float) -> int:
```
## Typage des tableaux numpy

Les tableaux numpy sont typés précisément : forme (nombre de dimensions) et dtype, via des alias définis en tête de notebook:

```python
import numpy as np

# Alias de types pour les tableaux numpy
Vec = np.ndarray[tuple[int], np.dtype[np.float64]]        # vecteur 1D de flottants
Mat = np.ndarray[tuple[int, int], np.dtype[np.float64]]   # matrice 2D de flottants
VecInt = np.ndarray[tuple[int], np.dtype[np.int64]]       # vecteur 1D d'entiers
```

- Déclare les alias **dont le notebook a besoin** (inutile d'en déclarer un jamais utilisé).
- La forme garde un commentaire quand elle porte un sens métier : `W: Mat  # (K, d)`.
- Pour une fonction **élément par élément** (activation `sigmoid_prime`, `tanh_prime`…), l'entrée et la sortie ont la même forme : type-la selon son usage (`Mat` si appliquée aux pré-activations d'un batch).

## Docstrings

Dans les docstrings, citer le code (noms, expressions) entre backticks **simples**, comme en markdown, jamais doubles (style reST) :

```python
# ❌
"""Probabilités supérieures ou égales à ``threshold``."""
# ✅
"""Probabilités supérieures ou égales à `threshold`."""
```

## Cellule « à exécuter » (affichage / résultat)

Quand une cellule ne demande **pas** d'écrire de code — elle affiche une figure, un résultat déjà calculé, illustre une notion — ne la formule pas comme un exercice :

- **Pas de verbe à l'impératif** (« Affichez », « Exécutez », « Calculez »…) : cela laisse croire qu'il y a du code à écrire, alors qu'il suffit d'exécuter la cellule.
- **Pas d'encadré** `<fieldset>` « ✏️ Exercice N ».
- Préférer une tournure descriptive : « On affiche ici … », « La cellule suivante affiche … », « Vérifiez vos réponses. »

```markdown
<!-- ❌ -->
Affichez les 5 perceptrons de l'exercice 1 et vérifiez vos réponses.

<!-- ✅ -->
On affiche ici les 5 perceptrons de l'exercice 1 ; vérifiez vos réponses.
```

Réserver l'impératif et la numérotation `Exercice` aux cellules où l'étudiant **écrit** quelque chose : du code, ou une réponse rédigée (question de lecture).

## Cellule de vérification

**Chaque exercice doit être suivi d'une cellule de code qui teste que le code est correct.** Elle vérifie par `assert` et imprime un message `… OK` en cas de succès.

```python
def check_forward(model, X, tol=1e-9):
    ...
    assert np.allclose(Z1, Z1r, atol=tol), "Z1 incorrect"
    print("forward check — OK")

m = PerceptronCache(2, 3, 1, seed=1)
X = np.random.default_rng(0).normal(size=(4, 2))
check_forward(m, X)
```

- La cellule de vérification **ne doit pas** être dans un bloc `# BEGIN`/`# END` : elle reste visible dans la version diffusée pour l'auto-évaluation.
- Elle suit **immédiatement** la cellule de l'exercice. La cellule de l'exercice s'arrête au `# END` (seule la mise en place nécessaire, ex. constantes ou dictionnaire à remplir, peut précéder le `# BEGIN`) : tout ce qui exploite le résultat (figures, tableaux, `print`, fonctions utilitaires d'affichage) va dans une **cellule séparée, placée après la vérification**. Ordre : énoncé → exercice → vérification → affichage. L'étudiant valide ainsi son code avant de lire les résultats, et une erreur d'affichage ne masque pas celle de son code.

```python
# ❌ une seule cellule : solution puis affichage, vérification en dessous
hists = {"μ=0": hist_plain}
# BEGIN
...
# END
fig, axes = plt.subplots(1, 2)
plot_curves(hists, ...)

# ✅ cellule 1 : l'exercice seul
hists = {"μ=0": hist_plain}
# BEGIN
...
# END

# ✅ cellule 2 : la vérification
check_hists()

# ✅ cellule 3 : l'affichage
fig, axes = plt.subplots(1, 2)
plot_curves(hists, ...)
```

Dans l'énoncé, annoncer l'affichage en conséquence (« Après la vérification, la cellule suivante affiche … »), pas « la cellule affiche ensuite ».
- Elle teste ce que l'étudiant vient de coder : comparaison à une implémentation naïve, gradient numérique, `assert` sur une valeur attendue, etc.

### Tester une fonction d'apprentissage (`fit`/`learn`)

Pour une fonction qui **apprend** (`fit_batch`, `fit_online`, `learn`, `train`, …), ne teste **pas** par heuristique (« la perte diminue », « l'accuracy > 0.9 »). Utilise des **données statiques** (poids et entrées fixés à la main, pas de hasard) et **simule le réseau à la main** pour obtenir la valeur attendue, puis `assert` en **égalité exacte** `==` — pas de `np.allclose`, pas de `abs(x - c) < tol` :

```python
def check_learn():
    p = Perceptron(0, 0, 0)
    p.learn(1, 1, 0, 0.1)   # y=1 != t=0 -> mise à jour
    assert p.w0 == 0.1
    assert p.w1 == -0.1
    assert p.w2 == -0.1
    print("learn check — OK")

check_learn()
```

L'égalité exacte n'est possible que si les valeurs sont choisies pour **tomber juste** (poids nuls, entrées `±1`, `r` simple) : le calcul à la main donne alors des littéraux exacts. Si le calcul fait apparaître des valeurs non représentables (`1/3`, sigmoid…), choisis d'autres données au lieu d'introduire une tolérance.

```python
def check_fit_batch():
    model = MLP([2, 1], output_activation="linear", seed=0)
    model.Ws = [np.array([[1.0, -2.0]])]
    model.bs = [np.array([0.0])]
    X = np.array([[1.0, 0.0], [0.0, 1.0]])
    t = np.array([[0.0], [0.0]])
    model.fit_batch(X, t, lr=0.5, epochs=1)

    # simulation à la main (sortie linéaire) :
    #   z = X @ W.T + b = [[1], [-2]]  ;  delta = z - t = [[1], [-2]]
    #   dW = delta.T @ X / 2 = [[0.5, -1]]  ;  db = delta.sum(0) / 2 = -0.5
    #   W -= lr*dW -> [[0.75, -1.5]]  ;  b -= lr*db -> 0.25
    assert np.array_equal(model.Ws[0], np.array([[0.75, -1.5]]))
    assert np.array_equal(model.bs[0], np.array([0.25]))
    print("fit_batch check — OK")

check_fit_batch()
```

- Une **époque** suffit : on vérifie la mécanique d'une mise à jour exacte, pas la convergence.
- Pour une variante **stochastique** (`fit_online`), fige l'ordre (`seed`) ou teste plutôt l'étape déterministe (`_step`/`fit_batch`).
- Pour un réseau à activation **non linéaire** (sigmoid/tanh), le résultat n'est pas un littéral exact : on ne peut pas écrire `==` une constante. On teste alors `forward`/`backward` sur des valeurs de référence pré-calculées (comparaison par `np.allclose`).

## Cellule de réponse `# TOCLEAR`

Pour fournir la réponse du corrigé à une question de lecture (énoncée comme un
exercice, voir « Écrire un exercice »), placer juste après l'énoncé une cellule **markdown** dont la première ligne non vide est
exactement `# TOCLEAR`, suivie du texte de la réponse. À la préparation
(`strip_solutions`, donc `prepare_notebooks.py` et `collect_lite_content.py`),
ces cellules sont supprimées. Les cellules code ne sont pas concernées, et un
`# TOCLEAR` qui n'est pas en première ligne non vide ne déclenche rien. Si
l'étudiant doit écrire sa réponse, laisser avant la cellule `# TOCLEAR` une
cellule markdown « *Votre réponse :* » (visible des deux côtés).

## Règles BEGIN/END

- `# BEGIN` et `# END` sur leur **propre ligne**, dans des cellules de code uniquement.
- Tout le code solution est entre les deux ; la ligne `# BEGIN` devient `# TODO` + `pass` à la préparation.
- Le code « pédagogique » non solution (imports, fonctions de visualisation, fonctions de test) reste **hors** des blocs.

### Corps du TODO

Les commentaires écrits **immédiatement après** `# BEGIN` (avant la première ligne de code solution) deviennent le corps du `# TODO` dans la version diffusée :

- `# <code>` → dé-commenté, devient du **code** (ex. `# raise NotImplementedError` → `raise NotImplementedError`).
- `## <texte>` → garde un seul `#`, reste un **indice** (commentaire).

```python
def forward(self, X):
    # BEGIN
    # raise NotImplementedError
    ## Indice : Z1 = Y0 @ W1.T + b1
    Y0 = X
    ...
    # END
```

donne, une fois préparé :

```python
def forward(self, X):
    # TODO
    raise NotImplementedError
    # Indice : Z1 = Y0 @ W1.T + b1
```

- Sans commentaire après `# BEGIN`, le script émet `# TODO` + `pass` comme avant.
- Si seul des indices (`##`) sont présents, un `pass` est ajouté pour éviter un corps vide.
- ⚠️ Tout commentaire en **première ligne** d'une solution sera dé-commenté : pour un commentaire ordinaire, écris-le avant `# BEGIN` ou utilise `##`.

### Variables attendues dans une cellule (hors fonction)

Quand le TODO doit définir des variables utilisées ensuite (affichage, vérification, exercices suivants), le corps du TODO les **nomme explicitement** sous forme de squelette `# var = ...`, précédé d'un rappel (`##`) des variables disponibles. Pas de `# raise NotImplementedError` : le squelette en tient lieu.

```python
# BEGIN
## Rappel : Xb_tr, tb_tr : données et cibles d'entraînement
# y_zero = ...
# model = ...
# ...
# y_mlp = ...
y_zero = np.zeros(len(tb_te))
...
# END
```

Pour une boucle qui remplit un dictionnaire, le squelette donne la boucle et la clé : `# for name, mu in MUS.items():` puis `#     hists[name] = ...`. Ne pas déclarer les placeholders `var = ...` hors du bloc (ils resteraient dans le corrigé).

## Erreurs courantes

- Marqueur `# BEGIN`/`# END` dans une cellule markdown → ignoré (le filtre ne traite que le code).
- Versionner un aperçu / une version diffusée dans le repo → seul le corrigé est versionné.
- Modifier le corrigé après la préparation → relancer le script.
- Cellule de vérification enfermée dans `# BEGIN`/`# END` → masquée à l'étudiant, il ne peut plus s'auto-tester.
