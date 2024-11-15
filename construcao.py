from libs import *
import libs
#import constraints
from plot import plot_solution

# Carrega os dados do arquivo CSV
def read_geolocation_data():
    # Lê o arquivo CSV
    df = pd.read_csv('probdata.csv',delimiter=';',header=None,decimal=',')
    
    # Renomeia as colunas para facilitar a leitura
    df.columns = ['latitude_base', 'longitude_base', 'latitude_ativo', 'longitude_ativo', 'distancia']
    
    # Identifica as bases de apoio e pontos de cliente únicos
    bases_unicas = df[['latitude_base', 'longitude_base']].drop_duplicates().reset_index(drop=True)
    ativos_unicos = df[['latitude_ativo', 'longitude_ativo']].drop_duplicates().reset_index(drop=True)
    
    # Calcula o número de clientes (ativos) e bases
    num_ativos = len(ativos_unicos)
    num_bases = len(bases_unicas)
    
    # Cria um dicionário para mapear bases e clientes aos seus índices
    base_indices = {tuple(base): idx for idx, base in bases_unicas.iterrows()}
    ativos_indices = {tuple(cliente): idx for idx, cliente in ativos_unicos.iterrows()}
    
    # Inicializa a matriz de distâncias dos ativos às bases
    distancias_bases_ativos = np.zeros((num_ativos, num_bases))
    
    # Preenche a matriz de distâncias
    for _, row in df.iterrows():
        ativos_idx = ativos_indices[(row['latitude_ativo'], row['longitude_ativo'])]
        base_idx = base_indices[(row['latitude_base'], row['longitude_base'])]
        distancias_bases_ativos[ativos_idx, base_idx] = row['distancia']

    # Preenche a matriz de coordenadas das bases
    #coords_bases = bases_unicas.to_numpy()
    #coords_ativos = ativos_unicos.to_numpy()
    
    return distancias_bases_ativos, bases_unicas, ativos_unicos

# Função para gerar uma solução base
def generate_solution(distancia_bases_ativos, funcao_obj):
    print("Gerar solucao")
    # Inicialize as variáveis de decisão
    # 'distancias_bases_ativos':np.zeros((num_ativos, num_bases)) # armazena as distâncias dos ativos "i" às bases "j"
    # distancias_bases_ativos pode ser fixo, de modo a ser utilizado apenas para consulta das distâncias

    solution = {
        'x':np.zeros((num_ativos, num_bases)), # atribuição de ativo "i" à base "j"
        'y':np.zeros((num_bases, num_equipes)), # ocupação de base "j" por equipe "k"
        'h':np.zeros((num_ativos, num_equipes)), # ativo "i" mantido por equipe "k"
        'penalty': np.zeros(0), # Armazena a penalidade da solução
        'fitness': np.zeros(0), # Armazena o ajuste da solução
        'penalty_fitness': np.zeros(0), # Armazena o ajuste somado a penalidade da solução
    }

    if funcao_obj == 1:
        return solucao_inicial1(solution, distancia_bases_ativos)
    #elif funcao_obj == 2:
        #return solucao_inicial2(solution)
    else:
        print("ERRO! Função objetivo não informada, heurística construtiva não aplicada")
        exit()

def solucao_inicial1(solution, distancia_bases_ativos):
    print("SOLUÇÃO INICIAL1")

    #(1) Calcular a soma das distâncias para os 100 ativos mais próximos de cada base
    soma_distancias_bases = []
    for base in range(num_bases):
        # Ordenar as distâncias dos ativos para a base atual
        distancias_ordenadas = np.sort(distancia_bases_ativos[:, base])
        # Somar as distâncias dos 100 ativos mais próximos
        soma_distancias = np.sum(distancias_ordenadas[:100])
        soma_distancias_bases.append((base, soma_distancias))

    # Ordenar as bases pela soma das distâncias (ordem crescente)
    soma_distancias_bases.sort(key=lambda x: x[1])

    # Selecionar as três bases com a menor soma de distâncias
    bases_ocupadas = [item[0] for item in soma_distancias_bases[:num_equipes]]

    #(2) Atribuir as equipes às bases selecionadas
    for equipe, base in enumerate(bases_ocupadas):
        solution['y'][base, equipe] = 1  # Marca que a equipe ocupa a base

    #(3) Atribuir cada ativo à base ocupada mais próxima
    for ativo in range(num_ativos):
        # Seleciona apenas as distâncias para as bases ocupadas
        distancias_para_ocupadas = distancia_bases_ativos[ativo, bases_ocupadas]
        # Encontra a base ocupada mais próxima
        base_mais_proxima_idx = np.argmin(distancias_para_ocupadas)
        base_mais_proxima = bases_ocupadas[base_mais_proxima_idx]
        solution['x'][ativo, base_mais_proxima] = 1  # Atribui o ativo à base

        equipe_responsavel = np.argmax(solution['y'][base_mais_proxima])  # Identifica a equipe da base
        solution['h'][ativo, equipe_responsavel] = 1  # Marca que o ativo é mantido pela equipe

    print("Solução inicial gerada com sucesso.")
    return solution


