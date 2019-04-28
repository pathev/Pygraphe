from tkinter import *
import importlib
import imp

from myToplevel import MyToplevel

from Arete import Arete,strp
from Sommet import Sommet
from Dijkstra import Moore_Dijkstra
from Euler import Cycle, Chaine

class ControllerOutil(Radiobutton):

    def __init__(self,model,fen,canvas,text,mode):
        self.model=model
        self.canvas=canvas
        Radiobutton.__init__(self,fen,text=text,bg='white',
                             borderwidth=2,relief="flat",highlightthickness=0,width=12,anchor='w',
                             variable=self.model.outil,value=mode,command=self.canvas.colors_change)

class ControllerGraphe(Canvas):

    def __init__(self,model,fen):
        Canvas.__init__(self,fen,width=500,height=500,bg='white',bd=4,relief="groove")
        self.model=model
        self.fen=fen
        self.bind("<Button-1>",self.utilise_outil)
        self.choix1=None
        self.choix2=None

    def utilise_outil(self,evt):
        outil=self.model.outil.get()
        if outil=="create":
            if not self.find_withtag(CURRENT):
                if self.choix1 is None:
                    Sommet(self.model,self.fen,self,evt.x,evt.y)
                else:
                    self.choix1.desel()
                    self.choix1=None
            elif self.find_withtag(CURRENT) and len(self.gettags(CURRENT))==2:
                if self.choix1 is None:
                    self.choix1=self.model.get_sommet(self.gettags(CURRENT)[0])
                    self.choix1.sel()
                else:
                    self.choix2=self.model.get_sommet(self.gettags(CURRENT)[0])
                    if self.choix1 != self.choix2 and not self.model.existe_arete(self.choix1.nom,self.choix2.nom):
                        Arete(self.model,self.fen,self,self.choix1,self.choix2)
                    self.choix1.desel()
                    self.choix1=None
                    self.choix2=None
        elif outil=="edit":
            if self.find_withtag(CURRENT) and len(self.gettags(CURRENT))==2:
                self.model.get_sommet(self.gettags(CURRENT)[0]).ask_nom()
            elif self.find_withtag(CURRENT) and len(self.gettags(CURRENT))==3:
                self.model.get_arete(self.gettags(CURRENT)[0],self.gettags(CURRENT)[1]).ask_poids()
        elif outil=="move":
            if self.find_withtag(CURRENT) and len(self.gettags(CURRENT))==2:
                self.bind("<Motion>",self.bouge_sommet)
                self.bind("<ButtonRelease-1>",self.stop_bouge)
            elif self.find_withtag(CURRENT) and len(self.gettags(CURRENT))==3:
                self.current_a=[self.gettags(CURRENT)[0],self.gettags(CURRENT)[1]]
                self.bind("<Motion>",self.bouge_arete)
                self.bind("<ButtonRelease-1>",self.stop_bouge)
        elif outil=="del":
            if self.find_withtag(CURRENT) and len(self.gettags(CURRENT))==2:
                s=self.model.get_sommet(self.gettags(CURRENT)[0])
                self.del_sommet(s)
            elif self.find_withtag(CURRENT) and len(self.gettags(CURRENT))==3:
                a=self.model.get_arete(self.gettags(CURRENT)[0],self.gettags(CURRENT)[1])
                self.del_arete(a)

    def colors_change(self):
        if not self.choix1 is None:
            self.choix1.desel()
            self.choix1=None
            self.choix2=None
        if self.model.outil.get()=="del":
            for s in self.model.sommets:
                s.set_deletecolor()
            for a in self.model.aretes:
                a.set_deletecolor()
        else:
            for s in self.model.sommets:
                s.set_defaultcolor()
            for a in self.model.aretes:
                a.set_defaultcolor()

    def bouge_sommet(self,evt):
        self.model.get_sommet(self.gettags(CURRENT)[0]).set_coords(evt.x,evt.y)
        self.model.CallUpdates()

    def bouge_arete(self,evt):
        self.model.get_arete(self.current_a[0],self.current_a[1]).set_p(evt.x,evt.y)

    def stop_bouge(self,evt):
        self.curent_a=None
        self.unbind("<Motion>")
        self.unbind("<ButtonRelease-1>")

    def del_arete(self,a):
        self.model.aretes.remove(a)
        a.Clear()

    def del_sommet(self,s):
        nom=s.nom
        self.model.sommets.remove(s)
        s.Clear()
        for a in self.model.get_all_aretes(nom):
            self.del_arete(a)

