from libs import *

def trocar_ativos_entre_bases(solution, dist_bases_ativos):
# Copiar a solução atual para não modificar diretamente a original
    new_solution = copy.deepcopy(solution) 

    # 1. Selecionar duas bases ocupadas por equipes (com base em 'y')
    bases_ocupadas = np.where(new_solution['y'] == 1)[0]

    if len(bases_ocupadas) < 2:
        print("Não há bases ocupadas suficientes para realizar a troca.")
        return new_solution
    
    # Selecionar aleatoriamente duas bases ocupadas
    base_1, base_2 = np.random.choice(bases_ocupadas, size=2, replace=False)

    # 2. Selecionar a base com mais ativos associados
    ativos_base_1 = np.where(new_solution['x'][:, base_1] == 1)[0]  # Ativos alocados à base 1
    ativos_base_2 = np.where(new_solution['x'][:, base_2] == 1)[0]  # Ativos alocados à base 2

    if len(ativos_base_1) > len(ativos_base_2):
        base_a_perder_ativo = base_1
        ativos_base_a_perder = ativos_base_1
        base_receber_ativo = base_2
    else:
        base_a_perder_ativo = base_2
        ativos_base_a_perder = ativos_base_2
        base_receber_ativo = base_1

    # 3. Selecionar os 5 ativos com menor valor de distância para a base que irá receber o ativo
    distancias_base_receber = dist_bases_ativos[ativos_base_a_perder, base_receber_ativo]
    # Obter os 5 ativos mais próximos
    ativos_proximos = np.argsort(distancias_base_receber)[:5]

    # 4. Selecionar aleatoriamente 1 ativo entre os 5 selecionados
    ativo_selecionado = np.random.choice(ativos_proximos)

    # 5. Alterar a alocação do ativo e da equipe
    # Remover o ativo da base de origem
    new_solution['x'][ativo_selecionado, base_a_perder_ativo] = 0
    # Atribuir o ativo à nova base
    new_solution['x'][ativo_selecionado, base_receber_ativo] = 1
    
    # Alterar a equipe do ativo
    # Precisamos encontrar a equipe associada a esse ativo na base original
    equipe_atual = np.where(new_solution['h'][ativo_selecionado, :] == 1)[0][0]
    # Alterar a equipe do ativo para a base de destino
    new_solution['h'][ativo_selecionado, equipe_atual] = 0
    nova_equipe = np.random.choice(np.where(new_solution['y'][base_receber_ativo,:] == 1)[0])  # Equipe alocada à base de destino
    new_solution['h'][ativo_selecionado, nova_equipe] = 1

    # Retornar a nova solução com a troca realizada
    return new_solution

def trocar_equipes_de_bases(solution, dist_bases_ativos):
    # Copiar a solução para criar uma nova
    new_solution = copy.deepcopy(solution) 
    
    # Pegar bases ativas (bases com equipes alocadas)
    bases_com_equipes = np.where(np.sum(new_solution['y'], axis=1) > 0)[0]

    # Inicializa um dicionário para armazenar a soma total das distâncias para cada base
    bases_total_distancia = {}

    # Itera sobre cada base ativa
    for base in bases_com_equipes:
        # Pega os ativos alocados à base
        ativos_da_base = np.where(solution['x'][:, base] == 1)[0]

        # Calcula a soma das distâncias dos ativos para a base
        soma_distancia = 0
        if len(ativos_da_base) > 0:
            for ativo in ativos_da_base:
                soma_distancia += dist_bases_ativos[ativo, base]

        # Armazena a soma da distância para a base
        bases_total_distancia[base] = soma_distancia

    # Ordenar as bases pelo total de distância e pegar as duas maiores
    bases_ordenadas = sorted(bases_total_distancia.items(), key=lambda x: x[1], reverse=True)
    duas_maiores_bases = bases_ordenadas[:2]

    # Selecionar duas bases aleatórias diferentes das maiores bases
    todas_as_bases = set(range(dist_bases_ativos.shape[1]))
    bases_disponiveis = list(todas_as_bases - set(bases_com_equipes))
    novas_bases = random.sample(bases_disponiveis, 2)

    # Realocar os ativos das duas maiores bases para as novas bases
    for i, base_antiga in enumerate(duas_maiores_bases):
        nova_base = novas_bases[i]
        ativos_da_base_antiga = np.where(new_solution['x'][:, base_antiga] == 1)[0]

        # Atualizar a alocação dos ativos para a nova base
        for ativo in ativos_da_base_antiga:
            new_solution['x'][ativo, base_antiga] = 0  # Remove o ativo da base antiga
            new_solution['x'][ativo, nova_base] = 1    # Aloca o ativo na nova base

    return new_solution



def neighborhood_change(solution,neighborhood,obj_function,dist_bases_ativos):
  
    if obj_function == 1:
        match neighborhood:
            case 1:
                return trocar_ativos_entre_bases(solution,dist_bases_ativos)
            case 2:
                return trocar_equipes_de_bases(solution,dist_bases_ativos)
            case 3:
                return solution

    """elif obj_function == 2:
        match neighborhood:
            case 1:
                return swap_clients_between_pas(solution)
            case 2:
                return shift_pa_positions(solution)
            case 3:
                return move_pa_solution(solution)
    """