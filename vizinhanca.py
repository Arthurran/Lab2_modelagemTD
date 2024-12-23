from libs import *

import numpy as np
import copy

def trocar_ativos_entre_bases(solution, dist_bases_ativos, coords_bases):
    # Copiar a solução atual para não modificar diretamente a original
    new_solution = copy.deepcopy(solution)

    # 1. Selecionar bases ocupadas por equipes (com base em 'y')
    bases_ocupadas = np.where(new_solution['y'] == 1)[0]

    if len(bases_ocupadas) < 2:
        print("ERRO! Não há bases ocupadas suficientes para realizar a troca.")
        return solution
    
    # 2. Selecionar aleatoriamente uma das bases ocupadas
    base_1 = np.random.choice(bases_ocupadas)
    
    # 3. Selecionar um entre os três ativos mais distantes de base_1
    ativos_base_1 = np.where(new_solution['x'][:, base_1] == 1)[0]
    distancias_ativos_base_1 = dist_bases_ativos[ativos_base_1, base_1]
    ativo_selecionado = np.random.choice(np.argsort(distancias_ativos_base_1)[:3]) # Selecionar um entre tres ativos de base_1 mais distantes

    if ativo_selecionado == None:
        print("ERRO! Não há ativos em base_1.")
        return solution
    
    # 4. Selecionar a base ocupada (exceto base_1) mais próxima de ativo_selecionado
    bases_ocupadas_menos_base1 = np.setdiff1d(bases_ocupadas, [base_1])
    distancias_para_bases = dist_bases_ativos[ativo_selecionado, bases_ocupadas_menos_base1]

    # Encontrar o índice da base mais próxima do ativo selecionado
    base_ocupada_mais_proxima_idx = np.argmin(distancias_para_bases)
    base_ocupada_mais_proxima = bases_ocupadas_menos_base1[base_ocupada_mais_proxima_idx]

    # 5. Alterar a alocação do ativo e da equipe
    # Remover o ativo da base de origem
    new_solution['x'][ativo_selecionado, base_1] = 0
    # Atribuir o ativo à nova base (base_2)
    new_solution['x'][ativo_selecionado, base_ocupada_mais_proxima] = 1
    
    # Alterar a equipe do ativo
    # Verificando se o ativo está alocado a alguma equipe
    indices_equipes = np.where(new_solution['h'][ativo_selecionado, :] == 1)[0]

    # Se não houver equipe atribuída ao ativo, podemos lidar com isso
    if len(indices_equipes) == 0:
        print(f"Erro: O ativo {ativo_selecionado} não está alocado a nenhuma equipe.")
        return solution

    # Caso contrário, atribuir a equipe corretamente
    equipe_antiga_ativo_selecionado = indices_equipes[0]
    
    # Remover o ativo da equipe atual
    new_solution['h'][ativo_selecionado, equipe_antiga_ativo_selecionado] = 0
    # Atribuir o ativo à nova equipe da base_2
    nova_equipe_ativo_selecionado = np.random.choice(np.where(new_solution['y'][base_ocupada_mais_proxima, :] == 1)[0]) 
    new_solution['h'][ativo_selecionado, nova_equipe_ativo_selecionado] = 1

    # Retornar a nova solução com a troca realizada
    return new_solution

def trocar_equipes_de_bases(solution, dist_bases_ativos, coords_bases):
    # Copiar a solução para criar uma nova
    new_solution = copy.deepcopy(solution) 
    
    # Pegar bases ativas (bases com equipes alocadas)
    bases_com_equipes = np.where(np.sum(new_solution['y'], axis=1) > 0)[0]

    # Inicializa um dicionário para armazenar a soma total das distâncias para cada base
    bases_total_distancia = {}

    # Selecionar aleatoriamente uma base entre as ocupadas
    if len(bases_com_equipes) == 0:
        print("Nenhuma base ocupada por equipes encontrada.")
        return solution  # Retorna a solução original se não houver bases ocupadas
    
    maior_base = np.random.choice(bases_com_equipes)
    coords_maior_base = coords_bases.loc[maior_base, ['latitude_base', 'longitude_base']].values

    todas_as_bases = set(range(dist_bases_ativos.shape[1]))
    bases_disponiveis = list(todas_as_bases - set(bases_com_equipes))

    # Calcular a distância euclidiana para cada base disponível
    distancias_disponiveis = {}
    for base_disponivel in bases_disponiveis:
        coords_base_disponivel = coords_bases.loc[base_disponivel, ['latitude_base', 'longitude_base']].values
        # Distancia das bases à 'maior_base' 
        distancia = np.sqrt(
            (coords_base_disponivel[0] - coords_maior_base[0])**2 + 
            (coords_base_disponivel[1] - coords_maior_base[1])**2
        )
        distancias_disponiveis[base_disponivel] = distancia

    # Ordenar as bases disponíveis pelas distâncias à maior base (opcional)
    bases_mais_proximas = sorted(distancias_disponiveis.items(), key=lambda x: x[1])

    # Selecionar aleatoriamente um índice entre as três bases mais próximas
    indices_mais_proximos = [base[0] for base in bases_mais_proximas[:3]]
    base_selecionada = random.choice(indices_mais_proximos)

    #atribuir equipe da 'maior_base' para 'nova_base'
    equipe_associada = np.where(new_solution['y'][maior_base, :] == 1)[0]
    if len(equipe_associada) > 0:
        k = equipe_associada[0]  # Assumindo que há uma única equipe associada

        # Atribuir a equipe `k` à `base_selecionada`
        new_solution['y'][maior_base, k] = 0  # Remove a equipe da maior_base
        new_solution['y'][base_selecionada, k] = 1  # Atribui a equipe à nova base selecionada

        # Realocar os ativos da maior_base para a base_selecionada
        ativos_da_base = np.where(new_solution['x'][:, maior_base] == 1)[0]
        for ativo in ativos_da_base:
            new_solution['x'][ativo, maior_base] = 0  # Remove ativo da maior_base
            new_solution['x'][ativo, base_selecionada] = 1  # Atribui ativo à nova base
    else:
        print(f"Nenhuma equipe associada à base {maior_base}.")
    
    return new_solution