class ControllerLanceDijkstra(Button):

    def __init__(self,model,fen,widget,canvas):
        Button.__init__(self,widget,text="Dijkstra",command=self.config,width=9)
        self.model=model
        self.fen=fen
        self.canvas=canvas
        self.depart=None
        self.arrivee=None
        self.popup=None
        self.latex=IntVar()
        self.results=None

    def config(self):

        G=self.model.creation_graphe()
        if self.popup is None:
            self.popup=MyToplevel(master=self.fen,width=179,height=88,bg="white")
            self.popup.protocol('WM_DELETE_WINDOW',lambda :self.popup.withdraw())
            self.popup.pack_propagate(0)
            self.popup.resizable(width=FALSE,height=FALSE)
            self.popup.title("Configuration")

            self.label_depart=Label(self.popup,text="Sommet de départ :",bg="white")
            self.label_depart.grid(row=0,column=0)

            self.entry_depart=Entry(self.popup,width=4)
            self.entry_depart.grid(row=0,column=1)
            self.entry_depart.focus()

            self.depart_erreur=Label(self.popup,text="Nom incorrect",fg="red",bg="white")

            self.label_arrivee=Label(self.popup,text="Sommet d’arrivée :",bg="white")
            self.label_arrivee.grid(row=2,column=0)

            self.entry_arrivee=Entry(self.popup,width=4)
            self.entry_arrivee.grid(row=2,column=1)
            self.entry_arrivee.bind("<Return>",lambda e:self.lance())
            self.entry_arrivee.bind("<KP_Enter>",lambda e:self.lance())

            self.arrivee_erreur=Label(self.popup,text="Nom incorrect",fg="red",bg="white")

            self.check_latex=Checkbutton(self.popup,text="Code LaTeX",variable=self.latex,bg="white")
            self.check_latex.grid(row=4,column=0,columnspan=2)

            self.button_annul=Button(self.popup,text="Annuler",command=self.popup.withdraw)
            self.button_annul.grid(row=5,column=0)
            self.button_annul.bind("<Return>",lambda e:self.popup.withdraw())
            self.button_annul.bind("<KP_Enter>",lambda e:self.popup.withdraw())

            self.button_go=Button(self.popup,text="Go !",command=self.lance)
            self.button_go.grid(row=5,column=1)
            self.button_go.bind("<Return>",lambda e:self.lance())
            self.button_go.bind("<KP_Enter>",lambda e:self.lance())

            self.popup.bind("<Escape>",lambda e:self.popup.withdraw())
        else:
            self.popup.deiconify()
            self.entry_depart.focus()

    def lance(self):
        G=self.model.creation_graphe()
        nom1=self.entry_depart.get()
        nom2=self.entry_arrivee.get()
        if not self.model.existe_sommet(nom1):
            self.depart_erreur.grid(row=1,column=0,columnspan=2)
        else:
            self.depart_erreur.grid_forget()
        if not self.model.existe_sommet(nom2):
            self.arrivee_erreur.grid(row=3,column=0,columnspan=2)
        else:
            self.arrivee_erreur.grid_forget()
        if self.model.existe_sommet(nom1) and self.model.existe_sommet(nom2):
            if self.latex.get()==1:
                latexBool=True
            else:
                latexBool=False
            try:
                chemin,poids,code,tableau=Moore_Dijkstra(G.get_matrice(),
                                                 G.indice_sommet(nom1),
                                                 G.indice_sommet(nom2),
                                                 G.get_sommet(),
                                                 latex=latexBool)
                self.popup.withdraw()
                self.print_results(chemin,poids,code,tableau)
            except:
                self.popup.withdraw()

    def print_results(self,chemin,poids,code,tableau):

        if self.results==None:
            self.results=MyToplevel(master=self.fen,width=624,height=250,bg="white")
            self.results.protocol('WM_DELETE_WINDOW',lambda :self.results.withdraw())
            self.results.title("Résultats")

            self.label_chemin=Label(self.results,text="Chemin :",bg="white")
            self.label_chemin.grid(row=0,column=0)

            self.text_chemin=Text(self.results,height=1)
            self.text_chemin.insert(END,chemin)
            self.text_chemin.grid(row=0,column=1)

            self.label_poids=Label(self.results,text="Poids :",bg="white")
            self.label_poids.grid(row=1,column=0)

            self.text_poids=Text(self.results,height=1)
            
            self.text_poids.insert(END,strp(poids))
            self.text_poids.grid(row=1,column=1)

            self.label_code=Label(self.results,text="Code LaTeX :",bg="white")
            self.text_code=Text(self.results)
            self.text_code.insert(END,code)

            self.frame_tableau=Frame(self.results,bg="white")
            for i in range(len(tableau)):
                for j in range(len(tableau[i])):
                    if len(tableau[i][j])==1:
                        Label(self.frame_tableau,text=tableau[i][j][0],bd=1,relief="ridge",bg="white",font="Arial 10").grid(row=i,column=j,sticky='EW')
                    else:
                        double=Frame(self.frame_tableau,bg="white",bd=1,relief="ridge")
                        Label(double,text=tableau[i][j][0],bd=0,bg="white",font="Arial 10 overstrike").grid(row=0,column=0,sticky='E')
                        Label(double,text=tableau[i][j][1],bd=0,bg="white",font="Arial 10").grid(row=0,column=1,sticky='W')
                        double.grid(row=i,column=j,sticky='EW')
                        double.grid_columnconfigure(0, weight=1, uniform="o")
                        double.grid_columnconfigure(1, weight=1, uniform="o")
            if len(tableau)>0:
                for j in range(len(tableau[0])):
                    self.frame_tableau.grid_columnconfigure(j, weight=1, uniform="o")

            if self.latex.get()==1:
                self.label_code.grid(row=2,column=0)
                self.text_code.grid(row=2,column=1)
            else:
                self.frame_tableau.grid(row=2,column=0,columnspan=2,sticky='EW')
                self.fen.update()

            self.button_close=Button(self.results,text="Fermer",command=self.results.withdraw)
            self.button_close.grid(row=3,column=0,columnspan=2)

            self.results.bind("<Escape>",lambda e:self.results.withdraw())
        else:
            self.text_chemin.delete(1.0,END)
            self.text_chemin.insert(END,chemin)

            self.text_poids.delete(1.0,END)
            self.text_poids.insert(END,strp(poids))

            self.text_code.delete(1.0,END)
            self.text_code.insert(END,code)

            if self.latex.get()==1:
                self.frame_tableau.grid_forget()
                self.label_code.grid(row=2,column=0)
                self.text_code.grid(row=2,column=1)
            else:
                self.label_code.grid_forget()
                self.text_code.grid_forget()
                self.frame_tableau.grid_forget()
                self.frame_tableau.destroy()
                self.frame_tableau=Frame(self.results,bg="white")

                for i in range(len(tableau)):
                    for j in range(len(tableau[i])):
                        if len(tableau[i][j])==1:
                            Label(self.frame_tableau,text=tableau[i][j][0],bd=1,relief="ridge",bg="white",font="Arial 10").grid(row=i,column=j,sticky='EW')
                        else:
                            double=Frame(self.frame_tableau,bg="white",bd=1,relief="ridge")
                            Label(double,text=tableau[i][j][0],bd=0,bg="white",font="Arial 10 overstrike").grid(row=0,column=0,sticky='E')
                            Label(double,text=tableau[i][j][1],bd=0,bg="white",font="Arial 10").grid(row=0,column=1,sticky='W')
                            double.grid(row=i,column=j,sticky='EW')
                            double.grid_columnconfigure(0, weight=1, uniform="o")
                            double.grid_columnconfigure(1, weight=1, uniform="o")
                if len(tableau)>0:
                    for j in range(len(tableau[0])):
                        self.frame_tableau.grid_columnconfigure(j, weight=1, uniform="o")
                self.frame_tableau.grid(row=2,column=0,columnspan=2,sticky='EW')

            self.results.deiconify()

