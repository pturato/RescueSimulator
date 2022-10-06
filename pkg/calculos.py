def calcula_num_vitm(vitm):
    est = [0,0,0,0]
    i = 0
    while(i < len(vitm)):
        if vitm[i]==1:
            est[0] = est[0]+1 #estável
        elif vitm[i]==2:
            est[1] = est[1]+1
        elif vitm[i]==3:
            est[2] = est[2]+1
        elif vitm[i]==4:
            est[3] = est[3]+1 #crítico
        i = i+1
    return est
#𝑐𝑙𝑎𝑠𝑠𝑒=4=𝑐𝑟í𝑡𝑖𝑐𝑜

#cálculos da Parte 1
#porcentual de vítimas encontradas
def pve(vitm_encontradas, vitm_ambiente):
    return vitm_encontradas/vitm_ambiente

#tempo por vítima encontrada
def tve(total_gasto, vitm_encontradas):
    return total_gasto/vitm_encontradas

#porcentual ponderado de vítimas encontradas por extrato de gravidade
def veg(vitm_encontradas, vitm_ambiente):
    v = calcula_num_vitm(vitm_encontradas)
    V = calcula_num_vitm(vitm_ambiente)
    return (4*v[3]+3*v[2]+2*v[1]+v[0])/(4*V[3]+3*V[2]+2*V[1]+V[0])

#cálculos da Parte 2
#porcentual de vítimas SALVAS
def pvs(vitm_salva, vitm_ambiente):
    return vitm_salva/vitm_ambiente

#Tempo por vítima salva
def tvs(total_gasto, vitm_salva):
    #com ts ≤ Ts
    return total_gasto/vitm_salva

#porcentual ponderado de vítimas salvas por extrato de gravidade
def vsg(vitm_salva, vitm_ambiente):
    v = calcula_num_vitm(vitm_salva)
    V = calcula_num_vitm(vitm_ambiente)
    return (4*v[3]+3*v[2]+2*v[1]+v[0])/(4*V[3]+3*V[2]+2*V[1]+V[0])
     