import numpy as np
import copy

def balancear_ativos_entre_equipes(solution, dist_bases_ativos): 
    new_solution = copy.deepcopy(solution) 

    # 1. Identificar a equipe com mais ativos e a equipe com menos ativos
    ativos_por_equipe = np.sum(new_solution['h'], axis=0)  # Número de ativos por equipe
    
    equipe_com_mais_ativos = np.argmax(ativos_por_equipe)  
    equipe_com_menos_ativos = np.argmin(ativos_por_equipe) 

    # 2. Selecionar os ativos da equipe com mais ativos
    ativos_da_equipe_com_mais = np.where(new_solution['h'][:, equipe_com_mais_ativos] == 1)[0]
    
    if len(ativos_da_equipe_com_mais) == 0:
        print("Erro: Não há ativos na equipe com mais ativos.")
        return solution

    # 3. Obter a base da equipe com mais ativos
    # Encontrar a base onde o ativo da equipe com mais ativos está alocado
    base_atual_ativo = np.where(new_solution['x'][ativos_da_equipe_com_mais, :] == 1)[1]
    
    if len(base_atual_ativo) == 0:
        print("Erro: Não foi possível encontrar a base do ativo.")
        return solution

    # 4. Calcular as distâncias dos ativos da equipe com mais ativos à base da equipe com mais ativos
    distancias_ativos_para_base = dist_bases_ativos[ativos_da_equipe_com_mais, base_atual_ativo[0]]
    
    # 5. Selecionar aleatoriamente um entre os cinco ativos mais próximos com base nas distâncias calculadas
    ativos_proximos = np.argsort(distancias_ativos_para_base)[:5]
    ativo_selecionado = np.random.choice(ativos_da_equipe_com_mais[ativos_proximos])
    
    # 6. Atribuir ativo da equipe com mais ativos para a equipe com menos ativos
    new_solution['h'][ativo_selecionado, equipe_com_mais_ativos] = 0
    new_solution['h'][ativo_selecionado, equipe_com_menos_ativos] = 1
    
    # 7. Atribuir o ativo da base da equipe com mais ativos para a base da equipe com menos ativos
    base_destino = np.where(new_solution['y'][:, equipe_com_menos_ativos] == 1)[0][0]  # Seleciona uma base da equipe com menos ativos
    new_solution['x'][ativo_selecionado, base_atual_ativo[0]] = 0  # Remove da base atual
    new_solution['x'][ativo_selecionado, base_destino] = 1  # Atribui à nova base

    # 8. Retornar a nova solução com a transferência realizada
    return new_solution

def neighborhood_change(solution,neighborhood,dist_bases_ativos, coords_bases):
  
    #if obj_function == 1:
    match neighborhood:
        case 1:
            return trocar_equipes_de_bases(solution,dist_bases_ativos,coords_bases)
        case 2:
            return trocar_ativos_entre_bases(solution,dist_bases_ativos,coords_bases)
        #case 3:
            #return balancear_ativos_entre_equipes(solution,dist_bases_ativos)
    """
    elif obj_function == 2:
        match neighborhood:
            case 1:
                return trocar_equipes_de_bases(solution,dist_bases_ativos,coords_bases)
            case 2:
                return trocar_ativos_entre_bases(solution,dist_bases_ativos,coords_bases)
            case 3:
                return balancear_ativos_entre_equipes(solution,dist_bases_ativos)
    """