# Relatório técnico: recomendações para a experiência e a resolução no atendimento

**Organização:** Agência AtendeBem  
**Fonte das evidências:** `notebooks/analise-suporte-cliente.ipynb`  
**Base analisada:** 1.000 registros de atendimento

## 1. Resumo executivo

A principal oportunidade identificada está na resolução dos problemas: 493 dos 1.000 registros foram solucionados, uma taxa observada de **49,3%**, abaixo da referência histórica de **55%**. Os intervalos calculados no notebook permanecem abaixo dessa referência. Recomenda-se tratar a taxa de resolução como um indicador prioritário de acompanhamento e examinar os atendimentos classificados como não solucionados para identificar oportunidades de melhoria.

**O tempo total do atendimento apresentou associação negativa forte com satisfação e NPS**. Também houve taxas de resolução menores entre clientes que esperaram 15 minutos ou mais do que entre aqueles que esperaram até 10 minutos. Esses resultados justificam acompanhar a duração dos atendimentos e revisar os casos com espera prolongada. As análises são associativas e não demonstram que o tempo, isoladamente, cause avaliações menores ou impeça a resolução.

A espera média observada foi de **13,36 minutos**, abaixo do benchmark de 15 minutos considerado no notebook. O sentimento do feedback apresentou pouca capacidade para distinguir problemas resolvidos dos não resolvidos e praticamente nenhuma associação com a variação do NPS. As diferenças observadas entre canais e tipos de problema permanecem inconclusivas; decisões específicas para esses grupos devem aguardar as comparações inferenciais indicadas no notebook.

## 2. Escopo e base de evidências

O notebook analisou 1.000 registros e informou não ter encontrado dados nulos, duplicados, valores inválidos aparentes ou outliers nas variáveis examinadas. As análises incluíram correlações de Pearson para relações entre variáveis numéricas, comparação de taxas de resolução por faixa de espera, medidas de associação entre sentimento e resolução, intervalos de confiança para médias e proporções e comparações exploratórias por canal e tipo de problema.

Os resultados descrevem a base analisada. A representatividade da amostra para todos os clientes da AtendeBem não foi estabelecida no notebook. Além disso, a escala e o método de cálculo da variável `Media_NPS` não foram especificados. Essas condições devem ser consideradas ao levar as conclusões para decisões sobre a população ou para comparações futuras.

## 3. Principais resultados e implicações para o negócio

### 3.1 Duração do atendimento e avaliações dos clientes

O tempo total foi calculado pela soma do tempo de espera e do tempo de resolução. Na amostra, atendimentos mais longos tenderam a acompanhar avaliações menores:

| Relação analisada | Resultado | Leitura para o negócio |
|---|---:|---|
| Tempo total e satisfação | r = -0,86; p < 0,001 | Durações maiores tendem a ocorrer junto de notas de satisfação menores. |
| Tempo total e NPS médio | r = -0,88; p < 0,001 | Durações maiores tendem a ocorrer junto de valores menores de NPS médio. |

Na análise complementar do NPS, o tempo de espera (r = -0,832), o tempo de resolução (r = -0,856) e a quantidade registrada de reclamações (r = -0,837) também apresentaram associações negativas fortes. A satisfação teve associação positiva forte com o NPS (r = 0,868). Esses indicadores apontam quais dimensões merecem acompanhamento conjunto; não identificam, por si só, a causa das avaliações.

### 3.2 Tempo de espera e resolução

As taxas observadas de resolução foram maiores nas faixas de espera até 10 minutos e menores a partir de 15 minutos. A tabela mostra os valores usados nessa comparação:

| Faixa de espera | Registros | Problema solucionado |
|---|---:|---:|
| Até 5 min | 218 | 71,10% |
| Entre 5–10 min | 167 | 64,07% |
| Entre 10–15 min | 165 | 51,52% |
| Entre 15–20 min | 148 | 27,70% |
| 20+ min | 302 | 34,77% |

O IV total foi **0,4623**, classificado no notebook como forte capacidade de separação entre resoluções e não resoluções. A taxa da faixa de 20 minutos ou mais sobe em relação à faixa de 15–20 minutos, portanto o padrão não é uma queda contínua a cada faixa. Em conjunto, os resultados sustentam uma associação entre espera curta e maior resolução observada. O notebook ressalta que outros fatores, como tipo ou complexidade do problema e características do atendimento, podem estar relacionados aos dois resultados.

### 3.3 Taxa de resolução e referência histórica

Foram observados **493 problemas solucionados (49,30%)** e **507 não solucionados**. A taxa ficou 5,7 pontos percentuais abaixo da referência histórica de 55%. Os intervalos de 95% apresentados no notebook também ficaram abaixo de 55%: Wilson, de 46,21% a 52,40%; Clopper–Pearson, de 46,16% a 52,45%; e aproximação *t* de Student, de 46,20% a 52,40%. Assim, a amostra não fornece evidência de que a taxa atual supere a referência.

### 3.4 Feedback de sentimento e indicadores de resultado

O sentimento do feedback apresentou **IV total de 0,0061** para distinguir problemas solucionados e não solucionados, resultado classificado como muito fraco. Na comparação entre sentimento e NPS, o η² foi **0,0008**: apenas **0,0814%** da variação observada no NPS esteve associada às categorias de sentimento. Embora o grupo de sentimento positivo tenha apresentado média e mediana de NPS ligeiramente superiores, as distribuições se sobrepuseram amplamente.

