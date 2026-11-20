# Teste A/B para Comparar médias de IDH entre Regiões
Este projeto tem caráter didático: usa uma situação de comparação entre regiões para apresentar, na prática, conceitos empregados em testes A/B e em testes de hipóteses. A proposta é acompanhar o caminho entre uma pergunta sobre os dados, a definição das hipóteses e a escolha de um método estatístico até a interpretação dos resultados, incluindo o que eles permitem concluir e quais são seus limites.

## 1. Problema e Objetivo

Neste cenário didático, a Secretaria da Educação solicita uma análise do IDHM Educação por região para investigar se as diferenças observadas entre as amostras podem ser consideradas **estatisticamente significativas**. A base reúne valores de uma amostra de municípios das regiões **Norte, Nordeste e Sul**, consolidados no arquivo `idhm_educacao.xlsx`.

O objetivo é explorar como testes de hipóteses ajudam a comparar grupos e a sustentar inferências a partir de dados amostrais. 

Ao longo do projeto, busca-se:

- Formular hipóteses nula e alternativa para a pergunta investigada.
- Escolher um teste estatístico compatível com a pergunta, o desenho da comparação e as características dos dados.
- Calcular e interpretar estatísticas de teste e valores-p, relacionando-os ao nível de significância definido.
- Discutir o alcance da inferência e comunicar os resultados à luz do contexto e das limitações do exercício.

## 2. Entregáveis
- [Notebook Didático](notebooks/ab-testing-idhm-brazil.ipynb)
  
## 3. Dados
### Fonte dos Dados
O arquivo `idhm_educacao.xlsx` foi disponibilizado pela **Preditiva Analytics** como material para estudo.

### Estrutura dos Dados
Cada linha representa um município diferente e cada coluna representa uma região. Os valores são os IDHs.

## 4. Estrutura do Repositório
```text
ab-teste-idh-brazil/
├── data/
│   └── idhm_educacao.xlsx
├── notebooks/
│   └── ab-testing-idhm-brazil.ipynb
├── .gitignore
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock
```

### 5. Autoria e licença

- **Autor:** [João Arantes](https://github.com/jooarantes)
- **LinkedIn:** [João Arantes](https://www.linkedin.com/in/joao-arantes-ds/)
- **Licença:** [MIT](LICENSE)

## [← Voltar ao README do Data Analysis Labs](../../README.md)
