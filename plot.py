from libs import *

# Graficos para visualização das soluções

# Função para plotar os PAs e os clientes em um grid
def plot_progress(progress, i):
    # Criar uma nova figura
    plt.figure(figsize=(12, 5))

    # Plotar resultados
    for i in range(i):
      plt.plot(progress[0]['fitness'], label='Fitness 1')
      plt.plot(progress[1]['fitness'], label='Fitness 2')
      plt.plot(progress[2]['fitness'], label='Fitness 3')
      plt.plot(progress[3]['fitness'], label='Fitness 4')
      plt.plot(progress[4]['fitness'], label='Fitness 5')
      # plt.scatter(client_coordinates[:, 0], client_coordinates[:, 1], marker='o', color='blue', label='Clientes')

    # Adicionar legendas e título
    plt.xlabel('Iterações')
    #plt.ylabel('Numero de PAs')
    #plt.title('Convergência das soluções')
    #plt.legend()

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



