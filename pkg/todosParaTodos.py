from aEstrela import astar


def todosParaTodos(maze, vitimas, base):
    estados = [base]
    estados.append(vitimas)
    caminhos = [len(estados)][len(estados)]
    
    for i in range(len(estados)):
        for j in range(i+1, len(estados)):
            caminhos[i][j] = astar(maze, estados[i], estados[j])
            caminhos[j][i] = astar(maze, estados[j], estados[i])