class ControllerEfface(Button):

    def __init__(self,model,fen,widget,canvas):
        Button.__init__(self,widget,text="Effacer",command=self.config,width=9)
        self.model=model
        self.fen=fen
        self.canvas=canvas
        self.popup=None

    def config(self):

        if self.popup==None:
            self.popup=MyToplevel(master=self.fen,width=100,height=46,bg="white")
            self.popup.protocol('WM_DELETE_WINDOW',lambda :self.popup.withdraw())
            self.popup.pack_propagate(0)
            self.popup.resizable(width=FALSE,height=FALSE)
            self.popup.title("Effacement")

            self.label_nom=Label(self.popup,text="Êtes-vous sûr ?",bg="white")
            self.label_nom.grid(row=0,column=0,columnspan=2)

            self.button_annul=Button(self.popup,text="Non",command=self.popup.withdraw)
            self.button_annul.grid(row=1,column=0)
            self.button_annul.bind("<Return>",lambda e:self.popup.withdraw())
            self.button_annul.bind("<KP_Enter>",lambda e:self.popup.withdraw())

            self.button_go=Button(self.popup,text="Oui",command=self.efface)
            self.button_go.grid(row=1,column=1)
            self.button_go.bind("<Return>",lambda e:self.efface())
            self.button_go.bind("<KP_Enter>",lambda e:self.efface())

            self.popup.bind("<Escape>",lambda e:self.popup.withdraw())
        else:
            self.popup.deiconify()

    def efface(self):
        self.model.Clear()
        self.popup.withdraw()

