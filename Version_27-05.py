import random
from random import randint
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from math import pi,exp,cos
import matplotlib.colors as couleurs


## Paramètres de la simulation

# Changer ces variables pour modifier le comportement

NB_FOURMIS_MAX = 20

ALPHA_INERTIE_ALLER = 1 #variable caractérisant la préférence au déplacement
ALPHA_INERTIE_RETOUR = 1

ALPHA_PHEROMONE_ALLER = 2
ALPHA_PHEROMONE_RETOUR = 3


UNITE_PHERO_ALLER = 1
UNITE_PHERO_RETOUR = 0.1

TIMER = 0
TIMER_PHEROMONE = 300000 #temps avant arrêt de l'émission des phéromones

TIMER_NEW_ANT = 10 # Nb itérations de la boucles principale entre l'apparition de chaque fourmi

TAUX_DISP_PHEROMONE = 0.96

TEMPS_PAUSE = 0.001 # vitesse d'affichage(cf.tout en bas)

MAX_ODEUR_FOURMILLIERE = 3 # valeur centrale de l'odeur de la fourmilière

DECROISSANCE_ODEUR_FOURMILIERE = 0.95


NB_RAU_INITIAL = 3 #ici, test manuel ; à implémenter dans remplit_RAU_au_hasard

# taille de l'environnement : rectangle de maxX*maxY cases pratiquables

maxX = 50
maxY = 50




### CREATION DE L'ENVIRONNEMENT

# codes pour le tableau d'environnement

CODE_OBSTACLE = 1
CODE_PRATICABLE = 0
CODE_RAU = 2
CODE_FOURMILIERE = 3


## Ce qui suit est un exemple d'environnement

ENVIRONNEMENT = np.zeros((maxX+2,maxY+2))

ENVIRONNEMENT[:,0] = CODE_OBSTACLE
ENVIRONNEMENT[0,:] = CODE_OBSTACLE
ENVIRONNEMENT[maxX+1,:] = CODE_OBSTACLE
ENVIRONNEMENT[:,maxY+1] = CODE_OBSTACLE


LISTE_POSITION_RAU = [ (40,5) , (41,5) , (40,6) , (42,5) , (42,6) , (40,4) , (41,4) , (42,4) , (39,5) , (39,6) , (39,7) , (38,5) , (38,6) , (38,4) ]

for k in range(5):
    ENVIRONNEMENT[k+5, 5:10] = CODE_RAU
    ENVIRONNEMENT[k+22, 7:12] = CODE_RAU
for k in range(3):
    ENVIRONNEMENT[k+10, 30:33] = CODE_RAU
    ENVIRONNEMENT[k+25 , 43:46] = CODE_RAU

for coord in LISTE_POSITION_RAU :
    ENVIRONNEMENT[coord] = CODE_RAU

CASE_FOURMILIERE = (24,24)

ENVIRONNEMENT[CASE_FOURMILIERE] = CODE_FOURMILIERE




# mettre plus tard : remplit_RAU_au_hasard(x) , remplit_obstacles_au_hasard(x)


##  TABLEAUX LIEES AUX PHEROMONES


TABLO_PHERO_ALLER = np.zeros((maxX+2,maxY+2))

TABLO_PHERO_RETOUR_VARIABLE = np.zeros((maxX+2,maxY+2))

TABLO_PHERO_RETOUR_FIXE = TABLO_PHERO_RETOUR.copy()


def distance(case1,case2) :
    return ( ( case1[0]-case2[0])**2 + ( case1[1]-case2[1])**2)**0.5



for i in range (maxX+2) :
    for j in range(maxY+2) :
        TABLO_PHERO_RETOUR_FIXE [i,j] = MAX_ODEUR_FOURMILLIERE*DECROISSANCE_ODEUR_FOURMILIERE**distance((i,j),CASE_FOURMILIERE)

TABLO_PHERO_RETOUR = TABLO_PHERO_RETOUR_VARIABLE + TABLO_PHERO_RETOUR_FIXE



## fonctions de  création  d'environnement

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




## Fonctions utilitaires


def liste_des_voisins_praticables(case):
    '''Renvoie liste des coordonnees des cases accessibles en partant d'une autre CASE, c'est à dire celles qui lui sont adjacentes (dont diagonales) et praticables'''
    i = case[0]
    j = case[1]
    voisins_potentiels = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1)] # parcours d'en haut à gauche, dans le sens horaire
    indice_voisins_praticables = []
    for candidat in voisins_potentiels:
        if (0 <= candidat[0] < ENVIRONNEMENT.shape[0]) and (0 <= candidat[1] < ENVIRONNEMENT.shape[1]) and (ENVIRONNEMENT[candidat] != CODE_OBSTACLE ):
            indice_voisins_praticables.append(candidat)
    return indice_voisins_praticables





