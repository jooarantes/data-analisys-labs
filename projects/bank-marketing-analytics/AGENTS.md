# Agente de dashboards do Banco XPTOKW

- Use `notebooks/banco-analise-campanha.ipynb` como fonte das análises, definições, gráficos e ressalvas. Os scripts devem recalcular as métricas da planilha em `data/`, seguindo os tratamentos do notebook.
- Distribua as análises entre o perfil dos clientes e a conversão da campanha. Preserve os rótulos `Sim` e `Não`, informe os denominadores e mantenha a distinção entre participação na base, participação nas compras e taxa de compra por grupo.
- Aplique a identidade visual local nos dois painéis. Use `#171717` para texto e cabeçalho, `#C5A15A` para destaques e séries, e `#F4F0E7` para o fundo. Use fonte serifada nos títulos e sem serifa na interface. A origem da especificação é `images/identidade-visual-banco-xptokw.png`.
- Apresente a conversão como resultado observado da campanha. Preserve as ressalvas de representatividade, duplicidade, incerteza e causalidade. Diferencie faixas exatas de ligações dos grupos acumulados e trate o IV como medida exploratória.
- Ao criar ou atualizar um painel, leia `.agents/skills/dashboard-html/SKILL.md` e use os scripts que fazem parte dela.
- Execute `uv run python .agents/skills/dashboard-html/scripts/gerar_dashboards.py` na raiz deste projeto para recriar os dois HTMLs em `reports/`. A implementação e a procedência da adaptação estão documentadas em `docs/arquitetura-agente-dashboard.md`.
