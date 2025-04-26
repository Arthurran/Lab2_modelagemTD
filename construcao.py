from libs import *
import libs
#import constraints
from plot import plot_solution

# Função para gerar uma solução base
def generate_solution():
    # print("Gerar solucao")
    # Inicialize as variáveis de decisão
    # 'distancias_bases_ativos':np.zeros((num_ativos, num_bases)) # armazena as distâncias dos ativos "i" às bases "j"
    # distancias_bases_ativos pode ser fixo, de modo a ser utilizado apenas para consulta das distâncias

    solution = {
        # Pico de fila
        # Qtd de servidores
        # vetor[servidores x nos]
        # Qtd de pacientes no nó n
        # Disponibilidade do nó = vetor de 
        
        'servidores':np.zeros((num_nos)) # Numero de servidores x No
        'penalty': np.zeros(0), # Armazena a penalidade da solução
        'fitness': np.zeros(0), # Armazena o ajuste da solucao
    }

    if prob_ativos is not None:
        return solucao_inicial3(solution, distancia_bases_ativos, prob_ativos)

    print("SOLUÇÃO INICIAL1")
    return solution

def solucao_inicial2(solution, distancia_bases_ativos, prob_ativos):
    print("SOLUÇÃO INICIAL2")

    #(1) Calcular a soma das distâncias para os 15 ativos mais próximos de cada base
    soma_distancias_bases = []
    for base in range(num_bases):
        # Ordenar as distâncias dos 20 ativos para a base atual
        distancias_ordenadas = np.sort(distancia_bases_ativos[:20, base])
        # Somar as distâncias dos ativos mais próximos
        soma_distancias = np.sum(distancias_ordenadas[:20])
        soma_distancias_bases.append((base, soma_distancias))

    # Ordenar as bases pela soma das distâncias (ordem crescente)
    soma_distancias_bases.sort(key=lambda x: x[1])

    # Selecionar as seis bases com a menor soma de distâncias
    top_6_bases = [item[0] for item in soma_distancias_bases[:6]]

    # Distribuir bases entre equipes 
    bases_ocupadas = random.sample(top_6_bases, k=num_equipes)

    #(2) Atribuir as equipes às bases selecionadas
    for equipe, base in enumerate(bases_ocupadas):
        solution['y'][base, equipe] = 1  # Marca que a equipe ocupa a base

    #(3) Distribuir os ativos entre as equipes
    distancias_bases_ocupadas = distancia_bases_ativos[:, bases_ocupadas]
    # Adicionar o index do ativo na coluna
    rows_indices = np.arange(distancias_bases_ocupadas.shape[0], dtype=int).reshape(-1, 1)
    dist_bases_ocupadas_com_index = np.hstack((rows_indices, distancias_bases_ocupadas))

    # Atribui ativos às bases (1 base por vez) 
    while dist_bases_ocupadas_com_index.shape[0] > 0:
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
            solution['x'][index_ativo_mais_proximo, bases_ocupadas[base_index-1]] = 1  # Atribui o ativo à base

            equipe_responsavel = np.argmax(solution['y'][bases_ocupadas[base_index-1]])  # Identifica a equipe da base
            solution['h'][index_ativo_mais_proximo, equipe_responsavel] = 1  # Marca que o ativo é mantido pela equipe

            # Delete the corresponding row from the matrix (now the matrix is updating)
            dist_bases_ocupadas_com_index = np.delete(dist_bases_ocupadas_com_index, ativo_mais_proximo, axis=0)

    print("Solução inicial gerada com sucesso.")
    return solution

def solucao_inicial3(solution, distancia_bases_ativos, prob_ativos):
    # print("SOLUÇÃO INICIAL3")

    #(1) Calcular a soma das distâncias para os 15 ativos mais próximos de cada base
    soma_distancias_bases = []
    for base in range(num_bases):
        # Ordenar as distâncias dos 15 ativos para a base atual
        distancias_ordenadas = np.sort(distancia_bases_ativos[:15, base])
        # Somar as distâncias dos ativos mais próximos
        soma_distancias = np.sum(distancias_ordenadas[:15])
        soma_distancias_bases.append((base, soma_distancias))

    # Ordenar as bases pela soma das distâncias (ordem crescente)
    soma_distancias_bases.sort(key=lambda x: x[1])

    # Selecionar as seis bases com a menor soma de distâncias
    top_6_bases = [item[0] for item in soma_distancias_bases[:6]]

    # Distribuir bases entre equipes 
    bases_ocupadas = random.sample(top_6_bases, k=num_equipes)

    #(2) Atribuir as equipes às bases selecionadas
    for equipe, base in enumerate(bases_ocupadas):
        solution['y'][base, equipe] = 1  # Marca que a equipe ocupa a base

    #(3) Distribuir os ativos entre as equipes
    distancias_bases_ocupadas = distancia_bases_ativos[:, bases_ocupadas]
    # Adicionar o index do ativo na coluna
    rows_indices = np.arange(distancias_bases_ocupadas.shape[0], dtype=int).reshape(-1, 1)
    dist_bases_ocupadas_com_index = np.hstack((rows_indices, distancias_bases_ocupadas))

    # Atribui ativos às bases (1 base por vez) até todos as bases possuírem o mínimo de ativos (30 para eta=0.7)
    while dist_bases_ocupadas_com_index.shape[0] > (num_ativos-((math.ceil(eta * (num_ativos / num_equipes))*num_equipes))-8):
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
            solution['x'][index_ativo_mais_proximo, bases_ocupadas[base_index-1]] = 1  # Atribui o ativo à base

            equipe_responsavel = np.argmax(solution['y'][bases_ocupadas[base_index-1]])  # Identifica a equipe da base
            solution['h'][index_ativo_mais_proximo, equipe_responsavel] = 1  # Marca que o ativo é mantido pela equipe

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
        solution['x'][index_ativo_mais_proximo, bases_ocupadas[base_index]] = 1  # Atribui o ativo à base

        equipe_responsavel = np.argmax(solution['y'][bases_ocupadas[base_index]])  # Identifica a equipe da base
        solution['h'][index_ativo_mais_proximo, equipe_responsavel] = 1  # Marca que o ativo é mantido pela equipe

        # Delete the corresponding row from the matrix (now the matrix is updating)
        dist_bases_ocupadas_com_index = np.delete(dist_bases_ocupadas_com_index, 0, axis=0)

    # print("Solução inicial gerada com sucesso.")
    return solution