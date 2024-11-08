# Trabalho Computacional de Teoria da Decisão

Este repositório contém o código e a documentação para o Trabalho Computacional da disciplina **ELE088 – Teoria da Decisão**. O projeto aborda a modelagem e otimização de problemas de alocação de equipes de manutenção para monitoramento de ativos em barragens de mineração, com foco em técnicas de otimização mono e multiobjetivo, além de métodos de auxílio à tomada de decisão.

## 📋 Conteúdo

- **Modelagem Matemática**: Formulação das funções objetivo e restrições para:
  - Minimização da distância total entre ativos e equipes de manutenção.
  - Balanceamento de carga entre equipes, minimizando a diferença no número de ativos alocados.
- **Algoritmos de Solução**:
  - Implementação de metaheurísticas para otimização mono e multiobjetivo.
  - Técnicas como busca local e heurísticas construtivas para geração de soluções iniciais e refinamento.
- **Tomada de Decisão Multicritério**:
  - Métodos aplicados: AHP, ELECTRE, PROMETHEE, TOPSIS.
  - Análise e comparação das soluções não-dominadas, considerando múltiplos critérios de desempenho.
- **Visualizações**:
  - Gráficos de convergência das metaheurísticas.
  - Ilustrações das melhores soluções, com alocação das equipes e conexões com os ativos monitorados.

## 📂 Estrutura de Arquivos

- `probdata.csv`: Arquivo contendo os dados de localização dos ativos e das bases de manutenção, incluindo distâncias estimadas.
- `src/`: Diretório com o código fonte das implementações das metaheurísticas e dos métodos de decisão.
- `docs/`: Relatório completo com documentação detalhada, abordando a modelagem, algoritmos e resultados.
- `results/`: Resultados da execução dos algoritmos, incluindo gráficos e figuras.

## 🧠 Problema Abordado

O problema envolve a alocação otimizada de equipes de manutenção em bases de operação, visando minimizar a distância percorrida e balancear a carga de trabalho entre as equipes. As restrições incluem:

1. Cada equipe deve ser alocada a exatamente uma base de manutenção.
2. Cada ativo deve ser atribuído a uma base e a uma equipe responsável.
3. O número de ativos por equipe deve respeitar um percentual mínimo definido pela empresa.

## 🛠️ Ferramentas e Tecnologias

- Linguagem: Python
- Bibliotecas: `osmnx`, `geopy`, `matplotlib`, `numpy`, `scipy`

## 📈 Resultados

- Execuções dos algoritmos de otimização mono e multiobjetivo realizadas 5 vezes para cada função objetivo.
- Apresentação dos valores mínimo, máximo e desvio padrão das soluções obtidas.
- Gráficos com as fronteiras não-dominadas e as melhores soluções encontradas.

## 📚 Referências

- Métodos de tomada de decisão multicritério: AHP, ELECTRE, PROMETHEE, TOPSIS.
- Metaheurísticas: Algoritmos baseados em busca local e heurísticas construtivas.

## 👨‍🏫 Professor

- Lucas S. Batista

---

**Nota:** O código e a documentação foram desenvolvidos para fins acadêmicos. As soluções apresentadas podem não ser adequadas para aplicações em escala industrial sem ajustes e validações adicionais.
