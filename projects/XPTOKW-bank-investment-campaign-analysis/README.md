# XPTOKW Bank Investment Campaign Analysis

Análise exploratória do perfil de clientes e dos resultados de uma campanha de venda de um produto de investimento do Banco XPTOKW.

## 1. Problema e objetivo

Após uma campanha de três meses realizada em todo o Brasil, a área de Marketing disponibilizou os resultados dos contatos feitos com clientes. A área de Analytics recebeu a missão de descrever esse público, entender como as compras se distribuem entre os grupos analisados e transformar os achados em informação útil para o planejamento de novas campanhas.

O objetivo é apoiar decisões de segmentação com evidências sobre idade, profissão, estado civil, formação, situação de crédito, hipoteca, empréstimo e quantidade de ligações. A análise é exploratória: ela descreve associações observadas e não estabelece relações causais nem garante o comportamento de campanhas futuras.

## 2. Perguntas centrais

- Qual é o perfil dos clientes da base e como ele se relaciona com a compra do título?
- Qual foi a proporção de clientes que comprou o título?
- Quais profissões mais frequentes, em conjunto, representam aproximadamente 80% da base?
- É possível afirmar que 66% dos clientes não têm Ensino Superior, considerando também a categoria de formação desconhecida?
- Quais características apresentam maior poder de distinção entre quem comprou e quem não comprou?
- Como a taxa observada de compra varia conforme o número de ligações?

## 3. Entregáveis

