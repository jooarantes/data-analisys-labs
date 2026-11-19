# Resumindo Dados de uma Base de Marketing
O projeto envolve a aplicação de técnicas estatísticas para resumir e identificar relações entre as variáveis de uma base de dados de marketing de uma e-commerce.

## 1. Problema e Objetivo

Esse projeto não apresenta um contexto de negócio específico. O objetivo é investigar relações entre variáveis da base de dados do e-commerce, através de uma exploração univariada e bivariada. Além disso, é necessário implementar elementos visuais adequados para os tipos de análises.

## 2. Perguntas Centrais
- Existe uma forte relação entre a **renda do cliente** e os seus **gastos** na plataforma?
- Quanto **mais tempo** um cliente é ativo, maior a sua frequência de **compras**?
- O **tempo de navegação** influencia o **valor das compras**?
- Clientes antigos tendem a ter maior satisfação?
- Qual é o nível de associação entre tempo de cliente e avaliação?

## 3. Entregáveis
- [Notebook 1 - Análise Univariada](notebooks/analise-univariada.ipynb)
- [Notebook 2 - Análise Bivariada](notebooks/analise-bivariada.ipynb)

## 4. Dados e Premissas
### Fonte dos Dados

O arquivo [`resumir-dados-marketing.xlsx`](data\resumir-dados-marketing.xlsx) foi disponibilizado pela **Preditiva Analytics** para realização do estudo.

### Estrutura dos Dados

A planilha contém 100 clientes com ID único. As variáveis são:

| Variável | Descrição |
|---|---|
| **id_cliente** | Identificador único do cliente |
| **idade** | Idade do cliente |
| **renda_mensal** | Renda mensal do cliente (em R$) |
| **valor_total_compras** | Valor total gasto pelo cliente nos últimos 12 meses (em R$) |
| **frequência_compras** | Quantidade de compras feitas no último ano |
| **tempo_cliente** | Tempo desde a primeira compra (em meses) |
| **avaliacao_satisfacao** | Nota de satisfação do cliente (1 a 10) |
| **tempo_navegacao** | Tempo médio de navegação no site antes da compra (em minutos) |

## 5. Estrutura do Repositório
```text
resumindo-dados-marketing/
├── data/
│   └── resumir-dados-marketing.xlsx
├── notebooks/
│   └── analise-bivariada.ipynb
│   └── analise-univariada.ipynb
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock
```

## 6. Autoria e licença

- **Autor:** [João Arantes](https://github.com/jooarantes)
- **LinkedIn:** [João Arantes](https://www.linkedin.com/in/joao-arantes-ds/)
- **Licença:** [MIT](LICENSE)

## [← Voltar ao README do Data Analysis Labs](../../README.md)