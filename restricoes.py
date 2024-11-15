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
    #Restrição: Um ativo só pode ser monitorado por uma base se esta base pertence a uma equipe.
    
    x = solution['x']
    y = solution['y']
    num_ativos, num_bases = x.shape
    num_bases, num_equipes = y.shape

    for i in range(num_ativos):
        for j in range(num_bases):
            for k in range(num_equipes):
                if x[i, j] > y[j, k]:
                    return False
    return True

def restricao_monitoramento(solution):
    #Restrição: Cada ativo deve estar associado a exatamente uma equipe.
    
    h = solution['h']
    return np.all(np.sum(h, axis=1) == 1)

def restricao_hik(solution):
    #Restrição: h_ik ≤ (x_ij + y_jk) / 2, ∀i ∈ {1, ..., n}, ∀j ∈ {1, ..., m}, ∀k ∈ {1, ..., s}
    
    x = solution['x']
    y = solution['y']
    h = solution['h']
    num_ativos, num_bases = x.shape
    num_bases, num_equipes = y.shape

    for i in range(num_ativos):
        for j in range(num_bases):
            for k in range(num_equipes):
                if h[i, k] > (x[i, j] + y[j, k]) / 2:
                    return False
    return True

def restricao_balanceamento(solution, eta, num_ativos, num_equipes):
    #Restrição de Balanceamento: Cada equipe deve ter uma carga mínima.
    
    h = solution['h']
    carga_minima = eta * (num_ativos / num_equipes)
    return np.all(np.sum(h, axis=0) >= carga_minima)

constraints = [restricao_cobertura_grupo, restricao_atribuicao_unica, restricao_compatibilidade, restricao_monitoramento, restricao_hik, restricao_balanceamento]
