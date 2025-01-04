from libs import *

import numpy as np
import copy

def swap_ativos_entre_bases(solution, dist_bases_ativos, coords_bases):
    # Copiar a solução atual para não modificar diretamente a original
    new_solution = copy.deepcopy(solution)

    # 1. Selecionar equipe1 para swap (alguma equipe que não seja a com menos ativos
    equipe1_para_swap = np.random.randint(0, num_equipes)

    # 2. Obter ativos de equipe1 
    ativos_equipe1 = np.where(new_solution['h'][:,equipe1_para_swap]==1)[0]

    # 3. Obter bases de equipes
    bases_equipes = []
    for equipe in range(new_solution['y'].shape[1]):  # Iterar por colunas (equipes)
        base_ocupada = np.where(new_solution['y'][:, equipe] == 1)[0]
        if base_ocupada.size > 0:  # Adicionar base ocupada apenas se existir
            bases_equipes.append(base_ocupada[0])

    bases_equipes = np.array(bases_equipes)
    
    # 4. Percorrer ativos de equipe1 e comparar distâncias a outras bases de outras equipes
    isSwap = False
    equipe2_para_swap = 0
    for ativo in ativos_equipe1:
        distancias = []
        for base in bases_equipes:
            #obtenção de distâncias de bases com equipes a ativo de equipe1
            dist = dist_bases_ativos[ativo,base]
            distancias = np.append(distancias, dist)
        
        if np.argmin(distancias) != equipe1_para_swap:
            isSwap = True
            #print("SWAP1:\n")
            equipe2_para_swap = np.argmin(distancias)
            base_equipe1 = bases_equipes[equipe1_para_swap]
            base_equipe2 = bases_equipes[equipe2_para_swap]

            # Trocar ativo de equipe1 para equipe2
            new_solution['h'][ativo, equipe1_para_swap] = 0
            new_solution['h'][ativo, equipe2_para_swap] = 1

            # Trocar ativo de base de equipe1 para base de equipe2
            new_solution['x'][ativo, base_equipe1] = 0
            new_solution['x'][ativo, base_equipe2] = 1

            break
    
    # 5. Verificar se não há algum ativo de equipe2 para ser transferido a equipe1 
    if isSwap:
        ativos_equipe2 = np.where(solution['h'][:,equipe2_para_swap]==1)[0]
        # Percorrer ativos de equipe2 e comparar distâncias a outras bases de outras equipes
        for ativo in ativos_equipe2:
            distancias = []
            for base in bases_equipes:
                #obtenção de distâncias de bases com equipes a ativo de equipe1
                dist = dist_bases_ativos[ativo,base]
                distancias = np.append(distancias, dist)
                
            if (np.argmin(distancias) != equipe2_para_swap) and (np.argmin(distancias) == equipe1_para_swap):
                base_equipe2 = bases_equipes[equipe2_para_swap]
                base_equipe1 = bases_equipes[equipe1_para_swap]
                #print("SWAP2:\n")
        
                # Trocar ativo de equipe1 para equipe2
                new_solution['h'][ativo,equipe2_para_swap] = 0
                new_solution['h'][ativo,equipe1_para_swap] = 1

                # Trocar ativo de base de equipe1 para base de equipe2
                new_solution['x'][ativo,base_equipe2] = 0
                new_solution['x'][ativo,base_equipe1] = 1

                if(np.sum(new_solution['h'][:, equipe1_para_swap],axis=0) == np.sum(new_solution['x'][:, base_equipe1],axis=0)):
                    if np.sum(new_solution['h'][:, equipe1_para_swap],axis=0) < 30:
                        exit()
                break
    return new_solution
    

