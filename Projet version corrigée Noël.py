import random
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import matplotlib.colors as couleurs

#FB  petit cadeau de Noël : je vous ai mis le code pour faire un affichage coloré (avec des couleurs paramétrables) et notamment des couleurs différentes pour les fourmis avec et sans RAU (au passage, pour que ce soit simple, j’ai  modifié le code que vous aviez déterminé pour les cases du tableau ENVIRONNEMENT : c’était bie nrpatique que vous ayez des variables globales plutôt que des « -1 » ici et là !)

#FB deuxièmement, je vous ai fait la boucle principale (avec un petit bonus : si on ferme la fenêtre, le programme s’arrête !). Une remarque stratégique :   cela aurait été bien de la mettre en place en premier pour pouvoir tester vos idées rapidement.

#FB le programme fonctionen de la façon suivante : on exécute simplement le fichier, et il nosu montre un exempel de simulation suivant

#FB Pour que ce soit clair, j'ai bien séparé les variables globales en deux : les variables techniques et celles liées à l'exemple actuel.

#FB Il y a parfois une petite erreur très subtile dans le mouvement des fourmis (rarement !). La verrez-vous ? =D

#FB Pour le moment, ça fait des fourmis qui sortent de la fourmilière et qui se promènenent au hasard et qui récupèrent parfois de la nourriture au hasard... De plus tout ça se fait sur un exemple pour le moment, à généraliser

## Variables globales techniques

#FB Je vais modifier les codes ci-dessous pour vous permettre d'avoir un code couleur précis, je vous expliquerai comment ça marche.

#FB Les deux variables suivantes vont permettre de dessiner le monde avec des couleurs définies :

# blanc pour les cases vides
# gri pour les obstacles
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


NB_RAU_COLLECTEES = 0 #idee booleen compteur de RAU rentrées à la maison qui acheve le programme (while)


INFLUENCE_COS_0 = 5
INFLUENCE_COS_PId4 = 3
INFLUENCE_COS_PId2 = 2
INFLUENCE_COS_3PId4 = 1
INFLUENCE_COS_PI = 0

INFLUENCE_CASE = 1

SIMULATION_EN_COURS = True # cette variable indique que la simulation est en cours (tant qu'elle vaut True, la boucle principale continue - elle devient False par exemple si on ferme la fenêtre grâce à un bout de code que je vous ai mis en cadeau bonus !)

## UN EXEMPLE

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

ENVIRONNEMENT[2,3] = ENVIRONNEMENT[7,6] = ENVIRONNEMENT[4,7] = CODE_OBSTACLE


print(ENVIRONNEMENT)



FOURMIS_SANS_RAU = [(5,5),(5,5),(5,5)]
FOURMIS_AVEC_RAU = []

#FB Pour quoi deux fois la ligne suivante ? J'en enlève un

VECTEUR_VITESSE_FOURMIS_AVEC_RAU = []
#VECTEUR_VITESSE_FOURMIS_AVEC_RAU = []

TEMPS_PAUSE = 1




## Mise en place aléatoire de l'environnement

#FB Je mets le code suivant dans une fonction pour que vous compreniez ce que je veux dire :


def remplit_RAU_au_hasard(nbUnites) :
    '''
    met nbUnites au hasard dans la variable globale ENVIRONNEMENT


    '''

    global NbRAU

    NbRAU = nbUnites

    #FB je remplace le input par un paramètre dans ma fonction

    positionsRAU = []

    #FB l'algo que vous utilisez ci-dessous ne fait pas ce que vous voulez de manière sure : si par hasard il tombe deux fois sur la même case, ou à un moment sur une case obstacle, à la fin vous aurez moins de cases RAU que vous le vouliez... à améliorer...

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

#FB Faire de même la fonction suivante :

def remplit_RAU_au_hasard(nbObstacles) :
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
        voisins_praticables = liste_des_voisins_praticables(ENVIRONNEMENT , caseactuelle)
        L_cos_voisins_praticables = []
        L_attractivite_des_voisins_praticables = []
        norme_vecteur_actuel = ( (delta_actuel[0])**2 + (delta_actuel[1])**2 )**(1/2)

        for case_possible in voisins_praticables :
            delta_case_possible = couple_delta(case_possible, case_actuelle)
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

    global FOURMIS_AVEC_RAU, FOURMIS_SANS_RAU
    #FB comprenez-vous l'intérêt de la ligne précédente ?


    #FB Comprenez-vous la différence de traitement ci-dessous entre fourmis avec et sans RAU ? Notamment, y a-t-il une importance à traiter d'abord les fourmis avec RAU ou est-ce indifférent ?


    for fourmi in FOURMIS_AVEC_RAU :
        FOURMIS_AVEC_RAU.remove(fourmi)
        FOURMIS_AVEC_RAU.append(deplacement_une_fourmi(fourmi))

    for fourmi in FOURMIS_SANS_RAU :
        FOURMIS_SANS_RAU.remove(fourmi)
        new_position = deplacement_une_fourmi(fourmi)
        if ENVIRONNEMENT[new_position] == NOURRITURE :
            print( "la fourmi",fourmi,"a bouffé en", new_position)
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
    if not FOURMIS_SANS_RAU :
        SIMULATION_EN_COURS = False
    #FB A quoi servent les deux lignes précédentes ?
    plt.pause(TEMPS_PAUSE)

plt.show()

