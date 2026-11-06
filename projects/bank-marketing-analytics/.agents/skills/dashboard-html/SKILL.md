---
name: dashboard-html
description: Gere dashboards HTML responsivos a partir de análises documentadas, com gráficos Chart.js, métricas reproduzíveis e identidade visual configurável por projeto.
---

# Dashboard HTML
Skill genérica para transformar qualquer dataset tabular em um dashboard interativo de arquivo único (HTML + Chart.js), pronto para enviar por e-mail ou abrir em qualquer navegador, sem instalação.

## Fluxo de trabalho

1. Leia o `AGENTS.md` do projeto e a fonte analítica indicada. Registre perguntas de negócio, recortes, denominadores, decisões de limpeza e ressalvas relevantes.
2. Inspecione esta pasta de skill antes de criar código novo. Reutilize seus scripts quando o trabalho corresponder a este fluxo. Os módulos ficam em `scripts/`:
   - `scripts/gerar_dashboards.py` é o ponto de entrada desta adaptação. Recebe a planilha Bank Marketing e gera os dois arquivos em `reports/`.
   - `scripts/dados_dashboard.py` valida e prepara os dados, aplica os cortes do notebook e calcula estatísticas e agregados.
   - `scripts/visualizacoes_dashboard.py` contém componentes de gráfico e apresentação. Reutilize a estrutura visual ao adaptar os tipos de gráfico.
   - `scripts/dashboard.css` define os estilos responsivos e a identidade visual desta adaptação.
   - `scripts/dashboard.js` inicializa Chart.js, formata eixos e dicas de ferramenta, redimensiona gráficos em seções recolhíveis e exibe as tabelas se a biblioteca não carregar.
3. Execute o ponto de entrada a partir da raiz do projeto. Para a adaptação bancária:

   ```powershell
   uv run python .agents/skills/dashboard-html/scripts/gerar_dashboards.py
   ```

4. Confira os principais valores gerados com a fonte analítica e verifique as saídas HTML no navegador em largura desktop e celular. Não leia valores de células de saída antigas de um notebook sem recalculá-los.

## Dados e apresentação

- O dashboard responde perguntas, não exibe dados. Antes de montar, identifique as 3-5 perguntas que a liderança quer responder (tendência? comparação? meta?). Cada gráfico existe para responder uma delas.
- Títulos com conclusão. Em vez de "Vendas por mês", escreva "Vendas crescem 12% no trimestre, puxadas pelo Sudeste". O executivo lê o título; o gráfico é a evidência.
- Arquivo único e offline-friendly. Dados embutidos como JSON no próprio HTML; única dependência externa é o CDN do Chart.js.
- Preserve classes, categorias, intervalos, denominadores e limitações definidas pela análise. Mostre contagens ao lado de taxas por grupo. Não introduza interpretações causais sem suporte analítico.
- Aplique paleta, tipografia e demais tokens indicados no `AGENTS.md` do projeto. Sem especificação local, use o padrão desta skill de fundo claro, uma cor principal e neutros para contexto.
- Organize a página por perguntas. Use títulos que ajudem a interpretar cada gráfico, texto curto para os achados e detalhes recolhíveis para tabelas extensas.
- Faça o HTML funcionar sem um processo de build no navegador. Incorpore os dados agregados como JSON e mantenha os cálculos de negócio em Python.

## Chart.js e responsividade

- Use Chart.js para gráficos interativos. Carregue a versão 4 pelo CDN oficial do pacote, com uma versão fixada na URL para tornar a saída reproduzível. Declare que gráficos precisam de internet para carregar o CDN.
- Cada `canvas` deve ter um contêiner próprio com `position: relative`, largura de 100% e uma altura CSS adequada ao gráfico. Configure `responsive: true` e `maintainAspectRatio: false` para o gráfico usar as dimensões do contêiner.
- Use CSS Grid com colunas `minmax(0, 1fr)`, permita que painéis encolham com `min-width: 0` e mude para uma coluna em telas estreitas. Evite larguras fixas em cartões e canvases.
- Recalcule alturas em uma media query quando a proporção ideal mudar no celular. Gráficos de barras horizontais podem manter o rótulo completo com rolagem horizontal dentro do painel; o restante da página não deve transbordar horizontalmente.
- Defina cores, legendas, eixos, dicas de ferramenta e formatação numérica de forma consistente com a identidade visual. Use cores diferenciáveis além da cor, como rótulos, marcadores ou padrões, quando for necessário distinguir séries.
- Dê ao `canvas` um `role="img"` e um `aria-label` descritivo. Coloque uma tabela de dados equivalente ou uma alternativa textual próxima ao gráfico para leitura assistiva e para valores quando JavaScript ou o CDN não carregar.
- Não trate os recursos interativos como único acesso aos números. Títulos, notas metodológicas, valores e denominadores importantes devem permanecer em HTML.

## Tipos de gráfico

Prefira barras horizontais para rankings e comparações categóricas, linhas para séries ordenadas, barras empilhadas para composição e mapas de calor quando duas dimensões forem cruzadas. Use rosca somente para poucas partes de um todo. Não use dupla escala sem uma justificativa clara. Não esconda denominadores em dicas de ferramenta.

## Referência de implementação

As opções responsivas seguem a orientação oficial do Chart.js. O contêiner dedicado deve controlar o tamanho do canvas, com `responsive: true` e `maintainAspectRatio: false`: [Chart.js — Responsive Charts](https://www.chartjs.org/docs/latest/configuration/responsive.html). Para acessibilidade, identifique o canvas com nome acessível e forneça os dados em HTML: [Chart.js — Accessibility](https://www.chartjs.org/docs/latest/general/accessibility.html).
