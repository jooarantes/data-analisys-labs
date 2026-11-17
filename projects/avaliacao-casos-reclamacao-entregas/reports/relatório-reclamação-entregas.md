# Relatório — avaliação de reclamações em entregas

## Indicadores principais

| Indicador | Resultado |
|---|---:|
| Período descrito no notebook | Três meses de entregas; as datas inicial e final não são informadas |
| Viagens analisadas | 1.000 |
| Entregas registradas | 6.097 |
| Distância percorrida no total | 232.322 km |
| Média de distância por entrega (média dos quocientes por viagem) | 65,49 km/entrega |
| Mediana de distância por entrega (mediana dos quocientes por viagem) | 51,00 km/entrega |
| Viagens com reclamação | 271 (27,1%) |
| Viagens sem reclamação | 729 (72,9%) |

Este relatório reúne as análises descritivas, tabelas e gráficos apresentados no notebook `notebooks/avaliacao-casos-reclamacao.ipynb`. A base tem 1.000 linhas e 8 colunas: identificador da viagem, número de entregas, tipo de caminhão, produto, distância, número de dias, número de paradas do motorista e ocorrência de reclamação.

## Observações importantes

### Qualidade e perfil dos dados

- O notebook apresenta 1.000 valores preenchidos em todas as colunas e **nenhuma linha duplicada**.
- As categorias exibidas são três tipos de caminhão (tanque grande, médio e pequeno), quatro produtos (A, B, C e D) e duas respostas para reclamação (Sim e Não). O notebook relata que não identificou valores inválidos ou inconsistências aparentes nessas categorias.
- Pela regra de intervalo interquartil usada no notebook, os percentuais de observações sinalizadas como outliers são: **9,30%** para número de entregas, **3,50%** para distância, **8,90%** para número de dias e **3,20%** para número de paradas do motorista. O notebook observa especialmente a quantidade de outliers em entregas e dias e recomenda cautela com medidas de tendência central.
- Nas variáveis numéricas, o número de entregas tem média **6,097**, mediana **3**, quartis **2 e 6** e máximo **50**. A distância tem média **232,322 km**, mediana **183 km**, quartis **94,75 e 311,25 km** e máximo **1.048 km**. O número de dias tem média **1,104**, mediana **1** e máximo **3**. O número de paradas tem média **4,787**, mediana **5** e máximo **17**.

### Entregas e distância

- A mediana de **3 entregas por viagem** e o terceiro quartil igual a **6** não dão suporte à afirmação de que mais da metade das viagens realiza mais de 6 entregas. A média de 6,097 não representa a quantidade feita pela maioria das viagens.
- O gráfico de dispersão e a correlação de Pearson indicam uma associação linear positiva entre número de entregas e distância: **r = 0,734**. Em geral, viagens com mais entregas tendem a ter distâncias maiores.
- O notebook destaca observações no limite de **50 entregas**, com distâncias próximas de **750 a 1.050 km**. Esses valores foram sinalizados como possíveis outliers e podem influenciar a correlação; o notebook recomenda verificar esses casos com a área de negócio.
- A correlação descreve associação linear e não demonstra causa e efeito.

### Reclamações por produto

- O IV de `produto` é **0,4204**, classificado como forte segundo as faixas de referência usadas no notebook. É uma medida exploratória de associação, não evidência de causalidade.
- A taxa de reclamação é maior para **Produto D (57,89%)**, seguida por **Produto C (46,72%)**. Produto B tem taxa de **23,04%**, e Produto A, **17,53%**.

| Produto | Viagens | Com reclamação | Sem reclamação | Taxa de reclamação |
|---|---:|---:|---:|---:|
| A | 388 | 68 | 320 | 17,53% |
| B | 395 | 91 | 304 | 23,04% |
| C | 122 | 57 | 65 | 46,72% |
| D | 95 | 55 | 40 | 57,89% |

- A tabela também mostra que A e B concentram a maior parte das viagens (388 e 395, respectivamente), enquanto C e D têm 122 e 95. O notebook recomenda considerar o tamanho de cada categoria ao interpretar taxas e sugere um teste de associação, como qui-quadrado, para uma avaliação formal.
- Na tabela de IV, `% Sim` representa a participação da categoria no total de reclamações; `Taxa Evento (%)` representa a proporção de reclamações dentro da própria categoria. São medidas diferentes.

### Reclamações por faixa de distância

