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
    plt.ylabel('Numero de PAs')
    plt.title('Convergência das soluções')
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


# Função para plotar os PAs e os clientes em um grid
def plot_solution(solution, coords_bases, coords_ativos):
    
    # Plotando o gráfico
    plt.figure(figsize=(10, 8))

    # Dados do DataFrame
    bases_latitude = coords_bases['latitude_base']
    bases_longitude = coords_bases['longitude_base']
    ativos_latitude = coords_ativos['latitude_ativo']
    ativos_longitude = coords_ativos['longitude_ativo']

    # Plotando as bases (com pentágonos e bordas pretas)
    plt.scatter(bases_longitude, bases_latitude, color='red', s=150, marker='p', label='Bases', edgecolors='black', facecolors='none', alpha=0.7)

    # Plotando os ativos (ativos) como pontos pequenos
    plt.scatter(ativos_longitude, ativos_latitude, color='blue', s=30, label='Ativos', alpha=0.7)

    # Plotando as equipes como pontos vermelhos dentro da base
    # pegar indexes de solution['y'] = 1
    bases_com_equipes = np.where(solution['y'] == 1)[0]

    # Filtrando o DataFrame com base nos índices em bases_com_equipes
    df_bases_com_equipes = coords_bases.iloc[bases_com_equipes]
    base_latitude_com_equipe = df_bases_com_equipes['latitude_base']
    base_longitude_com_equipe = df_bases_com_equipes['longitude_base']

    plt.scatter(base_longitude_com_equipe, base_latitude_com_equipe, color='red', s=70, label='Bases', edgecolors='black', alpha=0.7)

    # Ajustando os limites dos eixos para garantir que todos os pontos sejam visíveis
    plt.xlim(coords_bases['longitude_base'].min() - 0.05, coords_bases['longitude_base'].max() + 0.05)
    plt.ylim(coords_bases['latitude_base'].min() - 0.05, coords_bases['latitude_base'].max() + 0.05)

    # Títulos e rótulos
    plt.title('Bases e Ativos no Grid', fontsize=14)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Legenda
    plt.legend()

    # Exibindo o gráfico
    plt.grid(True)
    plt.show()


