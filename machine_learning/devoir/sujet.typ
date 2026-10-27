#import "../defs.typ": title, template, codly_args_example, warning-box, info-box
#import "@preview/showybox:2.0.4": showybox

#set text(lang: "fr", font: "New Computer Modern",)
#set page(paper: "a4", margin: (
  top: 2cm,
  bottom: 1cm,
  x: 1.5cm,
  y: 2cm,
))

#show: template.with(author: "Mathias Millet", suptitle: "Algo ESGI 3A",  title: "Contrôle continu - durée 1H")

#import "@preview/codly:1.3.0": *
#show: codly-init.with() 
#codly(
  display-icon: false,
  breakable: false, 
  stroke: 1pt + luma(240),
  languages: (
    python: (
      name: "Python",
      color: rgb("#47d147"),
    ),
    shell: (
      name: "Shell",
      color: luma(100)
    )
  ),
)



#showybox(
  [Nom, prénom:]
)

#showybox(
  frame: (
    title-color: blue.lighten(60%),
  ),
  title-style: (
    color: black,
    weight: "regular",
    align: center
  ),
  shadow: (
    offset: 3pt,
  ),
  title: [ *Consignes* ],
  [
    - *Documents et ordinateur non autorisés.*
  ]
)




= Exercice 1 - Nom de domaine

Quel rôle joue le nom de domaine dans une URL ?

\ 
\
\
\

= Exercice 2 - Requête web

Décrire les différents éléments d'une requête web HTTP (nom, exemple, utilité, ...)
#v(0.7cm)
#line(length: 100%)#v(0.7cm)
#line(length: 100%)#v(0.7cm)
#line(length: 100%)#v(0.7cm)
#line(length: 100%)#v(0.7cm)
#line(length: 100%)#v(0.7cm)
#line(length: 100%)#v(0.7cm)
#line(length: 100%)#v(0.7cm)

Le(s)quel(s) de ces éléments n'apparaissent pas dans la réponse ?
#v(0.7cm)
#line(length: 100%)
#v(0.7cm)
#line(length: 100%)
#v(0.7cm)
#line(length: 100%)
#pagebreak()



= Exercice 3 - Argparse

Voici le contenu du fichier `affiche_forme.py`:
```python


import argparse


parser = argparse.ArgumentParser(description="Affiche une forme")


parser.add_argument("--forme", choices=["triangle", "carré"], required=True)


parser.add_argument("--taille", type=int, required=True)


args = parser.parse_args()
```

1. Expliquer le rôle de chacune des lignes du code suivant
2. Donner un exemple d'appel du programme ci-dessus dans un terminal

\ 
#line(length: 100%)
3. Compléter le programme, afin qu'il ait le comportement décrit.

```python
import argparse

parser = argparse.ArgumentParser(description="Affiche une forme")
parser.add_argument("--forme", choices=["triangle", "carré"])
parser.add_argument("--taille", type=int)

args = parser.parse_args()

    |   |   |   | 
    |   |   |   | 
    |   |   |   |  
    |   |   |   | 
    |   |   |   | 
    |   |   |   | 
    |   |   |   | 
    |   |   |   |  
    |   |   |   |
    |   |   |   |  
    |   |   |   |
    |   |   |   |  
    |   |   |   |
    |   |   |   |  
    |   |   |   |  
```