- O IV das faixas de distância é **0,0364**, classificado no notebook como baixo poder para diferenciar viagens com e sem reclamação. As taxas não formam uma tendência consistente.
- As faixas acima de 650 km totalizam **33 viagens**, repartidas em grupos pequenos (de 4 a 12 viagens). O notebook alerta que as taxas dessas faixas são instáveis e devem ser interpretadas com cautela.

| Distância (km) | Viagens | Com reclamação | Taxa de reclamação |
|---|---:|---:|---:|
| 50–149 | 406 | 111 | 27,34% |
| 150–249 | 244 | 65 | 26,64% |
| 250–349 | 141 | 43 | 30,50% |
| 350–449 | 90 | 23 | 25,56% |
| 450–549 | 46 | 16 | 34,78% |
| 550–649 | 40 | 7 | 17,50% |
| 650–749 | 12 | 3 | 25,00% |
| 750–849 | 10 | 1 | 10,00% |
| 850–949 | 4 | 1 | 25,00% |
| 950–1049 | 7 | 1 | 14,29% |

### Distância por produto e paradas por reclamação

- Nos boxplots de distância por produto, A, B e C têm medianas próximas, entre **181,5 e 189 km**, e médias entre **226,5 e 233,7 km**. O Produto D apresenta a menor mediana (**158 km**), média de **230,2 km** e caixa de maior amplitude, conforme a descrição do notebook. Há outliers em todas as categorias. A comparação visual não aponta uma diferença marcante de distância por produto.
- As distribuições do número de paradas são semelhantes entre viagens com e sem reclamação. A mediana é **5** nas viagens com reclamação e **4** nas sem reclamação.
- O eta ao quadrado é **η² = 0,0020**: diferenças entre as categorias de reclamação estão associadas a **0,1960%** da variabilidade no número de paradas. O notebook interpreta a associação aparente como muito fraca.

### Distância por parada do motorista

- A métrica foi calculada como distância da viagem dividida pelo número de paradas do motorista. Na distribuição das 1.000 viagens, a média é **51,22 km/parada**, a mediana **44,29**, o primeiro quartil **26,15**, o terceiro quartil **67**, o desvio-padrão **37,24**, o mínimo **7,14** e o máximo **369 km/parada**.
- Os percentis da cauda superior são **P80 = 72,92**, **P90 = 90,70**, **P95 = 107,29** e **P99 = 178,67 km/parada**. O máximo está acima do P99.
- A tabela dos 10 registros acima do P99 mostra que todos têm `numero_dias = 1`; oito têm uma parada, um tem duas e um tem três. As distâncias desses casos vão de **206 a 588 km**. O caso de maior razão é uma viagem de **369 km com uma parada**.
- Entre esses 10 registros, oito não têm reclamação e dois têm; aparecem Produtos A e B quatro vezes cada, Produto D duas vezes e nenhum registro do Produto C. O notebook ressalta que esse recorte extremo não permite concluir que a distância por parada esteja relacionada a reclamações.
- O notebook explica que as paradas do motorista não têm motivo especificado e que paradas para entrega são registradas separadamente. Portanto, a razão descreve distância em relação à contagem de paradas, mas não mede diretamente cansaço nem identifica a finalidade das paradas.

## Perguntas de negócio

### Q1 — Mais da metade das viagens faz mais de 6 entregas?

**Os resultados apresentados não sustentam essa afirmação.** A mediana é 3 entregas e o terceiro quartil é 6. A média de 6,097 é puxada para cima por valores altos e não deve ser interpretada como se a maioria das viagens fizesse mais de 6 entregas.

### Q2 — Há correlação aparente entre número de entregas e distância?

**Sim, positiva e forte segundo o critério adotado no notebook:** Pearson **r = 0,734**. Viagens com mais entregas tendem a percorrer distâncias maiores. Os casos no limite de 50 entregas merecem conferência, pois podem influenciar a correlação. Associação não implica causalidade.

### Q3 — O produto entregue se relaciona com a existência de reclamações?

**As taxas observadas variam por produto e o IV é 0,4204**, classificado como forte nas faixas de referência do notebook. Produto D tem a maior taxa (57,89%), seguido de C (46,72%). O notebook recomenda considerar os tamanhos dos grupos e realizar um teste de associação para avaliação formal.

### Q4 — A distância se relaciona com a existência de reclamações?

**A análise não sustenta uma relação clara.** O IV é 0,0364, e as taxas por faixa não apresentam tendência consistente. As faixas acima de 650 km têm poucos registros, o que limita a estabilidade das taxas observadas.

### Q5 — Como a distância se distribui por tipo de produto?

