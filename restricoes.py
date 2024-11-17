from libs import *

def restricao_cobertura_grupo(solution):
    #Restrição: Cada grupo deve ter exatamente uma base associada.
    
    y = solution['y']
    return np.all(np.sum(y, axis=0) == 1)

def restricao_atribuicao_unica(solution):
    #Restrição: Cada ativo deve ser monitorado por exatamente uma base.
    
    x = solution['x']
    return np.all(np.sum(x, axis=1) == 1)

def restricao_compatibilidade(solution):
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


def restricao_monitoramento(solution):
    #Restrição: Cada ativo deve estar associado a exatamente uma equipe.
    
    h = solution['h']
    return np.all(np.sum(h, axis=1) == 1)

def restricao_hik(solution):
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

def restricao_balanceamento(solution):
    #Restrição de Balanceamento: Cada equipe deve ter uma carga mínima
    h = solution['h']
    num_ativos, num_equipes = h.shape
    carga_minima = eta * (num_ativos / num_equipes)
    
    # Verifica se cada equipe tem pelo menos a carga mínima de ativos
    return np.all(np.sum(h, axis=0) >= carga_minima)


constraints = [restricao_cobertura_grupo, restricao_atribuicao_unica, restricao_compatibilidade, restricao_monitoramento, restricao_hik, restricao_balanceamento]
