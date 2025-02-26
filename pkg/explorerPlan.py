from random import randint
from state import State

class ExplorerPlan:

    ACTIONS = ["N", "S", "L", "O", "NE", "NO", "SE", "SO"]

    MOVIMENTS = {
        "N" : (-1, 0),
        "S" : (1, 0),
        "L" : (0, 1),
        "O" : (0, -1),
        "NE" : (-1, 1),
        "NO" : (-1, -1),
        "SE" : (1, 1),
        "SO" : (1, -1),
        "NONE": (0, 0)
    }

    ANTI_ACTIONS = {
        "N" : "S",
        "S" : "N",
        "L" : "O",
        "O" : "L", 
        "NE" : "SO",
        "NO" : "SE",
        "SE" : "NO",
        "SO" : "NE"
    }

    INVALID_ACTIONS = {
        "N": [
            ("O", "NE"),
            ("L", "NO"),
            ("NO", "L"),
            ("NE", "O"),
            ("NONE", "NE"),
            ("NONE", "NO")
        ],

        "S": [
            ("O", "SE"),
            ("L", "SO"),
            ("SO", "L"),
            ("SE", "O"),
            ("NONE", "SE"),
            ("NONE", "SO")
        ],

        "L": [
            ("N", "SE"),
            ("S", "NE"),
            ("NE", "S"),
            ("SE", "N"),
            ("NONE", "NE"),
            ("NONE", "SE")
        ],

        "O": [
            ("N", "SO"),
            ("S", "NO"),
            ("NO", "S"),
            ("SO", "N"),
            ("NONE", "NO"),
            ("NONE", "SO")
        ],

        "NE": [("N", "L"), ("L", "N")],
        "NO": [("N", "O"), ("O", "N")],
        "SE": [("S", "L"), ("L", "S")],
        "SO": [("O", "S"), ("S", "O")]
    }



    def __init__(self, maxRows, maxColumns, goal, initialState, name = "none", mesh = "square"):
        """
        Define as variaveis necessárias para a utilização do explorer plan por um unico agente.
        """
        self.walls = []
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.initialState = initialState
        self.currentState = initialState
        self.goalPos = goal
        self.actions = []
        self.pushback = []
        self.pushback_flag = True

        """
        Inicializa as matrizes de ações possíveis e de pushback
        """
        for row in range(self.maxRows):
            possible_actions = []
            pushback_actions = []
            for column in range(self.maxColumns):
                possible_actions.append(self.ACTIONS.copy())
                pushback_actions.append([])
            self.actions.append(possible_actions)
            self.pushback.append(pushback_actions)
        #print(self.actions, len(self.actions))        

    def setWalls(self, walls):
        # row = 0
        # col = 0
        # for i in walls:
        #     col = 0
        #     for j in i:
        #         if j == 1:
        #             self.walls.append((row, col))
        #         col += 1
        #     row += 1
        pass
       
        
    def updateCurrentState(self, state):
         self.currentState = state

    def isPossibleToMove(self, toState):
        """Verifica se eh possivel ir da posicao atual para o estado (lin, col) considerando 
        a posicao das paredes do labirinto e movimentos na diagonal
        @param toState: instancia da classe State - um par (lin, col) - que aqui indica a posicao futura 
        @return: True quando é possivel ir do estado atual para o estado futuro """

        return True
        ## vai para fora do labirinto
        if (toState.col < 0 or toState.row < 0):
            return False

        if (toState.col >= self.maxColumns or toState.row >= self.maxRows):
            return False
        
        if len(self.walls) == 0:
            return True
        
        ## vai para cima de uma parede
        if (toState.row, toState.col) in self.walls:
            return False

        # vai na diagonal? Caso sim, nao pode ter paredes acima & dir. ou acima & esq. ou abaixo & dir. ou abaixo & esq.
        delta_row = toState.row - self.currentState.row
        delta_col = toState.col - self.currentState.col

        ## o movimento eh na diagonal
        if (delta_row !=0 and delta_col != 0):
            if (self.currentState.row + delta_row, self.currentState.col) in self.walls and (self.currentState.row, self.currentState.col + delta_col) in self.walls:
                return False
        
        return True

    # Mudar função para escolher a próxima posição com DFS 
    def getNextPosition(self):
         """ Sorteia uma direcao e calcula a posicao futura do agente 
         @return: tupla contendo a acao (direcao) e o estado futuro resultante da movimentacao """
         print(self.actions[self.currentState.row][self.currentState.col])
         print(self.pushback[self.currentState.row][self.currentState.col])
         if len(self.actions[self.currentState.row][self.currentState.col]) > 0:
            self.pushback_flag = True
            movDirection = self.actions[self.currentState.row][self.currentState.col].pop(0)
         else:
            self.pushback_flag = False
            movDirection = self.pushback[self.currentState.row][self.currentState.col].pop(-1)
         state = State(self.currentState.row + self.MOVIMENTS[movDirection][0], self.currentState.col + self.MOVIMENTS[movDirection][1])

         return movDirection, state

    def chooseAction(self):
        """ Escolhe o proximo movimento de forma aleatoria. 
        Eh a acao que vai ser executada pelo agente. 
        @return: tupla contendo a acao (direcao) e uma instância da classe State que representa a posição esperada após a execução
        """

        ## Tenta encontrar um movimento possivel dentro do tabuleiro 
        result = self.getNextPosition()

        while not self.isPossibleToMove(result[1]):
            result = self.getNextPosition()

        return result
        
    def run_valid_action(self, previousAction):
        if previousAction == "nop":
            return
        if self.pushback_flag == True:
            self.pushback[self.currentState.row][self.currentState.col].append(self.ANTI_ACTIONS[previousAction])

        if self.ANTI_ACTIONS[previousAction] in self.actions[self.currentState.row][self.currentState.col]:
            self.actions[self.currentState.row][self.currentState.col].remove(self.ANTI_ACTIONS[previousAction])
        for action in self.ACTIONS:
            row = self.currentState.row + self.MOVIMENTS[action][0]
            col = self.currentState.col + self.MOVIMENTS[action][1]
            if row >= 0 and col >= 0 and row < self.maxRows and col < self.maxColumns and self.ANTI_ACTIONS[action] in self.actions[row][col]:
                self.actions[row][col].remove(self.ANTI_ACTIONS[action])

    ## TO DO
    def run_invalid_action(self, previousAction):
        if previousAction == "nop":
            return
        for relatedActions, actionToRemove in self.INVALID_ACTIONS[previousAction]:
            row = self.currentState.row + self.MOVIMENTS[relatedActions][0]
            col = self.currentState.col + self.MOVIMENTS[relatedActions][1]
            if row > 0 and col > 0 and row < self.maxRows and  col < self.maxColumns:
                if actionToRemove in self.actions[row][col]:
                    self.actions[row][col].remove(actionToRemove)

    def do(self):
        """
        Método utilizado para o polimorfismo dos planos

        Retorna o movimento e o estado do plano (False = nao concluido, True = Concluido)
        """
        
        nextMove = self.move()
        return (nextMove[1], self.goalPos == State(nextMove[0][0], nextMove[0][1]))   
    
     


        
       
        
        
