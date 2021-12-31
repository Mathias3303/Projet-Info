import random
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import matplotlib.colors as couleurs


#FB Il y a parfois une petite erreur très subtile dans le mouvement des fourmis (rarement !). La verrez-vous ? =D

#FB Pour le moment, ça fait des fourmis qui sortent de la fourmilière et qui se promènenent au hasard et qui récupèrent parfois de la nourriture au hasard... De plus tout ça se fait sur un exemple pour le moment, à généraliser

## Variables globales techniques

#FB Je vais modifier les codes ci-dessous pour vous permettre d'avoir un code couleur précis, JE VOUS EXPLIQUERAI COMMENT CA MARCHE.

#FB Les deux variables suivantes vont permettre de dessiner le monde avec des couleurs définies :

# blanc pour les cases vides
# gris pour les obstacles
# vert pour la / les fourmilières
# rouge pour les stocks de nourriture

COULEURS = ["white","grey", "green", "red"]
CMAPU = couleurs.ListedColormap(COULEURS)

# Les fourmis auront aussi leurs couleurs suivant qu'elles sont "à vide" ou "portent un RAU"

COULEUR_FOURMI_SANS_RAU = "black"
COULEUR_FOURMI_AVEC_RAU = "orange"

# Maintenant les codes pour le tableau d'environnement

CODE_OBSTACLE = 1
CODE_PRATICABLE = 0
CODE_RAU = 2
CODE_FOURMILIERE = 3


NB_RAU_INITIAL = 3 #ici, test manuel ; à implémenter dans remplit_RAU_au_hasard
NB_RAU_COLLECTEES = 0 #idee booleen compteur de RAU rentrées à la maison qui acheve le programme (while), cf. dernière fonction


INFLUENCE_COS_0 = 5
INFLUENCE_COS_PId4 = 3
INFLUENCE_COS_PId2 = 2
INFLUENCE_COS_3PId4 = 1
INFLUENCE_COS_PI = 0

INFLUENCE_CASE = 1 #à supprimer ? ancien chemin pour le déplacement choisi


SIMULATION_EN_COURS = True # cette variable indique que la simulation est en cours (tant qu'elle vaut True, la boucle principale continue - elle devient False par exemple si on ferme la fenêtre grâce à un bout de code que je vous ai mis en cadeau bonus !)

## UN EXEMPLE à généraliser

# ENVIRONNEMENT : rectangle de maxX*maxY cases pratiquables

maxX = 10
maxY = 10
# taille FIXEE dans cet exemple

ENVIRONNEMENT = np.zeros((maxX+2,maxY+2))

ENVIRONNEMENT[:,0] = CODE_OBSTACLE
ENVIRONNEMENT[0,:] = CODE_OBSTACLE
ENVIRONNEMENT[maxX+1,:] = CODE_OBSTACLE
ENVIRONNEMENT[:,maxY+1] = CODE_OBSTACLE

LISTE_POSITION_RAU = [(2,2),(9,6), (5,9)]

for coord in LISTE_POSITION_RAU :
    ENVIRONNEMENT[coord] = CODE_RAU

ENVIRONNEMENT[(5,5)] = CODE_FOURMILIERE

print(ENVIRONNEMENT)



FOURMIS_SANS_RAU = [(5,5),(5,5),(5,5),(5,5),(5,5),(5,5),(5,5)]
FOURMIS_AVEC_RAU = []



VECTEUR_VITESSE_FOURMIS_AVEC_RAU = [] #à supprimer ? ancien chemin pour le déplacement choisi


TEMPS_PAUSE = 1 #nani ?




## Mise en place aléatoire de l'environnement

#FB Je mets le code suivant dans une fonction pour que vous compreniez ce que je veux dire :


def remplit_RAU_au_hasard(nbUnites) :
    '''
    met nbUnites au hasard dans la variable globale ENVIRONNEMENT


    '''

    global NB_RAU_INITIAL

    NB_RAU_INITIAL = nbUnites

    #FB je remplace le input par un paramètre dans ma fonction

    #FB l'algo que vous utilisez ci-dessous ne fait pas ce que vous voulez de manière sure : si par hasard il tombe deux fois sur la même case, ou à un moment sur une case obstacle, à la fin vous aurez moins de cases RAU que vous le vouliez... à améliorer...

    Nb_RAU_placees = 0

    if NB_RAU_INITIAL <= maxX*maxY:
        while Nb_RAU_placees < NB_RAU_INITIAL:
            xRAU = random.randint(1,maxX)
            yRAU = random.randint(1,maxY)
            positionRAU = (xRAU,yRAU)
            if ENVIRONNEMENT[positionRAU] == CODE_PRATICABLE:
                ENVIRONNEMENT[positionRAU] = CODE_RAU
                Nb_RAU_placees += 1

    else:
        print('Pas assez de place dans E pour autant de RAU')

