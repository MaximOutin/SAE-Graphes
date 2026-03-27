import numpy as np
import math
import re
import collections



########################################
# Classe GrapheValue
########################################
class GrapheValueNonOriente:
    """
    Classe qui représente des graphes valués non orientés.
    Les graphes valués sont représentés par leur matrice de valuation.
    Les sommets sont numérotés de 0 à n-1 (n étant le nombre de sommets).
    On peut également indiquer les noms des sommets du graphe, définis dans un dictionnaire.
    """
    
    def __init__(self, mat=[], noms=None):
        """
        Constructeur d'un graphe valué, à partir de sa matrice de valuation et des noms des sommets.
        Paramètres :
            mat : matrice de valuation du graphe.
            noms : dictionnaire qui associe son nom à chaque numéro de sommet.
        """
        self.matrice = mat
        if noms is None:
            self.noms_sommets = {x: x for x in range(len(self.matrice))}
        else:
            self.noms_sommets = noms
    
 

    def __str__(self):
        """
        Représentation du graphe valué, par une chaîne de caractères.
        Retour :
            chaîne de caractères contenant les noms des sommets et les valeurs de la matrice 
            de valuation du graphe.
        """
        res_str = "Noms des sommets :\n" + str(self.noms_sommets) + "\n"
        res_str = "Matrice de valuation du graphe :\n" + str(self.matrice) + "\n"
        return res_str
    
    
    def ecrit_dans_fichier_dot(self, nom_fichier:str):
        """
        Écrit le graphe dans un fichier au format DOT.
        Paramètres :
            nom_fichier (str) : nom du fichier DOT dans lequel écrire le graphe.
        """
        with open(nom_fichier, 'w') as f:
            print(nom_fichier)
            f.write("graph G {\n")

            for i in range(self.nb_sommets()):
                f.write(f'  {i} [label="{self.noms_sommets[i]}"];\n')
            f.write("\n")
            
            for i in range(self.nb_sommets()):
                for j in range(i, self.nb_sommets()):
                    print(i, " -- ", j)
                    if self.matrice[i, j] != math.inf:  # math.inf signifie absence d'arête
                        f.write(f'  {i} -- {j} [label="{self.matrice[i, j]}"];\n')
        
            f.write("}\n")

    
    def nb_sommets(self):
        """
        Calcule le nombre de sommets du graphe.
        Retour : 
            nombre de sommets du graphe.
        """
        return len(self.matrice)
    
    
    def nb_aretes(self):
        """
        Calcul le nombre d'arêtes du graphe.
        Retour : 
            nombre d'arêtes du graphe.
        """
        return ((self.nb_sommets())**2 - collections.Counter(self.matrice.flatten())[math.inf]) // 2
    
    
    def degre_sommet(self, s:int):
        """
        Calul du degré du sommet d'indice donné.
        Paramètres :
            s : indice du sommet considéré.
        Retour : 
            degré du sommet s.
        """
        return self.nb_sommets() - collections.Counter(self.matrice[s,:])[math.inf]


    def degres_sommets(self):
        """
        Calcul de la liste des degrés des sommets du graphe.
        Retour : 
            liste des degrés des sommets du graphe.
        """
        return [self.degre_sommet(i) for i in range(self.nb_sommets())]

    
    
    def construit_sous_graphe_induit(self, ens_sommets: set):
        """
    Construction du sous-graphe induit, à partir de l'ensemble de sommets donné.
    Paramètres :
        ens_sommets : ensemble de sommets à partir duquel construire le sous-graphe.
        """
        indices = sorted(list(ens_sommets))
        nouvellematrice = self.matrice[indices][:, indices]
        nouveauxnoms = {}
        for nouveaunum, anciennum in enumerate(indices):
            nomdusommet = self.noms_sommets[anciennum]
            nouveauxnoms[nouveaunum] = nomdusommet
        return GrapheValueNonOriente(nouvellematrice, nouveauxnoms)


    def calcule_cc(self):
        """
        Calcul des composantes connexes, retournées sous la forme d'une liste
        d'ensembles de numéros de sommets (chaque sous-ensemble correspond à une
        composante connexe).
        Retour:
            liste des ensembles de sommets correspondant à des composantes connexes.
        """
        sommetutilise = set()
        cc = []
        for sommet in range(self.nb_sommets()):
            if sommet not in sommetutilise:
                composanteconnexe=set()
                stack=[sommet]
                sommetutilise.add(sommet)

                while stack: #Tant qu'il reste des sommets non visité on boucle
                    scourrant=stack.pop()
                    composanteconnexe.add(scourrant)

                    for voisin,valeur in enumerate(self.matrice[scourrant]):
                        if valeur != math.inf and voisin not in sommetutilise:
                            sommetutilise.add(voisin)
                            stack.append(voisin)
                cc.append(composanteconnexe)
        return cc
        
    
    def est_connexe(self):
        """
        Test de la connexité du graphe courant.
        Retour : 
            vrai si le graphe est connexe ; faux sinon.
        """
        # calcul des composantes connexes du graphes
        cc = self.calcule_cc()
        
        # graphe connexe si une seule composante connexe
        return len(cc) == 1
    
        
    def plus_grosse_cc(self):
        """
        Calcule les composantes connexes du graphe et retourne le sous-graphe 
        correspondant à la plus grosse d'entre elles (en termes de nombre de sommets).
        Retour :
            le sous-graphe correspondant à la plus grosse composante connexe 
            (la numérotation des sommets n'est plus la même que dans le graphe de départ).
        """
        # calcul des composantes connexes
        ccs = self.calcule_cc()
        
        # sélection de l'ensemble le plus grand
        cc_grande = None
        for cc in ccs:
            len_cc_cour = len(cc)
            if cc_grande == None or len(cc_grande) < len_cc_cour:
                cc_grande = cc
            
        # construction du sous-graphe induit correspondant
        return self.construit_sous_graphe_induit(cc)



# Fonction principale

if __name__ == "__main__":
    test = np.full([3], math.inf)
    print(test, "\n")
    
    m = np.full([3,3], math.inf)
    g = GrapheValueNonOriente(m)
    print("Graphe g:\n", g)
    
    m2 = np.array([[math.inf, 3, 2.5, 8],
                   [3,math.inf,math.inf,7],
                   [2.5,math.inf,math.inf,1.5],
                   [8,7,1.5,math.inf],
                  ])
    g2 = GrapheValueNonOriente(m2, {0:"Teddy", 1:"Lisa", 2:"Mohamed", 3:"Levi"})
    print("\nSous graphe induit")
    selection = {0, 2}  # 0 = Teddy et 2 = Mohamed
    sous_graphe = g2.construit_sous_graphe_induit(selection)

    print("Nouveau dictionnaire de noms :", sous_graphe.noms_sommets)
    print("Matrice induite :\n", sous_graphe.matrice)
    print(f"Poids entre Teddy et Mohamed : {sous_graphe.matrice[0][1]}") #Dist = 2.5
    print("\nGraphe non connexe")
    # 0-1 sont liés, 2-3 sont liés, mais aucune liaison entre les deux groupes
    m3 = np.array([
        [math.inf, 5, math.inf, math.inf],
        [5, math.inf, math.inf, math.inf],
        [math.inf, math.inf, math.inf, 10],
        [math.inf, math.inf, 10, math.inf]
    ])
    g3 = GrapheValueNonOriente(m3, {0: "A", 1: "B", 2: "C", 3: "D"})

    ccs = g3.calcule_cc()
    print(f"Composantes connexes trouvées : {ccs}")
    print(f"Est connexe ? {g3.est_connexe()}")  #False
