#!/usr/bin/env python
# coding: utf-8



#!/usr/bin/env python
# coding: utf-8

#from gurobipy import *
import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt
import os

from math import *
from random import *
import time
seed(time.time())


# Fonctions sur les probas :



def proba_simple(k):
    """
    k : int -> float
    reourne la probabilité d'obtenir une face du dè sachant que l'on n'obtient pas de face 1
    """
    if k <= 1 or k>=7:
        return 0
    return 1./5


def Q(d, k):
    """
    d : int, k : int -> float
    retourne la formule de recurrence pour d dès et k points
    """
    if d == 1:
        if k>=2 and k<=6:
            return proba_simple(k)
        return 0
    if (k>=0 and k<=2*d-1) or k>6*d or k<=0:
        return 0
    return (1./5)*(Q(d-1, k-2) + Q(d-1, k-3) + Q(d-1, k-4) + Q(d-1, k-5) +Q(d-1, k-6))


def proba_Points(d, k):
    """
    d : int, k : int -> float
    retourne la probabilité d'obtenir k points en lançant d dès
    """
    if int(k) == 1:
        return 1 - np.power(5./6, d)
    if (k>0 and k<=2*d-1) or k>6*d:
        return 0
    return np.power(5./6, d)*Q(d,k)


def max_esperance(D, max_ = True):
    """
    D : int, max_ : (True) bool -> int
    max_ : si True on retourne le maximmum sinon on retourne la liste de l'esperance sur [1, D]
    retourne max EP(d) quand d est dans [1, D]
    """
    #t0 = time.time()
    if D>=6:     #A partir de 6 des on converge vers 6
        #print(time.time() - t0)
        return 6

    E = np.array([4*d*np.power(5./6, d) + 1 - np.power(5./6, d) for d in range(1,D+1) ])
    if max_ == False:
        return E
    #print(time.time() - t0)
    return np.argmax(E)+1


def tableau_proba(d):
    """
    d : int -> list[6*d](float)
    retourne le tableau des probabilites d'obtenir entre 1 et 6*d points pour d
    """
    return [proba_Points(d, k) for k in range(2*d, 6*d+1)]

def tableau_probaTotale():
    """
    ->nd.array[D, 6*D](float)
    retourne le tableau des probabilites d'obtenir entre 1 et 6*D points pour d dans [1,D]
    """
    TabD = []
    for d in range(1, D+1): # on itere sur le nombre de des qu'on peut lancer
        TabD.append([ proba_Points(d, k) for k in range(1, (6*D)+1)]) #pour chaque nbre de des on itere sur les probas des points
    return np.array(TabD)




def EGij_Final():
    """
    -> nd.array[N+6*D, N+6*D](float), nd.array[N+6*D, N+6*D](int)
    retourne la matrice des EG(i,j) et des des optimaux pour (i,j) pour tout i, j
    """
    #Esperances
    EG = np.zeros((N+6*D, N+6*D))
    #Des optimaux
    des_EG = np.zeros((N+6*D, N+6*D))
    #initialisation
    for i in range(N, N+6*D):
        for j in range(N):
            EG[i,j] = 1
            EG[j,i] = -1
        for k in range(N, N+6*D):
            EG[i,k] = 1

    #La recursivite
    for i in range(N-1, -1, -1):
        for j in range(i, -1, -1):
            Temp1 = -np.sum(P_tot*EG[j,i+1:i+1 + D*6], axis = 1)
            Temp2 = -np.sum(P_tot*EG[i,j+1:j+1 + D*6], axis = 1)
            des_EG[i,j] = np.argmax(Temp1) + 1
            EG[i,j] = np.max(Temp1)
            des_EG[j,i] = np.argmax(Temp2) + 1
            EG[j,i] = np.max(Temp2)


    return EG, des_EG.astype(int)

