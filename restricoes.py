from libs import *

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