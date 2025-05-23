from libs import *
import construcao 
import plot
from vizinhanca import neighborhood_change 
import globals

# Função objetivo 1: Minimizar pico de fila
def objective_function_1(solution, constraints, dist_bases_ativos, prob_ativos):

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
    solution['distancias'] = soma_ativos_a_bases

    # Calculo das penalidades
    solution['penalty'] = penalty_method(solution, constraints, dist_bases_ativos, prob_ativos)

    # Aplicação das penalidades
    solution['penalty_fitness'] = solution['penalty'] + solution['fitness']

# Minimizar tempo de ociosidade
def objective_function_2(solution, constraints, dist_bases_ativos, prob_ativos):
    solution['fitness'] = 0
    solution['penalty'] = 0

    # Calculo da solução 
    soma_distancia_probabilidade = 0
    bases_com_equipes = np.where(solution['y'] == 1)[0] 

    for base in bases_com_equipes:
        ativos_da_base = np.where(solution['x'][:,base]==1)[0] 

        # Cálculo de fitness
        if len(ativos_da_base) > 0:
            for ativo in ativos_da_base:
               soma_distancia_probabilidade += (dist_bases_ativos[ativo,base] * prob_ativos[ativo,2])
            
    solution['fitness'] = soma_distancia_probabilidade
    solution['distancias_ponderadas'] = soma_distancia_probabilidade

    solution['penalty'] = penalty_method(solution, constraints, dist_bases_ativos, prob_ativos)

    # Aplicação das penalidades
    solution['penalty_fitness'] = solution['penalty'] + solution['fitness']

def objective_function_weighted_sum(solution, constraints, dist_bases_ativos, prob_ativos):
    """
    Função objetivo utilizando soma ponderada.
    Combina os dois objetivos normalizados com um peso alpha.
    """

    if solution is None:
        raise ValueError("A solução passada para a função objetivo é None. Verifique a inicialização da solução.")

    # Inicializa fitness e penalidade
    solution['fitness'] = 0
    solution['penalty'] = 0

    # Normalização da Função Objetivo 1: Minimizar distâncias
    bases_com_equipes = np.where(solution['y'] == 1)[0]

    soma_ativos_a_bases = 0
    for base in bases_com_equipes:
        ativos_da_base = np.where(solution['x'][:, base] == 1)[0]
        if len(ativos_da_base) > 0:
            for ativo in ativos_da_base:
                soma_ativos_a_bases += dist_bases_ativos[ativo, base]

    solution['distancias'] = soma_ativos_a_bases

    if (globals.max_val1 - globals.min_val1) == 0:
        Funcao_1_Norm = 0
    else:
        Funcao_1_Norm = (soma_ativos_a_bases - globals.min_val1) / (globals.max_val1 - globals.min_val1)

    # Normalização da Função Objetivo 2: Minimizar probabilidade de falha ponderada pela distância
    soma_distancia_probabilidade = 0
    for base in bases_com_equipes:
        ativos_da_base = np.where(solution['x'][:, base] == 1)[0]
        if len(ativos_da_base) > 0:
            for ativo in ativos_da_base:
                soma_distancia_probabilidade += dist_bases_ativos[ativo, base] * prob_ativos[ativo, 2]

    solution['distancias_ponderadas'] = soma_distancia_probabilidade

    if (globals.max_val2 - globals.min_val2) == 0:
        Funcao_2_Norm = 0
    else:
        Funcao_2_Norm = (soma_distancia_probabilidade - globals.min_val2) / (globals.max_val2 - globals.min_val2)

    # Combinação ponderada das funções objetivo
    solution['fitness'] = (globals.alpha * Funcao_1_Norm) + ((1 - globals.alpha) * Funcao_2_Norm)

    # Cálculo da penalidade com sua implementação existente
    solution['penalty'] = penalty_method(solution, constraints, dist_bases_ativos, prob_ativos)

    # Aplicação das penalidades
    solution['penalty_fitness'] = solution['penalty'] + solution['fitness']

    return solution

# Aplicar as penalidades para as violações de restrições
def penalty_method(solution, constraints, dist_bases_ativos, prob_ativos):
    penalty = 0
    iterador = 1
    for constraint in constraints:
      if not constraint(solution, dist_bases_ativos, prob_ativos):
        #print(f"Contraint problematica: {iterador}")
        penalty += 1
      iterador += 1
    #print("\n----------------------------------------------------------\n")
    return penalty

def solution_check(new_solution, solution):
    # 1. Se a nova solução tiver penalidade menor, aceitar imediatamente
    if new_solution['penalty'] < solution['penalty']:
        return True

    """
    # 2. Se as penalidades são iguais, tentar minimizar o balanceamento de equipes
    if new_solution['penalty'] == solution['penalty'] and new_solution['penalty'] != 0:
        # A redução do balanceamento de equipes pode ajudar a diminuir a penalidade
        if new_solution['balanceamento_equipes'] < solution['balanceamento_equipes']:
            return True
    """

    # 3. Depois que a penalidade for zero, aceitamos soluções com fitness menor
    if new_solution['penalty'] == 0:
        # Aceitar se o fitness for menor
        if new_solution['fitness'] < solution['fitness']:
            return True

    return False

def bvns_method(objective_function, constraints, max_iter=500, neighborhood_max = 2):

    progress = {
        'fitness': np.zeros(max_iter),
        'penalty': np.zeros(max_iter),
        'penalty_fitness': np.zeros(max_iter)
    }

    dist_bases_ativos, coords_bases, coords_ativos = construcao.read_geolocation_data() 
    #Leitura das probabilidades
    prob_ativos = (pd.read_excel('probfalhaativos.xlsx',header=None)).to_numpy()

    obj_function = 0
    if objective_function == objective_function_1:
        # print("FUNÇÃO OBJETIVO 1")
        obj_function = 1
    elif objective_function == objective_function_2:
        # print("FUNÇÃO OBJETIVO 2")
        obj_function = 2
    elif objective_function == objective_function_weighted_sum:
        # print("OTIMIZAÇÃO MULTIOBJETIVO: SOMA PONDERADA")
        obj_function = 3
        neighborhood_max = 4

    solution = construcao.generate_solution(dist_bases_ativos, prob_ativos)

    #plot.plot_solution(solution, coords_bases, coords_ativos)

    objective_function(solution, constraints, dist_bases_ativos, prob_ativos)

    for i in range(max_iter):
      neighborhood = 1

      progress['fitness'][i] = solution['fitness']
      progress['penalty'][i] = solution['penalty']

      while neighborhood <= neighborhood_max:

        new_solution = neighborhood_change(solution, obj_function, neighborhood, dist_bases_ativos, prob_ativos)

        # Avaliar a solução
        objective_function(new_solution, constraints, dist_bases_ativos, prob_ativos)

        # Compara a solução nova com a atual com as soluções da vizinhança      
        if solution_check(new_solution, solution):
            # print(f'Estrutura de vizinhanca: {neighborhood}')
            # print(f"solution['fitness']: {solution['fitness']}")
            # print(f"solution['penalty']: {solution['penalty']}")
            solution = copy.deepcopy(new_solution)
            # print(f"new_solution['fitness']: {solution['fitness']}")
            # print(f"new_solution['penalty']: {solution['penalty']}")

            # print(f"Equipe1: {np.sum(solution['h'][:,0])}\nEquipe2: {np.sum(solution['h'][:,1])}\nEquipe3: {np.sum(solution['h'][:,2])}\n")
            
        neighborhood += 1
    # print("\n----------------------------------------------------------\n")
    
    #plot.plot_solution(solution, coords_bases, coords_ativos)
    return solution, progress