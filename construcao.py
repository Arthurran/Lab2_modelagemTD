from libs import *
import constraints
from plot import plot_solution

# Carrega os dados do arquivo CSV
def get_distancias_bases_ativos(nome_arquivo):
    # Lê o arquivo CSV
    df = pd.read_csv(nome_arquivo, header=None)
    
    # Renomeia as colunas para facilitar a leitura
    df.columns = ['latitude_base', 'longitude_base', 'latitude_cliente', 'longitude_cliente', 'distancia']
    
    # Identifica as bases de apoio e pontos de cliente únicos
    bases_unicas = df[['latitude_base', 'longitude_base']].drop_duplicates().reset_index(drop=True)
    clientes_unicos = df[['latitude_cliente', 'longitude_cliente']].drop_duplicates().reset_index(drop=True)
    
    # Calcula o número de clientes (ativos) e bases
    num_ativos = len(clientes_unicos)
    num_bases = len(bases_unicas)
    
    # Cria um dicionário para mapear bases e clientes aos seus índices
    base_indices = {tuple(base): idx for idx, base in bases_unicas.iterrows()}
    cliente_indices = {tuple(cliente): idx for idx, cliente in clientes_unicos.iterrows()}
    
    # Inicializa a matriz de distâncias dos ativos às bases
    distancias_bases_ativos = np.zeros((num_ativos, num_bases))
    
    # Preenche a matriz de distâncias
    for _, row in df.iterrows():
        cliente_idx = cliente_indices[(row['latitude_cliente'], row['longitude_cliente'])]
        base_idx = base_indices[(row['latitude_base'], row['longitude_base'])]
        distancias_bases_ativos[cliente_idx, base_idx] = row['distancia']
    
    return distancias_bases_ativos, bases_unicas, clientes_unicos 

# Função para gerar uma solução qualquer
def generate_solution(clients_data,obj_function,constructor_heuristic=True):
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

    return solution

def solucao_inicial1(solution):
   print("SOLUÇÃO INICIAL1")



   return solution


