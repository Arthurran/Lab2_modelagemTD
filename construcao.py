from libs import *
import constraints
from plot import plot_solution

# Carrega os dados dos clientes do arquivo CSV
def get_clients():
  clients = np.genfromtxt('clientes.csv', delimiter=',')
  return clients

# Função para gerar uma solução qualquer
def generate_solution(clients_data,obj_function,constructor_heuristic=True):
    print("Gerar solucao")
    # Inicialize as variáveis de decisão
    solution = {
        #'x': np.zeros((num_pa_locations, num_clients)),  # Variáveis de decisão para atribuição de clientes a PAs
        #'y': np.zeros(num_pa_locations),  # Variáveis de decisão para ativação de PAs
        #'client_coordinates': np.zeros((num_clients, num_clients)),  # Armazena as posições (x,y) de cada cliente
        #'client_pa_distances': np.zeros((num_pa_locations, num_clients)),  # Armazena a distancia entre cliente e PA
        #'client_bandwidth': np.zeros(num_clients), # Armazena a largura de banda necessária de cada cliente
        #'penalty': np.zeros(0), # Armazena a penalidade da solução
        #'fitness': np.zeros(0), # Armazena o ajuste da solução
        #'penalty_fitness': np.zeros(0), # Armazena o ajuste somado a penalidade da solução
        #'pas_distances': np.zeros((num_pa_locations, num_pa_locations))
    }

    return solution