- [Notebook de análise da campanha](notebooks/banco-analise-campanha.ipynb) — exploração, perguntas de negócio, análise de conversão, Information Value e estimativa de incerteza.
- [Dashboard de perfil dos clientes](https://jooarantes.github.io/data-analisys-labs/projects/bank-marketing-analytics/dashboards/dashboard-perfil-clientes.html) — composição demográfica, profissional e financeira da base.
- [Dashboard de conversão da campanha](https://jooarantes.github.io/data-analisys-labs/projects/bank-marketing-analytics/dashboards/dashboard-conversao-campanha.html) — compras, incerteza, taxas por segmento e análise de ligações.

## 4. Dados e premissas
### Fonte dos Dados
O arquivo `bank_marketing.xlsx` foi disponibilizado pela **Preditiva Analytics** como material complementar de um estudo de caso. O workbook está em [`data/bank_marketing.xlsx`](data/bank_marketing.xlsx).

### Estrutura dos dados

Cada linha representa um cliente e contém características de perfil e relacionamento bancário, informações sobre contatos da campanha e a resposta à oferta. O notebook lê a planilha `bank_marketing`, usando a linha de cabeçalho a partir da segunda linha do arquivo e as colunas B a K.

Variáveis usadas na análise incluem:

- **Perfil**: idade, profissão, estado civil e formação;
- **Relacionamento financeiro**: saldo em conta, inadimplência, hipoteca e empréstimo;
- **Campanha**: quantidade de ligações realizadas;
- **Resultado**: contratação do título (`Sim` ou `Não`).

### Premissas de implementação

- A análise assume que cada registro deve corresponder a um cliente. Foram identificados 278 registros duplicados entre 9.684 linhas e removidos, resultando em 9.406 observações analisadas. A duplicidade foi tratada como repetição indevida, embora não haja identificador de cliente documentado que permita confirmar isso de forma independente.
- `Sim` é tratado como evento de compra e `Não` como não compra.
- A categoria `Desconhecido` em formação não é presumida como ausência de Ensino Superior; por isso, a proporção depende do tratamento dado a esse grupo.

## 5. Métodos, técnicas e ferramentas

O projeto segue este fluxo:

1. Carrega a planilha e verifica estrutura, valores ausentes, duplicidades, domínios e valores extremos.
2. Resume o perfil dos clientes e responde às perguntas de negócio. Para identificar as profissões que concentram aproximadamente 80% da base, usa frequências e frequência acumulada em uma análise de Pareto.
3. Compara a distribuição de compras e não compras entre categorias e faixas de idade, saldo e quantidade de ligações.
4. Calcula *Weight of Evidence* (WoE) e *Information Value* (IV) para explorar o poder de separação de cada variável. O IV é usado como indicador exploratório, não como prova de causalidade ou critério isolado para seleção de público.
5. Estima a proporção observada de compras e compara intervalos de confiança de Wilson e Clopper–Pearson, além de uma aproximação por t de Student.
6. Explora probabilidades condicionais para grupos definidos pelo número de ligações e discute explicações alternativas para a associação observada.
7. Foi utilizado um agente para construir os dashboards a partir das análises do notebook. A [arquitetura do agente de dashboard](docs/arquitetura-agente-dashboard.md) descreve o fluxo, a skill, os scripts e como regenerar os painéis.

> Os dashboards são gerados pelo script de entrada em `.agents/skills/dashboard-html/scripts/gerar_dashboards.py`. Seus módulos auxiliares ficam junto da skill. Os gráficos Chart.js carregam a biblioteca pela CDN e precisam de conexão com a internet.


**Stack:** Python 3.12+, Jupyter Notebook, pandas, NumPy, SciPy, Matplotlib, Seaborn e openpyxl. A implementação de IV e WoE está em [`src/analise_IV.py`](src/analise_IV.py), com testes em [`tests/test_analise_iv.py`](tests/test_analise_iv.py). As dependências estão declaradas em [`pyproject.toml`](pyproject.toml).


## 6. Limitações e cuidados

- **Sem valor ou custo da campanha:** não é possível calcular retorno sobre investimento, custo por aquisição ou avaliar a rentabilidade da ação.
- **Sem taxa histórica ou grupo de controle:** a conversão observada não permite concluir se a campanha foi boa ou ruim, nem atribuir as compras à campanha.
- **Sem datas individuais:** sabe-se apenas que a campanha durou três meses. Não é possível avaliar sazonalidade, evolução temporal ou tempo até a compra.
- **Representatividade não documentada:** não há informação suficiente sobre o processo de seleção dos clientes. A taxa observada e os intervalos de confiança não devem ser automaticamente projetados para todos os clientes ou para novas campanhas.
- **Duplicados sem identificador verificável:** a remoção depende da premissa de que linhas duplicadas são repetições do mesmo cliente, e não ocorrências legítimas.
- **Associação não implica causalidade:** clientes menos propensos a comprar podem ter recebido mais contatos; além disso, contatos podem cessar após a compra. Assim, a quantidade de ligações pode ser consequência do andamento da campanha, e não causa da conversão observada.
- **Dados ausentes sobre contexto e elegibilidade:** não há informação detalhada sobre oferta, canal, regras de seleção, exposição efetiva ou motivos de recusa, o que pode afetar comparações entre segmentos.
- **Categorias e grupos pequenos:** percentuais de categorias com poucos clientes podem ser instáveis. A leitura deve considerar as contagens e a incerteza, não apenas a taxa percentual.
- **Saldo e valores extremos:** outliers estatísticos não são necessariamente erros. As faixas de saldo e o tratamento de valores extremos devem ser validados com a área de negócio antes de orientar decisões.

## 7. Possíveis extensões

- Investigar, com a área de negócio, custo, valor da oferta, critérios de seleção, datas, histórico de campanhas e existência de grupo de controle.
- Avaliar a incerteza das taxas por segmento e testar diferenças entre grupos, levando em conta o tamanho das amostras e comparações múltiplas.
- Ajustar um modelo de regressão logística para analisar a associação entre perfil e compra em conjunto, validar seu desempenho fora da amostra e verificar calibração. Isso não substituiria um desenho causal para medir o efeito da campanha.
- Estratificar a relação entre ligações e conversão por idade, profissão, formação e histórico de campanhas, para investigar possíveis fatores de confusão.
- Com dados temporais e de contato mais completos, analisar o momento da conversão, a sequência de tentativas e o efeito incremental de contatos adicionais.
- Consolidar os resultados em relatório executivo, com recomendações validadas junto ao Marketing.

## 8. Estrutura do repositório

```text
bank-marketing-analytics/
├── data/
│   └── bank_marketing.xlsx
├── docs/
│   └── arquitetura-agente-dashboard.md
├── .agents/
│   └── skills/dashboard-html/
│       ├── SKILL.md
│       └── scripts/
│           ├── dados_dashboard.py
│           ├── dashboard.css
│           ├── dashboard.js
│           ├── gerar_dashboards.py
│           └── visualizacoes_dashboard.py
├── images/
│   └── identidade-visual-banco-xptokw.png
├── notebooks/
│   └── banco-analise-campanha.ipynb
├── reports/
│   ├── dashboard-perfil-clientes.html
│   └── dashboard-conversao-campanha.html
├── src/
│   ├── __init__.py
│   └── analise_IV.py
├── tests/
│   └── test_analise_iv.py
├── .gitignore
├── AGENTS.md
├── pyproject.toml
├── README.md
└── uv.lock
```

## 9. Veja também

- [Como encontrar bons públicos para uma campanha: uma investigação com dados bancários](https://medium.com/@jooaarantes/como-encontrar-bons-p%C3%BAblicos-para-uma-campanha-uma-investiga%C3%A7%C3%A3o-com-dados-banc%C3%A1rios-db1f0f21b6da?postPublishedType=initial) — artigo no Medium com a lógica e os detalhes da análise.

## 10. Autoria e licença

- **Autor:** [João Arantes](https://github.com/jooarantes)
- **LinkedIn:** [João Arantes](https://www.linkedin.com/in/joao-arantes-ds/)
- **Portfólio:** link a adicionar quando o site for publicado.
- **Código:** licenciado sob [MIT](../../LICENSE), conforme a licença na raiz do repositório.

## [← Voltar ao README do Data Analysis Labs](../../README.md)


