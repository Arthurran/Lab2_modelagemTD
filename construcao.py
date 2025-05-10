from libs import *
import libs
import globals
#import constraints
from plot import plot_solution

# Função para gerar uma solução base
def generate_solution():
    # print("Gerar solucao")
    # Inicialize as variáveis de decisão

    solution = {
        # Pico de fila
        # Qtd de servidores
        # vetor[servidores x nos]
        # Qtd de pacientes no nó n
        # Disponibilidade do nó = vetor de 
        
        'servidores':np.zeros((globals.num_nos)), # Numero de servidores x No
        'penalty': np.zeros(0), # Armazena a penalidade da solução
        'fitness': np.zeros(0), # Armazena o ajuste da solucao
    }

    return solution

def solution_initial(solution):
    servidores = solution['servidores']
    
    
