from libs import *
import constraints
from plot import plot_solution

# Carrega os dados do arquivo CSV
def get_clients():
  return 

# Função para gerar uma solução qualquer
def generate_solution(clients_data,obj_function,constructor_heuristic=True):
    print("Gerar solucao")
    # Inicialize as variáveis de decisão
    solution = {
        'x':np.zeros((num_ativos, num_bases)),
        'y':np.zeros((num_bases, num_equipe)),
        'h':np.zeros((num_ativos, num_equipe)),
        'coordenadas_ativos':np.zeros(num_ativos),
        'coordenadas_bases':np.zeros(num_bases) 
    }

    return solution