**As distribuições são, em geral, semelhantes.** A, B e C têm medianas próximas; D tem mediana menor, média próxima às demais e maior amplitude da caixa. Há outliers em todas as categorias, mas a comparação visual não mostra diferença marcante que permita afirmar associação entre produto e maiores distâncias.

### Q6 — Há associação aparente entre reclamações e número de paradas do motorista?

**A associação aparente é muito fraca.** As distribuições são semelhantes, embora a mediana seja 5 paradas para viagens com reclamação e 4 para viagens sem reclamação. O eta ao quadrado de 0,0020 indica que somente 0,1960% da variabilidade do número de paradas está associada às diferenças entre os grupos.

## Perguntas e hipóteses para aprofundar com a área de negócio

As perguntas abaixo podem ajudar a validar os registros, contextualizar os padrões observados e orientar análises futuras.

### Escopo e definição dos dados

- **Quais são as datas exatas cobertas pelos três meses analisados?** Os registros representam todos os períodos e tipos de viagem relevantes para a operação?
- **Como são definidas e registradas uma viagem, uma entrega e uma reclamação?** Uma viagem pode ter mais de uma reclamação ou reclamação associada a uma entrega específica?
- **A taxa de reclamação de 27,1% pode ser comparada com um histórico, uma meta ou outro período equivalente?** Qual referência a operação usa para avaliar esse indicador?
- **Quais informações operacionais existem além das colunas desta base?** Por exemplo: motivo e gravidade da reclamação, rota/região, datas, motorista, cliente, tipo de ocorrência e condições da entrega.

### Entregas, distância e registros extremos

- **O valor de 50 entregas por viagem é um limite operacional, um limite de registro ou um valor observado sem truncamento?** Os casos nesse limite e as viagens com distâncias próximas de 750 a 1.050 km são válidos?
- **A associação entre número de entregas e distância (Pearson r = 0,734) permanece quando os casos com 50 entregas e as viagens mais longas são verificados ou analisados separadamente?**
- **Como a distância é medida — por rota planejada, odômetro ou outra fonte — e como são tratadas viagens com múltiplas entregas?** Isso ajuda a contextualizar a média e a mediana de distância por entrega.
- **Os registros sinalizados como outliers em entregas, dias, distância e paradas correspondem a operações legítimas?** Há critérios operacionais para identificar combinações que precisam de revisão?

### Diferenças de reclamação por produto e distância

- **O que pode diferenciar operacionalmente os Produtos C e D dos Produtos A e B?** Há diferenças de manuseio, acondicionamento, risco de avaria, cliente, rota ou processo de entrega que valha investigar junto às reclamações?
- **As taxas mais altas observadas para C (46,72%) e D (57,89%) persistem em outros períodos e dentro de grupos comparáveis de rota, cliente e tipo de caminhão?** Os tamanhos menores desses grupos (122 viagens para C e 95 para D) devem ser considerados ao priorizar a investigação.
- **Quais são os motivos e a gravidade das reclamações por produto?** A taxa isolada não mostra se os tipos de problema são semelhantes entre produtos.
- **Há algum motivo operacional para a ausência de uma tendência consistente entre distância e reclamação?** Seria útil avaliar outros fatores em conjunto com distância e verificar se os padrões mudam por rota, produto ou tipo de caminhão.
- **Como devem ser definidas as faixas de distância para futuras análises?** As faixas acima de 650 km têm poucos registros (33 no total); a área tem critérios de rota ou operação que permitam agrupamentos mais informativos?

### Paradas do motorista e duração das viagens

- **O que conta como “parada do motorista” e como esse dado é registrado?** A base não identifica o motivo, enquanto as paradas para entrega são contabilizadas separadamente.
- **É possível distinguir descanso, necessidade pessoal, emergência, problema mecânico e outras paradas?** Essa informação permitiria interpretar melhor a razão distância/parada e apoiar a avaliação operacional que o notebook propõe.
- **Os 10 registros acima do P99 de distância por parada — todos com um dia de viagem, oito com uma parada e distâncias de 206 a 588 km — são compatíveis com as regras de registro e operação?** Vale conferir também os horários, a duração real e a contagem das paradas desses casos.
- **A diferença de mediana de paradas entre viagens com reclamação (5) e sem reclamação (4) muda quando as viagens são comparadas por distância, duração ou tipo de ocorrência?** O eta ao quadrado observado é muito pequeno (0,0020), então qualquer aprofundamento deve considerar outros fatores e não tratar essa diferença como explicação da reclamação.
