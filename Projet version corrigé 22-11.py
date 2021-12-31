from random import * #FB je déconseille ça
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

#FB ATTENTION, comme je vous l'ai dit, je déconseille formellement de mettre dans un même tableau l'environnement et les fourmis.

#FB Ayez plutôt une liste des fourmis avec RAU et une liste des fourmis sans RAU

#FB Voir fichier exemple_de_ce_que_je_dis.py donné le drive

## Variables globales
CODE_OBSTACLE = -1
CODE_PRATICABLE = 0
CODE_RAU = 3



## Environnement E, rectangle de maxX*maxY cases praticables
maxX = int(input('nombres de lignes de E = '))
maxY = int(input('nombre de colonnes de E = '))

#FB Attention : les jurys ne veulent pas d'input (sauf nécessité du genre interface texte pour un jeu)

#FB Mettez des valeurs choisies (voir le fichier exemple_de_ce_que_je_dis.py)

E = np.zeros((maxX+2,maxY+2))  #FB "E est le tableau qui code l'environnement"
#FB Pourquoi ces "+ 2" ?

#FB personnellement je n'utiliserais pas "E" mais "ENVIRONNEMENT" (ou un autre mot, mais quelque chose d'explicite)

E[:,0] = CODE_OBSTACLE
E[0,:] = CODE_OBSTACLE
E[maxX+1,:] = CODE_OBSTACLE
E[:,maxY+1] = CODE_OBSTACLE
print(E)


## Position des fourmis sans RAU
E[(6,6)] = CODE_FOURMI_SANS_RAU #FB Même remarque...
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

#FB Je supprime (en la commentant) toute la partie d'input suivante. C'est impossible de tester votre programme si on doit  remplir un formulaire à chaque fois ! =D

#FB Et les jurys demandent explicitement de ne pas le faire

'''
NbRAU = int(input('Nombre de RAU à t=0 : ')) #FB pas d'input pour ça
positionsRAU = []
if NbRAU <= maxX*maxY:
    for k in range(NbRAU):
        xRAU = int(input('x de RAU : '))  #FB C'est beaucoup trop pénible pour tester votre code. Faites un tableau tout prêt
        yRAU = int(input('y de RAU : '))
        xyRAU = (xRAU,yRAU)
        if E[xyRAU] == CODE_PRATICABLE:
            positionsRAU.append((xRAU,yRAU))
    for l in positionsRAU:
        E[l] = CODE_RAU
    print(E)
else:
    print('Pas assez de place dans E pour autant de RAU') #FB en plus ça évite ce genre de cas pénibles
'''

#FB Faites quelque chose comme ça :

NbRAU = 5
E[1,2] = E[4,4] =E[7,2] = E[8,10] = E[8,2] = CODE_RAU

#FB Si vous tenez absolument aux input(), mettez ça dans une fonction, pour qu'on ait le CHOIX

#FB Sinon, utilisez les exemples 4.1 ou 4.2 du TP4 ! =)

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
            if E[l] == CODE_PRATICABLE:
                E[l] = CODE_RAU
        #print(E) #FB Bien c'est très bien de faire un print()
        #FB On n'oublie pas de l'enlever (ou le commenter) quand on est sûr de son code
    else:
        print('Pas assez de place dans E pour autant de RAU')




## Affichage graphique
def affichage_graphique() :
    plt.imshow(E)  #FB on affiche le terrain

    #FB Puis on affiche les fourmis

    liste_x = [fourmi[1] for fourmi in FOURMIS_AVEC_RAU]
    liste_y = [fourmi[0] for fourmi in FOURMIS_AVEC_RAU]

    plt.scatter(liste_x , liste_y)

    liste_x = [fourmi[1] for fourmi in FOURMIS_SANS_RAU]
    liste_y = [fourmi[0] for fourmi in FOURMIS_SANS_RAU]

    plt.scatter(liste_x , liste_y)

    plt.axis('equal')
    plt.show()

