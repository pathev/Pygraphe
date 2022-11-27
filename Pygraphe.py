#! /usr/bin/python3
# -*- coding: utf-8 -*-

#####################################
#                                   #
#         Patrick Thévenon          #
#                                   #
#         de Mars 2014              #
#              à Mars 2015          #
#                                   #
# version : 1.5                     #
#####################################

from tkinter import *
from Model import Model
from Controllers import *

if __name__ == '__main__':

    fen = Tk()
    fen.resizable(width=FALSE, height=FALSE)
    fen.title("Créateur de Graphe")
    model=Model()

    zone_graphe=ControllerGraphe(model,fen)

    frame_outils=Frame(fen,bg='white') # Outils

    radio_outils=[ControllerOutil(model,frame_outils,zone_graphe,text,mode) for text,mode in model.outils]
    lno=range(len(radio_outils))
    for i in lno:
        radio_outils[i].grid(row=0,column=i,sticky='W')
    for i in lno:
        frame_outils.columnconfigure(i,weight=1,uniform="o")

    frame_outils.grid(row=0,column=0,sticky="WE")

    frame_bottom=Frame(fen)

    zone_graphe.grid(row=1,column=0)

    frame_checks=Frame(frame_bottom,bg='white') # Options (dé)sélectionnables

    check_oriente=Checkbutton(frame_checks,text="orienté",variable=model.oriente)
    check_oriente.grid(row=0,column=0)

    frame_checks.grid(row=0,column=0)
    frame_bottom.columnconfigure(0,weight=1)
    frame_bottom.rowconfigure(0,weight=1)

    frame_buttons=Frame(frame_bottom) # Boutons

    bouton_Dijkstra=ControllerLanceDijkstra(model,fen,frame_buttons,zone_graphe)
    bouton_Dijkstra.grid(row=0,column=0)

    bouton_Euler=ControllerEuler(model,fen,frame_buttons,zone_graphe)
    bouton_Euler.grid(row=0,column=1)

    bouton_tikz=ControllerTikz(model,fen,frame_buttons,zone_graphe)
    bouton_tikz.grid(row=0,column=2)

    bouton_efface=ControllerEfface(model,fen,frame_buttons,zone_graphe)
    bouton_efface.grid(row=1,column=0)

    bouton_charge=ControllerCharge(model,fen,frame_buttons,zone_graphe)
    bouton_charge.grid(row=1,column=1)

    bouton_sauve=ControllerSauve(model,fen,frame_buttons,zone_graphe)
    bouton_sauve.grid(row=1,column=2)

    bouton_quitte=Button(frame_buttons,text="Quitter",command=fen.destroy,activebackground='red')
    bouton_quitte.grid(row=0,column=3,rowspan=2)

    for i in range(4):
        frame_buttons.columnconfigure(i,weight=1,uniform="o")
    frame_buttons.grid(row=0,column=1)

    frame_bottom.grid(row=2,column=0)
    frame_bottom.columnconfigure(0,weight=1,uniform="o")
    frame_bottom.columnconfigure(1,weight=4,uniform="o")

    fen.columnconfigure(0,weight=1)

    model.oriente.trace("w",lambda *e:UpdateOriente(model,bouton_Euler))

    fen.mainloop()