def trocar_ativos_entre_bases2(solution, dist_bases_ativos, coords_bases):

    # Copiar a solução atual para não modificar diretamente a original
    new_solution = copy.deepcopy(solution)

    # 1. Selecionar bases ocupadas por equipes (com base em 'y')
    bases_ocupadas = np.where(new_solution['y'] == 1)[0]

    if len(bases_ocupadas) < 2:
        print("ERRO! Não há bases ocupadas suficientes para realizar a troca.")
        return solution
    
    # 2. Selecionar aleatoriamente uma das bases ocupadas
    base_1 = np.random.choice(bases_ocupadas)

    # 3. Selecionar o ativo mais distante de base_1
    ativos_base_1 = np.where(new_solution['x'][:, base_1] == 1)[0]
    distancias_ativos_base_1 = dist_bases_ativos[ativos_base_1, base_1]
    ativo_mais_distante = np.random.choice(np.argsort(distancias_ativos_base_1)[0]) # Selecionar o ativo de base_1 mais distante

    if ativo_mais_distante == None:
        print("ERRO! Não há ativos em base_1.")
        return solution
    
    # 4. Selecionar a base ocupada (exceto base_1) mais próxima de ativo_selecionado
    bases_ocupadas_menos_base1 = np.setdiff1d(bases_ocupadas, [base_1])
    distancias_para_bases = dist_bases_ativos[ativo_mais_distante, bases_ocupadas_menos_base1]

    # Encontrar o índice da base mais próxima do ativo selecionado
    base_ocupada_mais_proxima_idx = np.argmin(distancias_para_bases)
    base_ocupada_mais_proxima = bases_ocupadas_menos_base1[base_ocupada_mais_proxima_idx]

    # 5. Alterar a alocação do ativo e da equipe
    # Remover o ativo da base de origem
    new_solution['x'][ativo_mais_distante, base_1] = 0
    # Atribuir o ativo à nova base (base_2)
    new_solution['x'][ativo_mais_distante, base_ocupada_mais_proxima] = 1
    
    # Alterar a equipe do ativo
    # Verificando se o ativo está alocado a alguma equipe
    indices_equipes = np.where(new_solution['h'][ativo_mais_distante, :] == 1)[0]

    # Se não houver equipe atribuída ao ativo, podemos lidar com isso
    if len(indices_equipes) == 0:
        print(f"Erro: O ativo {ativo_mais_distante} não está alocado a nenhuma equipe.")
        return solution

    # Caso contrário, atribuir a equipe corretamente
    equipe_antiga_ativo_selecionado = indices_equipes[0]
    
    # Remover o ativo da equipe atual
    new_solution['h'][ativo_mais_distante, equipe_antiga_ativo_selecionado] = 0
    # Atribuir o ativo à nova equipe da base_2
    nova_equipe_ativo_selecionado = np.random.choice(np.where(new_solution['y'][base_ocupada_mais_proxima, :] == 1)[0]) 
    new_solution['h'][ativo_mais_distante, nova_equipe_ativo_selecionado] = 1

    return new_solution