Na comparação descritiva, o grupo com feedback positivo teve média de NPS de 55,9 e mediana de 59,0; no grupo negativo, os valores foram 55,3 e 57,0; no neutro, 53,9 e 51,5. As diferenças entre os valores centrais são pequenas diante da ampla sobreposição das distribuições. Portanto, o sentimento registrado não deve ser interpretado como indicador confiável de resolução nem como substituto do NPS. Para acompanhar cada resultado, o relatório recomenda usar os próprios campos já analisados: `Problema_Solucionado` para resolução e `Media_NPS` para NPS.

### 3.5 Espera média, canais e tipos de problema

O tempo médio de espera foi de **13,36 minutos**, com intervalo de confiança de 95% entre **12,81 e 13,90 minutos**. Como o limite superior ficou abaixo do benchmark de 15 minutos, a média observada está compatível com a referência, sob a condição de que a amostra represente adequadamente a população. Esse resultado descreve a média; não significa que todos os atendimentos ficaram abaixo de 15 minutos.

Nas comparações por canal, Redes Sociais apresentou a menor média observada de espera (**12,54 minutos**) e WhatsApp, a maior (**14,47 minutos**). A sobreposição dos intervalos entre canais impede concluir, com essa comparação, que seus tempos médios sejam diferentes na população.

Por tipo de problema, Dúvida apresentou a maior proporção observada de casos não solucionados (**53,4%**) e Atendimento Ruim, a menor (**46,7%**). Os intervalos de confiança de 95% se sobrepuseram amplamente. As posições dessas categorias são descritivas e não confirmam diferenças populacionais.

## 4. Plano de recomendação

| Prioridade | Recomendação | Evidência | Acompanhamento com dados já disponíveis |
|---|---|---|---|
| 1 | Manter a taxa de resolução sob acompanhamento gerencial e revisar os registros classificados como não solucionados para identificar oportunidades de melhoria no atendimento. | A taxa observada foi 49,30%, abaixo da referência de 55%; 507 registros estavam sem solução. | Acompanhar `Problema_Solucionado` como proporção e confrontar o resultado com a referência histórica de 55%, considerando a incerteza apresentada no notebook. |
| 2 | Usar as faixas de espera como sinal para examinar atendimentos que chegaram a 15 minutos ou mais e entender o que ocorreu nos casos sem solução. | As taxas de resolução foram maiores até 10 minutos e menores nas faixas a partir de 15 minutos; o IV das faixas foi 0,4623. | Comparar `Tempo_Espera` e `Problema_Solucionado` por faixa, mantendo visíveis a taxa e o volume de registros em cada grupo. |
| 3 | Revisar os atendimentos com maior tempo total, observando espera, resolução, satisfação e NPS em conjunto, para localizar casos que mereçam análise operacional. | O tempo total teve associações negativas fortes com satisfação e NPS; espera, resolução e reclamações também se associaram negativamente ao NPS. | Acompanhar `Tempo_Espera`, `Tempo_Resolucao`, a soma dos dois tempos, `Satisfacao_Cliente`, `Media_NPS` e `Qtd_Reclamacoes` em conjunto. |
| 4 | Usar o sentimento como contexto qualitativo do feedback, mantendo a resolução e o NPS medidos pelos respectivos campos da base. | O IV de sentimento para resolução foi 0,0061 e o η² para NPS foi 0,0008. | Conferir `Problema_Solucionado` e `Media_NPS` diretamente ao avaliar esses resultados. |
| 5 | Aprofundar as comparações por canal e tipo de problema antes de orientar mudanças específicas para esses grupos. | Os intervalos se sobrepuseram nas comparações observadas; o notebook recomenda ANOVA para tempos por canal, se os pressupostos forem atendidos, e qui-quadrado com V de Cramér para resolução por tipo de problema. | Apresentar os resultados dos testes e a medida de associação junto das proporções ou médias, incluindo os intervalos de confiança. |

## 5. Diretrizes de interpretação

- As correlações e associações descrevem padrões observados; o notebook não testou relações causais nem avaliou intervenções operacionais.
- As diferenças pontuais entre canais e tipos de problema não foram confirmadas por testes inferenciais no notebook. A própria seção de aprofundamento recomenda essas análises como próximo passo.
- A média de espera abaixo de 15 minutos representa o comportamento médio da amostra e não descreve cada atendimento individual.
- A generalização dos resultados depende de a amostra representar adequadamente a população atendida. A definição de `Media_NPS` também precisa ser conhecida para interpretar sua escala em decisões futuras.

## 6. Conclusão

Os resultados apontam três frentes sustentadas pelas análises: acompanhar a taxa de resolução, examinar o vínculo observado entre tempos de atendimento e avaliações dos clientes e investigar os casos com espera prolongada. O sentimento do feedback, isoladamente, não representa adequadamente a resolução ou o NPS. Já as comparações por canal e tipo de problema precisam de aprofundamento estatístico antes de orientar decisões segmentadas. As recomendações acima se limitam aos achados, às cautelas e aos próximos passos explicitados no notebook.
