# Instalação do PuLP
#!pip install pulp -- descomentar pra rodar no google collab

# Importação
import pulp
import random
import matplotlib.pyplot as plt

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

problema = pulp.LpProblem("Alocacao_de_Equipes_e_Ativos", pulp.LpMinimize)

x = pulp.LpVariable.dicts("x", [(i, j) for i in range(n) for j in range(m)], cat="Binary")
y = pulp.LpVariable.dicts("y", [(j, k) for j in range(m) for k in range(s)], cat="Binary")
h = pulp.LpVariable.dicts("h", [(i, k) for i in range(n) for k in range(s)], cat="Binary")
z = pulp.LpVariable.dicts("z", [(i, j, k) for i in range(n) for j in range(m) for k in range(s)], cat="Binary")

problema += pulp.lpSum(distancias[i][j] * x[(i, j)] for i in range(n) for j in range(m)), "MinDistanciaTotal"

# Restrições
# Restrição 1: Cada equipe deve estar em uma base
for j in range(m):
    problema += pulp.lpSum(y[(j, k)] for k in range(s)) == 1

# Restrição 2: Cada ativo deve ser atribuído a uma base
for i in range(n):
    problema += pulp.lpSum(x[(i, j)] for j in range(m)) == 1

# Restrição 3: Ativo só pode ser atribuído a uma base com equipe
for i in range(n):
    for j in range(m):
        problema += x[(i, j)] <= pulp.lpSum(y[(j, k)] for k in range(s))

# Restrição 4: Cada ativo mantido por uma equipe
for i in range(n):
    problema += pulp.lpSum(h[(i, k)] for k in range(s)) == 1

# Restrição 5: Ativo só pode ser mantido se a equipe estiver na base do ativo
for i in range(n):
    for j in range(m):
        for k in range(s):
            problema += z[(i, j, k)] <= x[(i, j)]
            problema += z[(i, j, k)] <= y[(j, k)]
            problema += z[(i, j, k)] >= x[(i, j)] + y[(j, k)] - 1
            problema += h[(i, k)] <= pulp.lpSum(z[(i, j, k)] for j in range(m))

# Restrição 6: Cada equipe deve manter no mínimo uma quantidade de ativos
for k in range(s):
    problema += pulp.lpSum(h[(i, k)] for i in range(n)) >= eta * (n / s)

problema.solve()

print("Status:", pulp.LpStatus[problema.status])
for var in problema.variables():
    print(f"{var.name} = {var.varValue}")



# Visualizacao dos dados
# Extração da solução ótima
melhor_solucao_x = [[x[(i, j)].varValue for j in range(m)] for i in range(n)]
melhor_solucao_y = [[y[(j, k)].varValue for k in range(s)] for j in range(m)]

print("Solução ótima para x (atribuição de ativos):")
for i in range(n):
    print(f"Ativo {i+1}: {melhor_solucao_x[i]}")

print("\nSolução ótima para y (alocação de equipes):")
for j in range(m):
    print(f"Base {j+1}: {melhor_solucao_y[j]}")


random.seed(42)
coordenadas_bases = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(m)]
coordenadas_ativos = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(n)]

print("Coordenadas das Bases:", coordenadas_bases)
print("Coordenadas dos Ativos:", coordenadas_ativos)

plt.figure(figsize=(10, 10))

for j in range(m):
    if any(melhor_solucao_y[j]):  # Se a base está ocupada por uma equipe
        plt.scatter(*coordenadas_bases[j], marker='s', color='blue', s=100, label=f"Base {j+1}")

for i in range(n):
    plt.scatter(*coordenadas_ativos[i], color='red', s=50, label=f"Ativo {i+1}")
    for j in range(m):
        if melhor_solucao_x[i][j] == 1:  # Ativo i atribuído à base j
            plt.plot([coordenadas_ativos[i][0], coordenadas_bases[j][0]],
                     [coordenadas_ativos[i][1], coordenadas_bases[j][1]], 'k--')

# Configurações do gráfico
plt.title("Alocação de Ativos e Bases")
plt.xlabel("Coordenada X")
plt.ylabel("Coordenada Y")
plt.legend(loc="best")
plt.show()