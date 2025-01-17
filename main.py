from libs import *
import metodo 
from restricoes import constraints, multiconstraints
from metodo import objective_function_1, objective_function_2, objective_function_weighted_sum
from plot import plot_progress, plot_pareto_fronts, plot_solution
from construcao import read_geolocation_data

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


# e-Restrito
result_e = []
progress_e = {}
best_solution_e = {}

new_alpha = 0.1
for i in range(0,10): 
    change_alpha(new_alpha)
    best_solution_e[i], progress_e[i] = metodo.bvns_method(objective_function_1, multiconstraints)
    new_alpha = new_alpha + 0.1
    result_e.append(best_solution_e[i]['fitness'])
    #plot_solution(best_solution_e[i])


# PLOT DE FRONTEIRAS PARETO
pareto_fronts_weighted_sum = []  # Armazena as 10 fronteiras de Pareto de soma ponderada
pareto_fronts_e_restrito = []  # Armazena as 10 fronteiras de Pareto de e-restrito  


#PLOT DE SOMA PONDERADA
for i in range(0,10):
    # print("\n--------------------------------")
    # print(f"{i}\nbest_solution_w['fitness']: {best_solution_w[i]['fitness']}")
    # print(f"best_solution_w['distancias']: {best_solution_w[i]['distancias']}")
    # print(f"best_solution_w['distancias_ponderadas']: {best_solution_w[i]['distancias_ponderadas']}")
    # print(f"best_solution_w['penalty']: {best_solution_w[i]['penalty']}")
    # Adiciona todas as tuplas diretamente à lista principal
    pareto_fronts_weighted_sum.append((best_solution_w[i]['distancias'], best_solution_w[i]['distancias_ponderadas']))

virtual_alpha = 0.1
#PLOT DE E-RESTRITO
for i in range(0,10):
    epsilon_2 = globals.min_val2 + virtual_alpha * (globals.max_val2 - globals.min_val2)
    # print("\n--------------------------------")
    # print(f"{i}\nbest_solution_e['fitness']: {best_solution_e[i]['fitness']}")
    # print(f"best_solution_e['distancias']: {best_solution_e[i]['distancias']}")
    # print(f"best_solution_e['distancias_ponderadas']: {best_solution_e[i]['distancias_ponderadas']}")
    # print(f"best_solution_e['penalty']: {best_solution_e[i]['penalty']}")
    # Adiciona todas as tuplas diretamente à lista principal
    pareto_fronts_e_restrito.append((best_solution_e[i]['distancias'], epsilon_2))
    virtual_alpha = virtual_alpha + 0.1

# Plotar as fronteiras de Pareto
# plot_pareto_fronts([pareto_fronts_weighted_sum], "Fronteiras de Pareto - Soma Ponderada")
# plot_pareto_fronts([pareto_fronts_e_restrito], "Fronteiras de Pareto - e-Restrito")

#all_pareto_fronts = [pareto_fronts_weighted_sum, pareto_fronts_e_restrito]
#plot_pareto_fronts(all_pareto_fronts, "Fronteiras de Pareto - Soma Ponderada e e-Restrito")
def get_pareto_front(points):
    points = np.array(points)
    is_dominated = np.zeros(len(points), dtype=bool)

    for i, point in enumerate(points):
        # Verifica se `point` é dominado por outro ponto
        is_dominated[i] = np.any(
            np.all(points <= point, axis=1) & np.any(points < point, axis=1)
        )
    
    # Retorna apenas os pontos não dominados
    return points[~is_dominated].tolist()

# Combina todas as fronteiras de Pareto em um único conjunto de pontos
combined_pareto_points = pareto_fronts_weighted_sum + pareto_fronts_e_restrito

# Obtém os pontos não dominados
non_dominated_points = get_pareto_front(combined_pareto_points)

# Garante o formato de lista de tuplas
non_dominated_points = [(float(x), float(y)) for x, y in non_dominated_points]


def calculate_balance_std(solution):
    """
    Calcula o desvio padrão do balanceamento de carga entre equipes.

    Parâmetros:
    - solution: Dicionário contendo 'h' (matriz de alocação de ativos às equipes).

    Retorna:
    - O desvio padrão da carga entre equipes.
    """
    num_ativos_por_equipe = np.sum(solution['h'], axis=0)  # Soma de ativos por equipe
    balance_std = np.std(num_ativos_por_equipe)  # Desvio padrão da distribuição de carga
    return balance_std


