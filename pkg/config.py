import sys
import os
import time

class Config:
    def __init__(self, ambientePath, sinaisVitaisPath):
        self.ambientePath = ambientePath
        self.sinaisVitaisPath = sinaisVitaisPath
        self.ambiente = {}
        self.sinaisVitais = []
        self.loadAmbiente()
        self.loadSinaisVitais()

    def loadAmbiente(self):
        arq = open(self.ambientePath,"r") 
        for line in arq:
            ## O formato de cada linha é: var valor
            ## As variáveis são 
            ## Base: posição inicial do agente
            ## Te e Ts: tempo limite para vasculhar e tempo para salvar
            ## XMax e YMax: definem o tamanho do labirinto
            ## Vitimas: posição das vítimas no labirinto
            ## Paredes: posição das paredes no labirinto
            values = line.split(" ")
            if values[0] == "Base":
                x, y = values[1].split(",")
                self.ambiente[values[0]] = [int(x), int(y)]
            elif values[0] == "Te" or values[0] == "Ts" or values[0] == "XMax" or values[0] == "YMax":
                self.ambiente[values[0]] = int(values[1])
            elif values[0] == "Vitimas" or values[0] == "Parede":
                value = []
                for pos in values:
                    if pos == values[0]:
                        continue
                    else:
                        x, y = pos.split(",")
                        value.append([int(x), int(y)])
                self.ambiente[values[0]] = value

        print("dicionario config: ", self.ambiente)

    def loadSinaisVitais(self):
        arq = open(self.sinaisVitaisPath, "r")
        for line in arq:
            values = line.split(",")
            self.sinaisVitais.append(
                [
                    float(x) if i > 0 else int(x) for i, x in enumerate(values)
                ]
            )
        # teste
        # print(self.sinaisVitais)

    def getBase(self):
        return self.ambiente["Base"]

    def getTe(self):
            return self.ambiente["Te"]

    def getTs(self):
        return self.ambiente["Ts"]

    def getXMax(self):
        return self.ambiente["XMax"]

    def getYMax(self):
        return self.ambiente["YMax"]

    def getVitimas(self):
        return self.ambiente["Vitimas"]

    def getParedes(self):
        return self.ambiente["Parede"]
    
    def getSinaisVitais(self):
        return self.sinaisVitais

## Para teste da classe
# def main():
#     config = Config("config_data/ambiente.txt", "config_data/sinaisvitais.txt")
#     # print(config.getSinaisVitais())
#     # print(config.getBase(), "\n",
#     #       config.getTe(), "\n",
#     #       config.getTs(), "\n",
#     #       config.getXMax(), "\n",
#     #       config.getYMax(), "\n",
#     #       config.getVitimas(), "\n",
#     #       config.getParedes())

    

# if __name__ == '__main__':
#     main()