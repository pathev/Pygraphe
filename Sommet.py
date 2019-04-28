from tkinter import *
from myToplevel import MyToplevel

defcolor="burlywood1"
selcolor="azure"
actcolor="yellow"
actselcolor="aquamarine3"
delcolor="red"

class Sommet:

    def __init__(self,model,fen,canvas,x,y,nom=None):
        self.model=model
        self.fen=fen
        self.canvas=canvas
        self.nom=nom
        self.x=x
        self.y=y
        self.r=12

        self.rep=canvas.create_oval(self.x-self.r,self.y-self.r,
                           self.x+self.r,self.y+self.r,
                           fill=defcolor,activefill=actcolor)

        self.text=canvas.create_text(self.x,self.y,state=DISABLED)

        self.popup=None
        if self.nom is None:
            self.ask_nom()
        else:
            self.model.ajoute_sommet(self)
            self.canvas.itemconfigure(self.text,text=self.nom)
            self.canvas.itemconfigure(self.rep,tags=(self.nom))

    def set_coords(self,x,y):
        self.x=x
        self.y=y

    def ask_nom(self):
        if self.popup is None:
            self.popup=MyToplevel(master=self.fen,width=200,height=20,bg="white")
            self.popup.pack_propagate(0)
            self.popup.resizable(width=FALSE,height=FALSE)
            self.popup.title("Nom du sommet")

            self.entry_nom=Entry(self.popup,width=3)
            if not self.nom is None:
                self.entry_nom.delete(0,END)
                self.entry_nom.insert(0,self.nom)
                self.entry_nom.bind("<Escape>",lambda e:self.set_nom(self.nom))
                self.popup.protocol('WM_DELETE_WINDOW',lambda :self.set_nom(self.nom))
            else:
                self.entry_nom.bind("<Escape>",lambda e:self.cancel())
                self.popup.protocol('WM_DELETE_WINDOW',lambda :self.cancel())
            self.entry_nom.pack()
            self.entry_nom.focus()
            self.label_erreur=Label(self.popup,text="Nom incorrect",fg="red",bg="white")
        else:
            self.entry_nom.delete(0,END)
            self.entry_nom.insert(0,self.nom)
            self.entry_nom.bind("<Escape>",lambda e:self.set_nom(self.nom))
            self.popup.protocol('WM_DELETE_WINDOW',lambda :self.set_nom(self.nom))
            self.popup.deiconify()
            self.entry_nom.focus()

        self.entry_nom.bind("<Return>",lambda e:self.set_nom(self.entry_nom.get()))
        self.entry_nom.bind("<KP_Enter>",lambda e:self.set_nom(self.entry_nom.get()))

    def set_nom(self,nom):
        if not (nom=="" or self.model.existe_sommet(nom[:3])):
            if self.nom is None:
                self.model.ajoute_sommet(self)
            self.nom=nom[:3]
            self.canvas.itemconfigure(self.text,text=self.nom)
            if 'current' in self.canvas.gettags(self.rep):
                self.canvas.itemconfigure(self.rep,tags=(self.nom,'current'))
            else:
                self.canvas.itemconfigure(self.rep,tags=(self.nom))
            self.model.CallUpdates()
            if not self.popup is None:
                self.label_erreur.pack_forget()
                self.popup.pack_propagate(0)
                self.popup.withdraw()
        elif nom==self.nom:
            self.label_erreur.pack_forget()
            self.popup.pack_propagate(0)
            self.popup.withdraw()
        else:            
            self.label_erreur.pack()
            self.popup.pack_propagate(1)

    def cancel(self):
        self.Clear()
        self.popup.withdraw()

    def sel(self):
        self.canvas.itemconfigure(self.rep,fill=selcolor,activefill=actselcolor)

    def desel(self):
        self.canvas.itemconfigure(self.rep,fill=defcolor,activefill=actcolor)

    def set_deletecolor(self):
        self.canvas.itemconfigure(self.rep,activefill=delcolor)

    def set_defaultcolor(self):
        self.canvas.itemconfigure(self.rep,activefill=actcolor)

    def update(self):
        self.canvas.coords(self.rep,
                           self.x-self.r,self.y-self.r,
                           self.x+self.r,self.y+self.r)
        self.canvas.coords(self.text,self.x,self.y)

    def Clear(self):
        self.canvas.delete(self.rep)
        self.canvas.delete(self.text)