def calculate_distance_std(solution, dist_bases_ativos):
    """
    Calcula o desvio padrão da distância total percorrida por equipe.

    Parâmetros:
    - solution: Dicionário contendo 'x' (matriz de alocação de ativos às bases) e 'h' (equipes).
    - dist_bases_ativos: Matriz de distâncias dos ativos às bases.

    Retorna:
    - O desvio padrão das distâncias percorridas por equipe.
    """
    num_equipes = solution['h'].shape[1]
    distancias_por_equipe = np.zeros(num_equipes)

    for equipe in range(num_equipes):
        ativos_na_equipe = np.where(solution['h'][:, equipe] == 1)[0]  # Índices dos ativos da equipe
        for ativo in ativos_na_equipe:
            base = np.where(solution['x'][ativo] == 1)[0]  # Base associada ao ativo
            if len(base) > 0:  # Evitar erros caso não haja base associada
                distancias_por_equipe[equipe] += dist_bases_ativos[ativo, base[0]]

    distance_std = np.std(distancias_por_equipe)  # Desvio padrão das distâncias percorridas
    return distance_std


# Carregar matriz de distâncias
dist_bases_ativos, bases_unicas, ativos_unicos = read_geolocation_data()

# Lista para armazenar os novos critérios
additional_criteria = []

# Ajustar full_solutions para corresponder ao número de pontos não dominados
full_solutions = list(best_solution_w.values()) + list(best_solution_e.values())
full_solutions = full_solutions[:len(non_dominated_points)]  # Garante tamanho correto

for solution in full_solutions:
    balance_std = calculate_balance_std(solution)
    distance_std = calculate_distance_std(solution, dist_bases_ativos)
    additional_criteria.append((balance_std, distance_std))

# Adicionando os novos critérios às soluções não dominadas
non_dominated_points_extended = [
    (*sol, add1, add2) for sol, (add1, add2) in zip(non_dominated_points, additional_criteria)
]

# Verificar a nova estrutura das soluções
print("Soluções não dominadas com critérios adicionais:")
for sol in non_dominated_points_extended:
    print(sol)


# Garantir que os valores são float e remover duplicatas
non_dominated_points_plot = list(set([(float(sol[0]), float(sol[1])) for sol in non_dominated_points_extended]))


# Agora a função aceita o formato correto [(x, y), ...]
plot_pareto_fronts([non_dominated_points_plot], "Fronteira de Pareto - Soluções Não Dominadas")


###############################################################################
# Matriz de comparação por pares ajustada para 2 critérios
# Critério 1 (P_w) é mais importante que Critério 2 (P_ϵ)
print(len(non_dominated_points))


# Nova matriz de comparação por pares para 4 critérios
comparison_matrix = np.array([
    [1, 9, 7, 5],    # P_w (mais importante)
    [1/9, 1, 3, 3],  # P_ϵ 
    [1/7, 1/3, 1, 3],  # Bσ (balanceamento)
    [1/5, 1/3, 1/3, 1]  # Dσ (distância percorrida)
])

# Normalização da matriz
column_sums = comparison_matrix.sum(axis=0)
normalized_matrix = comparison_matrix / column_sums

# Cálculo dos pesos dos critérios
criteria_weights = normalized_matrix.mean(axis=1)

# Exibir pesos dos critérios
print("\nPesos dos critérios (AHP):", criteria_weights)

# Normalizar as alternativas para os 4 critérios
alternatives_array = np.array(non_dominated_points_extended)
min_values = alternatives_array.min(axis=0)
max_values = alternatives_array.max(axis=0)
normalized_alternatives = (alternatives_array - min_values) / (max_values - min_values)

# Cálculo do score final para cada alternativa
scores_ahp = normalized_alternatives @ criteria_weights

# Ranqueamento das alternativas
ranking_ahp = np.argsort(-scores_ahp)  # Ordem decrescente de scores
print("\nRanking AHP com 4 critérios:")
for i, idx in enumerate(ranking_ahp):
    print(f"{i+1}: Solução {non_dominated_points_extended[idx]} com score {scores_ahp[idx]:.4f}")


