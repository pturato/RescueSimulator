def salva(caminhos, vitimas, tempo, base):
    gravidades = []
    for j in range(len(vitimas)):
        pos_vitima = vitimas[j][0]
        gravidades.append([pos_vitima,vitimas[j][1][len(vitimas[j][1])-1]])
    gravidades.sort(key=lambda i: i[1])
    print(gravidades)

# def genetico2020():
#     from random import getrandbits, randint, random, choice

# def individual(n_de_itens):
#     """Cria um membro da populacao"""
#     return [ getrandbits(1) for x in range(n_de_itens) ]

# def population(n_de_individuos, n_de_itens):
#     """"Cria a populacao"""
#     return [ individual(n_de_itens) for x in range(n_de_individuos) ]

# def fitness(individuo, peso_maximo, pesos_e_valores):
#     """Faz avaliacao do individuo"""
#     peso_total, valor_total = 0, 0
#     for indice, valor in enumerate(individuo): #para cada indivíduo 
#         #0 e 1 significa se a vítima vai ou não ser salva (está dentro daquela solução)
#         peso_total += (individuo[indice] * pesos_e_valores[indice][0])
#         valor_total += (individuo[indice] * pesos_e_valores[indice][1])

#     if (peso_maximo - peso_total) < 0:
#         return -1 #retorna -1 no caso de peso excedido
#         #indivíduo não vai ser considerado na solução
#     return valor_total #se for um individuo valido retorna seu valor, sendo maior melhor

# def media_fitness(populacao, peso_maximo, pesos_e_valores): #só leva em consideracao os elementos que respeitem o peso maximo da mochila
#     """Encontra a avalicao media da populacao"""
#     summed = sum(fitness(x, peso_maximo, pesos_e_valores) for x in populacao if fitness(x, peso_maximo, pesos_e_valores) >= 0)
#     return summed / (len(populacao) * 1.0)

# def selecao_roleta(pais):
#     """Seleciona um pai e uma mae baseado nas regras da roleta"""
#     #sorteia dois indivíduos para fazer o cruzamento
#     def sortear(fitness_total, indice_a_ignorar=-1): #2 parametro garante que não vai selecionar o mesmo elemento
#         """Monta roleta para realizar o sorteio"""
#         roleta, acumulado, valor_sorteado = [], 0, random()

#         if indice_a_ignorar!=-1: #Desconta do total, o valor que sera retirado da roleta
#             fitness_total -= valores[0][indice_a_ignorar]

#         for indice, i in enumerate(valores[0]):
#             if indice_a_ignorar==indice: #ignora o valor ja utilizado na roleta
#                 continue
#             acumulado += i
#             roleta.append(acumulado/fitness_total)
#             if roleta[-1] >= valor_sorteado:
#                 return indice
    
#     valores = list(zip(*pais)) #cria 2 listas com os valores fitness e os cromossomos
#     fitness_total = sum(valores[0])

#     indice_pai = sortear(fitness_total) 
#     indice_mae = sortear(fitness_total, indice_pai) #remover o pai da roleta para não haver elitismo

#     pai = valores[1][indice_pai]
#     mae = valores[1][indice_mae]
    
#     return pai, mae

# def evolve(populacao, peso_maximo, pesos_e_valores, n_de_cromossomos, mutate=0.05): 
#     """Tabula cada individuo e o seu fitness"""
#     pais = [ [fitness(x, peso_maximo, pesos_e_valores), x] for x in populacao if fitness(x, peso_maximo, pesos_e_valores) >= 0]
#     #vetor que tem a pontuação do indivíduo e o código genético (x) para todos os indivíduos
#     #só armazena indicvíduos válidos (não ultrapassa o tempo máximo)
#     pais.sort(reverse=True) #ordem crescente na lista, colocando os melhores indivíduos no começo
    
