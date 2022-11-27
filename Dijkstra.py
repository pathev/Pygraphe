from Arete import strp
from tkinter import *

def Moore_Dijkstra(Matrice,depart,arrivee,Noms,latex=False): # Algorithme principal
    n=len(Matrice) # nombre de sommets
    etat=[[False,None,None] for i in range(n)] # [bloque,Noeud precedent,distance]
    actuel=depart
    etat[actuel]=[True,None,0]
    code=""
    tableau=[]
    if latex:
        code="%Nécessite le package ulem\n\\begin{center}\n"
        code+="\\begin{tabular}{|*{"+str(n)+"}{c|}l|}\n"
        code+="\\hline\n"
        for nom in Noms:
            code+=" "+nom+" &"
        code+=" Choix \\\\\n"
        code+="\\hline\n"
        for nom in Noms:
            if nom==Noms[depart]:
                code+=" 0 &"
            else:
                code+=" $\\infty$ &"
        code+=" "+Noms[depart]+"(0) \\\\\n"
        code+="\\hline\n"
    else:
        tableau+=[[[nom] for nom in Noms]+[["Choix"]]]
        tableau+=[[["∞"] for nom in Noms]+[[Noms[depart]+"(0)"]]]
        tableau[-1][depart]=["0"]
    while not etat[arrivee][0]:
        dactuel=etat[actuel][2]
        mini=None
        futuractuel=None
        ligne=[]
        for i in range(n):
            if not etat[i][0]:
                di=etat[i][2]
                d=Matrice[actuel][i]
                if d != None:
                    dnouveau=dactuel+d
                    if di==None or di>dnouveau:
                        di=dnouveau
                        etat[i][1:3]=[actuel,di]
                        if latex:
                            code+=" "+strp(di)+"("+Noms[actuel]+") &"
                        else:
                            ligne+=[[strp(di)+"("+Noms[actuel]+")"]]
                    elif latex:
                        if di==None:
                            code+=" $\\infty$ &"
                        else:
                            code+=" \\sout{"+strp(dnouveau)+"("+Noms[actuel]+")} "+strp(di)+"("+Noms[etat[i][1]]+") &"
                    else:
                        if di==None:
                            ligne+=[["∞"]]
                        else:
                            ligne+=[[strp(dnouveau)+"("+Noms[actuel]+")",strp(di)+"("+Noms[etat[i][1]]+")"]]
                elif latex:
                    if di==None:
                        code+=" $\\infty$ &"
                    else:
                        code+=" "+strp(di)+"("+Noms[etat[i][1]]+") &"
                else:
                    if di==None:
                        ligne+=[["∞"]]
                    else:
                        ligne+=[[strp(di)+"("+Noms[etat[i][1]]+")"]]
                if di != None and (mini == None or di<mini):
                    mini=di
                    futuractuel=i
            elif latex:
                code+=" \\vrule &"
            else:
                ligne+=[["|"]]
        if latex:
            code+=" "+Noms[futuractuel]+"("+strp(mini)+") \\\\\n"
            code+="\\hline\n"
        else:
            ligne+=[[Noms[futuractuel]+"("+strp(mini)+")"]]
            tableau+=[ligne]
        actuel=futuractuel
        etat[actuel][0]=True
    chemin=[Noms[actuel]]
    while actuel!=depart:
        actuel=etat[actuel][1]
        chemin=[Noms[actuel]]+chemin
    strchemin=''
    i=0
    while i<len(chemin)-1:
        strchemin+=chemin[i]+" -> "
        i+=1
    strchemin+=chemin[i]
    if latex:
        code+="\\end{tabular}\n"
        code+="\\end{center}"
    return strchemin,etat[arrivee][2],code,tableau
