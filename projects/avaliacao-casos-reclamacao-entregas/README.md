# Avaliação de Casos de Reclamação em Entregas

Análise exploratória de viagens realizadas por caminhões-tanque para investigar indicadores logísticos e sua relação com reclamações de entrega. O estudo organiza perguntas iniciais para apoiar o alinhamento entre as equipes de logística e experiência do cliente.

## 1. Problema e objetivo

O time de logística, em conjunto com a equipe de experiência do cliente, quer compreender quais características das viagens podem estar associadas à ocorrência de reclamações. A análise usa dados dos últimos três meses para descrever as viagens e levantar pontos que merecem investigação preventiva.

O objetivo é responder às perguntas de negócio com evidências descritivas e medidas exploratórias. Associações observadas não demonstram que uma característica da viagem cause reclamações.

## 2. Perguntas centrais

- Mais da metade das viagens teve mais de seis entregas?
- Há correlação aparente entre o número de entregas e a distância percorrida?
- O tipo de produto apresenta associação com a ocorrência de reclamações segundo o *Information Value* (IV)?
- A distância apresenta associação com reclamações segundo o IV?
- Como a distância se distribui entre os tipos de produto?
- O R² indica associação aparente entre reclamações e número de paradas do motorista?

## 3. Entregáveis

- [Notebook de avaliação das reclamações em entregas](notebooks/avaliacao-casos-reclamacao.ipynb) — exploração da base e análise das perguntas de negócio.
- [Relatório de análise de reclamações](reports/relatório-reclamação-entregas.md)

## 4. Dados e premissas

### Fonte dos dados

O arquivo [`Relatorio_Entregas.xlsx`](data/Relatorio_Entregas.xlsx) contém registros de viagens dos últimos três meses e foi disponibilizado pela **Preditiva Analytics**.

### Estrutura dos dados

Cada linha representa uma viagem. A descrição fornecida para a base contempla:

| Campo | Descrição |
|---|---|
| ID da viagem | Código identificador único da viagem. |
| Número de entregas | Quantidade de entregas realizadas na viagem. |
| Tipo de caminhão | Tipo de caminhão usado no transporte. |
| Produto | Produto transportado; cada viagem entrega um único tipo de produto. |
| Distância | Distância total percorrida no trajeto. |
| Número de dias | Duração total da viagem, em dias. |
| Número de paradas do motorista | Quantidade de paradas durante a viagem, por qualquer motivo. |
| Reclamação | Indicação de existência de reclamação associada à viagem. |


### Premissas e verificações

- A unidade de análise é a viagem; o ID deve identificar registros únicos.
- O número de paradas do motorista não contabiliza a parada da entrega.

## 5. Métodos, técnicas e ferramentas

O roteiro de análise proposto no notebook abrange:

1. Inspecionar a estrutura da planilha, os tipos de dados, valores ausentes, duplicidades e categorias.
2. Calcular a proporção de viagens com mais de seis entregas e compará-la com 50% para avaliar a afirmação apresentada pela liderança.
3. Explorar a relação entre entregas e distância por meio de visualização e correlação apropriada aos dados.
4. Calcular IV e WoE para explorar a capacidade de separação entre categorias/faixas de produto ou distância e a ocorrência de reclamações.
5. Comparar visualmente a distribuição da distância por produto.
6. Usar o R² conforme implementado no notebook para quantificar a associação aparente entre reclamações e paradas, deixando explícita a codificação e o modelo utilizados.

**Stack declarada:** Python 3.12+, Jupyter, pandas, NumPy, SciPy, Matplotlib, Seaborn e openpyxl. As dependências estão registradas em [`pyproject.toml`](pyproject.toml) e [`uv.lock`](uv.lock).

## 6. Limitações e Cuidados

- **Escopo temporal curto:** a base cobre três meses; padrões observados podem não se manter em outros períodos ou sazonalidades.
- **Representatividade desconhecida:** sem documentação do processo de coleta, não é possível presumir que as viagens representem toda a operação.
- **Associação não é causalidade:** distância, tipo de produto, número de entregas, paradas e reclamações podem se relacionar com outros fatores operacionais não registrados.
- **IV depende do tratamento dos dados:** a distância é numérica e pode precisar de discretização; categorias pequenas ou raras podem tornar as estimativas instáveis. O IV não substitui validação de modelo nem teste causal.

## 7. Próximos passos possíveis

- Investigar outros fatores operacionais relevantes, como tipo de caminhão, duração, região e condições da rota, se estiverem disponíveis.
- Repetir a análise em períodos comparáveis para avaliar a estabilidade dos indicadores antes de transformar os achados em ações preventivas.

## 8. Estrutura do repositório

```text
avaliacao-casos-reclamacao-entregas/
├── data/
│   └── Relatorio_Entregas.xlsx
├── notebooks/
│   └── avaliacao-casos-reclamacao.ipynb
├── reports/
│   └── relatório-reclamação-entregas.md
├── src/
│   ├── __init__.py
│   └── analise_IV.py
├── tests/
│   └── test_analise_iv.py
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock
```

## 9. Autoria e licença

- **Autor:** [João Arantes](https://github.com/jooarantes)
- **LinkedIn:** [João Arantes](https://www.linkedin.com/in/joao-arantes-ds/)
- **Licença:** [MIT](LICENSE)

## [← Voltar ao README do Data Analysis Labs](../../README.md)