#     # REPRODUCAO
#     filhos = []
#     while len(filhos) < n_de_cromossomos: #loop até ter o número de cromossomos desejados (quantos indivíduos queremos)
#         homem, mulher = selecao_roleta(pais) #roleta para ver quais indivíduos vão fazer parte da reprodução
#         meio = len(homem) // 2 #pega metade dos genes
#         filho = homem[:meio] + mulher[meio:] #primeira metade do pai e segunda metade da mãe
#         filhos.append(filho) #filho adicionado a lista (nova geração)
    
#     # MUTACAO
#     #para não ficar preso em um ótimo local (solução boa mas não a melhor)
#     for individuo in filhos: 
#         if mutate > random(): #definido como parâmetro na função
#             #chance de 5% de mutação
#             pos_to_mutate = randint(0, len(individuo)-1) #sorteia um dos genes que vai alterar
#             if individuo[pos_to_mutate] == 1: #altera gene
#                 individuo[pos_to_mutate] = 0
#             else:
#                 individuo[pos_to_mutate] = 1

#     return filhos #retorna nova geração

# def genetico(caminhos, vitimas): #(posicao, gravidade)
#                 #[peso,valor]
#                 #[custo um para outro, gravidade de quem a gente chega]
#     custos = []
#     pos_vitimas = []
#     gravidades = []
#     pesos_e_valores = [caminhos[0][0],0]
#     for i in range(len(caminhos)):
#         custo = caminhos[i][0]
#         custos.append(custo)
#         vitima = caminhos[i][1]
#         pos_vitimas.append(vitima[len(vitima)-1]) 
#         for j in range(len(pos_vitimas)):
#             if pos_vitimas in vitimas[j][0]:
#                 gravidades.append(vitimas[j][1][len(vitimas[j][1])-1])
#             #posicao_vitima = vitimas[i][0]
#         pesos_e_valores.append(custo, gravidade)
    
#     pesos_e_vares = custos, gravidades 
#     #[[8, 25], [10, 75], [5, 20], [6, 50],
#     # [10, 10], [7, 60], [20, 28], [14, 100]] #definir como vamos calcular a gravidade
#                     #valor maior aqui consideraria como o mais grave (ele busca o maior valor possível)
#     peso_maximo = 30 #tempo limite - tempo da vítima mais longe
#     n_de_cromossomos = 150
#     geracoes = 80
#     n_de_itens = len(pesos_e_valores) #Analogo aos pesos e valores

#     #EXECUCAO DOS PROCEDIMENTOS
#     populacao = population(n_de_cromossomos, n_de_itens) #gera população aleatória
#     historico_de_fitness = [media_fitness(populacao, peso_maximo, pesos_e_valores)] #média de pontuação que a população fez
#     for i in range(geracoes): #repete até o valor de gerações definido
#         populacao = evolve(populacao, peso_maximo, pesos_e_valores, n_de_cromossomos) #nova geração
#         historico_de_fitness.append(media_fitness(populacao, peso_maximo, pesos_e_valores)) #média de pontuação que a nova geração fez

#     #PRINTS DO TERMINAL
#     for indice,dados in enumerate(historico_de_fitness):
#         print("Geracao: ", indice," | Media de valor na mochila: ", dados)

#     print("\nPeso máximo:",peso_maximo,"g\n\nItens disponíveis:")
#     for indice,i in enumerate(pesos_e_valores):
#         print("Item ",indice+1,": ",i[0],"g | R$",i[1])
        
#     print("\nExemplos de boas solucoes: ")
#     for i in range(5):
#         print(populacao[i])

#     #GERADOR DE GRAFICO
#     from matplotlib import pyplot as plt
#     plt.plot(range(len(historico_de_fitness)), historico_de_fitness)
#     plt.grid(True, zorder=0)
#     plt.title("Problema da mochila")
#     plt.xlabel("Geracao")
#     plt.ylabel("Valor medio da mochila")
#     plt.show()