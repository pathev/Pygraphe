class Graphe:

    def __init__(self,n,M=None,S=None,o=0):
        self.ordre=n
        self.oriente=o
        if M is None:
            self.matrice=[[None for i in range(self.ordre)] for j in range(self.ordre)]
        else:
            self.matrice=M
        if S is None:
            self.sommet=[None for i in range(self.ordre)]
        else:
            self.sommet=S

    def __str__(self):
      text="Ordre du graphe : "+str(self.ordre)+"\n"
      text+="Matrice :\n["
      for i in range(self.ordre):
          text+=str(self.matrice[i])
          if i<self.ordre-1:
              text+=",\n "
          else:
              text+="]\n"
      text+="Nom des sommets :\n"+str(self.sommet)
      return text

    def get_matrice(self):
        return self.matrice

    def get_sommet(self):
        return self.sommet

    def noms_sommets(self):
        return str(self.sommet)

    def nomme_sommet(self,i,nom): # donne un nom à un sommet
        self.sommet[i]=nom

    def indice_sommet(self,nom): # cherche l’indice correspondant à un sommet
        i=0
        n=self.ordre
        while i<n and self.sommet[i] != nom:
           i+=1
        if i==n:
            raise ValueError("Le nom '"+nom+"' n’apparaît pas dans la liste des sommets")
        else:
            return i

    def existe_nom(self,nom): # Vérifie l’existence d’un sommet de nom donné
        try:
            i=self.indice_sommet(nom)
            return True
        except ValueError:
            return False

    def creer_arete_indices(self,i1,i2,poids): # Fonction interne
        self.matrice[i1][i2]=poids
        if not (self.oriente==1):
            self.matrice[i2][i1]=poids

    def creer_arete_noms(self,nom1,nom2,poids): # Fonction appelée de l’extérieur
        i1=self.indice_sommet(nom1)
        i2=self.indice_sommet(nom2)
        self.creer_arete_indices(i1,i2,poids)

    def enlever_arete_indices(self,i1,i2): # Fonction interne
        self.matrice[i1][i2]=None
        if not (self.oriente==1):
            self.matrice[i2][i1]=None

    def enlever_arete_noms(self,nom1,nom2): # Fonction appelée de l’extérieur
        i1=self.indice_sommet(nom1)
        i2=self.indice_sommet(nom2)
        self.enlever_arete_indices(i1,i2)
