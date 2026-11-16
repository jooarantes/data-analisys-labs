# Análise de Suporte ao Cliente — Agência AtendeBem

Análise exploratória de atendimentos ao cliente para investigar relações entre tempos de espera e resolução, satisfação, NPS, sentimento dos feedbacks e solução dos problemas. O estudo também estima a taxa de resolução e compara os resultados com referências definidas para o negócio.

## 1. Problema e objetivo

A Agência AtendeBem quer compreender quais aspectos dos atendimentos estão associados à satisfação dos clientes e à resolução de seus problemas. O projeto usa uma base de registros de atendimento para responder perguntas de negócio e sintetizar recomendações para acompanhamento operacional.

O objetivo é descrever os padrões observados na amostra e indicar pontos que merecem investigação. As análises são exploratórias e associativas: não demonstram que o tempo de espera ou qualquer outra variável cause mudanças na resolução, na satisfação ou no NPS.

## 2. Perguntas centrais

- Como o tempo total de atendimento se relaciona com satisfação e NPS?
- Como espera, tempo de resolução, reclamações e satisfação se associam ao NPS?
- O sentimento registrado no feedback distingue atendimentos com e sem resolução?
- Como a taxa observada de resolução varia entre faixas de espera?
- As categorias de sentimento apresentam valores diferentes de NPS?
- A média de espera é compatível com o benchmark de 15 minutos?
- A taxa de resolução supera a referência histórica de 55%?
- O tempo de espera difere entre canais? A proporção de problemas não solucionados difere entre tipos de problema?

## 3. Entregáveis

- [Notebook de análise do suporte](notebooks/analise-suporte-cliente.ipynb) — exploração dos dados, perguntas de negócio, medidas de associação e intervalos de confiança.
- [Relatório técnico de recomendações](reports/plano-recomendacao.md) — síntese dos resultados, implicações e ações sugeridas para acompanhamento.

## 4. Dados e premissas

### Fonte dos dados

O arquivo [`area-de-atendimento.xlsx`](data/area-de-atendimento.xlsx) foi disponibilizado pela **Preditiva Analytics** como material complementar do estudo.

### Estrutura dos dados

Cada linha representa um registro de atendimento. A base contém 1.000 registros e as variáveis abaixo:

| Variável | Descrição |
|---|---|
| `ID_Cliente` | Identificador registrado para o cliente. |
| `Tempo_Espera` | Tempo aguardado até o atendimento, em minutos. |
| `Tempo_Resolucao` | Tempo gasto no atendimento para tratar o problema, em minutos. |
| `Satisfacao_Cliente` | Nota de satisfação atribuída pelo cliente, de 0 a 10. |
| `Canal_Atendimento` | Canal utilizado, como telefone, chat, e-mail, WhatsApp ou redes sociais. |
| `Tipo_Problema` | Categoria do problema relatado, como dúvida, produto defeituoso, atendimento ruim ou cobrança. |
| `Feedback_Sentimento` | Sentimento classificado no feedback: positivo, neutro ou negativo. |
| `Media_NPS` | Valor médio de NPS associado ao registro; a escala e o método de cálculo não foram especificados. |
| `Qtd_Reclamacoes` | Quantidade de reclamações registrada para o cliente ou atendimento. |
| `Problema_Solucionado` | Indica se o problema foi solucionado (`Sim` ou `Não`). |

### Premissas e verificações

- Para a análise de duração, `Tempo de atendimento` é definido como `Tempo_Espera + Tempo_Resolucao`.
- `Sim` em `Problema_Solucionado` representa o evento de resolução.
- O benchmark de espera é 15 minutos e a referência histórica de resolução é 55%, conforme definido nas perguntas do estudo; não são estimativas derivadas desta base.
- A amostra contém 1.000 registros, mas seu processo de seleção e sua representatividade em relação a todos os clientes da AtendeBem não foram estabelecidos.

## 5. Métodos, técnicas e ferramentas

O notebook segue este fluxo:

