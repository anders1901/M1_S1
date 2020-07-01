# -*- coding: utf-8 -*-
#CALLE VIERA Andersson
#3521501

"""

Dictionnaires décrivants les transposés et symétries de relations,
ainsi que les listes de relations obtenues avec les compositions de base
dans le tableau donné en TD

"""

# transpose : dict[str:str]
transpose = {
    '<':'>',
    '>':'<',
    'e':'et',
    's':'st',
    'et':'e',
    'st':'s',
    'd':'dt',
    'm':'mt',
    'dt':'d',
    'mt':'m',
    'o':'ot',
    'ot':'o',
    '=':'='
    }

# symetrie : dict[str:str]
symetrie = {
    '<':'>',
    '>':'<',
    'e':'s',
    's':'e',
    'et':'st',
    'st':'et',
    'd':'d',
    'm':'mt',
    'dt':'dt',
    'mt':'m',
    'o':'ot',
    'ot':'o',
    '=':'='
    }

# compositionBase : dict[tuple[str,str]:set[str]]
compositionBase = {
        ('<','<'):{'<'},
        ('<','m'):{'<'},
        ('<','o'):{'<'},
        ('<','et'):{'<'},
        ('<','s'):{'<'},
        ('<','d'):{'<','m','o','s','d'},
        ('<','dt'):{'<'},
        ('<','e'):{'<','m','o','s','d'},
        ('<','st'):{'<'},
        ('<','ot'):{'<','m','o','s','d'},
        ('<','mt'):{'<','m','o','s','d'},
        ('<','>'):{'<','>','m','mt','o','ot','e','et','s','st','d','dt','='},
        ('m','m'):{'<'},
        ('m','o'):{'<'},
        ('m','et'):{'<'},
        ('m','s'):{'m'},
        ('m','d'):{'o','s','d'},
        ('m','dt'):{'<'},
        ('m','e'):{'o','s','d'},
        ('m','st'):{'m'},
        ('m','ot'):{'o','s','d'},
        ('m','mt'):{'e','et','='},
        ('o','o'):{'<','m','o'},
        ('o','et'):{'<','m','o'},
        ('o','s'):{'o'},
        ('o','d'):{'o','s','d'},
        ('o','dt'):{'<','m','o','et','dt'},
        ('o','e'):{'o','s','d'},
        ('o','st'):{'o','et','dt'},
        ('o','ot'):{'o','ot','e','et','d','dt','st','s','='},
        ('s','et'):{'<','m','o'},
        ('s','s'):{'s'},
        ('s','d'):{'d'},
        ('s','dt'):{'<','m','o','et','dt'},
        ('s','e'):{'d'},
        ('s','st'):{'s','st','='},
        ('et','s'):{'o'},
        ('et','d'):{'o','s','d'},
        ('et','dt'):{'dt'},
        ('et','e'):{'e','et','='},
        ('d','d'):{'d'},
        ('d','dt'):{'<','>','m','mt','o','ot','e','et','s','st','d','dt','='},
        ('dt','d'):{'o','ot','e','et','d','dt','st','s','='}
        }

#Exercice 1 :
#Question 2 :
def transposeSet(S):
    St = set()
    for s in S:
        St.add(transpose[s])
    return St

def symetrieSet(S):
    Ss = set()
    for s in S:
        Ss.add(symetrie[s])
    return Ss

#Question 3 :
def compose(r1, r2):
    """
    r1, r2 : str -> set(str)
    """
    if r1 == '=': #si = aucun changement
        return {r2}
    elif r2 == '=':
        return {r1}

    if (r1,r2) in compositionBase.keys(): #clef dans la base de composition
        return compositionBase[(r1, r2)]
    elif (transpose[r2],transpose[r1]) in compositionBase.keys(): #première formule
        return transposeSet(compositionBase[(transpose[r2],transpose[r1])])
    elif (symetrie[r1],symetrie[r2]) in compositionBase.keys(): #seconde formule
        return symetrieSet(compositionBase[(symetrie[r1],symetrie[r2])])
    else: #dernière formules si les autres fonctionnent pas
         return symetrieSet(transposeSet(compositionBase[(transpose[symetrie[r2]],transpose[symetrie[r1]])]))