# EG la matrice de gain
def resolutionPL(EG):
    """
    EG : nd.array[D, D](float) - > nd.array(float)
    retourne le vecteur des probabilites grace au PL
    """
    m = Model("PL")
    #on recupere la taille de la matrice de gain
    D=len(EG)

    # declaration des variables de decision
    x = []
    for i in range(0,D):
        x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="p%d" % (i+1)))
    # z sera la fonction objectif
    z = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="z")
    # maj du modele pour integrer les nouvelles variables
    m.update()

    obj = LinExpr();
    obj += z

    # Definition des contraintes
    for i in range(0,D):
        temp=0
        for j in range(0,D):
            temp+=EG[j][i]*x[j]
        m.addConstr(temp >= z, "Contrainte%d" % (i))

    contTemp=0
    for t in range(0,D):
        contTemp+=x[t]

    m.addConstr(contTemp==1, "Contrainte%d" % 10)

    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)

    # Resolution
    m.optimize()
    """
    print("")
    print('Solution optimale:')
    for j in range(0,D):
        print('x%d'%(j+1), '=', x[j].x)
    """
    return np.array([ x[j].x for j in range(0, D)])

################################################################################
def EG1():
    """
    -> nd.array[D, D](float)
    rerourne la tableau des EG1 pour d1 et d2 dans [1, D]
    """
    EG1_Tot = np.zeros((D, D))
    for d1 in range(D):
        for d2 in range(D):
            EG1_Tot[d1, d2] = np.sum([np.sum(P_tot[d2, x]*P_tot[d1, x+1:6*(d1+1)]) for x in range(0, 6*(d2+1))]) - np.sum([np.sum(P_tot[d1, x]*P_tot[d2, x+1:6*(d2+1)]) for x in range(0, 6*(d1+1))])
    return EG1_Tot



# Fonctions sur le Jeu :


def choixDPL(vect):
    """
    vect : nd.array(float) -> int
    retourne le d optimal selon le vecteur de probabilite vect
    """
    rand=random()
    d=D
    while(d):
        rand-=vect[d-1]
        if(rand<0):
            return d
        d-=1

def simul_des(n_des):
    """
    n_des : int -> nd.array(int)
    Simule le tirage de n_des dès
    """
    return np.array([randint(1,6) for n in range(n_des)])

def calcul_points(Des):
    """
    Des : nd.array(int) -> int
    retourne les points associés au lancé de dès
    """
    if sum(Des == 1)!=0:  #Si il y a des 1
        return 1
    return sum(Des)

def nb_des_strat(strat, points, name, ia = False,):
    """
    strat : int, points : list[2](int), name : int, ia : (False) bool -> int
    ia : permet de savoir si J2 est un joueur (False) ou alors simulé (True)
    name : nom du joueur
    retourne le nombre de dès à lancer en fonction de la stratégie adoptée
    """
    des = -1    #on initialise à -1
    if strat == 0:
        if ia == True:
            des = randint(1,D)   #Si pas de stratégie et ia alors nombre aléatoire de dès
        else:
            print("\tVous pouvez choisir de lancer entre 1 et %d dès"%D)
            des = int(input("Veuillez choisir le nombre de dès : "))
            while(des<=0 or des >D):   #Tant que l'utilisateur n'a pas choisi de nombre de dès correct
                print("Nombre de dès incorrect")
                des = int(input("Veuillez choisir le nombre de dès : "))

    elif strat == 1 :
        des = max_esperance(D)   #Si stratégie naive alors max(EP)
        if ia == False:
            print("\tChoix de dès optimal pour la startégie : %d"%des)

    elif strat == 2:
        #print(points)
        if name == 1:
            des = des_EG_ij[int(points[0]), int(points[1])]
        else:
            des = des_EG_ij[int(points[1]), int(points[0])]
        if ia == False:
            print("\tChoix de dès optimal pour la startégie : %d"%des)
    elif strat == 3:
        des = D
    else:
        print("La stratégie choisit n'est pas bonne, veuillez la rechoisir.")
    return des

def choix_strategie(nb_joueurs, debut = False, name = 1):
    """
    nb_joueurs : int, debut : (False) bool > strat 1 ou strat2
    renvoie les stratégies adoptées par le joueur 1 et joueur 2
    debut : si c'est le début de la partie (True) on initilaise l'ia
    """
    if nb_joueurs >= 1:
        print("Choix de la stratégie pour le joueur %d :"%name)
        strat1 = int(input("0 : Aucune \t \t 1 : Stratégie Aveugle \t \t 2 : Stratégie Optimale\n"))
        while(strat1>2 or strat1<0):
            print("Choix de stratégie incorrect.")
            strat1 = int(input("0 : Aucune \t \t 1 : Stratégie Aveugle \t \t 2 : Stratégie Optimale\n"))

        if nb_joueurs == 2:
            print("Choix de la stratégie pour le joueur 2 :")
            strat2 = int(input("0 : Aucune \t \t 1 : Stratégie Aveugle \t \t 2 : Stratégie Optimale\n"))
            return strat1, strat2
        else:
            if debut == True:
                print("Choix de la difficulté : ")
                strat2 = int(input("0 : Facile \t \t 1 : Moyen \t \t 2 : Dur \n"))
                return strat1, strat2
    else:
        raise ValueError("Nombre de joueurs incorrect")
    return strat1




