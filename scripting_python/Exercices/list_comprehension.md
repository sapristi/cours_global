# Introduction

Exercices qui permettent de s'exercer aux "list-comprehension". On utilisera les listes suivantes:


```python
fruits = ['mango', 'kiwi', 'strawberry', 'guava', 'pineapple', 'mandarin orange']

numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 17, 19, 23, 256, -8, -4, -2, 5, -9]
```

# Partie 1: list comprehension

## Exemple : ajouter 1 à chaque élément de la liste numbers - avec une boucle for


```python
# Example for loop solution to add 1 to each number in the list
numbers_plus_one = []
for number in numbers:
    numbers_plus_one.append(number + 1)
numbers_plus_one
```




    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 18, 20, 24, 257, -7, -3, -1, 6, -8]



et avec une list-comprehension 


```python
# Example of using a list comprehension to create a list of the numbers plus one.
numbers_plus_one = [
    number + 1 
    for number in numbers
]
numbers_plus_one
```




    [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 18, 20, 24, 257, -7, -3, -1, 6, -8]



# Exercices

## Exercice 1

Obtenr le même résultat avec une list-comprehension


```python
# Example code that creates a list of all of the list of strings in fruits and uppercases every string
output = []
for fruit in fruits:
    output.append(fruit.upper())
```

## Exercice 2

Écrire une expression "list comprehension" pour chacun des cas suivants:
- une liste qui contient chaque fruit qui s'écrit avec strictement plus de 4 caractères
- une liste qui contient chaque fruit qui s'écrit avec exactement 5 characters
- une liste qui contient le nombre de carcatères dans chaque fruit. Par exemple [5, 4, 10, etc... ]

## Exercice 3

Rappel: on filtre sur la liste `numbers` définie au début de l'exercice.

- Déclarer une nouvelle variable `even_numbers` qui contient les nombres pairs
- Déclarer une nouvelle variable `numbers_squared` qui contient chaque nombre au carré.
- Déclarer une nouvelle variable `odd_negative_numbers` qui contient les nombres qui sont à la fois impairs et négatifs.

# Partie 2: dict comprehension

Les dict-comprehension fonctionnent de manière similaire aux list-comprehension, sauf que:
- on utilise des accolades plutôt que des crochets
- on utilise `:` pour séparer les clés des valeurs


## Exemple

Dictionnaire qui à chaque nombre strictement positif, associe ce nombre + 2:
```
{
    x: x + 2 for x in numbers
    if x > 0
}
```

## Exercices


Créer les dictionnaires suivants (en spécifiant le type), à partir  des listes `fruits` et `numbers`:
- dictionnaire qui a chaque nombre associe le carré de ce nombre
- dictionnaire associant chaque fruit au nombre de lettres
- dictionnaire associant le nombre de lettres à chaque fruit, lorsque le nombre de lettres est pair
- dictionnaire qui associe l'indexe de chaque nombre à ce nombre ( on pourra utiliser la fonction python `enumerate`


```python

```