class ControllerCharge(Button):

    def __init__(self,model,fen,widget,canvas,state=NORMAL):
        Button.__init__(self,widget,text="Charger",command=self.config,width=9,state=state)
        self.model=model
        self.fen=fen
        self.canvas=canvas
        self.popup=None

    def config(self):

        if self.popup==None:
            self.popup=MyToplevel(master=self.fen,width=266,height=48,bg="white")
            self.popup.protocol('WM_DELETE_WINDOW',lambda :self.popup.withdraw())
            self.popup.pack_propagate(0)
            self.popup.resizable(width=FALSE,height=FALSE)
            self.popup.title("Chargement")

            self.label_nom=Label(self.popup,text="Nom de fichier :",bg="white")
            self.label_nom.grid(row=0,column=0)

            self.entry_nom=Entry(self.popup)
            self.entry_nom.grid(row=0,column=1)
            self.entry_nom.focus()
            self.entry_nom.bind("<Return>",lambda e:self.charge())
            self.entry_nom.bind("<KP_Enter>",lambda e:self.charge())

            self.button_annul=Button(self.popup,text="Annuler",command=self.popup.withdraw)
            self.button_annul.grid(row=2,column=0)
            self.button_annul.bind("<Return>",lambda e:self.popup.withdraw())
            self.button_annul.bind("<KP_Enter>",lambda e:self.popup.withdraw())

            self.button_go=Button(self.popup,text="Charger",command=self.charge)
            self.button_go.grid(row=2,column=1)
            self.button_go.bind("<Return>",lambda e:self.charge())
            self.button_go.bind("<KP_Enter>",lambda e:self.charge())

            self.label_erreur=Label(self.popup,text="Erreur de chargement",fg="red",bg="white")

            self.popup.bind("<Escape>",lambda e:self.popup.withdraw())
        else:
            self.label_erreur.grid_forget()
            self.popup.deiconify()

    def charge(self):
        try:
            mod = importlib.import_module("Save."+self.entry_nom.get())
            mod = imp.reload(mod) # pour permettre le rechargement en cas de modification
            self.model.Clear()
            for nom,x,y in mod.S:
                Sommet(self.model,self.fen,self.canvas,x,y,nom=nom)
            for s1,s2,poids,p in mod.A:
                Arete(self.model,self.fen,self.canvas,
                      s1=self.model.get_sommet(s1),
                      s2=self.model.get_sommet(s2),
                      poids=float(poids),p=p)
            self.model.oriente.set(mod.o)
            self.popup.withdraw()
            self.canvas.colors_change()
        except:
            self.label_erreur.grid(row=1,column=0,columnspan=2)

