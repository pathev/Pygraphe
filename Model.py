from tkinter import *
from Graphe import Graphe

class Model:

    def __init__(self):
        self.sommets = []
        self.aretes = []
        self.outils= [("Création","create"),
                     ("Édition","edit"),
                     ("Déplacement","move"),
                     ("Suppression","del")]
        self.outil=StringVar()
        self.outil.set("create")
        self.oriente=IntVar()

    def existe_sommet(self,nom):
        i=0
        trouve=False
        while i<len(self.sommets) and not trouve:
            trouve=self.sommets[i].nom==nom
            i+=1        
        return trouve

    def get_sommet(self,nom):
        i=0
        trouve=False
        while i<len(self.sommets) and not trouve:
            trouve=self.sommets[i].nom==nom
            i+=1        
        if trouve:
            return self.sommets[i-1]
        else:
            return None

    def ajoute_sommet(self,sommet):
        self.sommets+=[sommet]

    def existe_arete(self,s1,s2,o=False): # s1 et s2 sont les noms
        i=0
        trouve=False
        B=not(o or self.oriente.get()==1)
        while i<len(self.aretes) and not trouve:
            trouve=(self.aretes[i].s1.nom==s1 and self.aretes[i].s2.nom==s2) or (B and self.aretes[i].s1.nom==s2 and self.aretes[i].s2.nom==s1)
            i+=1
        return trouve

    def get_arete(self,s1,s2): # s1 et s2 sont les noms
        i=0
        trouve=False
        while i<len(self.aretes) and not trouve:
            trouve=(self.aretes[i].s1.nom==s1 and self.aretes[i].s2.nom==s2) or (self.oriente.get()!=1 and self.aretes[i].s1.nom==s2 and self.aretes[i].s2.nom==s1)
            i+=1        
        if trouve:
            return self.aretes[i-1]
        else:
            return None

    def get_all_aretes(self,s):
        l=[]
        for i in range(len(self.aretes)):
            if self.aretes[i].s1.nom==s or self.aretes[i].s2.nom==s:
                l+=[self.aretes[i]]
        return l

    def degre_sommet(self,s):
        d=0
        for i in range(len(self.aretes)):
            nom1=self.aretes[i].s1.nom
            nom2=self.aretes[i].s2.nom
            if (nom1==s or nom2==s) and (not self.existe_arete(nom2,nom1,o=True) or nom1<nom2): # hors doublon
                d+=1
        return d

    def degre_impair(self):
        return [s.nom for s in self.sommets if self.degre_sommet(s.nom)%2 == 1]

    def get_edges_set(self): # hors doublons

        ens=set()
        for a in self.aretes:
            c=(a.s1.nom,a.s2.nom)
            if (c[1],c[0]) not in set(): 
                ens=ens.union({c})
        return ens

    def ajoute_arete(self,arete):
        self.aretes+=[arete]

    def creation_graphe(self):

        n=len(self.sommets)
        S=[self.sommets[i].nom for i in range(n)]
        S.sort()
        G=Graphe(n,S=S,o=self.oriente.get())
        for a in self.aretes:
            G.creer_arete_noms(a.s1.nom,a.s2.nom,a.poids)
        return G

    def get_dict(self):

        dic = {}
        n=len(self.sommets)
        dic['S']=[[s.nom, s.x, s.y] for s in self.sommets]
        dic['A']=[[a.s1.nom,a.s2.nom,a.poids,a.p] for a in self.aretes]
        dic['o']=self.oriente.get()

        return dic

    def Clear(self):

        for s in self.sommets:
            s.Clear()
        self.sommets=[]

        for a in self.aretes:
            a.Clear()
        self.aretes=[]

    def CallUpdates(self):
        for s in self.sommets:
            s.update()
        for a in self.aretes:
            a.update()
