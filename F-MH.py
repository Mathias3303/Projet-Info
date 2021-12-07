from random import * #FB je déconseille ça
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

## Variables globales
CODE_OBSTACLE = -1
CODE_PRATICABLE = 0
CODE_RAU = 3
CODE_FOURMILIERE = 8


NB_RAU_COLLECTEES = 0 #idee booleen compteur de RAU rentrées à la maison qui acheve le programme (while)


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

ENVIRONNEMENT[(6,6)] = CODE_FOURMILIERE


print(ENVIRONNEMENT)


## Position des fourmis
FOURMIS_SANS_RAU = []
FOURMIS_AVEC_RAU = [(5,5),(7,4)]

VECTEUR_VITESSE_FOURMIS_AVEC_RAU = []
VECTEUR_VITESSE_FOURMIS_AVEC_RAU = []


## Liste des cases pratiquables parmi les 8 voisines de "case"
def liste_des_voisins_praticables(tableau,case):
    '''Renvoie liste des coordonnees des cases accessibles'''
    i = case[0]
    j = case[1]
    voisins_potentiels = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1)]
    indice_voisins_praticables = []
    for candidat in voisins_potentiels:
        if (0 <= candidat[0] < tableau.shape[0]) and (0 <= candidat[1] < tableau.shape[1]):
            indice_voisins_praticables.append(candidat)
    return indice_voisins_praticables


## Deplacement aléatoire, contraint par les obstacles, d'une fourmi de "caseAvant" à "caseAprès"

def deplacement_aleatoire() :
    for k in range(len(FOURMIS_AVEC_RAU)) :
        L = liste_des_voisins_praticables(ENVIRONNEMENT, FOURMIS_AVEC_RAU[k])
        nb_hasard = randint(0, len(L)-1)
        FOURMIS_AVEC_RAU[k] = L[nb_hasard]


    for k in range(len(FOURMIS_SANS_RAU)) :
        L = liste_des_voisins_praticables(ENVIRONNEMENT, FOURMIS_SANS_RAU[k])
        nb_hasard = randint(0, len(L)-1)
        FOURMIS_SANS_RAU[k] = L[nb_hasard]


## Attractivité de l'environnement pour la fourmi active

def delta(case_suivante , case_actuelle):
    di = case_suivante[0] - case_actuelle[0]
    dj = case_suivante[1] - case_actuelle[1]
    liste_delta = [ di , dj ]
    return liste_delta




def poids_deplacement():
    for k in range(len(FOURMIS_AVEC_RAU)):
        case_actuelle = FOURMIS_AVEC_RAU[k]
        delta_actuel = VECTEUR_VITESSE_FOURMIS_AVEC_RAU[k]
        voisins_praticables = liste_des_voisins_praticables(ENVIRONNEMENT , caseactuelle)
        L_delta_possible = []
        for case_possible in voisins_praticables :
            L_delta_possible.append( delta(case_possible , caseactuelle) )






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
    '''fonction qui affiche l'ENVIRONNEMENT'''
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