class ControllerSauve(Button):

    def __init__(self,model,fen,widget,canvas,state=NORMAL):
        Button.__init__(self,widget,text="Sauver",command=self.config,width=9,state=state)
        self.model=model
        self.fen=fen
        self.canvas=canvas
        self.popup=None
        self.overwrite=IntVar()

    def config(self):

        if self.popup==None:
            self.popup=MyToplevel(master=self.fen,width=266,height=48,bg="white")
            self.popup.protocol('WM_DELETE_WINDOW',lambda :self.popup.withdraw())
            self.popup.pack_propagate(0)
            self.popup.resizable(width=FALSE,height=FALSE)
            self.popup.title("Sauvegarde")

            self.label_nom=Label(self.popup,text="Nom de fichier :",bg="white")
            self.label_nom.grid(row=0,column=0)

            self.entry_nom=Entry(self.popup)
            self.entry_nom.grid(row=0,column=1)
            self.entry_nom.focus()
            self.entry_nom.bind("<Return>",lambda e:self.sauve())
            self.entry_nom.bind("<KP_Enter>",lambda e:self.sauve())

            self.label_existe=Label(self.popup,text="Le fichier existe déjà",fg="red",bg="white")

            self.check_overwrite=Checkbutton(self.popup,text="Écraser",variable=self.overwrite)

            self.button_annul=Button(self.popup,text="Annuler",command=self.popup.withdraw)
            self.button_annul.grid(row=2,column=0)
            self.button_annul.bind("<Return>",lambda e:self.popup.withdraw())
            self.button_annul.bind("<KP_Enter>",lambda e:self.popup.withdraw())

            self.button_go=Button(self.popup,text="Sauver",command=self.sauve)
            self.button_go.grid(row=2,column=1)
            self.button_go.bind("<Return>",lambda e:self.sauve())
            self.button_go.bind("<KP_Enter>",lambda e:self.sauve())

            self.popup.bind("<Escape>",lambda e:self.popup.withdraw())
        else:
            self.popup.deiconify()

    def sauve(self):
        code=self.model.Sauve_code()
        nomfichier="Save/"+self.entry_nom.get()+".py"
        try:
          with open(nomfichier):
            if self.overwrite.get()==1:
              self.label_existe.grid_forget()
              self.check_overwrite.grid_forget()
              Go=True
              self.overwrite.set(0)
            else:
              self.label_existe.grid(row=1,column=0)
              self.check_overwrite.grid(row=1,column=1)
              Go=False
        except OSError:
            Go=True
        if Go:
            fichier=open(nomfichier,mode='w',encoding='utf-8')
            fichier.write(code)
            self.popup.withdraw()

class ControllerTikz(Button):

    def __init__(self,model,fen,widget,canvas):
        Button.__init__(self,widget,text="Tikz",command=self.lance,width=9)
        self.model=model
        self.fen=fen
        self.canvas=canvas
        self.results=None
        self.code=None

    def lance(self):

        code="% Nécessite le package tikz\n"
        code+="\\begin{center}\n"
        code+="\\begin{tikzpicture}[scale=18/500,%\n"
        if self.model.oriente.get()==1:
            code+="                    f/.style={->,very thick,>=stealth\'},%\n"
            fleche="[f] "
        else:
            fleche=" "
        code+="                    s/.style={draw,circle},%\n"
        code+="                    p/.style={fill=white,inner sep=2pt}]\n"

        S,A=self.model.Sauve_lists()

        for nom,x,y in S:
            code+="\\node[s] ("+nom+") at ("+str(x)+","+str(500-y)+") {"+nom+"} ;\n"

        for s1,s2,poids,p in A:
            code+="\\draw"+fleche+"("+s1+") -- ("+s2+") node[pos="+str(p)+",p]{$"+strp(poids)+"$} ;\n"

        code+="\\end{tikzpicture}\n"
        code+="\\end{center}"

        self.code=code

        self.print_results()

    def print_results(self):

        if self.results==None:
            self.results=MyToplevel(master=self.fen,width=648,height=370,bg="white")
            self.results.protocol('WM_DELETE_WINDOW',lambda :self.results.withdraw())
            self.results.title("Code Tikz du graphe")

            self.label_code=Label(self.results,text="Code LaTeX :",bg="white")
            self.text_code=Text(self.results)
            self.text_code.insert(END,self.code)
            self.label_code.grid(row=0,column=0)
            self.text_code.grid(row=0,column=1)

            self.button_close=Button(self.results,text="Fermer",command=self.results.withdraw)
            self.button_close.grid(row=1,column=0,columnspan=2)

            self.results.bind("<Escape>",lambda e:self.results.withdraw())
        else:
            self.text_code.delete(1.0,END)
            self.text_code.insert(END,self.code)

            self.results.deiconify()