def trocar_equipes_de_bases2(solution, dist_bases_ativos, coords_bases):
    # Copiar a solução para criar uma nova
    new_solution = copy.deepcopy(solution) 
    
    # Pegar bases ativas (bases com equipes alocadas)
    bases_com_equipes = np.where(np.sum(new_solution['y'], axis=1) > 0)[0]

    # Selecionar aleatoriamente uma base entre as ocupadas
    if len(bases_com_equipes) == 0:
        print("Nenhuma base ocupada por equipes encontrada.")
        return solution  # Retorna a solução original se não houver bases ocupadas
    
    base_a_desocupar = np.random.choice(bases_com_equipes)

    todas_as_bases = set(range(dist_bases_ativos.shape[1]))
    bases_disponiveis = list(todas_as_bases - set(bases_com_equipes))

    # selecionar uma base aleatoria (sem equipe alocada) dentre as seis com menor soma de distâncias
    soma_distancias_bases = []
    for base_disponivel in bases_disponiveis:
        # Ordenar as distâncias dos 15 ativos para a base atual
        distancias_ordenadas = np.sort(dist_bases_ativos[:15, base_disponivel])
        # Somar as distâncias dos ativos mais próximos
        soma_distancias = np.sum(distancias_ordenadas[:15])
        soma_distancias_bases.append((base_disponivel, soma_distancias))

    # Selecionar as seis bases não ocupadas com a menor soma de distâncias e escolhe uma base
    top_6_bases = [item[0] for item in soma_distancias_bases[:6]]
    base_a_ocupar = np.random.choice(top_6_bases)

    # Atribui equipe de base_escolhida
    equipe_associada = np.where(new_solution['y'][base_a_desocupar, :] == 1)[0]
    if len(equipe_associada) > 0:
        k = equipe_associada[0]  # Assumindo que há uma única equipe associada

        # Atribuir a equipe `k` à `base_selecionada`
        new_solution['y'][base_a_desocupar, k] = 0  # Remove a equipe da maior_base
        new_solution['y'][base_a_ocupar, k] = 1  # Atribui a equipe à nova base selecionada

        # Rearranjar os ativos tal como na construção
        bases_com_equipes = np.where(np.sum(new_solution['y'], axis=1) > 0)[0]

        new_solution['x'] = np.zeros((num_ativos, num_bases)) # desassociação de ativos para bases
        new_solution['h'] = np.zeros((num_ativos, num_equipes)) # desassociação de ativos para equipes

        distancias_bases_ocupadas = dist_bases_ativos[:, bases_com_equipes]
        # Adicionar o index do ativo na coluna
        rows_indices = np.arange(distancias_bases_ocupadas.shape[0], dtype=int).reshape(-1, 1)
        dist_bases_ocupadas_com_index = np.hstack((rows_indices, distancias_bases_ocupadas))

        # Atribui ativos às bases (1 base por vez) até todos as bases possuírem o mínimo de ativos (30 para eta=0.7)
        while dist_bases_ocupadas_com_index.shape[0] > (num_ativos-((math.ceil(eta * (num_ativos / num_equipes))*num_equipes))-12):
            for base_index in range(1, dist_bases_ocupadas_com_index.shape[1]):  # Start from the second column
                # Check if the matrix becomes empty
                if dist_bases_ocupadas_com_index.shape[0] == 0:
                    break

                # Get the column excluding the index (first column)
                distancias_ativos_a_base = dist_bases_ocupadas_com_index[:, base_index]

                # Obtêm o index do ativo na matriz
                ativo_mais_proximo = np.argmin(distancias_ativos_a_base)

                # Obtêm o index original do ativo
                index_ativo_mais_proximo = int(dist_bases_ocupadas_com_index[ativo_mais_proximo,0])

                # Atribuir ativo a base e equipe
                new_solution['x'][index_ativo_mais_proximo, bases_com_equipes[base_index-1]] = 1  # Atribui o ativo à base

                equipe_responsavel = np.argmax(new_solution['y'][bases_com_equipes[base_index-1]])  # Identifica a equipe da base
                new_solution['h'][index_ativo_mais_proximo, equipe_responsavel] = 1  # Marca que o ativo é mantido pela equipe

                # Delete the corresponding row from the matrix (now the matrix is updating)
                dist_bases_ocupadas_com_index = np.delete(dist_bases_ocupadas_com_index, ativo_mais_proximo, axis=0)

        #Atribui ativos a bases ocupadas mais próximas não importando o balanceio 
        while dist_bases_ocupadas_com_index.shape[0] > 0:    
            # Check if the matrix becomes empty
            if dist_bases_ocupadas_com_index.shape[0] == 0:
                break

            # Pega primeira linha da matriz de distâncias e define em qual base(coluna) está o menor valor de distâncias
            distancia_bases_a_ativo = dist_bases_ocupadas_com_index[0,1:]
            base_index = np.argmin(distancia_bases_a_ativo)

            # Obtêm o index original do ativo
            index_ativo_mais_proximo = int(dist_bases_ocupadas_com_index[0,0])

            # Atribuir ativo a base e equipe
            new_solution['x'][index_ativo_mais_proximo, bases_com_equipes[base_index]] = 1  # Atribui o ativo à base

            equipe_responsavel = np.argmax(new_solution['y'][bases_com_equipes[base_index]])  # Identifica a equipe da base
            new_solution['h'][index_ativo_mais_proximo, equipe_responsavel] = 1  # Marca que o ativo é mantido pela equipe

            # Delete the corresponding row from the matrix (now the matrix is updating)
            dist_bases_ocupadas_com_index = np.delete(dist_bases_ocupadas_com_index, 0, axis=0)

            """ativos_da_base = np.where(new_solution['x'][:, base_a_desocupar] == 1)[0]
            for ativo in ativos_da_base:
                new_solution['x'][ativo, base_a_desocupar] = 0  # Remove ativo da maior_base
                new_solution['x'][ativo, base_a_ocupar] = 1  # Atribui ativo à nova base
            """
    else:
        print(f"Nenhuma equipe associada à base {base_a_desocupar}.")

    return new_solution

import numpy as np
import copy

def neighborhood_change(solution,neighborhood,dist_bases_ativos, coords_bases):
  
    #if obj_function == 1:
    match neighborhood:
        case 1:
            return swap_ativos_entre_bases(solution,dist_bases_ativos,coords_bases)
        case 2:
            return trocar_equipes_de_bases2(solution,dist_bases_ativos,coords_bases)
        #case 3:
            #return trocar_equipes_de_bases2(solution,dist_bases_ativos,coords_bases)
    """
    elif obj_function == 2: swap_ativos_entre_bases(solution,dist_bases_ativos,coords_bases)
        match neighborhood:
            case 1:
                return trocar_equipes_de_bases(solution,dist_bases_ativos,coords_bases)
            case 2:
                return trocar_ativos_entre_bases2(solution,dist_bases_ativos,coords_bases)
            case 3:
                return balancear_ativos_entre_equipes(solution,dist_bases_ativos)
    """