#FB Faire de même la fonction suivante :

def remplit_obstacles_au_hasard(nbObstacles) :
    '''
    met nbObstacles obstacles dans la variable ENVIRONNEMENT
    '''

    #FB A faire





## fonctions utilitaires

#FB le but de la fonction suivante est peu clair : vu son usage plus loin, il me semble qu'il s'agit de donner les cases voisines SANS OBSTACLES. Mais vous n'enlevez pas les obstacles... dans ce cas il faut la modifier (je le fais)

def liste_des_voisins_praticables(tableau,case):
    '''Renvoie liste des coordonnees des cases accessibles, c'est ) dire sur le tableau et sans obstacle'''
    i = case[0]
    j = case[1]
    voisins_potentiels = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1)]
    indice_voisins_praticables = []
    for candidat in voisins_potentiels:
        if (0 <= candidat[0] < tableau.shape[0]) and (0 <= candidat[1] < tableau.shape[1]) and (tableau[candidat] != CODE_OBSTACLE ):
            indice_voisins_praticables.append(candidat)
    return indice_voisins_praticables


## Deplacement aléatoire, contraint par les obstacles, d'une fourmi de "caseAvant" à "caseAprès"

#FB Je reformate ça plus bas dans la partie ## Deplacement des fourmis : une fonction générique qui fait une boucle sur les fourmis et qui gère notamment la transformation des fourmis sans RAU en fourmis avec RAU, et une fonction qui fait le déplacement d'une fourmi à la fois.

#FB Je laisse votre code en commentaire ci-dessous, comparez avec ce que j'ai fait :

'''

def deplacement_aleatoire() :
    for k in range(len(FOURMIS_AVEC_RAU)) :
        L = liste_des_voisins_praticables(ENVIRONNEMENT, FOURMIS_AVEC_RAU[k])
        nb_hasard = randint(0, len(L)-1)
        FOURMIS_AVEC_RAU[k] = L[nb_hasard]


    for k in range(len(FOURMIS_SANS_RAU)) :
        L = liste_des_voisins_praticables(ENVIRONNEMENT, FOURMIS_SANS_RAU[k])
        nb_hasard = randint(0, len(L)-1)
        FOURMIS_SANS_RAU[k] = L[nb_hasard]

'''

## Attractivité de l'environnement pour la fourmi active


#FB je ne regarde pas les deux fonctions suivantes, car je ne sais pas exactement ce que vous voulez faire (pas de docstring...)

#FB Avec le setting graphique que je vous ai mis, vous allez pouvoir les tester vous-même et voir si ça fait ce que vous voulez.

def couple_delta(case_suivante , case_actuelle):
    di = case_suivante[0] - case_actuelle[0]
    dj = case_suivante[1] - case_actuelle[1]
    couple_delta = ( di , dj )
    return couple_delta




def poids_deplacement():
    for k in range(len(FOURMIS_AVEC_RAU)):
        case_actuelle = FOURMIS_AVEC_RAU[k]
        delta_actuel = VECTEUR_VITESSE_FOURMIS_AVEC_RAU[k] #couple_delta de l'actuel
        voisins_praticables = liste_des_voisins_praticables(ENVIRONNEMENT , case_actuelle)
        L_cos_voisins_praticables = []
        L_attractivite_des_voisins_praticables = []
        norme_vecteur_actuel = ( (delta_actuel[0])**2 + (delta_actuel[1])**2 )**(1/2)

        for case_possible in voisins_praticables :
            delta_possible = couple_delta(case_possible, case_actuelle)
            produit_scalaire = np.dot(delta_actuel, delta_case_possible)
            norme_vecteur_possible =( (delta_possible[0])**2 + (delta_possible[1])**2 )**(1/2)
            cos_case_possible = produit_scalaire / norme_vecteur_possible
            L_cos_voisins_praticables.append(cos_case_possible)

        for element in L_cos_voisins_praticables :
            if element == 0 :
                L_attractivite_des_voisins_praticables.append(INFLUENCE_COS_0)
            if element == pi/4 or element == -pi/4 :
                L_attractivite_des_voisins_praticables.append(INFLUENCE_COS_PId4)
            if element == pi/2 or element == -pi/2 :
                L_attractivite_des_voisins_praticables.append(INFLUENCE_COS_PId2)
            if element == 3*pi/4 or element == -3*pi/4 :
                L_attractivite_des_voisins_praticables.append(INFLUENCE_COS_3PId4)
            if element == pi or element == -pi :
                L_attractivite_des_voisins_praticables.append(INFLUENCE_COS_PI)