def Joueur(nb_joueurs, strat, points, ia = False, name = 1):
    """
    strat : int, strat : int, points : int, D : int, ia : (False) bool, name : (1) int -> int
    retourne le nouveau nombre de points de J1
    ia : permet de savoir si le joueur 2 est une ia (True) ou un vrai joueur (False)
    name : permet d'identifier quel joueur joue
    """
    des = nb_des_strat(strat, points, name, ia)
    res = simul_des(des)
    pts = calcul_points(res)
    points[name-1] += pts
    if nb_joueurs !=0:
        print("Resultat du lancer de %d des : "%des)
        print(res)
        print("Points obtenus : %d"%pts)
        print("Score actuel : %d"%points[name-1])
    return points[name-1]

def jeu_sequentiel(nb_joueurs, strat, pts, mixte = True):
    """
    nb_joueurs : int, strat : list(int), pts: list(int), mixte : (True) bool > list(int)
    nb_joeurs : si egale à 0 alors simule un partie entre deux joueurs
    mixte : si egale a True alors on veut changer de stratégie entre les tours
    retourne le nombre de points à la fin de la partie pour les deux joueurs
    """
    t = 1
    while pts[0]<N and pts[1]<N:    #Tant qu'aucun joueur n'a depasse le nombre N de points on continue
        if nb_joueurs>0:
            print("------------------------------------------------------------------------------")
            print("------------------------------------Tour %d------------------------------------"%t)
            print("------------------------------------------------------------------------------")
            print("-----------------------------------Joueur 1-----------------------------------")
        pts[0] = Joueur(nb_joueurs, strat[0], pts, ia = True if nb_joueurs == 0 else False, name = 1) #On calcul le nouveau nombre de points de J1
        if pts[0]>=N:   #Si on depasse le seuil on s'arrete
            break
        if nb_joueurs>1:
            print("-----------------------------------Joueur 2-----------------------------------")
        elif nb_joueurs == 1 :
            print("--------------------------------------IA--------------------------------------")
        #On calcul le nouveau nombre de points de J2, si ia alors nb_jouers = 1%2 = 1 = False
        pts[1] = Joueur(nb_joueurs,strat[1], pts, ia = True if nb_joueurs == 0 else bool(nb_joueurs%2), name = 2)  #On calcul le nouveau nombre de points de J2, si ia alors nb_jouers = 1%2 = 1 = True
        if pts[1]>=N:    #Si on depasse le seuil on s'arrete
            break

        #On demande aux joueurs si ils veulent changer de stratégie ou non

        if nb_joueurs >=1 and mixte == True:
            choix1 = 0
            choix2 = 0
            print("Joueur 1, voulez vous changer de stratégie ?")
            choix1 = int(input("0: Non \t \t 1 : Oui\n"))
            if nb_joueurs == 2:
                print("Joueur 2, voulez vous changer de stratégie ?")
                choix2 = int(input("0: Non \t \t 1 : Oui\n"))
            if choix1 == 1 and choix2 == 1:
                strat[0], strat[1] = choix_strategie(choix1 + choix2)
            elif choix1 == 1:
                strat[0] = choix_strategie(choix1)
            elif choix2==1:
                strat[1] = choix_strategie(choix2, name = 2)
        t+=1
    if nb_joueurs>0:
        if pts[0]>N:
            print("Le joueur 1 a gagné avec %d points"%pts[0])
        else:
            if nb_joueurs == 2:
                print("Le joueur 2 a gagné avec %d points"%pts[1])
            else :
                print("L'I.A a gagné avec %d points"%pts[1])
    return pts


