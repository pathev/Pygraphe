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
        code+="\\begin{tabular}{|*{"+str(n)+"}{c|}}\n"
        code+="\\hline\n"
        for nom in Noms:
            code+=" "+nom+" &"
        code=code[:-1]+" \\\\\n"
        code+="\\hline\n"
        for nom in Noms:
            if nom==Noms[depart]:
                code+=" 0 &"
            else:
                code+=" $\\infty$ &"
        code=code[:-1]+" \\\\\n"
        code+="\\hline\n"
    else:
        tableau+=[[[nom] for nom in Noms]]
        tableau+=[[["∞"] for nom in Noms]]
        tableau[-1][depart]=["0"]
    while not etat[arrivee][0]:
        dactuel=etat[actuel][2]
        min=None
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
                if di != None and (min == None or di<min):
                    min=di
                    futuractuel=i
            elif latex:
                code+=" | &"
            else:
                ligne+=[["|"]]
        if latex:
            code=code[:-1]+" \\\\\n"
            code+="\\hline\n"
        else:
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
