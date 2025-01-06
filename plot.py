from libs import *

# Graficos para visualização das soluções

# Função para plotar os PAs e os clientes em um grid
def plot_progress(progress, i):
    # Criar uma nova figura
    plt.figure(figsize=(12, 5))

    # Plotar resultados
    for idx in range(i):
        plt.plot(progress[idx]['fitness'], label=f'Fitness {idx + 1}')

    # Adicionar legendas e título
    plt.xlabel('Iterações')
    plt.ylabel('fitness')
    plt.title('Convergência das soluções')
    plt.legend()

    # Mostrar o gráfico
    plt.show()

def plot_pareto_fronts(pareto_data, title):
    """
    Plota as fronteiras de Pareto para as soluções fornecidas.
    
    Parâmetros:
    - pareto_data: lista de listas de tuplas [(x, y)], onde cada lista representa uma fronteira.
    - title: título do gráfico.
    """
    # Verificar se os dados estão no formato correto
    if not all(isinstance(front, list) and all(isinstance(point, tuple) and len(point) == 2 for point in front) for front in pareto_data):
        raise ValueError("Os dados devem ser uma lista de listas de tuplas [(x, y)].")
    
    plt.figure(figsize=(10, 6))

    # Iterar sobre cada fronteira de Pareto e plotá-la
    for idx, front in enumerate(pareto_data):
        # Ordenar os pontos em cada fronteira pelo eixo X (quantidade de PAs ou distância, dependendo do problema)
        front_sorted = sorted(front, key=lambda t: t[0])
        x_values = [point[0] for point in front_sorted]
        y_values = [point[1] for point in front_sorted]

        # Plotar cada fronteira com um estilo diferente
        plt.plot(x_values, y_values, marker='o', linestyle='-', label=f'Fronteira {idx + 1}')

    # Personalização do gráfico
    plt.title(title, fontsize=14)
    plt.xlabel('Distâncias', fontsize=12)
    plt.ylabel('Distâncias Ponderadas', fontsize=12)
    plt.grid(True)
    plt.legend(fontsize=12)

    # Mostrar o gráfico
    plt.show()

def cor_vibrante():
    # Gerar valores RGB mais vibrantes
    r = random.randint(180, 255)  # Valor de vermelho entre 180 e 255
    g = random.randint(0, 255)    # Valor de verde entre 0 e 255
    b = random.randint(0, 255)    # Valor de azul entre 0 e 255

    # Converter para formato hexadecimal
    cor_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return cor_hex

def plot_solution(solution, coords_bases, coords_ativos):
    # Configurar o gráfico
    plt.figure(figsize=(10, 8))
    cores = ['red', 'blue', 'green'] #red = 0, blue = 1, green = 2

    # Plotar todas as bases
    plt.scatter(
        coords_bases['longitude_base'], coords_bases['latitude_base'],
        color='gray', s=150, marker='p', edgecolors='black', label='Bases', alpha=0.6
    )

    bases_com_equipes = []
    # Iterar pelas equipes e bases
    for equipe in range(num_equipes):
        for base in range(num_bases):
            if solution['y'][base][equipe] == 1:
                bases_com_equipes.append(base)

    # Converter para numpy array, se necessário
    bases_com_equipes = np.array(bases_com_equipes)
    bases_ativas = coords_bases.iloc[bases_com_equipes]

    # Iterar sobre cada equipe
    for k in range(num_equipes):
        if k < len(bases_ativas):
            # Plotar as equipes associada à equipe k
            plt.scatter(
                bases_ativas.iloc[k]['longitude_base'], bases_ativas.iloc[k]['latitude_base'],
                color=cores[k], s=70, label=f'Equipe {k}', edgecolors='black', alpha=0.8, linewidths = 0.5
            )

        # Plotar os ativos atendidos pela equipe k
        ativos_na_equipe_k = np.where(solution['h'][:,k] == 1)[0]
        ativos_k = coords_ativos.iloc[ativos_na_equipe_k]
        
        plt.scatter(
          ativos_k['longitude_ativo'], ativos_k['latitude_ativo'],
          color=cores[k], s=20, label=f'Ativos Equipe {k}', alpha=0.7
        )

    # Ajustar limites e adicionar detalhes ao gráfico
    plt.title('Distribuição de Bases e Ativos', fontsize=14)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.grid(True)

    # Exibir o gráfico
    plt.show()



