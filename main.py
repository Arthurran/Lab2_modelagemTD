from libs import *
import metodo 
from restricoes import constraints
from metodo import objective_function_1, objective_function_2, objective_function_weighted_sum
from plot import plot_progress, plot_pareto_fronts, plot_solution

"""
ENTREGA TC1: FUNÇÕES MONOOBJETIVO
# Chamar o algoritmo de Penalidade para otimizar cada função objetivo individualmente
result = []
progress = {}
best_solution = {}

for i in range(5): #ALTERAR RANGE 1 PARA 5
    best_solution[i], progress[i] = metodo.bvns_method(objective_function_2, constraints)
    print("FITNESS: ", best_solution[i]['fitness'])
    print("PENALIDADE: ",best_solution[i]['penalty'])
    print("FIT+PEN: ",best_solution[i]['penalty_fitness'])
    result.append(best_solution[i]['penalty_fitness'])
    #print("num PAs: ", i, np.sum(best_solution[i]['y']))
    #plot_solution(best_solution[i])
    #print("PAs coord: ", i, best_solution['pa_coordinates'])

print('\n--- MELHOR SOLUÇÃO de f1 ENCONTRADA ---\n')
print('O valor MIN encontrado foi:', np.min(result))
print('O valor STD encontrado foi:', np.std(result))
print('O valor MAX encontrado foi:', np.max(result))

# Plotar a solução da função objetivo 1
plot_progress(progress,5)
"""
#ENTREGA TC2: FUNÇÕES MULTIOBJETIVO SOMA PONDERADA E E-RESTRITO

def minimos_maximos (solution_1, solution_2):
    globals.min_val1 = np.sum(solution_1['y']) #Mínimo função objetivo 1
    globals.max_val1 = np.sum(solution_2['y']) #Máximo função objetivo 1
    globals.min_val2 = np.sum(np.multiply(solution_2['client_pa_distances'], solution_2['x'])) #Mínimo resultado função objetivo 2
    globals.max_val2 = np.sum(np.multiply(solution_1['client_pa_distances'], solution_1['x'])) #Máximo resultado função objetivo 2

def change_alpha (new_alpha):
    globals.alpha = new_alpha

# SOMA PONDERADA 
result_w = []
progress_w = {}
best_solution_w = {}

new_alpha = 0.1
for i in range(0,10): 
    change_alpha(new_alpha)
    best_solution_w[i], progress_w[i] = metodo.bvns_method(objective_function_weighted_sum, constraints)
    new_alpha = new_alpha + 0.1
    result_w.append(best_solution_w[i]['fitness'])
    #plot_solution(best_solution_w[i])

"""
# e-Restrito
result_e = []
progress_e = {}
best_solution_e = {}

new_alpha = 0.1
for i in range(9): 
    change_alpha(new_alpha)
    best_solution_e[i], progress_e[i] = metodo.bvns_method(objective_function_2, multiconstraints)
    new_alpha = new_alpha + 0.1
    result_e.append(best_solution_e[i]['fitness'])
    #plot_solution(best_solution_e[i])

"""
# PLOT DE FRONTEIRAS PARETO
pareto_fronts_weighted_sum = []  # Armazena as 10 fronteiras de Pareto de soma ponderada
pareto_fronts_e_restrito = []  # Armazena as 10 fronteiras de Pareto de e-restrito  

for i in range(0,10):
    print("\n--------------------------------")
    print(f"{i}\nbest_solution_w['fitness']: {best_solution_w[i]['fitness']}")
    print(f"best_solution_w['distancias']: {best_solution_w[i]['distancias']}")
    print(f"best_solution_w['distancias_ponderadas']: {best_solution_w[i]['distancias_ponderadas']}")
    print(f"best_solution_w['penalty']: {best_solution_w[i]['penalty']}")
    # Adiciona todas as tuplas diretamente à lista principal
    pareto_fronts_weighted_sum.append((best_solution_w[i]['distancias'], best_solution_w[i]['distancias_ponderadas']))

# Plotar as fronteiras de Pareto
plot_pareto_fronts([pareto_fronts_weighted_sum], "Fronteiras de Pareto - Soma Ponderada")
#plot_pareto_fronts([pareto_fronts_e_restrito], "Fronteiras de Pareto - e-Restrito")