def couple_delta(case_suivante , case_actuelle):
    '''
    renvoie un vecteur vitesse instantanée entre 2 cases traversées successives
    '''
    di = case_suivante[0] - case_actuelle[0]
    dj = case_suivante[1] - case_actuelle[1]
    couple_delta = ( di , dj )
    return couple_delta



def attractivites_directionnelles(case, delta_actuel, liste_cases_voisines) :

    liste_attractivites = []

    for voisin in liste_cases_voisines :
        delta_possible = couple_delta(voisin,case)

        produit_scalaire = np.dot(delta_actuel, delta_possible) # produit scalaire entre vecteur avant et vecteur suivant
        norme_vecteur_possible =( (delta_possible[0])**2 + (delta_possible[1])**2 )**(1/2) # norme du vecteur vitesse qui pointe vers une case possible
        norme_vecteur_actuel = ( (delta_actuel[0])**2 + (delta_actuel[1])**2 )**(1/2)
        cos_case_possible = produit_scalaire / (norme_vecteur_possible*norme_vecteur_actuel)

        liste_attractivites.append(cos_case_possible)

    return liste_attractivites




## FONCTIONS DE DEPLACEMENT



#FB Nouvelle fonction  unique

def probas_mouvement_une_fourmi (fourmi, cases_voisines, tablo_type_pheromone, alpha_inertie, alpha_pheromone) :
    '''
    prend :
    - une fourmi
    - la liste des cases voisines (pas la peine de la calculer plusieurs fois)
    - le tableau correspondant au type de phéromones auxquelles cette fourmi est sensible (aller/retour)
    - le poids de l'inertie pour cette fourmie
    - le poids des pheromones

    renvoie la liste des probas pour chaque case voisine

    Exemple :

    Pour un déplacement aléatoire complet, mettre les deux alpha à 0

    Pour un déplacement ne dépendant que de l'inertie mettre alpha_pheromone à zéro, etc.

    '''


    n = len(cases_voisines) # nb de cases voisines

    liste_att_dir  = attractivites_directionnelles(fourmi[0], fourmi[2],  cases_voisines)

    liste_att_phero = [ tablo_type_pheromone[c] for c in cases_voisines]

    liste_mixee =  [exp(alpha_inertie*liste_att_dir[k] + alpha_pheromone*liste_att_phero[k]) for k in range(n) ]

    S = sum(liste_mixee)


    return  [x/S for x in liste_mixee]



def deplace_une_fourmi(fourmi) :
    '''
    prend une fourmi, et renvoie sa nouvelle position
    '''
    if fourmi[1] :
        tablo_phero = TABLO_PHERO_RETOUR
        alpha_inertie = ALPHA_INERTIE_RETOUR
        alpha_pheromone = ALPHA_PHEROMONE_RETOUR
    else :
        tablo_phero = TABLO_PHERO_ALLER
        alpha_inertie = ALPHA_INERTIE_ALLER
        alpha_pheromone = ALPHA_PHEROMONE_ALLER

    cases_voisines = liste_des_voisins_praticables(fourmi[0])

    distrib = probas_mouvement_une_fourmi (fourmi, cases_voisines, tablo_phero, alpha_inertie, alpha_pheromone)

    return random.choices(cases_voisines, distrib)[0]

#FB La fonction suivante remplace les votres :

def deplacement_des_fourmis() :
    nb_fourmis = len(FOURMIS)

    for indice_fourmi in range(nb_fourmis - 1,-1,-1) :
        fourmi = FOURMIS[indice_fourmi]
        new_position = deplace_une_fourmi(fourmi)

        # gestion des cas particuliers : changement d'état, retour fourilière

        if fourmi[1] and new_position == CASE_FOURMILIERE :
            print("une fourmi rentre au bercail")
        elif (not fourmi[1]) and ENVIRONNEMENT[new_position] == CODE_RAU:
            print("une fourmi mange")
            new_dir = (-fourmi[2][0],-fourmi[2][1])
            new_etat = [new_position, True, new_dir]
            FOURMIS.append(new_etat)
            ENVIRONNEMENT[new_position] = CODE_PRATICABLE
        else :
            new_dir = (new_position[0]-fourmi[0][0],new_position[1]-fourmi[0][1])
            new_etat = [new_position, fourmi[1], new_dir]
            FOURMIS.append(new_etat)


        del FOURMIS[indice_fourmi]


def liberation_pheromones() :
    for fourmi in FOURMIS :
        if fourmi[1] :
            TABLO_PHERO_ALLER[fourmi[0]] += UNITE_PHERO_ALLER
        else :
            TABLO_PHERO_RETOUR_VARIABLE[fourmi[0]] += UNITE_PHERO_RETOUR




## Affichage graphique et interaction



# Variables globales de gestion de l'affichage graphique


# blanc pour les cases vides
# gris pour les obstacles
# vert pour la / les fourmilières
# rouge pour les stocks de nourriture

