from libs import *
import construcao 
import plot
from vizinhanca import neighborhood_change 

# Função objetivo 1: Minimizar distâncias 
def objective_function_1(solution, constraints, dist_bases_ativos):

    solution['fitness'] = 0
    solution['penalty'] = 0
    #solution['penalty_fitness'] = 0

    #CÁLCULO DO FITNESS
    bases_com_equipes = np.where(solution['y'] == 1)[0]

    # Inicializa a soma total das distâncias
    soma_ativos_a_bases = 0 
    
    for base in bases_com_equipes:
        ativos_da_base = np.where(solution['x'][:,base]==1)[0] #index dos ativos da base 

        # Soma as distâncias dos ativos para a base
        if len(ativos_da_base) > 0:
            for ativo in ativos_da_base:
               soma_ativos_a_bases += dist_bases_ativos[ativo,base]
        
    solution['fitness'] = soma_ativos_a_bases

    # Calculo das penalidades
    solution['penalty'] = penalty_method(solution, constraints)

    # Cálculo do balanceamento entre as equipes
    ativos_por_equipe = solution['h'].sum(axis=0)
    mais_ativos = np.max(ativos_por_equipe)
    menos_ativos = np.min(ativos_por_equipe)
    solution['balanceamento_equipes'] = mais_ativos - menos_ativos

    # Aplicação das penalidades
    solution['penalty_fitness'] = solution['penalty'] + solution['fitness']

def objective_function_2(solution, constraints):
    solution['fitness'] = 0
    solution['penalty'] = 0

    #ativos_por_equipes = np.where(solution['h'] == 1)[0]
    ativos_por_equipe = solution['h'].sum(axis=0)

    mais_ativos = np.max(ativos_por_equipe)
    menos_ativos = np.min(ativos_por_equipe)

    diferenca_ativos_entre_equipes = mais_ativos - menos_ativos

    solution['fitness'] = diferenca_ativos_entre_equipes
    solution['balanceamento_equipes'] = diferenca_ativos_entre_equipes

    # Calculo das penalidades
    solution['penalty'] = penalty_method(solution, constraints)

    # Aplicação das penalidades
    solution['penalty_fitness'] = solution['penalty'] + solution['fitness']

# Aplicar as penalidades para as violações de restrições
def penalty_method(solution, constraints):
    penalty = 0
    iterador = 1
    for constraint in constraints:
      if not constraint(solution):
        #print(f"Contraint problematica: {iterador}")
        penalty += 1
      iterador += 1
    #print("\n----------------------------------------------------------\n")
    return penalty

def solution_check(new_solution, solution):
    # 1. Se a nova solução tiver penalidade menor, aceitar imediatamente
    if new_solution['penalty'] < solution['penalty']:
        return True

    # 2. Se as penalidades são iguais, tentar minimizar o balanceamento de equipes
    if new_solution['penalty'] == solution['penalty'] and new_solution['penalty'] != 0:
        # A redução do balanceamento de equipes pode ajudar a diminuir a penalidade
        if new_solution['balanceamento_equipes'] < solution['balanceamento_equipes']:
            return True

    # 3. Depois que a penalidade for zero, aceitamos soluções com fitness menor
    if new_solution['penalty'] == 0:
        # Aceitar se o fitness for menor
        if new_solution['fitness'] < solution['fitness']:
            return True

    return False

def bvns_method(objective_function, constraints, max_iter=1000, neighborhood_max = 3):

    progress = {
        'fitness': np.zeros(max_iter),
        'penalty': np.zeros(max_iter),
        'penalty_fitness': np.zeros(max_iter)
    }

    obj_function = 0
    if objective_function == objective_function_1:
        obj_function = 1
    elif objective_function == objective_function_2:
        obj_function = 2

    dist_bases_ativos, coords_bases, coords_ativos = construcao.read_geolocation_data() 
    solution = construcao.generate_solution(dist_bases_ativos,obj_function)

    #plot.plot_solution(solution, coords_bases, coords_ativos)

    objective_function(solution, constraints, dist_bases_ativos)
    for i in range(max_iter):
      neighborhood = 1

      progress['fitness'][i] = solution['fitness']
      progress['penalty'][i] = solution['penalty']

      while neighborhood <= neighborhood_max:

        new_solution = neighborhood_change(solution, neighborhood,obj_function, dist_bases_ativos, coords_bases)

        # Avaliar a solução
        objective_function(new_solution, constraints, dist_bases_ativos)

        # Compara a solução nova com a atual com as soluções da vizinhança
        if solution_check(new_solution, solution):
            print(f'Estrutura de vizinhanca: {neighborhood}')
            print(f"solution['fitness']: {solution['fitness']}")
            print(f"solution['penalty']: {solution['penalty']}")
            solution = copy.deepcopy(new_solution)
            print(f"new_solution['fitness']: {solution['fitness']}")
            print(f"new_solution['penalty']: {solution['penalty']}")
            
        neighborhood += 1
    print("\n----------------------------------------------------------\n")
    return solution, progress