def calculate_promethee(alternatives, weights):
    num_alternatives, num_criteria = alternatives.shape
    preference_matrix = np.zeros((num_alternatives, num_alternatives, num_criteria))

    # Função de preferência linear para cada critério
    for i in range(num_alternatives):
        for j in range(num_alternatives):
            if i != j:
                preference_matrix[i, j] = np.maximum(0, alternatives[i] - alternatives[j])

    # Calcular a matriz de preferência ponderada
    weighted_preferences = preference_matrix * weights

    # Fluxo positivo (ϕ⁺) e negativo (ϕ⁻)
    phi_positive = np.sum(weighted_preferences.sum(axis=2), axis=1)  # Preferências emitidas
    phi_negative = np.sum(weighted_preferences.sum(axis=2), axis=0)  # Preferências recebidas

    # Fluxo líquido (ϕ = ϕ⁺ - ϕ⁻)
    phi_net = phi_positive - phi_negative

    return phi_net

# Pesos ajustados para os 4 critérios
criteria_weights_promethee = np.array([0.5, 0.3, 0.15, 0.05])

# Aplicar PROMETHEE
phi_net_promethee = calculate_promethee(normalized_alternatives, criteria_weights_promethee)

# Ranqueamento das alternativas
ranking_promethee = np.argsort(-phi_net_promethee)  # Ordem decrescente de fluxo líquido
print("\nRanking PROMETHEE com 4 critérios:")
for i, idx in enumerate(ranking_promethee):
    print(f"{i+1}: Solução {non_dominated_points_extended[idx]} com fluxo líquido {phi_net_promethee[idx]:.4f}")


# Calcular Robustez Geral da Solução (Rg)
robustness_scores = [(0.5 * B_sigma + 0.5 * D_sigma) for (_, _, B_sigma, D_sigma) in non_dominated_points_extended]

# Criar um novo ranking considerando Rg
ranking_robustness = np.argsort(robustness_scores)  # Ordenação crescente (menor desvio é melhor)

print("\nRanking baseado na Robustez Geral (Rg):")
for i, idx in enumerate(ranking_robustness):
    print(f"{i+1}: Solução {non_dominated_points_extended[idx]} com Rg {robustness_scores[idx]:.4f}")

# Escolher a solução final considerando todos os critérios
final_choice = non_dominated_points_extended[ranking_robustness[0]]

print("\n Solução FINAL escolhida considerando Robustez Geral:", final_choice)


# Separar os valores de P_w e P_epsilon das soluções não dominadas
P_w_values = [sol[0] for sol in non_dominated_points_extended]
P_epsilon_values = [sol[1] for sol in non_dominated_points_extended]

# Selecionar a solução escolhida automaticamente com base no ranking AHP
chosen_solution_index = np.argmax(scores_ahp)  # Índice da melhor solução no AHP
chosen_solution = non_dominated_points_extended[chosen_solution_index]

# Selecionar a melhor solução baseada na Robustez (menor R_g)
robust_solution_index = np.argmin([rg for _, _, _, rg in non_dominated_points_extended])  
robust_solution = non_dominated_points_extended[robust_solution_index]


# Criar o gráfico
plt.figure(figsize=(8,6))
plt.scatter(P_w_values, P_epsilon_values, label="Soluções Não Dominadas", color="blue")  # Todas as soluções
plt.scatter(chosen_solution[0], chosen_solution[1], color="red", s=100, label="Solução Escolhida (AHP/PROMETHEE)", edgecolors='black')  # Solução escolhida
plt.scatter(robust_solution[0], robust_solution[1], color="green", s=100, label="Melhor Robustez (R_g)", edgecolors='black')  # Solução mais robusta

# Adicionar anotações nos pontos destacados
plt.annotate("Escolhida", (chosen_solution[0], chosen_solution[1]), textcoords="offset points", xytext=(-10,10), ha='center', fontsize=10, color="red")
plt.annotate("Mais Robusta", (robust_solution[0], robust_solution[1]), textcoords="offset points", xytext=(-10,-15), ha='center', fontsize=10, color="green")

