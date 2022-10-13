import sys
import os
import time

## Importa as classes que serao usadas
sys.path.append(os.path.join("pkg"))
from model import Model
from agentExplorer import AgentExplorer
from agentSalvador import AgentSalvador
from config import Config


## Metodo utilizado para permitir que o usuario construa o labirindo clicando em cima
def buildMaze(model):
    model.drawToBuild()
    step = model.getStep()
    while step == "build":
        model.drawToBuild()
        step = model.getStep()
    ## Atualiza o labirinto
    model.updateMaze()

def main():
    # Cria dicionario com as configuracoes do ambiente
    configDict = Config("config_data/ambiente.txt", "config_data/sinais_vitais_com_label.txt")

    # Cria o ambiente (modelo) = Labirinto com suas paredes
    mesh = "square"

    ## nome do arquivo de configuracao do ambiente - deve estar na pasta <proj>/config_data
    loadMaze = "ambiente"

    model = Model(configDict.ambiente, mesh, loadMaze)
    buildMaze(model)

    model.maze.board.posAgent
    #model.maze.board.posGoal
    # Define a posição inicial do agente no ambiente - corresponde ao estado inicial
    #model.setAgentPos(model.maze.board.posAgent[0],model.maze.board.posAgent[1])
    model.setAgentPos(configDict.ambiente["Base"][0],configDict.ambiente["Base"][1])
    #model.setGoalPos(model.maze.board.posGoal[0],model.maze.board.posGoal[1])  
    model.draw()

    # Cria um agente
    agent = AgentExplorer(model,configDict.ambiente)

    ## Ciclo de raciocínio do agente
    agent.deliberate()
    while agent.deliberate() != -1:
        model.draw()
        time.sleep(0.01) # para dar tempo de visualizar as movimentacoes do agente no labirinto
    model.draw()    

    vitimas = agent.vitimasEncontradas()
    maze = agent.mazeExplorado()

    # Cria um agente salvador
    agentSalvador = AgentSalvador(model,configDict.ambiente, vitimas, maze) 

    ## Ciclo de raciocínio do agente
    agentSalvador.deliberate()
    while agentSalvador.deliberate() != -1:
        model.draw()
        time.sleep(0.01) # para dar tempo de visualizar as movimentacoes do agente no labirinto
    model.draw()    
        
if __name__ == '__main__':
    main()
