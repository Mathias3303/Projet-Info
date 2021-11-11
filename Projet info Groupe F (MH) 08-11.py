from random import *
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

## Variables majeures
CODE_FOURMI = 1
CODE_OBSTACLE = -1
CODE_PRATICABLE = 0


## Environnement E, carré de 10*10 cases praticables
E = np.zeros((11,11))
E[:,0] = CODE_OBSTACLE
E[0,:] = CODE_OBSTACLE
E[10,:] = CODE_OBSTACLE
E[:,10] = CODE_OBSTACLE
print(E)


## Placement des fourmis
E[5,5] = CODE_FOURMI
print(E)


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


print ('Fini')


