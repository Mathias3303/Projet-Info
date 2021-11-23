from random import randint
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

## Variables globales
CODE_OBSTACLE = -1
CODE_PRATICABLE = 0
CODE_RAU = 3


INFLUENCE_DEPLACEMENT = 5
INFLUENCE_CASE = 1

## Environnement E, rectangle de maxX*maxY cases pratiquables
maxX = 10
maxY = 10
# taille E FIXEE

ENVIRONNEMENT = np.zeros((maxX+2,maxY+2))
ENVIRONNEMENT[:,0] = CODE_OBSTACLE
ENVIRONNEMENT[0,:] = CODE_OBSTACLE
ENVIRONNEMENT[maxX+1,:] = CODE_OBSTACLE
ENVIRONNEMENT[:,maxY+1] = CODE_OBSTACLE

LISTE_POSITION_RAU = [(5,5),(4,4)]

for coord in LISTE_POSITION_RAU :
    ENVIRONNEMENT[coord] = CODE_RAU


print(ENVIRONNEMENT)


## Position des fourmis, WARNING : ne pas les mettre sur les CODE_OBSTACLE
FOURMIS_SANS_RAU = [(4,6),(6,6)]
FOURMIS_AVEC_RAU = [(4,8),(2,8)]


## Liste des cases pratiquables parmi les 8 voisines de "case"
def liste_des_voisins_pratiquables(tableau,case):
    '''Renvoie liste des coordonnees des cases accessibles'''
    i = case[0]
    j = case[1]
    voisins_potentiels = [(i-1,j),(i+1,j),(i,j-1),(i,j+1),(i-1,j-1),(i+1,j+1),(i+1,j-1),(i-1,j+1)]
    indice_voisins_pratiquables = []
    for candidat in voisins_potentiels:
        if (0 <= candidat[0] < tableau.shape[0]) and (0 <= candidat[1] < tableau.shape[1]):
            indice_voisins_pratiquables.append(candidat)
    return indice_voisins_pratiquables


## Deplacement aléatoire, contraint par les obstacles, d'une fourmi de "caseAvant" à "caseAprès"

def deplacement_aleatoire() :
    for k in range(len(FOURMIS_AVEC_RAU)) :
        L = liste_des_voisins_pratiquables(ENVIRONNEMENT, FOURMIS_AVEC_RAU[k])
        nb_hasard = randint(0, len(L)-1)
        FOURMIS_AVEC_RAU[k] = L[nb_hasard]


    for k in range(len(FOURMIS_SANS_RAU)) :
        L = liste_des_voisins_pratiquables(ENVIRONNEMENT, FOURMIS_SANS_RAU[k])
        nb_hasard = randint(0, len(L)-1)
        FOURMIS_SANS_RAU[k] = L[nb_hasard]


## Attractivité de l'environnement pour la fourmi active

def attrac_deplacement() :

    for k in range(len(FOURMIS_AVEC_RAU)) :
        Lcoord = liste_des_voisins_pratiquables(ENVIRONNEMENT, FOURMIS_AVEC_RAU[k])
        Lattract = [INFLUENCE_CASE for x in Lcoord]

    print(Lattract)


## Mise en place choisie des RAU




## Mise en place aléatoire des RAU

#FB Je mets le code suivant dans une fonction pour que vous compreniez ce que je veux dire :


def remplit_RAU_au_hasard(nbUnites) :

    global NbRAU

    NbRAU = nbUnites

    #FB je remplace le input par un paramètre dans ma fonction

    positionsRAU = []

    if NbRAU <= maxX*maxY:
        for k in range(NbRAU):
            xRAU = randint(1,maxX)
            yRAU = randint(1,maxY)
            positionsRAU.append((xRAU,yRAU))
        for l in positionsRAU:
            if ENVIRONNEMENT[l] == CODE_PRATICABLE:
                ENVIRONNEMENT[l] = CODE_RAU
        #print(ENVIRONNEMENT) #FB Bien c'est très bien de faire un print()
        #FB On n'oublie pas de l'enlever (ou le commenter) quand on est sûr de son code
    else:
        print('Pas assez de place dans E pour autant de RAU')



## Affichage graphique
def affichage_graphique() :
    plt.imshow(ENVIRONNEMENT)  #FB on affiche le terrain

    #FB Puis on affiche les fourmis

    liste_x = [fourmi[1] for fourmi in FOURMIS_AVEC_RAU]
    liste_y = [fourmi[0] for fourmi in FOURMIS_AVEC_RAU]

    plt.scatter(liste_x , liste_y)

    liste_x = [fourmi[1] for fourmi in FOURMIS_SANS_RAU]
    liste_y = [fourmi[0] for fourmi in FOURMIS_SANS_RAU]

    plt.scatter(liste_x , liste_y)

    plt.axis('equal')
    plt.show()