def jeu_simultane(nb_joueurs, strat, pts, mixte = True):
    """
    nb_joueurs : int, strat : list(int), pts: list(int), mixte : (True) bool > int
    nb_joeurs : si egale à 0 alors simule un partie entre deux joueurs
    mixte : si egale a True alors on veut changer de stratégie entre les tours
    retourne qui est le joueur gagnant
    """

    t = 1
    while pts[0]<N and pts[1]<N:    #Tant qu'aucun joueur n'a depasse le nombre N de points on continue
        if nb_joueurs>0:
            print("------------------------------------------------------------------------------")
            print("------------------------------------Tour %d------------------------------------"%t)
            print("------------------------------------------------------------------------------")
            print("-----------------------------------Joueur 1-----------------------------------")
        if(strat[0]<2):
            pts[0] = Joueur(nb_joueurs, strat[0], pts, ia = True if nb_joueurs == 0 else False, name = 1) #On calcul le nouveau nombre de points de J1
        else:
            ptd = choixDPL(VectProb)
            res = simul_des(ptd)
            ptstemp = calcul_points(res)
            pts[0]= ptstemp
            if nb_joueurs !=0:
                print("Resultat du lancer de %d des : "%ptd)
                print(res)
                print("Points obtenus : %d"%ptstemp)
                print("Score actuel : %d"%pts[0])

        if nb_joueurs>1:
            print("-----------------------------------Joueur 2-----------------------------------")
        elif nb_joueurs == 1:
            print("--------------------------------------IA--------------------------------------")
        #pts[1] = Joueur(nb_joueurs, strat[1], pts, ia = True if nb_joueurs == 0 else bool(nb_joueurs%2), name = 2)  #On calcul le nouveau nombre de points de J2, si ia alors nb_jouers = 1%2 = 1 = True
        if(strat[1]<2):
            pts[1] = Joueur(nb_joueurs, strat[1], pts, ia = True if nb_joueurs == 0 else bool(nb_joueurs%2), name = 2) #On calcul le nouveau nombre de points de J1
        else:
            ptd = choixDPL(VectProb)
            res = simul_des(ptd)
            ptstemp = calcul_points(res)
            pts[1]= ptstemp
            if nb_joueurs !=0:
                print("Resultat du lancer de %d des : "%ptd)
                print(res)
                print("Points obtenus : %d"%ptstemp)
                print("Score actuel : %d"%pts[1])

        if pts[1]>=N:    #Si on depasse le seuil on s'arrete
            break
        if pts[0]>=N:   #Si on depasse le seuil on s'arrete
            break
        #On demande aux joueurs si ils veulent changer de stratégie ou non

        if nb_joueurs >=1 and mixte == True:
            choix1 = 0
            choix2 = 0
            """
            print("Joueur 1, voulez vous changer de stratégie ?")
            choix1 = int(input("0: Non \t \t 1 : Oui\n"))
            if nb_joueurs == 2:
                print("Joueur 2, voulez vous changer de stratégie ?")
                choix2 = int(input("0: Non \t \t 1 : Oui\n"))
            if choix1 == 1 and choix2 == 1:
                strat[0], strat[1] = choix_strategie(choix1 + choix2)
            elif choix1 == 1:
                strat[0] = choix_strategie(choix1)
            elif choix2==1:
                strat[1] = choix_strategie(choix2, name = 2)
            """
        t+=1
    joueurGagnant=0
    if pts[0]>pts[1]:
        if nb_joueurs>0:
            print("Le joueur 1 a gagné avec %d points"%pts[0])
        joueurGagnant=1
    elif(pts[1]>pts[0]):
        joueurGagnant=2
        if nb_joueurs>0:
            if nb_joueurs == 2:
                print("Le joueur 2 a gagné avec %d points"%pts[1])
            else :
                print("L'I.A a gagné avec %d points"%pts[1])
    else:
        if nb_joueurs>0:
            print("Egalité ! Avec %d points"%pts[0])
    return joueurGagnant


def esperanceSimultane():
    """
    retourne le tableau des probabilite que J1 gagne et qu'il y ait egalite pour Aveugle et Opti
    """
    Max = 1000
    G1 = np.zeros((2, 2))
    G2 = np.zeros((2, 2))
    for a in range(1,3):
        for b in range(1,3):
            for i in range(Max):
                Pts_1 = 0
                Pts_2 = 0
                strat = [a, b]
                Points = [Pts_1, Pts_2]
                G = jeu_simultane(0, strat, Points)
                if G==1:
                    G1[a-1,b-1]+=1
                if G==0:
                    G2[a-1,b-1]+=1
    return G1/Max,G2/Max

