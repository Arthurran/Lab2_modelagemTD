from libs import *

def restricao_cobertura_grupo(solution, dist_bases_ativos, prob_ativos):
    #Restrição: Cada grupo deve ter exatamente uma base associada.
    
    y = solution['y']
    return np.all(np.sum(y, axis=0) == 1)

def restricao_atribuicao_unica(solution, dist_bases_ativos, prob_ativos):
    #Restrição: Cada ativo deve ser monitorado por exatamente uma base.
    
    x = solution['x']
    return np.all(np.sum(x, axis=1) == 1)

def restricao_compatibilidade(solution, dist_bases_ativos, prob_ativos):
    # Restrição: Um ativo só pode ser monitorado por uma base se esta base pertence a uma equipe
    x = solution['x']
    y = solution['y']
    num_ativos, num_bases = x.shape
    num_bases, num_equipes = y.shape

    for i in range(num_ativos):
        for j in range(num_bases):
            # Verifica se o ativo i está associado à base j
            if x[i, j] == 1:
                # Verifica se a base j está associada a alguma equipe k
                if np.sum(y[j, :]) == 0:  # Se base j não tem nenhuma equipe associada
                    return False
    return True


def restricao_monitoramento(solution, dist_bases_ativos, prob_ativos):
    #Restrição: Cada ativo deve estar associado a exatamente uma equipe.
    
    h = solution['h']
    return np.all(np.sum(h, axis=1) == 1)

def restricao_hik(solution, dist_bases_ativos, prob_ativos):
    # Restrição: Cada ativo deve estar atribuído a uma equipe, e a equipe deve ocupar a base na qual o ativo está alocado
    x = solution['x']
    y = solution['y']
    h = solution['h']
    num_ativos, num_bases = x.shape
    num_bases, num_equipes = y.shape
    num_ativos, num_equipes = h.shape

    for i in range(num_ativos):
        for j in range(num_bases):
            # Verifica se o ativo i está associado à base j
            if x[i, j] == 1:
                # Verifica se a base j está associada a uma equipe k
                equipe_associada = np.any(y[j, :] == 1)
                if not equipe_associada:
                    return False  # Se a base não tem nenhuma equipe associada, retorna False

                # Verifica se o ativo i está associado a uma equipe k que ocupa a base j
                equipe_ativa = np.any(h[i, :] == 1)
                if equipe_ativa:
                    # Verifica se a equipe associada ao ativo também ocupa a base
                    if not np.any(np.logical_and(y[j, :], h[i, :])):  # Utiliza np.logical_and ao invés de &
                        return False  # Se a equipe não ocupa a base onde o ativo está, retorna False
    return True

def restricao_balanceamento(solution, dist_bases_ativos, prob_ativos):
    #Restrição de Balanceamento: Cada equipe deve ter uma carga mínima
    h = solution['h']
    num_ativos, num_equipes = h.shape
    carga_minima = eta * (num_ativos / num_equipes)
    
    # Verifica se cada equipe tem pelo menos a carga mínima de ativos
    return np.all(np.sum(h, axis=0) >= carga_minima)

def restricao_f2(solution, dist_bases_ativos, prob_ativos):
    # Calculando a soma ponderada das distâncias entre as bases e os ativos
    soma_distancia_probabilidade = 0
    bases_com_equipes = np.where(solution['y'] == 1)[0]

    for base in bases_com_equipes:
        ativos_da_base = np.where(solution['x'][:, base] == 1)[0]

        # Cálculo da soma ponderada de distâncias
        for ativo in ativos_da_base:
            soma_distancia_probabilidade += (dist_bases_ativos[ativo, base] * prob_ativos[ativo, 2])

    # Restrição Função 2: Limitar o valor de epsilon_2 com base em alpha
    epsilon_2 = globals.min_val2 + globals.alpha * (globals.max_val2 - globals.min_val2)
    return soma_distancia_probabilidade <= epsilon_2

constraints = [restricao_cobertura_grupo, restricao_atribuicao_unica, restricao_compatibilidade, restricao_monitoramento, restricao_hik, restricao_balanceamento]
multiconstraints = [restricao_cobertura_grupo, restricao_atribuicao_unica, restricao_compatibilidade, restricao_monitoramento, restricao_hik, restricao_balanceamento, restricao_f2]