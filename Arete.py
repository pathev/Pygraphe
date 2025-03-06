from tkinter import *
from myToplevel import MyToplevel

delcolor="red"
defcolor={'fleche':"gray",'poids':"black"}
actcolor="orange"

def strp(poids): # chaîne de caractère pour un float qui peut être entier
    if type(poids) == int:
        return str(poids)
    elif poids.is_integer():
        return str(poids)[:-2]
    else:
        return str(poids).replace('.',',')

def dxy(x1,y1,x2,y2,r):
    (xv,yv)=(x2-x1,y2-y1)
    n=(xv**2+yv**2)**(1/2)
    q=r/n
    return (xv*q,yv*q)

class Arete:

    def __init__(self,model,fen,canvas,s1,s2,poids=None,p=0.5):
        self.model=model
        self.fen=fen
        self.canvas=canvas
        self.s1=s1
        self.s2=s2
        self.poids=poids
        self.p=round(p,2)
        (x1,y1)=(self.s1.x,self.s1.y)
        (x2,y2)=(self.s2.x,self.s2.y)
        r=self.s1.r
        (dx,dy)=dxy(x1,y1,x2,y2,r)
        self.rep=canvas.create_line(x1+dx,y1+dy,x2-dx,y2-dy,
                                    fill=defcolor['fleche'],
                                    activefill=actcolor)
        if self.model.oriente.get():
            self.canvas.itemconfigure(self.rep,arrow="last")
        else:
            self.canvas.itemconfigure(self.rep,arrow="none")
        self.canvas.tag_lower(self.rep)

        self.text=canvas.create_text(self.p*x2+(1-self.p)*x1,
                                     self.p*y2+(1-self.p)*y1,
                                     fill=defcolor['poids'],
                                     activefill=actcolor)
        self.popup=None
        if poids is None:
            if self.model.pondere.get():
                self.ask_poids()
            else:
                self.poids = 1.
                self.model.ajoute_arete(self)
                self.canvas.itemconfigure(self.text,state='hidden')
                self.canvas.itemconfigure(self.text,text=strp(self.poids))
        else:
            if self.model.pondere.get():
                self.canvas.itemconfigure(self.text,state='hidden')
            self.model.ajoute_arete(self)
            self.canvas.itemconfigure(self.text,text=strp(self.poids))
            self.canvas.itemconfigure(self.rep,tags=(self.s1.nom,self.s2.nom))
            

    def ask_poids(self):
        if self.popup is None:
            self.popup=MyToplevel(master=self.fen,width=200,height=20,bg="white")
            self.popup.pack_propagate(0)
            self.popup.resizable(width=FALSE,height=FALSE)
            self.popup.title("Poids de l’arête")

            self.entry_poids=Entry(self.popup,width=3)
            if not self.poids is None:
                self.entry_poids.delete(0,END)
                self.entry_poids.insert(0,strp(self.poids))
                self.entry_poids.bind("<Escape>",lambda e:self.set_poids(str(self.poids)))
                self.popup.protocol('WM_DELETE_WINDOW',lambda :self.set_poids(str(self.poids)))
            else:
                self.entry_poids.bind("<Escape>",lambda e:self.cancel())
                self.popup.protocol('WM_DELETE_WINDOW',lambda :self.cancel())
            self.entry_poids.pack()
            self.entry_poids.focus()

            self.label_erreur=Label(self.popup,text="Poids incorrect",fg="red",bg="white")
        else:
            self.entry_poids.delete(0,END)
            self.entry_poids.insert(0,strp(self.poids))
            self.entry_poids.bind("<Escape>",lambda e:self.set_poids(str(self.poids)))
            self.popup.protocol('WM_DELETE_WINDOW',lambda :self.set_poids(str(self.poids)))
            self.popup.deiconify()
            self.entry_poids.focus()

        self.entry_poids.bind("<Return>",lambda e:self.set_poids(self.entry_poids.get()))
        self.entry_poids.bind("<KP_Enter>",lambda e:self.set_poids(self.entry_poids.get()))

    def set_poids(self,poids):
        poids=poids.replace(',','.')
        if poids.replace('.','').isnumeric():
            if self.poids is None:
                self.model.ajoute_arete(self)
            self.poids=float(poids)
            self.canvas.itemconfigure(self.text,text=strp(self.poids))
            self.canvas.itemconfigure(self.rep,tags=(self.s1.nom,self.s2.nom))
            if not self.popup is None:
                self.label_erreur.pack_forget()
                self.popup.pack_propagate(0)
                self.popup.withdraw()
        else:
            self.label_erreur.pack()
            self.popup.pack_propagate(1)

    def set_p(self,x,y):

        v_arete=[self.s2.x-self.s1.x,self.s2.y-self.s1.y]
        v=[x-self.s1.x,y-self.s1.y]
        p=v_arete[0]*v[0]+v_arete[1]*v[1]
        l=(v_arete[0]**2+v_arete[1]**2)**(1/2)
        self.p=round(max(0,min(1,p/(l**2))),2)
        self.update() # pas très propre

    def cancel(self):
        self.Clear()
        self.popup.withdraw()

    def set_deletecolor(self):
        self.canvas.itemconfigure(self.rep,activefill=delcolor)
        self.canvas.itemconfigure(self.text,activefill=defcolor['poids'])
        self.canvas.itemconfigure(self.text,tags=())
        self.canvas.itemconfigure(self.rep,tags=(self.s1.nom,self.s2.nom))
        self.canvas.tag_bind(self.rep,"<Enter>",self.highlight)
        self.canvas.tag_bind(self.rep,"<Leave>",self.delight)

    def set_defaultcolor(self):
        self.canvas.itemconfigure(self.rep,activefill=defcolor['fleche'])
        self.canvas.itemconfigure(self.text,activefill=actcolor)
        self.canvas.itemconfigure(self.text,tags=(self.s1.nom,self.s2.nom))
        self.canvas.itemconfigure(self.rep,tags=())
        self.canvas.tag_unbind(self.rep,"<Enter>")
        self.canvas.tag_unbind(self.rep,"<Leave>")

    def highlight(self,evt):
        self.canvas.itemconfigure(self.rep,width=4)

    def delight(self,evt):
        self.canvas.itemconfigure(self.rep,width=1)

    def update(self):

        (x1,y1)=(self.s1.x,self.s1.y)
        (x2,y2)=(self.s2.x,self.s2.y)
        r=self.s1.r
        (dx,dy)=dxy(x1,y1,x2,y2,r)
        self.canvas.coords(self.text,
                           self.p*x2+(1-self.p)*x1,
                           self.p*y2+(1-self.p)*y1)
        self.canvas.coords(self.rep,x1+dx,y1+dy,x2-dx,y2-dy)
        if self.model.pondere.get():
            self.canvas.itemconfigure(self.text,state='normal')
        else:
            self.canvas.itemconfigure(self.text,state='hidden')
        if self.model.oriente.get():
            self.canvas.itemconfigure(self.rep,arrow="last")
        else:
            self.canvas.itemconfigure(self.rep,arrow="none")

    def Clear(self):
        self.canvas.delete(self.rep)
        self.canvas.delete(self.text)