def esperance():
    """
    retourne le tableau des probabilites que J1 gagne selon les stratégies de Strat
    """
    Max = 1000
    Strat_values = list(Strat.values())
    G1 = np.zeros((len(Strat_values), len(Strat_values)))
    for a in range(len(Strat_values)):
        for b in range(0, len(Strat_values)):
            for i in range(Max):
                Pts_1 = 0
                Pts_2 = 0
                strat = [Strat_values[a], Strat_values[b]]
                Points = [Pts_1, Pts_2]
                G = jeu_sequentiel(0, strat, Points)
                if G[0]>=G[1]:
                    G1[Strat_values[a], Strat_values[b]]+=1
    return G1/Max


def experimentale():
    """
    permet de tester et faire varier les N et  D
    """
    global N, D, EG_ij, des_EG_ij, EG1, P_tot, Max, VectProb
    print("- Veuillez choisir le mode de jeu :")
    type_jeu = int(input("0 : Variante sequentielle \t \t 1 : Variante simultanee en un tour\n"))
    while(type_jeu>1 or type_jeu<0):
        print("Choix incorrect, veuillez ré-essayer.")
        type_jeu = int(input("0 : Variante sequentielle \t \t 1 : Variante simultanee\n"))

    if(not type_jeu):
        print("Que voulez vous faire varier ?")
        var = int(input("0 : N \t \t 1 : D\n"))
        while(var>1 or var<0):
            print("Choix incorrect, veuillez ré-essayer.")
            var = int(input("0 : N \t \t 1 : D\n"))

        print("Valeur de N max :")
        N = int(input("  N = "))
        Nmax = N

        print("Valeur de D max :")
        D = int(input("  D = "))
        Dmax = D
    else:
        var=3
        N=1
        print("- Veuillez choisir le nombre de dès : ")
        D = int(input("  D = "))
    print("----------------------------------Chargement---------------------------------\n")
    P_tot = tableau_probaTotale()
    if type_jeu == 0:
        EG_ij, des_EG_ij = EGij_Final()
    elif type_jeu == 1:
        EG1 = EG1()
        VectProb = resolutionPL(EG1)

    E_N = []
    E_D = []
    if var == 0 or var == 2:
        #N = Nmax
        N_ = [n for n in range(1,N+1,10)]
        for n in N_:
            N = n
            E_N.append(esperance())
            print("Probabilité de gagner si N = %d et D = %d"%(N, D))
            print(E_N[-1])
            print("\n")
        E_NM = np.mean(E_N, axis=0)
        print(E_NM)
    elif var == 1 or var == 2:
        D_ = [d for d in range(1, D+1)]
        for d in D_:
            D = d
            E_D.append(esperance())

            print("Probabilité de gagner si N = %d et D = %d"%(N, D))
            print(E_D[-1])
            print("\n")
        E_DM = np.mean(E_D, axis=0)
        print(E_DM)
    elif var==3:
        E_N,E_D=esperanceSimultane()
        print(E_N,"Probabilite pour J1 de gagner\n")
        print(E_D,"Probabilite d'egalite\n")
    return np.array(E_N), np.array(E_D)


# Lancement du jeu en lui même :