1. Carrega e inspeciona a base, verificando estrutura, valores ausentes, duplicidades, domínios e valores extremos.
2. Usa gráficos de dispersão e correlação de Pearson para explorar associações entre variáveis numéricas. Os p-valores são apresentados como evidência estatística de associação linear diferente de zero, sob as premissas do teste.
3. Calcula *Weight of Evidence* (WoE) e *Information Value* (IV) para explorar a capacidade de separação de categorias ou faixas em relação à resolução. Essas medidas não demonstram causalidade nem constituem, isoladamente, validação de um indicador operacional.
4. Compara a distribuição de `Media_NPS` entre sentimentos e calcula η² para quantificar a proporção da variação associada aos grupos.
5. Estima intervalo *t* de Student para o tempo médio de espera e intervalos de Wilson e Clopper–Pearson para a proporção de problemas solucionados; também apresenta uma aproximação por *t* para comparação.
6. Explora diferenças de tempo de espera entre canais e de resolução entre tipos de problema por meio de estimativas e intervalos de confiança. O notebook recomenda testes inferenciais diretos como aprofundamento, pois as comparações apresentadas não confirmam diferenças entre grupos.
7. Reúne as evidências e recomendações no relatório técnico.

**Stack:** Python 3.12+, Jupyter Notebook, pandas, NumPy, SciPy, Matplotlib, Seaborn e openpyxl. A implementação de IV e WoE está em [`src/analise_IV.py`](src/analise_IV.py), com testes em [`tests/test_analise_iv.py`](tests/test_analise_iv.py). As dependências estão declaradas em [`pyproject.toml`](pyproject.toml) e [`uv.lock`](uv.lock).

## 6. Limitações e cuidados

- **Representatividade desconhecida:** sem informação sobre como os atendimentos foram selecionados, não é possível generalizar automaticamente taxas e intervalos para todos os clientes da AtendeBem.
- **Associações não são efeitos causais:** as correlações e diferenças observadas não mostram que reduzir a espera, por si só, aumentaria satisfação ou resolução. Complexidade do problema e outras características do atendimento podem se relacionar com ambos.
- **Definição do NPS incompleta:** a escala e o método de cálculo de `Media_NPS` não foram documentados; isso limita a interpretação dos valores e comparações externas.
- **Comparações entre grupos inconclusivas:** a sobreposição dos intervalos de confiança para canais e tipos de problema não substitui um teste direto de diferenças. ANOVA (se os pressupostos forem atendidos) e qui-quadrado com V de Cramér são indicados como próximos passos, não como resultados já obtidos.
- **Média não descreve cada atendimento:** a espera média abaixo de 15 minutos não significa que todos os clientes foram atendidos dentro desse prazo.
- **Sentimento não substitui métricas de resultado:** nesta amostra, o sentimento teve pouco poder de separação para resolução e quase nenhuma associação com a variação do NPS; cada resultado deve ser acompanhado por seu próprio campo.
- **IV é exploratório:** sua interpretação depende da distribuição e do número de observações em cada categoria; valores altos também exigem revisão das categorias e da base.

## 7. Próximos passos possíveis

- Validar com a área de negócio o processo de amostragem e a definição, escala e cálculo de `Media_NPS`.
- Acompanhar a taxa de resolução em relação à referência de 55% e revisar os 507 registros classificados como não solucionados para identificar oportunidades de melhoria.
- Examinar atendimentos com espera de 15 minutos ou mais, relacionando espera, resolução, satisfação e NPS sem presumir causalidade.
- Comparar formalmente médias de espera entre canais e proporções de resolução entre tipos de problema, incluindo tamanhos dos grupos, intervalos e medidas de efeito.
- Repetir o acompanhamento em períodos comparáveis e com critérios de coleta documentados para avaliar a estabilidade dos indicadores.

## 8. Estrutura do repositório

```text
customer-support/
├── data/
│   └── area-de-atendimento.xlsx
├── notebooks/
│   └── analise-suporte-cliente.ipynb
├── reports/
│   └── plano-recomendacao.md
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
