"""Gráficos Chart.js com dados agregados e alternativas textuais em HTML."""

from base64 import b64encode
from html import escape
from io import BytesIO
import json

import matplotlib as mpl
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

ESCURO = "#171717"
DOURADO = "#C5A15A"


def numero(valor: float, casas: int = 0) -> str:
    return f"{valor:,.{casas}f}".translate(str.maketrans(".,", ",."))


def percentual(valor: float, casas: int = 2) -> str:
    return f"{numero(valor, casas)}%" if pd.notna(valor) else "—"


def tabela(dados: pd.DataFrame, legenda: str) -> str:
    html = dados.to_html(index=False, border=0, escape=True)
    html = html.replace(">", f"><caption>{escape(legenda)}</caption>", 1)
    return f'<div class="rolagem" tabindex="0" role="region" aria-label="{escape(legenda)}">{html}</div>'


def grafico(config: dict, descricao: str, dados: pd.DataFrame, altura: int = 310) -> str:
    """Embute configuração JSON escapada e tabela equivalente ao canvas."""
    payload = json.dumps(config, ensure_ascii=False, allow_nan=False).replace("<", "\\u003c")
    return (
        f'<figure class="visualizacao"><div class="chart-container" style="--altura:{altura}px">'
        f'<canvas role="img" aria-label="{escape(descricao)}">{escape(descricao)}</canvas></div>'
        f'<script type="application/json" class="chart-data">{payload}</script>'
        f'<details class="dados-grafico"><summary>Ver dados do gráfico</summary>'
        f'{tabela(dados, descricao)}</details></figure>'
    )


def barras(linhas: list[tuple[str, float, str]], escala: float = 100,
           referencia: float | None = None, metrica: str = "percentual",
           descricao: str = "Distribuição por categoria") -> str:
    valores = [float(valor) for _, valor, _ in linhas]
    config = {
        "type": "bar", "horizontal": True, "metric": metrica, "max": escala,
        "reference": referencia,
        "data": {"labels": [str(rotulo) for rotulo, _, _ in linhas], "datasets": [{
            "label": descricao, "data": valores,
            "backgroundColor": [ESCURO if valor < 0 else DOURADO for valor in valores],
            "borderRadius": 5, "maxBarThickness": 26,
            "details": [detalhe for _, _, detalhe in linhas],
        }]},
    }
    quadro = pd.DataFrame([(rotulo, detalhe) for rotulo, _, detalhe in linhas], columns=["Grupo", "Resultado"])
    return grafico(config, descricao, quadro, max(170, 48 * len(linhas) + 45))


def distribuicao(serie: pd.Series, unidade: str) -> str:
    contagens, limites = np.histogram(serie.to_numpy(), bins=30)
    rotulos = [f"{numero(a, 1)} – {numero(b, 1)}" for a, b in zip(limites[:-1], limites[1:])]
    config = {
        "type": "bar", "metric": "contagem", "axisTitle": unidade,
        "data": {"labels": rotulos, "datasets": [{
            "label": "Clientes", "data": contagens.tolist(), "backgroundColor": DOURADO,
            "barPercentage": 1, "categoryPercentage": 1, "borderColor": "#fffdf9", "borderWidth": 1,
        }]},
    }
    quadro = pd.DataFrame({"Intervalo": rotulos, "Clientes": [numero(v) for v in contagens]})
    histograma = grafico(config, f"Distribuição de {unidade.lower()}", quadro)
    # Chart.js básico não inclui boxplot. Preserva-se o resumo do notebook em SVG.
    figura = Figure(figsize=(5.6, 1.1), layout="constrained")
    eixo = figura.subplots()
    eixo.boxplot(serie, orientation="horizontal", showfliers=False, patch_artist=True,
                 boxprops={"facecolor": DOURADO}, medianprops={"color": ESCURO, "linewidth": 2})
    eixo.set_yticks([])
    eixo.xaxis.set_major_formatter(FuncFormatter(lambda valor, _: numero(valor)))
    eixo.spines[["top", "right", "left"]].set_visible(False)
    arquivo = BytesIO()
    with mpl.rc_context({"svg.hashsalt": "bank-marketing-analytics"}):
        figura.savefig(arquivo, format="svg", bbox_inches="tight", transparent=True, metadata={"Date": None})
    imagem = b64encode(arquivo.getvalue()).decode("ascii")
    return histograma + f'<details><summary>Ver boxplot</summary><img class="grafico" src="data:image/svg+xml;base64,{imagem}" alt="Boxplot de {escape(unidade)}"></details>'


