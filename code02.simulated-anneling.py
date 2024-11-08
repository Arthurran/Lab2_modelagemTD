import random
import numpy as np

# Dados do problema
n = 10  # número de ativos
m = 5   # número de bases
s = 3   # número de equipes
eta = 0.2
distancias = [[10, 20, 30, 25, 15],
              [15, 30, 10, 35, 20],
              [20, 25, 15, 10, 30],
              [25, 35, 20, 15, 25],
              [30, 10, 25, 20, 35],
              [15, 20, 30, 10, 25],
              [20, 25, 35, 15, 10],
              [30, 15, 20, 25, 35],
              [25, 20, 15, 30, 10],
              [10, 30, 25, 20, 15]]

def calcular_custo(solucao_x):
    return sum(distancias[i][j] * solucao_x[i][j] for i in range(n) for j in range(m))

def gerar_solucao_inicial():
    solucao_x = np.zeros((n, m), dtype=int)
    solucao_y = np.zeros((m, s), dtype=int)
    solucao_h = np.zeros((n, s), dtype=int)
    
    for k in range(s):
        j = random.choice(range(m))
        solucao_y[j][k] = 1
    
    for i in range(n):
        j = random.choice([j for j in range(m) if any(solucao_y[j])])
        solucao_x[i][j] = 1
        k = random.choice([k for k in range(s) if solucao_y[j][k] == 1])
        solucao_h[i][k] = 1
    
    return solucao_x, solucao_y, solucao_h

def vizinhanca(solucao_x, solucao_y, solucao_h):
    nova_solucao_x = np.copy(solucao_x)
    nova_solucao_y = np.copy(solucao_y)
    nova_solucao_h = np.copy(solucao_h)
    
    i = random.choice(range(n))
    j = random.choice(range(m))

    if any(nova_solucao_y[j]):  
        nova_solucao_x[i] = 0
        nova_solucao_x[i][j] = 1
    return nova_solucao_x, nova_solucao_y, nova_solucao_h

def simulated_annealing(temperatura_inicial, taxa_resfriamento, iteracoes):
    solucao_x, solucao_y, solucao_h = gerar_solucao_inicial()
    custo = calcular_custo(solucao_x)
    melhor_custo = custo
    melhor_solucao = (solucao_x, solucao_y, solucao_h)
    
    temperatura = temperatura_inicial
    for _ in range(iteracoes):
        nova_solucao_x, nova_solucao_y, nova_solucao_h = vizinhanca(solucao_x, solucao_y, solucao_h)
        novo_custo = calcular_custo(nova_solucao_x)
        
        if novo_custo < custo or random.uniform(0, 1) < np.exp((custo - novo_custo) / temperatura):
            solucao_x, solucao_y, solucao_h = nova_solucao_x, nova_solucao_y, nova_solucao_h
            custo = novo_custo
            
            if custo < melhor_custo:
                melhor_custo = custo
                melhor_solucao = (solucao_x, solucao_y, solucao_h)
        
        temperatura *= taxa_resfriamento
    
    return melhor_solucao, melhor_custo

temperatura_inicial = 1000
taxa_resfriamento = 0.95
iteracoes = 1000

melhor_solucao, melhor_custo = simulated_annealing(temperatura_inicial, taxa_resfriamento, iteracoes)
print("Melhor custo encontrado:", melhor_custo)
