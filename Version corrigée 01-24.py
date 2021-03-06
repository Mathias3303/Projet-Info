import random
from random import randint
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from math import pi,exp,cos
import matplotlib.colors as couleurs

### COMMENTAIRES

#FB Il y a parfois une petite erreur très subtile dans le mouvement des fourmis (rarement !). La verrez-vous ? =D

#FB Pour le moment, ça fait des fourmis qui sortent de la fourmilière et qui se promènenent au hasard et qui récupèrent parfois de la nourriture au hasard... De plus tout ça se fait sur un exemple pour le moment, à généraliser
#FB Je vais modifier les codes ci-dessous pour vous permettre d'avoir un code couleur précis, JE VOUS EXPLIQUERAI COMMENT CA MARCHE.

#FB Les deux variables suivantes vont permettre de dessiner le monde avec des couleurs définies :









### VARIABLES GLOBALES

## pour l'affichage graphique


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


## pour l'arrêt ou la poursuite de la simulation

NB_RAU_INITIAL = 3 #ici, test manuel ; à implémenter dans remplit_RAU_au_hasard
NB_RAU_COLLECTEES = 0 #idee booleen compteur de RAU rentrées à la maison qui acheve le programme (while), cf. dernière fonction

SIMULATION_EN_COURS = True # cette variable indique que la simulation est en cours (tant qu'elle vaut True, la boucle principale continue - elle devient False par exemple si on ferme la fenêtre grâce à un bout de code que je vous ai mis en cadeau bonus !)


## liées à l'interprétation de l'inertie

EPSILON_COS = 0.001
INFLUENCE_COS_0 = 8
INFLUENCE_COS_PId4 = 5
INFLUENCE_COS_PId2 = 3
INFLUENCE_COS_3PId4 = 2
INFLUENCE_COS_PI = 1


VECTEUR_VITESSE_FOURMIS_SANS_RAU = [(1,1), (-1,1), (1,0)]
VECTEUR_VITESSE_FOURMIS_AVEC_RAU = []


ALPHA_INERTIE = 0.001 #variable caractérisant la préférence au déplacement


INFLUENCE_CASE = 1 #à supprimer ? ancien chemin pour le déplacement choisi


## liées à l'interprétation de l'inertie

ALPHA_PHEROMONE = 'à faire'









### DEFINITION DE L'ENVIRONNEMENT





# ENVIRONNEMENT : rectangle de maxX*maxY cases pratiquables

maxX = 10
maxY = 10
# taille FIXEE dans cet exemple (à généraliser avec un environnement généré au hasard)

ENVIRONNEMENT = np.zeros((maxX+2,maxY+2))

ENVIRONNEMENT[:,0] = CODE_OBSTACLE
ENVIRONNEMENT[0,:] = CODE_OBSTACLE
ENVIRONNEMENT[maxX+1,:] = CODE_OBSTACLE
ENVIRONNEMENT[:,maxY+1] = CODE_OBSTACLE

LISTE_POSITION_RAU = [(2,2),(10,10), (5,8)]

for coord in LISTE_POSITION_RAU :
    ENVIRONNEMENT[coord] = CODE_RAU

ENVIRONNEMENT[(5,5)] = CODE_FOURMILIERE

print(ENVIRONNEMENT)



FOURMIS_SANS_RAU = [(5,5),(5,5),(5,5)]
FOURMIS_AVEC_RAU = []



TEMPS_PAUSE = 1 # à quoi ça sert ?



# mettre plus tard : remplit_RAU_au_hasard(x) , remplit_obstacles_au_hasard(x)














### FONCTIONS UTILITAIRES


## fonctions liées à l'environnement

def remplit_RAU_au_hasard(nbUnites) :
    '''
    met nbUnites au hasard dans la variable globale ENVIRONNEMENT
    '''

    global NB_RAU_INITIAL

    NB_RAU_INITIAL = nbUnites

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
        print('Pas assez de place dans ENVIRONNEMENT pour autant de RAU')