COULEURS = ["white","grey", "green", "red"]
CMAPU = couleurs.ListedColormap(COULEURS)

# Les fourmis auront aussi leurs couleurs suivant qu'elles sont "à vide" ou "portent un RAU"

COULEUR_FOURMI_SANS_RAU = "black"
COULEUR_FOURMI_AVEC_RAU = "orange"


def ferme_fenetre(event) : # fonction appelée quand on ferme la fenêtre
    global SIMULATION_EN_COURS

    SIMULATION_EN_COURS = False


def affichage_graphique() :
    ax1.cla() #FB à chaque nouvel affichage, Commencer par tout effacer

    ax1.axis('off')

    ax1.imshow(ENVIRONNEMENT,cmap=CMAPU)  # On affiche le terrain

    FOURMIS_AVEC_RAU = [fourmi[0] for fourmi in FOURMIS if fourmi[1]] # positions des fourmis avec RAU
    FOURMIS_SANS_RAU = [fourmi[0] for fourmi in FOURMIS if not fourmi[1]] # positions des fourmis sans RAU

    # Puis on affiche les fourmis

    liste_i = [fourmi[0] for fourmi in FOURMIS_AVEC_RAU]
    liste_j = [fourmi[1] for fourmi in FOURMIS_AVEC_RAU]


    ax1.scatter(liste_j , liste_i,color = COULEUR_FOURMI_AVEC_RAU, s = 50, marker = 'o' )


    liste_i = [fourmi[0] for fourmi in FOURMIS_SANS_RAU]
    liste_j = [fourmi[1] for fourmi in FOURMIS_SANS_RAU]


    ax1.scatter(liste_j , liste_i, color = COULEUR_FOURMI_SANS_RAU, s = 50, marker = 'o')

    ax1.axis('equal')

    ax2.cla() # "efface les axes courants" : cela efface l'ancienne position des fourmis

    ax2.axis('off')  #supprime les axes du tableau

    ax2.imshow(TABLO_PHERO_ALLER)
    ax2.set_title("phéromones ALLER")

    ax3.cla() # "efface les axes courants" : cela efface l'ancienne position des fourmis

    ax3.axis('off')  #supprime les axes du tableau

    ax3.imshow(TABLO_PHERO_RETOUR)

    ax3.set_title("phéromones retour")




    #plt.show() #FB Attention, le plt.show() doit en fait se trouver ailleurs (à la fin de la boucle principale), ici on va utiliser : # COMMENTAIRE SUPPRIMABLE

    plt.draw()






## initialisation de la simulation


NB_RAU_COLLECTEES = 0 #idee booleen compteur de RAU rentrées à la maison qui acheve le programme (while), cf. dernière fonction

SIMULATION_EN_COURS = True # cette variable indique que la simulation est en cours (tant qu'elle vaut True, la boucle principale continue - elle devient False par exemple si on ferme la fenêtre grâce à un bout de code que je vous ai mis en cadeau bonus !)

FOURMIS = [[ CASE_FOURMILIERE, False , (randint(-1,1),randint(-1,1))]] # Liste des fourmis, on commence avec une fourmi


# chque fourmi sera une liste : [coordonnées , Rau ou pas, vecteur déplacement ]

# corrdonnées = couple
# RAU ou pas = booléen
# vecteur déplacement = couple


fig, (ax1, ax2,ax3) = plt.subplots(1, 3)

fig.canvas.mpl_connect('close_event', ferme_fenetre)


## Boucle Principale


while SIMULATION_EN_COURS :
    #print("-------")
    affichage_graphique()
    liberation_pheromones()
    deplacement_des_fourmis()

    TIMER += 1

    if TIMER % TIMER_NEW_ANT == 0 and len(FOURMIS) <= NB_FOURMIS_MAX:
        FOURMIS.append([ CASE_FOURMILIERE, False , (randint(-1,1),randint(-1,1))])

    TABLO_PHERO_ALLER *= TAUX_DISP_PHEROMONE

    TABLO_PHERO_RETOUR_VARIABLE *= TAUX_DISP_PHEROMONE
    TABLO_PHERO_RETOUR = TABLO_PHERO_RETOUR_VARIABLE + TABLO_PHERO_RETOUR_FIXE

    #FB j'enlève le code suivant pour le moment

    '''
    if NB_RAU_COLLECTEES == NB_RAU_INITIAL : #La simulation s'arrête quand x sont récoltées (implémenter l'unicité de la RAU, une réserve limitée ?) (OU quand toutes les fourmis sont rentrés à la fourmilière avec une RAU ?)
        SIMULATION_EN_COURS = False

    '''
    plt.pause(TEMPS_PAUSE)

plt.show()


#Si on met un fort ALPHA_PHEROMONE personne va vouloir rentrer à la fourmilière elles vont juste tourner autour


##
#dans fonction deplacement : codepheromone*tauxdisp
#dans boucle finale : timer pour arreter emission au bout d'un moment