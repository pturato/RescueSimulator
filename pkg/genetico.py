from asyncio import base_events
import calculos
from random import getrandbits, randint, random, choice
from random import shuffle
import sys

def genetico():
    from random import getrandbits, randint, random, choice

def individual(n_de_itens):
    """Cria um membro da populacao"""
    return [ getrandbits(1) for x in range(n_de_itens) ]

def population(n_de_individuos, n_de_itens):
    """"Cria a populacao"""
    return [ individual(n_de_itens) for x in range(n_de_individuos) ]

def fitness(individuo, tempoMax, vitimas, caminhos): 
    base = 0 #considera a base antes da primeira vítima na lista de individuo
    posicoes_vitimas = []
    print("Indivíduo ",individuo)
    for i in range(len(individuo)-1):
        if individuo[i]==1:
            posicoes_vitimas.append(i) #guardar as posicoes das vítimas pelo índice da posição que contém 1 no vetor indivíduo
    #shuffle(posicoes_vitimas) #deixar sequencia de vitimas aleatoria
    
    tempo_caminho = 0.0
    vitimas_salvas = []
    caminho = []

    for k in range(len(posicoes_vitimas)-1): #percorre as vítimas
        vitimas_salvas.append(vitimas[posicoes_vitimas[k]+1]) #soma 1 para nunca dar 0, que é nossa base no caminhos
        if k != len(posicoes_vitimas)-2:
            if caminhos[base][posicoes_vitimas[k]+1] == 0: #ir daquela vítima para ela mesma
                print("Algo deu errado :(")
                sys.exit()
            caminho.append(caminhos[base][posicoes_vitimas[k]+1]) #ir da base para a vítima
            tempo_caminho = tempo_caminho + caminhos[base][posicoes_vitimas[k]+1][0] #no caminhos a base é zero
            base=posicoes_vitimas[k]+1 #muda a base para a vítima que era o destino
        else:
            #última execução, retorna para a base
            
            caminho.append(caminhos[base][0])
            tempo_caminho = tempo_caminho + caminhos[base][0][0]

        if (tempo_caminho > tempoMax): #solução não valido
            print("Inválido :(")
            return -1

        vitimas_gravidade = []
        for vitima in range(len(vitimas)): #pegar sinal vital das vitimas escolhidas na solução
            sinal = vitimas[vitima][1] 
            vitimas_gravidade.append(sinal[len(sinal)-1]) #somente última posição do sinal vital

        v = calculos.calcula_num_vitm(vitimas_gravidade) #vetor com o cálculo da gravidade
        #tenho o menor caminho e o genetivo vai escolher o com maior vitimas por gravidade
        print("Valor do cálculo da gravidade ", 4*v[3]+3*v[2]+2*v[1]+v[0])
        fitness = (4*v[3]+3*v[2]+2*v[1]+v[0])/tempo_caminho #quanto menor o tempo do caminho, maior o resultado da solução
        print("Tempo caminho ",tempo_caminho)
        print("Valor do cálculo total ", fitness) 
        
        return fitness #se for um individuo valido retorna seu valor, sendo quanto maior melhor

def media_fitness(populacao, tempoMax, vitimas, caminhos): #só leva em consideracao os elementos que respeitem o tempo maximo
    """Encontra a avalicao media da populacao"""
    summed = sum(fitness(individuo, tempoMax, vitimas, caminhos) for individuo in populacao if fitness(individuo, tempoMax, vitimas, caminhos) >= 0)
    return summed / (len(populacao) * 1.0)

def selecao_roleta(pais):
    """Seleciona um pai e uma mae baseado nas regras da roleta"""
    #sorteia dois indivíduos para fazer o cruzamento
    def sortear(fitness_total, indice_a_ignorar=-1): #2 parametro garante que não vai selecionar o mesmo elemento
        """Monta roleta para realizar o sorteio"""
        roleta, acumulado, valor_sorteado = [], 0, random()

        if indice_a_ignorar!=-1: #Desconta do total, o valor que sera retirado da roleta
            fitness_total -= valores[0][indice_a_ignorar]

        for indice, i in enumerate(valores[0]):
            if indice_a_ignorar==indice: #ignora o valor ja utilizado na roleta
                continue
            acumulado += i
            roleta.append(acumulado/fitness_total)
            if roleta[-1] >= valor_sorteado:
                return indice
    
    valores = list(zip(*pais)) #cria 2 listas com os valores fitness e os cromossomos
    fitness_total = sum(valores[0])

    indice_pai = sortear(fitness_total) 
    indice_mae = sortear(fitness_total, indice_pai) #remover o pai da roleta para não haver elitismo

    pai = valores[1][indice_pai]
    mae = valores[1][indice_mae]
    
    return pai, mae