## Deplacement des fourmis

def deplacement_une_fourmi(fourmi) :
    '''
    pour le moment, chaque fourmi se promène aléatoirement
    '''
    nouvelle_pos = random.choice(liste_des_voisins_praticables(ENVIRONNEMENT,fourmi))
    print("la fourmi", fourmi,"va en ", nouvelle_pos)
    return nouvelle_pos




def deplacement_des_fourmis() :

    '''
    gère le déplacement de toutes les fourmis, et le changemetn d'état entre "sans RAU" et "avec RAU"
    '''

    global NB_RAU_COLLECTEES
    global FOURMIS_AVEC_RAU, FOURMIS_SANS_RAU


    #FB Comprenez-vous la différence de traitement ci-dessous entre fourmis avec et sans RAU ? Notamment, y a-t-il une importance à traiter d'abord les fourmis avec RAU ou est-ce indifférent ?


    for fourmi in FOURMIS_AVEC_RAU :
        FOURMIS_AVEC_RAU.remove(fourmi)
        new_position = deplacement_une_fourmi(fourmi)
        if ENVIRONNEMENT[new_position] == CODE_FOURMILIERE :
            print( "la fourmi", fourmi, "a rempli son quota")
            NB_RAU_COLLECTEES += 1
        else :
            FOURMIS_AVEC_RAU.append(deplacement_une_fourmi(fourmi))

    for fourmi in FOURMIS_SANS_RAU :
        FOURMIS_SANS_RAU.remove(fourmi)
        new_position = deplacement_une_fourmi(fourmi)
        if ENVIRONNEMENT[new_position] == CODE_RAU :
            print( "la fourmi",fourmi,"a récupéré de la bouffe en", new_position)
            FOURMIS_AVEC_RAU.append(new_position)
        else :
            FOURMIS_SANS_RAU.append(new_position)



## Affichage graphique et interaction

def ferme_fenetre(event) : # fonction appelée quand on ferme la fenêtre
    global SIMULATION_EN_COURS

    SIMULATION_EN_COURS = False


def affichage_graphique() :
    plt.cla() #FB à chaque nouvel affichage, Commencer par tout effacer

    plt.imshow(ENVIRONNEMENT,cmap=CMAPU)  # on affiche le terrain

    # Puis on affiche les fourmis

    liste_x = [fourmi[1] for fourmi in FOURMIS_AVEC_RAU]
    liste_y = [fourmi[0] for fourmi in FOURMIS_AVEC_RAU]

    plt.scatter(liste_x , liste_y,color = COULEUR_FOURMI_AVEC_RAU, s = 50, marker = 'o' )

    liste_x = [fourmi[1] for fourmi in FOURMIS_SANS_RAU]
    liste_y = [fourmi[0] for fourmi in FOURMIS_SANS_RAU]

    plt.scatter(liste_x , liste_y,color = COULEUR_FOURMI_SANS_RAU, s = 50, marker = 'o')

    plt.axis('equal')

    #plt.show() #FB Attention, le plt.show() doit en fait se trouver ailleurs (à la fin de la boucle principale), ici on va utiliser :

    plt.draw()


## Initialisation de Matplotlib et Boucle Principale

fig, ax = plt.subplots()

fig.canvas.mpl_connect('close_event', ferme_fenetre)

while SIMULATION_EN_COURS :
    print("-------")
    deplacement_des_fourmis()
    affichage_graphique()
    if NB_RAU_COLLECTEES == NB_RAU_INITIAL : #La simulation s'arrête quand toutes les RAU sont récoltées (implémenter l'unicité de la RAU, une réserve limitée ?) (OU quand toutes les fourmis sont rentrés à la fourmillière avec une RAU ?)
        SIMULATION_EN_COURS = False
    #FB A quoi servent les deux lignes précédentes ?
    plt.pause(TEMPS_PAUSE)

plt.show()