def remplit_Obstacles_au_hasard(nbUnites) :
    '''
    met nbObstacles obstacles dans la variable ENVIRONNEMENT
    '''

    Nb_Obstacles = nbUnites # faire une variable globale ?
    Nb_Obstacles_places = 0
    positionsObstacles = []

    if Nb_Obstacles <= maxX*maxY :
        while Nb_Obstacles_places < Nb_Obstacles :  #for k in range(nbObstacles) :
            xObs = randint(1, maxX)
            yObs = randint(1, maxY)
            positionsObstacles.append((xObs, yObs))
            for l in positionsObstacles :
                if ENVIRONNEMENT[l] ==  CODE_PRATICABLE :
                    ENVIRONNEMENT[l] = CODE_OBSTACLE
                    Nb_Obstacles_places += 1
    else :
        print('Pas assez de place dans ENVIRONNEMENT pour autant d obstacles')


    # à insérer sur github



## liste des voisins praticables ATTENTION MODIFICATION IMPORTANTE !

def liste_des_voisins_praticables(case):
    '''Renvoie liste des coordonnees des cases accessibles en partant d'une autre case, c'est à dire celles qui lui sont adjacentes (dont diagonales) et praticables'''
    i = case[0]
    j = case[1]
    voisins_potentiels = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1)] # parcours d'en haut à gauche, dans le sens horaire
    indice_voisins_praticables = []
    for candidat in voisins_potentiels:
        if (0 <= candidat[0] < ENVIRONNEMENT.shape[0]) and (0 <= candidat[1] < ENVIRONNEMENT.shape[1]) and (ENVIRONNEMENT[candidat] != CODE_OBSTACLE ):
            indice_voisins_praticables.append(candidat)
    return indice_voisins_praticables



## fonctions de calculs

def couple_delta(case_suivante , case_actuelle):
    '''
    renvoie un vecteur vitesse instantanée entre 2 cases traversées successives
    '''
    di = case_suivante[0] - case_actuelle[0]
    dj = case_suivante[1] - case_actuelle[1]
    couple_delta = ( di , dj )
    return couple_delta


def cos_des_deltas(delta_actuel, delta_possible) :
    produit_scalaire = np.dot(delta_actuel, delta_possible) #produit scalaire entre vecteur avant et vecteur suivant
    norme_vecteur_possible =( (delta_possible[0])**2 + (delta_possible[1])**2 )**(1/2) #norme du vecteur vitesse qui pointe vers une case possible
    norme_vecteur_actuel = ( (delta_actuel[0])**2 + (delta_actuel[1])**2 )**(1/2)
    cos_case_possible = produit_scalaire / (norme_vecteur_possible*norme_vecteur_actuel) #on divise par la norme pour isoler cos


    # arrondissement des valeurs de cos obtenues :

    if abs(cos_case_possible - cos(0)) <= EPSILON_COS :
        cos_case_possible = cos(0)

    elif abs(cos_case_possible - cos(pi/4)) <= EPSILON_COS :
        cos_case_possible = cos(pi/4)

    elif abs(cos_case_possible - cos(pi/2)) <= EPSILON_COS :
        cos_case_possible = cos(pi/2)

    elif abs(cos_case_possible - cos(3*pi/4)) <= EPSILON_COS :
        cos_case_possible = cos(3*pi/4)

    elif abs(cos_case_possible - cos(pi)) <= EPSILON_COS :
        cos_case_possible = cos(pi)

    return cos_case_possible





### FONCTIONS D'ATTRACTIVITE

## pour l'inertie

def attractivite_inertie_une_fourmi(fourmi):


    global ALPHA_INERTIE

    case_actuelle = fourmi
    delta_actuel = VECTEUR_VITESSE_FOURMIS_SANS_RAU[0] #couple_delta de l'actuel ATTENTION NE TRAITE QU'UN GROUPE DE FOURMIS
    voisins_praticables = liste_des_voisins_praticables(case_actuelle)
    L_cos_voisins_praticables = []
    L_attractivite_inertie_des_voisins_praticables = []


    for case_possible in voisins_praticables :
        delta_possible = couple_delta(case_possible, case_actuelle) #vecteur vitesse de case actuelle à case possible
        cos_case_possible = cos_des_deltas(delta_actuel, delta_possible)

        L_cos_voisins_praticables.append(cos_case_possible) #liste des cos de l'angle formé par les vecteurs actuel et possible

    for x in L_cos_voisins_praticables :
        if x == cos(0) :
            L_attractivite_inertie_des_voisins_praticables.append(INFLUENCE_COS_0)

        elif x == cos(pi/4) :
            L_attractivite_inertie_des_voisins_praticables.append(INFLUENCE_COS_PId4)

        elif x == cos(pi/2) :
            L_attractivite_inertie_des_voisins_praticables.append(INFLUENCE_COS_PId2)

        elif x == cos(3*pi/4) :
            L_attractivite_inertie_des_voisins_praticables.append(INFLUENCE_COS_3PId4)

        elif x == cos(pi) :
            L_attractivite_inertie_des_voisins_praticables.append(INFLUENCE_COS_PI)

    return L_attractivite_inertie_des_voisins_praticables