def pareto(frequencias: pd.Series) -> str:
    acumulado = frequencias.cumsum() / frequencias.sum() * 100
    config = {
        "type": "bar", "metric": "contagem", "secondary": True, "legend": True,
        "data": {"labels": frequencias.index.tolist(), "datasets": [
            {"label": "Clientes", "data": frequencias.tolist(), "backgroundColor": DOURADO,
             "borderRadius": 4, "yAxisID": "y", "order": 2},
            {"type": "line", "label": "Participação acumulada", "data": acumulado.tolist(),
             "borderColor": ESCURO, "backgroundColor": ESCURO, "pointRadius": 3,
             "yAxisID": "y1", "order": 1},
        ]},
    }
    quadro = pd.DataFrame({"Profissão": frequencias.index, "Clientes": frequencias.map(numero).values,
                          "% acumulado": acumulado.map(lambda v: percentual(v, 1)).values})
    return grafico(config, "Pareto por profissão — clientes e participação acumulada", quadro, 380)


def curvas_ligacoes(dados: pd.DataFrame, taxa_geral: float) -> str:
    series = []
    for (nome, grupo), cor, marcador in zip(
        dados.groupby("condicao", sort=False), [DOURADO, ESCURO], ["circle", "rect"], strict=True,
    ):
        series.append({"label": nome, "data": [float(v) if pd.notna(v) else None for v in grupo["taxa"]],
                       "borderColor": cor, "backgroundColor": cor, "pointStyle": marcador,
                       "pointRadius": 5, "borderWidth": 2.5, "tension": 0,
                       "details": [f"{numero(c)} compras em {numero(n)} clientes"
                                   for c, n in zip(grupo["compras"], grupo["total"])]})
    quadro = dados.rename(columns={"condicao": "Condição", "limiar": "k", "total": "Clientes", "compras": "Compras", "taxa": "Taxa"}).copy()
    quadro["Taxa"] = quadro["Taxa"].map(percentual)
    return grafico({"type": "line", "metric": "percentual", "legend": True,
                    "reference": taxa_geral, "max": 100, "axisTitle": "Limiar de ligações (k)",
                    "data": {"labels": [2, 3, 4, 5], "datasets": series}},
                   "Compra por condição acumulada de ligações", quadro)


def mapa_calor(cruzamento: pd.DataFrame) -> str:
    """A tabela colorida permite ler taxas e contagens sem JavaScript."""
    totais = cruzamento["total"].unstack(fill_value=0)
    compras = cruzamento["compras"].unstack(fill_value=0)
    cabecalho = "".join(f'<th scope="col">{escape(str(coluna))}</th>' for coluna in totais)
    linhas = []
    for idade, totais_idade in totais.iterrows():
        celulas = []
        for profissao, total in totais_idade.items():
            if not total:
                celulas.append('<td class="sem-dados">—</td>')
                continue
            taxa = 100 * compras.loc[idade, profissao] / total
            celulas.append(f'<td style="--intensidade:{taxa / 100:.3f}"><strong>{percentual(taxa, 1)}'
                           f'</strong><small>n = {numero(total)}</small></td>')
        linhas.append(f'<tr><th scope="row">{escape(str(idade))}</th>{"".join(celulas)}</tr>')
    return (
        '<div class="rolagem" tabindex="0" role="region" aria-label="Mapa de calor por idade e profissão"><table class="mapa">'
        '<caption>Taxa de compra e tamanho de cada grupo</caption>'
        f'<thead><tr><th scope="col">Faixa etária</th>{cabecalho}</tr></thead>'
        f'<tbody>{"".join(linhas)}</tbody></table></div>'
    )
