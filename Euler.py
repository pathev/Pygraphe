def Cycle(edges_set,depart):

    path =[]

    while edges_set != set():
        if path == []:
            copy=edges_set.copy()
            e=edges_set.pop()
            while not (e[0] == depart or e[1] == depart):
                e=edges_set.pop()
            edges_set=copy
            edges_set.remove(e)
            if e[0] == depart:
                cycle=[e[0],e[1]]
            else:
                cycle=[e[1],e[0]]
        else:
            copy=edges_set.copy()
            e=edges_set.pop()
            while not (e[0] in path or e[1] in path):
                e=edges_set.pop()
            edges_set=copy
            edges_set.remove(e)
            if e[0] in path:
                cycle = [e[0],e[1]]
            else:
                cycle = [e[1],e[0]]
        while cycle[0] != cycle[-1]:
            s=cycle[-1]
            copy=edges_set.copy()
            e=edges_set.pop()
            while not (s == e[0] or s == e[1]):
                e=edges_set.pop()
            if s == e[0]:
                cycle+=[e[1]]
            else:
                cycle+=[e[0]]
            edges_set=copy
            edges_set.remove(e)
        if path == []:
            path=cycle
        else:
            i=path.index(cycle[0])
            path=path[:i]+cycle+path[i+1:]
    
    return path

def Chaine(edges_set,depart,arrivee):

    def find(path,s1,s2):
        i=-1
        for k in range(len(path)-1):
            if path[k]==s1 and path[k+1]==s2:
                i=k
                break
        return i

    if (depart,arrivee) in edges_set:
        edges_set.add((arrivee,depart))
    else:
        edges_set.add((depart,arrivee))
    path = Cycle(edges_set,depart)
    i=find(path,depart,arrivee)
    if i != -1:
        return path[i:0:-1]+path[-1:i:-1]
    else:
        i=find(path,arrivee,depart)+1
        return path[i:]+path[1:i]