#TESTS
print(compose("=", "d") == {"d"})
print(compose("m", "d") == {"d", "o", "s"})
print(compose("ot", ">") == {">"})
print(compose(">", "e") == {">"})
print(compose("ot", "m") == {"dt", "et", "o"})

#Question 4 :
def compositionSet(S1, S2):
    Comp = set()
    for s1 in S1:
        for s2 in S2:
            Comp|=compose(s1, s2)
    return Comp
#TESTS
#S1 = {"=", "m", "ot"}
#S2 = {"d", ">", "m"}
#print(compositionSet(S1, S2))


#Exercice 2 :
#Question 1 :
class Graphe:
    def __init__(self, nodes, rel):
        self.noeuds = nodes    #Noeuds du graphe
        self.relations = rel     #Relations du Graphe

    def getRelations(self, i, j):
        #print("self.relations.keys()", self.relations.keys())
        if (i,j) in self.relations.keys():
            return self.relations[(i,j)]
        elif (j,i) in self.relations.keys():
            return transposeSet(self.relations[(j,i)])
        else:
            return set()

    def setRelations(self, i, j, R): #met a jour la relation i j dans le graphe
        if (i,j) in self.relations.keys():
            self.relations[(i,j)] = R
            if (j, i) in self.relations.keys():
                self.relations[(j,i)]=R
        else:
            if (j,i) in self.relations.keys():
                self.relations[(j,i)]=R
            else:
                self.relations[(i,j)]=R

    def getNode(self):#retourne la liste des noeuds
        return self.noeuds

    def addNode(self,N): #ajoute un noeud au graphe
        self.noeuds.add(N)

#Question 2 :
def propagation(G, i, j):
    rel = G.getRelations(i, j)
    Pile = [(i, j, rel)]


    while len(Pile) > 0:

        S = Pile.pop(0)
        i = S[0]
        j = S[1]
        rel = S[2]

        for k in G.noeuds:
            if k != i and k != j:
                r_ik = G.getRelations(i, k)
                r_kj = G.getRelations(k, j)
                new_ik = r_ik & compositionSet(rel, G.getRelations(j,k) )
                new_kj = r_kj & compositionSet(G.getRelations(k,i), rel)
                if len(new_ik) == 0 or len(new_kj) == 0:
                    break
                if new_ik != r_ik:     #ik<=new_ik and len(ak)==len(new_ak):
                    G.setRelations(i, k, new_ik)
                    Pile.append((i, k, new_ik))
                if new_kj != r_kj:     #kj<=new_kj and len(kb)==len(new_kb):
                    G.setRelations(k, j, new_kj)
                    Pile.append((k, j, new_kj))

#Question 3 :
def ajouter(G, relation):
    N = list(relation.keys())[0]
    #print("N", N)
    nodes = G.getNode()
    for item in N:
        if item not in nodes:
            G.addNode(item)

    #print("G.getRelations(N[0],N[1])", type(G.getRelations(N[0],N[1])))
    G.setRelations(N[0], N[1], G.getRelations(N[0],N[1]) ^ relation[N])
    propagation(G, N[0], N[1])

#Question 4 :
G1 = Graphe( {'A','B','C'}, { ('A','B') : {'<'}, ('A','C') : {'>'} } )
print("Graphe 1")
print(G1.relations)
ajouter(G1, { ('B','C') : {'='} })
print(G1.relations)


G2 = Graphe( {'A','B','C'}, { ('A','B') : {'<'}, ('A','C') : {'<'} } )
print("Graphe 2")
print(G2.relations)
ajouter(G2, { ('B','C') : {'='} })
print(G2.relations)

#Question 5 :

#On crée le graphe
G_q5 = Graphe(set(),dict())
#On va ajouter les sommets et relations
ajouter( G_q5, { ('L','S') : {'ot','mt'} } )
ajouter( G_q5, { ('S','R') : {'<','m','mt','>'} } )
print(G_q5.relations )
#ajouter( G_q5, { ('L','R') : {'o','dt', ">"} } )
ajouter( G_q5, { ('L','R') :{'o','dt', '>', 'm', 'et', '=', 'st', 's'}})
print(G_q5.relations )