class ControllerEuler(Button):

    def __init__(self,model,fen,widget,canvas):
        Button.__init__(self,widget,text="Euler",command=self.lance,width=9)
        self.model=model
        self.fen=fen
        self.canvas=canvas
        self.popup=None
        self.result=None
        self.path=None
        self.kind=None

    def elegant_path(self,path):
        elegant = ""
        for c in path:
            elegant+=c+" -> "
        return elegant[:-4]


    def lance(self):

        impair = self.model.degre_impair()

        nb_impair = len(impair)

        if not nb_impair in [0,2]:
            self.result = "Aucun cycle eulérien, aucune chaîne eulérienne"
            self.path = ""
            self.kind = None
        else:
            edges_set=self.model.get_edges_set()
            if nb_impair == 0:
                if edges_set != set():
                    self.result = "Si le graphe est connexe, un cycle eulérien"
                    try:
                        self.path = self.elegant_path(Cycle(edges_set,self.model.sommets[0].nom))
                        # pas propre (l’utilisation des données du modèle)
                        self.kind = "Cycle :"
                    except:
                        self.path = "Aucun cycle eulérien trouvé"
                        self.kind = "Erreur :"
                else:
                    self.result = "Le graphe est vide"
                    self.path = ""
                    self.kind = None
            else: # nb_impair == 2
                self.result = "Si le graphe est connexe, une chaîne eulérienne"
                try:
                    self.path = self.elegant_path(Chaine(edges_set,impair[0],impair[1]))
                    self.kind = "Chaîne :"
                except:
                    self.path = "Aucune chaîne eulérienne trouvée"
                    self.kind = "Erreur :"

        self.print_results()


    def print_results(self):

        if self.popup==None:
            self.popup=MyToplevel(master=self.fen,width=601,height=68,bg="white")
            self.popup.protocol('WM_DELETE_WINDOW',lambda :self.popup.withdraw())
            self.popup.title("Cycle ou chaîne d’Euler")

            self.label_result=Label(self.popup,text="Info :",bg="white")
            self.text_result=Text(self.popup,height=1)
            self.text_result.insert(END,self.result)
            self.label_result.grid(row=0,column=0)
            self.text_result.grid(row=0,column=1)

            self.label_path=Label(self.popup,text=self.kind,bg="white")
            self.text_path=Text(self.popup,height=1)
            self.text_path.insert(END,self.path)
            self.label_path.grid(row=1,column=0)
            self.text_path.grid(row=1,column=1)

            self.button_close=Button(self.popup,text="Fermer",command=self.popup.withdraw)
            self.button_close.grid(row=2,column=0,columnspan=2)

            self.popup.bind("<Escape>",lambda e:self.popup.withdraw())
        else:
            self.text_result.delete(1.0,END)
            self.text_result.insert(END,self.result)
            self.text_path.delete(1.0,END)
            self.text_path.insert(END,self.path)
            self.label_path.configure(text=self.kind)

            self.popup.deiconify()

def UpdateOriente(model,bouton_Euler):

    if model.oriente.get()==1:
        bouton_Euler.config(state=DISABLED)
    else:
        bouton_Euler.config(state=NORMAL)
    model.CallUpdates()