def game():
    """
    Fonction qui va lancer le jeu
    """
    global D, N, EG_ij, des_EG_ij, EG1, P_tot, Max, VectProb

    print("Voulez vous lire les règles du jeu ?")
    regles = int(input("0: Non \t \t 1 : Oui\n"))
    if regles == 1:
        print("---------------------------------Règles du Jeu--------------------------------")
        print("En début de partie on choisit : \n - N : le nombre de points maximum. \n - D : le nombre de dès dont on dipose.")
        print("Le but du jeu est d'être le premier à atteindre au moins N points.\n")
        print("A chaque tour on choisit de lancer entre 1 et D dès.")
        print("Si au moins un des dès tombe sur 1 alors on marque 1 point. \nSinon on marque autant de points que la somme des faces des dès lancés.\n")
        print("Dans la variante séquentielle chaque joueur joue à tour de rôle. \nTandis que dans la variant simultanée les deux joueurs jouent en même temps.")
        print("En cas d'égalité sur le nombre de points c'est le joueur qui aura le plus dépassé N qui gagne.")
        print("-------------------------------------FIN--------------------------------------\n")

    print("- Veuillez choisir le mode de jeu :")
    type_jeu = int(input("0 : Variante sequentielle \t \t 1 : Variante simultanee en un tour\n"))
    while(type_jeu>1 or type_jeu<0):
        print("Choix incorrect, veuillez ré-essayer.")
        type_jeu = int(input("0 : Variante sequentielle \t \t 1 : Variante simultanee\n"))

    if(not type_jeu):
        print("- Veuillez choisir le nombre de points maximum : ")
        N = int(input("  N = "))
    else:
        N=1
    print("- Veuillez choisir le nombre de dès : ")
    D = int(input("  D = "))
    print("----------------------------------Chargement---------------------------------\n")
    P_tot = tableau_probaTotale()
    if type_jeu == 0:
        EG_ij, des_EG_ij = EGij_Final()
    elif type_jeu == 1:
        EG1 = EG1()
        VectProb = resolutionPL(EG1)
    if(not type_jeu):
        print("Voulez vous afficher vos probabilités de gagner selon differentes stratégies ? ")
        mode = int(input("0 : Non \t \t 1 : Oui\n"))
        while(mode>1 or mode <0):
            print("Choix incorrect, veuillez ré-essayer.")
            mode = int(input("0 : Non \t \t 1 : Oui\n"))
        if mode ==1:
            G1 = esperance()
            print("Probabilité pour le joueur 1 de gagner selon les stratégies ( [i][j] est la probabilité de gagner de J1 en jouant la stratégie i contre J2 avec la stratégie j) : ")
            print("random : 0, aveugle : 1, optimale : 2, max : 3")
            print(G1)
            print("Souhaitez vous commencer le jeu ?")
            mode = 1 - int(input("0 : Non \t \t 1 : Oui\n"))
        if mode == 0:
            nb_joueurs = int(input("- Veuillez entrer le nombre de joueurs :\n  "))
            #Permet de choisir un bon nombre de joueurs
            while(nb_joueurs>2 or nb_joueurs<1):
                print("Nombre de Joueurs incorrect.")
                nb_joueurs = int(input("- Veuillez entrer le nombre de joueurs :\n  "))

        os.system('cls' if os.name == 'nt' else 'clear')     #permet de clear l'ecran
        if(not type_jeu):
            print("Voulez vous changer de stratégie en cours de jeu ?")
            mixt = int(input("0 : Non \t \t 1 : Oui\n"))
            while(mixt>1 or mixt <0):
                print("Choix incorrect, veuillez ré-essayer.")
                mixt = int(input("0 : Non \t \t 1 : Oui\n"))
        else:
            mixt=0

        strat1, strat2 = choix_strategie(nb_joueurs, debut = True)

        Pts_1 = 0
        Pts_2 = 0
        strat = [strat1, strat2]
        Points = [Pts_1, Pts_2]
        os.system('cls' if os.name == 'nt' else 'clear')     #permet de clear l'ecran
        if type_jeu == 0:
            jeu_sequentiel(nb_joueurs, strat, Points, mixte = bool(mixt))
        elif type_jeu == 1:
            """
            print("- Veuillez choisir le mode de jeu :")
            type_simu = int(input("0 : Jeu en un coup \t \t 1 : Jeu normal.\n"))
            while(type_jeu>1 or type_jeu<0):
                print("Choix incorrect, veuillez ré-essayer.")
            if type_simu == 0:
                N = 1
            """
            jeu_simultane(nb_joueurs, strat, Points, mixte = bool(mixt))


def main():

    global Strat

    Strat = {"random" : 0, "aveugle" : 1, "optimale" : 2, "max" : 3}

    print("Bienvenue dans le jeu de la Bataille des dès V.0.1!")
    print("Que voulez vous faire ?")
    choice = int(input("0 : Evaluation experimentale des stratégies \t \t 1 : Mise en oeuvre du jeu\n"))
    while(choice>1 or choice <0):
        print("Choix incorrect, veuillez ré-essayer.")
        choice = int(input("0 : Evaluation experimentale des stratégies \t \t 1 : Mise en ouvre du jeu "))
    if choice == 0:
        experimentale()
    else:
        game()

if __name__ == "__main__":
    main()