## pour les phéromones environnants

#def attractivite_pheromones_une_fourmi():  A FAIRE






### FONCTIONS DE DEPLACEMENT


def deplacement_inertie_et_pheromones_une_fourmi(fourmi):
    '''
    chaque fourmi se déplace selon son inertie et les phéromones alentours
    '''

    cases_possibles = liste_des_voisins_praticables(fourmi)

    attractivite_inertie = attractivite_inertie_une_fourmi(fourmi)
    #attractivite_pheromones = attractivite_pheromones_une_fourmi(fourmi)

    attractivite_inertie_softmax = [exp(ALPHA_INERTIE*x) for x in attractivite_inertie] # ajouter même chose avec pheromones

    nouvelle_case = random.choices(cases_possibles , attractivite_inertie_softmax ) # choix pondéré par les attractivités ATTENTION C'EST UN ARRAY
    print(nouvelle_case)

    return nouvelle_case[0]






def deplacement_aleatoire_une_fourmi(fourmi) :
    '''
    chaque fourmi se promène aléatoirement
    '''
    nouvelle_case = random.choice(liste_des_voisins_praticables(fourmi))
    print("la fourmi", fourmi,"va en ", nouvelle_case)
    return nouvelle_case




def deplacement_des_fourmis() :

    '''
    gère le déplacement de toutes les fourmis, et le passage entre "sans RAU" et "avec RAU"
    '''

    global NB_RAU_COLLECTEES
    global FOURMIS_AVEC_RAU, FOURMIS_SANS_RAU


    L_provisoire_AVEC_RAU = [] #création de listes de stockage provisoires
    L_provisoire_SANS_RAU = []

    for fourmi in FOURMIS_AVEC_RAU:
        new_position = deplacement_aleatoire_une_fourmi(fourmi) # on peut remplacer 'aleatoire' par 'inertie_et_pheromones' et inversement
        if ENVIRONNEMENT[new_position] == CODE_FOURMILIERE :
            print( "la fourmi", fourmi, "a rempli son quota")
            NB_RAU_COLLECTEES += 1
        else :
            L_provisoire_AVEC_RAU.append(new_position)


    for fourmi in FOURMIS_SANS_RAU :
        new_position = deplacement_inertie_et_pheromones_une_fourmi(fourmi) # on peut remplacer 'aleatoire' par 'inertie_et_pheromones' et inversement
        if ENVIRONNEMENT[new_position] == CODE_RAU :
            print( "la fourmi",fourmi,"a récupéré de la bouffe en", new_position)
            L_provisoire_AVEC_RAU.append(new_position)
        else :
            L_provisoire_SANS_RAU.append(new_position)


    FOURMIS_AVEC_RAU = L_provisoire_AVEC_RAU
    FOURMIS_SANS_RAU = L_provisoire_SANS_RAU







### GESTION ET AFFICHAGE SIMULATION

## Affichage graphique et interaction

def ferme_fenetre(event) : # fonction appelée quand on ferme la fenêtre
    global SIMULATION_EN_COURS

    SIMULATION_EN_COURS = False


def affichage_graphique() :
    plt.cla() #FB à chaque nouvel affichage, Commencer par tout effacer

    plt.imshow(ENVIRONNEMENT,cmap=CMAPU)  # On affiche le terrain

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
    if NB_RAU_COLLECTEES == NB_RAU_INITIAL : #La simulation s'arrête quand toutes les RAU sont récoltées (implémenter l'unicité de la RAU, une réserve limitée ?) (OU quand toutes les fourmis sont rentrés à la fourmilière avec une RAU ?)
        SIMULATION_EN_COURS = False
    plt.pause(TEMPS_PAUSE)

plt.show()