def evolve(populacao, tempoMax, vitimas, n_de_cromossomos, caminhos, mutate=0.05):
    """Tabula cada individuo e o seu fitness"""
    pais = [ [fitness(x, tempoMax, vitimas, caminhos), x] for x in populacao if fitness(x, tempoMax, vitimas, caminhos) >= 0]
    #só armazena indivíduos válidos (não ultrapassa o tempo máximo)
    print("Pais ",pais) #achar individuos 
    pais.sort(reverse=True) #ordem crescente na lista, colocando os melhores indivíduos no começo
    
    # REPRODUCAO
    filhos = []
    while len(filhos) < n_de_cromossomos: #loop até ter o número de cromossomos desejados (quantos indivíduos queremos)
        homem, mulher = selecao_roleta(pais) #roleta para ver quais indivíduos vão fazer parte da reprodução
        meio = len(homem) // 2 #pega metade dos genes
        filho = homem[:meio] + mulher[meio:] #primeira metade do pai e segunda metade da mãe
        filhos.append(filho) #filho adicionado a lista (nova geração)
    # while len(filhos) < n_de_cromossomos: #loop até ter o número de cromossomos desejados (quantos indivíduos queremos)
    #     homem, mulher = selecao_roleta(pais) #roleta para ver quais indivíduos vão fazer parte da reprodução
    #     meio = randint(0, len(homem)-1) #pega metade dos genes
    #     filho = homem[:meio] + mulher[meio:] #primeira metade do pai e segunda metade da mãe
    #     filhos.append(filho) #filho adicionado a lista (nova geração)
    
    # MUTACAO
    #para não ficar preso em um ótimo local (solução boa mas não a melhor)
    for individuo in filhos: 
        if mutate > random(): #definido como parâmetro na função
            #chance de 5% de mutação
            pos_to_mutate = randint(0, len(individuo)-1) #sorteia um dos genes que vai alterar
            if individuo[pos_to_mutate] == 1: #altera gene
                individuo[pos_to_mutate] = 0
            else:
                individuo[pos_to_mutate] = 1

    return filhos #retorna nova geração

def genetico(caminhos, vitimas, tempoMax): 
    n_de_cromossomos = 150
    geracoes = 30
    n_de_itens = len(vitimas)-1 #numeros de vítimas

    #EXECUCAO DOS PROCEDIMENTOS
    populacao = population(n_de_cromossomos, n_de_itens) #gera população aleatória
    #vetor de 0 e 1 para cada vitima (escolhida ou não na solucao)
    historico_de_fitness = [media_fitness(populacao, tempoMax, vitimas, caminhos)]
    for i in range(geracoes): #repete até o valor de gerações definido
        populacao = evolve(populacao, tempoMax, vitimas, n_de_cromossomos, caminhos) #nova geração
        historico_de_fitness.append(media_fitness(populacao, tempoMax, vitimas, caminhos)) #média de pontuação que a nova geração fez
        
    #PRINTS DO TERMINAL
    for indice,dados in enumerate(historico_de_fitness):
        print("Geracao: ", indice," | Média da população: ", dados)

    print("\nTempo máximo:",tempoMax,"\n\nVítimas:")
    for indice,i in enumerate(vitimas):
        print("Vítima ",indice+1,": ",i[0]," | ",i[1])
        
    print("\nExemplos de boas solucoes: ")
    for i in range(5):
        print(populacao[i])

    individuo = populacao[0]
    posicoes_vitimas = []
    for i in range(len(individuo)-1):
        if individuo[i]==1:
            posicoes_vitimas.append(i) #vitimas escolhidas pelo genético

    base = 0
    tempo_caminho = 0.0
    vitimas_salvas = []
    caminho = []
    for k in range(len(posicoes_vitimas)-1):
        vitimas_salvas.append(vitimas[posicoes_vitimas[k]+1]) #somei um para nunca dar 0, que é nossa base no caminhos
        if k != len(posicoes_vitimas)-2:
            if caminhos[base][posicoes_vitimas[k]+1] == 0: #ir daquela vítima para ela mesma
                print("Algo deu errado :(")
                sys.exit()
            caminho.append(caminhos[base][posicoes_vitimas[k]+1])
            tempo_caminho = tempo_caminho + caminhos[base][posicoes_vitimas[k]+1][0] #no caminhos a base é zero
            base=posicoes_vitimas[k]+1
        else:
            #volta para base
            caminho.append(caminhos[base][0])
            #print("CAMINHOS ",caminhos)
            #print("AQUI ", caminhos[posicoes_vitimas[k]+1][base][0])
            tempo_caminho = tempo_caminho + caminhos[base][0][0]
    print("Caminho :\n",caminho)
    print("Tempo deste caminho: ",tempo_caminho)
    print("Tempo máximo: ",tempoMax)
    print("Número de vítimas salvas: ",len(posicoes_vitimas))

    caminho_sequencial = caminho[0][1]
    for i in range(1, len(caminho)):
        caminho_sequencial += (caminho[i][1][1:]) 
    print("caminho_sequencial ",caminho_sequencial)
    return caminho_sequencial