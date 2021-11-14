from random import *
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

## Variables majeures
CODE_FOURMI_SANS_RAU = 1
CODE_FOURMI_AVEC_RAU = 2
CODE_OBSTACLE = -1
CODE_PRATICABLE = 0
CODE_RAU = 3


## Environnement E, rectangle de maxX*maxY cases praticables
maxX = int(input('nombres de lignes de E = '))
maxY = int(input('nombre de colonnes de E = '))
E = np.zeros((maxX+2,maxY+2))
E[:,0] = CODE_OBSTACLE
E[0,:] = CODE_OBSTACLE
E[maxX+1,:] = CODE_OBSTACLE
E[:,maxY+1] = CODE_OBSTACLE
print(E)


## Position des fourmis sans RAU
E[(6,6)] = CODE_FOURMI_SANS_RAU
print(E)

## Position des fourmis avec RAU



## Liste des cases praticables parmi les 8 voisines de "case"
def liste_des_voisins_praticables(tableau,case):
    i = case[0]
    j = case[1]
    voisins_potentiels = [(i-1,j),(i+1,j),(i,j-1),(i,j+1),(i-1,j-1),(i+1,j+1),(i+1,j-1),(i-1,j+1)]
    indice_voisins_praticables = []
    for candidat in voisins_potentiels:
        if (0 <= candidat[0] < tableau.shape[0]) and (0 <= candidat[1] < tableau.shape[1]):
            indice_voisins_praticables.append(candidat)
    return indice_voisins_praticables



## Deplacement aléatoire, contraint par les obstacles, d'une fourmi de "caseAvant" à "caseAprès"
def deplacement_aleatoire(tableau, caseAvant):
    natureFourmi = tableau[caseAvant]
    indice_voisins = liste_des_voisins_praticables(tableau, caseAvant)
    case_au_hasard = randint(0,len(indice_voisins))
    caseApres = indice_voisins[case_au_hasard]
    tableau[caseAvant] = 0
    tableau[caseApres] = natureFourmi
    return E




## Attractivité de l'environnement pour la fourmi active






## Mise en place choisie des RAU
NbRAU = int(input('Nombre de RAU à t=0 : '))
positionsRAU = []
if NbRAU <= maxX*maxY:
    for k in range(NbRAU):
        xRAU = int(input('x de RAU : '))
        yRAU = int(input('y de RAU : '))
        xyRAU = (xRAU,yRAU)
        if E[xyRAU] == CODE_PRATICABLE:
            positionsRAU.append((xRAU,yRAU))
    for l in positionsRAU:
        E[l] = CODE_RAU
    print(E)
else:
    print('Pas assez de place dans E pour autant de RAU')


## Mise en place aléatoire des RAU
NbRAU = int(input('Nombre de RAU à t=0 : '))
positionsRAU = []
if NbRAU <= maxX*maxY:
    for k in range(NbRAU):
        xRAU = randint(1,maxX)
        yRAU = randint(1,maxY)
        positionsRAU.append((xRAU,yRAU))
    for l in positionsRAU:
        if E[l] == CODE_PRATICABLE:
            E[l] = CODE_RAU
    print(E)
else:
    print('Pas assez de place dans E pour autant de RAU')