# Configurar rótulos e título
plt.xlabel("P_w (Soma Ponderada)")
plt.ylabel("P_ε (ε-Restrito)")
plt.title("Fronteira de Soluções Avaliadas na Tomada de Decisão")
plt.legend()
plt.grid(True)

# Mostrar o gráfico
plt.show()

def plot_solution_map(solution, base_coords, ativo_coords):
    """
    Plota a solução final com as bases e seus ativos conectados.

    Parâmetros:
    - solution: Dicionário contendo 'h' (matriz de alocação de ativos às equipes).
    - base_coords: Lista de coordenadas (x, y) das bases.
    - ativo_coords: Lista de coordenadas (x, y) dos ativos.
    """

    plt.figure(figsize=(8, 6))

    num_bases = solution['h'].shape[1]  # Número de bases (equipes)
    num_ativos = solution['h'].shape[0]  # Número de ativos

    # Criar listas para evitar legendas duplicadas
    legend_added = {"base_disponivel": False, "base_ocupada": False, "ativo": False}

    # Plotar todas as bases disponíveis (hexágonos vazios)
    for base in base_coords:
        if not legend_added["base_disponivel"]:
            plt.scatter(base[0], base[1], marker='p', facecolors='none', edgecolors='green', s=150, label="Bases disponível")
            legend_added["base_disponivel"] = True
        else:
            plt.scatter(base[0], base[1], marker='p', facecolors='none', edgecolors='green', s=150)

    # Plotar ativos (pontos roxos)
    for ativo in ativo_coords:
        if not legend_added["ativo"]:
            plt.scatter(ativo[0], ativo[1], color='purple', s=50, label="Ativos")
            legend_added["ativo"] = True
        else:
            plt.scatter(ativo[0], ativo[1], color='purple', s=50)

    # Adicionar conexões entre bases ocupadas e ativos atendidos
    for equipe in range(num_bases):
        ativos_atendidos = np.where(solution['h'][:, equipe] == 1)[0]  # Ativos atendidos pela equipe
        if len(ativos_atendidos) > 0:  # Se a base estiver ativa
            if not legend_added["base_ocupada"]:
                plt.scatter(base_coords[equipe][0], base_coords[equipe][1], marker='p', color='green', edgecolors='black', s=200, label="Bases ocupada")  # Base ocupada
                plt.scatter(base_coords[equipe][0], base_coords[equipe][1], color='black', s=50)  # Ponto preto dentro
                legend_added["base_ocupada"] = True
            else:
                plt.scatter(base_coords[equipe][0], base_coords[equipe][1], marker='p', color='green', edgecolors='black', s=200)  # Base ocupada
                plt.scatter(base_coords[equipe][0], base_coords[equipe][1], color='black', s=50)  # Ponto preto dentro

            # Conectar base ocupada aos ativos atendidos
            for ativo in ativos_atendidos:
                plt.plot([base_coords[equipe][0], ativo_coords[ativo][0]], 
                         [base_coords[equipe][1], ativo_coords[ativo][1]], 
                         color='blue', linestyle='-', linewidth=1)  # Linha de conexão

    # Ajustes do gráfico
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.title("Solução Final - Alocação de Equipes e Ativos")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()


# Carregar as coordenadas das bases e ativos
dist_bases_ativos, base_coordinates, ativo_coordinates = read_geolocation_data()
# Garantir que base_coords e ativo_coords são listas de tuplas
# base_coordinates = [(row[0], row[1]) for row in base_coordinates.to_numpy()]
# ativo_coordinates = [(row[0], row[1]) for row in ativo_coordinates.to_numpy()]


# Selecionar a solução final escolhida (AHP/PROMETHEE)
final_solution = best_solution_w[0]  # Pegamos a melhor solução

# Converter listas de coordenadas para DataFrames, caso plot_solution espere esse formato
df_base_coordinates = pd.DataFrame(base_coordinates, columns=['longitude_base', 'latitude_base'])
df_ativo_coordinates = pd.DataFrame(ativo_coordinates, columns=['longitude_ativo', 'latitude_ativo'])

# Chamar a função com o formato correto
plot_solution(final_solution, df_base_coordinates, df_ativo_coordinates)



