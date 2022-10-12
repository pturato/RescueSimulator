import sys
from aEstrela import astar
#import numpy as np

def todosParaTodos(maze, vitimas, base):
    #print("base: ", base," vitimas: ", vitimas)
    #estados = [([base]),[0]]
    #print("base !!!!!!!!!!!!!!!!!!!!!!!! ",base, type(base))
    #sys.exit()
    estados=[]
    #base=(0,0) #MUDAR AQUI!!!!!!!!!!!!!!
    for i in range(len(vitimas)-1):
        estados.append(vitimas[i])
    #print("estados: ",estados)
    #caminhos = np.zeros((len(estados),len(estados)), dtype=int)
    #caminhos = [len(estados)][len(estados)]
    caminhos = [ [0 for i in range(len(estados))] for j in range(len(estados))]
    #print(caminhos)
    #base
    for j in range(1, len(estados)):
        #print("ANTES de ", base, " até ", estados[j][0]," caminho ",caminhos[0][j])
        caminhos[0][j] = astar(maze, base, estados[j][0])
        #print("de ", base, " até ", estados[j][0]," caminho ",caminhos[0][j])
    for i in range(1, len(estados)): #começa a partir da primeira linha
        #for i in range(len(estados)-1): FUNCIONANDO
        #for j in range(i+1, len(estados)):
        for j in range(i+1, len(estados)): #os iguais vão continuar zero
            # if(estados[i] == estados[j]):
            #      caminhos[i][j] = 0
            # else:
            #print("de ", estados[i][0], " até j = ",j," result", estados[j][0])
            #print("caminho ", caminhos[i][j])
            caminhos[i][j] = astar(maze, estados[i][0], estados[j][0])
            #caminhos[j][i] = astar(maze, estados[j], estados[i])
    for i in range(len(estados)-1, 0, -1): 
        for j in range(i-1, 0, -1):
        #for j in range(i-1, len(estados)-1):
            caminhos[i][j] = astar(maze, estados[i][0], estados[j][0])
    #volta para a base (coluna 0)
    for j in range(1, len(estados)):
        #print("ANTES de ", estados[j][0], " até ", base)
        caminhos[j][0] = astar(maze, estados[j][0], base)
        #print("caminho dele",caminhos[0][j])
            
    #print("caminhos: ", caminhos) OK
    return caminhos #matriz com caminhos de i até j