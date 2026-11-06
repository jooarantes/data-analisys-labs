"""Gera os dois dashboards com os recursos da skill dashboard-html."""

from html import escape
from pathlib import Path
import sys

import pandas as pd

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ))

from dados_dashboard import (
    ALVO, LIGACOES, ORDEM_FORMACAO, PERFIL, SALDO, SEGMENTOS,
    carregar_campanha, intervalos_conversao, probabilidades_ligacoes, tabelas_conversao,
)
from visualizacoes_dashboard import (
    barras, curvas_ligacoes, distribuicao, mapa_calor, numero, pareto, percentual, tabela,
)

PAGINAS = {
    "perfil": ("Perfil dos clientes", "dashboard-perfil-clientes.html"),
    "conversao": ("Conversão da campanha", "dashboard-conversao-campanha.html"),
}


def pagina(tipo: str, introducao: str, conteudo: str) -> str:
    titulo, _ = PAGINAS[tipo]
    links = []
    for chave, (nome, arquivo) in PAGINAS.items():
        atual = ' aria-current="page"' if chave == tipo else ""
        links.append(f'<a href="{arquivo}"{atual}>{nome}</a>')
    estilo = Path(__file__).with_name("dashboard.css").read_text(encoding="utf-8")
    interacoes = Path(__file__).with_name("dashboard.js").read_text(encoding="utf-8")
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{titulo} | Banco XPTOKW</title>
  <style>{estilo}</style>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js" defer></script>
</head>
<body>
  <header class="topo">
    <div class="largura">
      <div class="marca-banco"><span class="simbolo" aria-hidden="true">X</span> Banco XPTOKW</div>
      <p class="sobretitulo">Estudo de campanha · Título de investimento</p>
      <h1>{titulo}</h1>
      <p class="introducao">{introducao}</p>
    </div>
  </header>
  <main class="largura">
    <nav class="nav" aria-label="Dashboards">{"".join(links)}</nav>
    <p class="aviso-graficos destaque" role="status" hidden>Os gráficos não carregaram.
    Consulte as tabelas de dados abaixo ou recarregue a página com conexão à internet.</p>
    <noscript><p class="destaque">Ative JavaScript para explorar os gráficos.
    Os valores estão disponíveis nas tabelas de cada seção.</p></noscript>
    {conteudo}
    <footer>
      <p>Fonte: planilha Bank Marketing, disponibilizada pela Preditiva Analytics.
      A análise considera os registros após a remoção de duplicatas exatas, conforme a premissa do estudo.</p>
      <p><a href="../notebooks/banco-analise-campanha.ipynb">Notebook de referência</a>
      · <a href="../docs/arquitetura-agente-dashboard.md">Arquitetura e reprodução</a></p>
      <p>Os gráficos interativos precisam de conexão à internet. As tabelas permanecem disponíveis no arquivo.</p>
    </footer>
  </main>
  <script>{interacoes}</script>
</body>
</html>
"""


def indicadores(itens: list[tuple[str, str, str]]) -> str:
    cartoes = [
        f'<div class="kpi"><span class="rotulo">{rotulo}</span>'
        f'<strong class="numero">{valor}</strong><small>{nota}</small></div>'
        for rotulo, valor, nota in itens
    ]
    return f'<div class="kpis" aria-label="Indicadores principais">{"".join(cartoes)}</div>'


def frequencias(contagens: pd.Series, descricao: str) -> str:
    total = contagens.sum()
    return barras([
        (str(rotulo), 100 * qtd / total, f"{percentual(100 * qtd / total, 1)} · {numero(qtd)} clientes")
        for rotulo, qtd in contagens.items()
    ], descricao=descricao)


def resumo_numerico(serie: pd.Series, casas: int) -> str:
    q1, mediana, q3 = serie.quantile([.25, .5, .75])
    iqr = q3 - q1
    atipicos = serie.lt(q1 - 1.5 * iqr) | serie.gt(q3 + 1.5 * iqr)
    medidas = [
        ("Média", serie.mean()), ("Desvio padrão", serie.std()),
        ("Mínimo", serie.min()), ("Primeiro quartil", q1), ("Mediana", mediana),
        ("Terceiro quartil", q3), ("Máximo", serie.max()),
    ]
    linhas = [(medida, numero(valor, casas)) for medida, valor in medidas]
    linhas.append(("Valores atípicos pelo critério de 1,5 × IQR", percentual(100 * atipicos.mean())))
    quadro = tabela(pd.DataFrame(linhas, columns=["Medida", "Valor"]), "Estatísticas descritivas")
    return (
        f'<details><summary>Ver estatísticas descritivas</summary>{quadro}'
        '<p class="nota">O histograma inclui todos os valores. O boxplot resume a distribuição '
        'sem marcar os pontos atípicos individualmente.</p></details>'
    )


def perfil(dados: pd.DataFrame, total_bruto: int) -> str:
    total = len(dados)
    idade, saldo = dados["Idade"], dados[SALDO]
    idade_q1, idade_q3 = idade.quantile([.25, .75])
    saldo_q1, saldo_q3 = saldo.quantile([.25, .75])
    profissoes = dados["Profissão"].value_counts()
    acumulado = profissoes.cumsum() / total * 100
    ate_80 = int(acumulado.lt(80).sum()) + 1
    lista_80 = ", ".join(map(escape, profissoes.index[:ate_80]))
    civil = dados["Estado_Civil"].value_counts()
    estado_principal = escape(str(civil.index[0]))
    proporcao_civil = percentual(100 * civil.iloc[0] / total, 1)
    formacao = dados["Formação"].value_counts().reindex(ORDEM_FORMACAO, fill_value=0)
    sem_superior = formacao[["Fundamental", "Ensino Médio"]].sum()
    limite_superior = sem_superior + formacao["Desconhecido"]
    financeiro = []
    for coluna, condicao in [
        ("Cliente_Devedor?", "tinham registro de inadimplência"),
        ("Tem_Hipoteca?", "tinham hipoteca"),
        ("Tem_Emprestimo?", "tinham empréstimo pessoal"),
    ]:
        contagens = dados[coluna].value_counts().reindex(["Sim", "Não"], fill_value=0)
        financeiro.append(
            f'<div><h3>{percentual(100 * contagens["Sim"] / total, 1)} dos clientes {condicao}</h3>'
            f'{frequencias(contagens, PERFIL[coluna])}</div>'
        )
    kpis = indicadores([
        ("Clientes analisados", numero(total), f"{numero(total_bruto - total)} duplicatas removidas"),
        ("Idade mediana", f"{numero(idade.median())} anos", f"Média de {numero(idade.mean(), 1)} anos"),
        ("Saldo mediano", f"R$ {numero(saldo.median(), 2)}", "Saldo em conta corrente"),
    ])
    kpis = kpis.replace('class="kpis"', 'class="kpis kpis-centralizados"')
    conteudo = f"""
    {kpis}
    <nav class="nav indice" aria-label="Perguntas sobre o perfil dos clientes">
      <a href="#profissoes">Quais profissões concentram a base?</a>
      <a href="#demografia">Qual é o perfil demográfico?</a>
      <a href="#formacao">Qual é o nível de formação?</a>
      <a href="#financeiro">Como é o perfil financeiro?</a>
    </nav>
    <section class="painel" id="profissoes">
      <h2>{percentual(acumulado.iloc[ate_80 - 1], 1)} da base se concentra em {numero(ate_80)} profissões</h2>
      <p>Em ordem de frequência, os grupos são {lista_80}.</p>
      {pareto(profissoes)}
    </section>
    <section id="demografia" class="painel">
      <h2>Metade dos clientes está entre {numero(idade_q1)} e {numero(idade_q3)} anos</h2>
      <div class="grade">
        <div>
          <p>As idades observadas vão de {numero(idade.min())} a {numero(idade.max())} anos.</p>
          {distribuicao(idade, "Idade (anos)")}
          {resumo_numerico(idade, 2)}
        </div>
        <div>
          <h3>“{estado_principal}” é o estado civil mais frequente, com {proporcao_civil} da base</h3>
          {frequencias(civil, "Clientes por estado civil")}
        </div>
      </div>
    </section>
    <section id="formacao" class="painel">
      <h2>A parcela sem Ensino Superior fica entre {percentual(100 * sem_superior / total, 1)} e {percentual(100 * limite_superior / total, 1)}</h2>
      <p>O limite inferior conta os {numero(sem_superior)} clientes com formação até o Ensino Médio.
      O limite superior supõe que nenhum dos {numero(formacao["Desconhecido"])} clientes com formação “Desconhecido”
      tenha Ensino Superior.</p>
      {frequencias(formacao, "Clientes por nível de formação")}
    </section>
    <section id="financeiro" class="painel">
      <h2>O saldo mediano em conta corrente foi de R$ {numero(saldo.median(), 2)}</h2>
      <div class="grade">
        <div>
          <p>Metade dos saldos fica entre R$ {numero(saldo_q1, 2)} e R$ {numero(saldo_q3, 2)}.
          A média foi de R$ {numero(saldo.mean(), 2)}.</p>
          {distribuicao(saldo, "Saldo (R$)")}
          {resumo_numerico(saldo, 2)}
        </div>
        {"".join(financeiro)}
      </div>
    </section>
    """
    return pagina("perfil", "Quem são os clientes que receberam a oferta de investimento?", conteudo)


def taxas_segmento(dados: pd.DataFrame, taxa_geral: float, descricao: str) -> str:
    return barras([
        (str(categoria), linha["Taxa Evento (%)"],
         f'{percentual(linha["Taxa Evento (%)"])} · {numero(linha["Sim"])} de {numero(linha["Total"])}')
        for categoria, linha in dados.iterrows()
    ], referencia=taxa_geral, descricao=descricao)


def detalhes_segmento(dados: pd.DataFrame, nome: str, taxa_geral: float) -> str:
    exibicao = dados.rename(columns={"Taxa Evento (%)": "Taxa de compra"}).copy()
    exibicao.insert(0, "Grupo", dados.index.astype(str))
    for coluna in ("Sim", "Não", "Total"):
        exibicao[coluna] = exibicao[coluna].map(numero)
    for coluna in ("Freq Rel (%)", "% Não", "% Sim", "Taxa de compra"):
        exibicao[coluna] = exibicao[coluna].map(percentual)
    for coluna in ("WoE", "IV Parcial"):
        exibicao[coluna] = exibicao[coluna].map(lambda valor: numero(valor, 4))
    grupo = dados["Taxa Evento (%)"].idxmax()
    maior = dados.loc[grupo]
    return (
        f'<details><summary>{nome}</summary>'
        f'<p>A maior taxa observada foi de {percentual(maior["Taxa Evento (%)"])} no grupo “{escape(str(grupo))}”, '
        f'com {numero(maior["Sim"])} compras em {numero(maior["Total"])} clientes.</p>'
        f'{taxas_segmento(dados, taxa_geral, f"Taxa de compra por {nome.lower()}")}'
        f'{tabela(exibicao, f"{nome} · contagens, taxas e medidas de associação")}</details>'
    )


def destaques_woe(tabelas: dict[str, pd.DataFrame]) -> str:
    linhas = [
        (f"{nome} · {categoria}", linha["WoE"], int(linha["Total"]))
        for coluna, nome in SEGMENTOS.items()
        for categoria, linha in tabelas[coluna].iterrows()
    ]
    top = sorted(linhas, key=lambda linha: abs(linha[1]), reverse=True)[:10]
    escala = max(abs(linha[1]) for linha in top) or 1
    grafico = barras([(rotulo, woe, f"{numero(woe, 4)} · n = {numero(total)}")
                      for rotulo, woe, total in top], escala=escala, metrica="decimal",
                     descricao="Dez maiores magnitudes de Weight of Evidence (WoE)")
    return f'<h3>{escape(top[0][0])} teve o WoE de maior magnitude</h3>{grafico}'


def conversao(dados: pd.DataFrame) -> str:
    total = len(dados)
    compras = int(dados[ALVO].eq("Sim").sum())
    taxa_geral = 100 * compras / total
    intervalos = intervalos_conversao(compras, total)
    wilson = " a ".join(percentual(100 * limite) for limite in intervalos["Wilson"])
    tabela_ic = tabela(pd.DataFrame([
        (metodo, percentual(100 * limites[0]), percentual(100 * limites[1]))
        for metodo, limites in intervalos.items()
    ], columns=["Método", "Limite inferior", "Limite superior"]), "Intervalos de confiança de 95%")
    tabelas, ranking, cruzamento = tabelas_conversao(dados)
    idades = tabelas["Faixa_Idade"]
    melhor_faixa = str(idades["Taxa Evento (%)"].idxmax())
    faixa = (
        f"{melhor_faixa.removesuffix('+')} anos ou mais" if melhor_faixa.endswith("+")
        else f"{melhor_faixa.replace('–', ' a ')} anos"
    )
    melhor_idade = idades.loc[melhor_faixa]
    hipotecas = tabelas["Tem_Hipoteca?"]["Taxa Evento (%)"]
    titulo_segmentos = "Taxa de compra entre os grupos observados"
    titulo_hipoteca = "Taxa de compra por situação de hipoteca"
    if len(hipotecas) == 2:
        diferenca = abs(hipotecas["Não"] - hipotecas["Sim"])
        titulo_hipoteca = f"Taxa de {percentual(hipotecas['Não'])} sem hipoteca e de {percentual(hipotecas['Sim'])} com hipoteca"
        if diferenca:
            grupo = "sem hipoteca" if hipotecas["Não"] > hipotecas["Sim"] else "com hipoteca"
            titulo_segmentos = f"A taxa de compra foi {numero(diferenca, 1)} p.p. maior entre clientes {grupo}"
    segmentos = "".join(detalhes_segmento(tabelas[coluna], nome, taxa_geral) for coluna, nome in SEGMENTOS.items())
    faixas_ligacoes = tabelas["Faixa_Qtd_Ligações"]
    taxas_ligacoes = faixas_ligacoes["Taxa Evento (%)"]
    titulo_ligacoes = "A taxa de compra por faixa de ligações"
    if {"1", "5+"}.issubset(taxas_ligacoes.index):
        titulo_ligacoes = (
            f"A taxa foi de {percentual(taxas_ligacoes['1'])} no grupo de uma ligação "
            f"e de {percentual(taxas_ligacoes['5+'])} no de cinco ou mais"
        )
    ligacoes = probabilidades_ligacoes(dados)
    taxa_minimo_duas = ligacoes.loc[
        ligacoes["condicao"].eq("k ou mais ligações") & ligacoes["limiar"].eq(2), "taxa"
    ].iloc[0]
    titulo_acumulado = "Taxa por número mínimo ou máximo de ligações"
    if pd.notna(taxa_minimo_duas):
        titulo_acumulado = f"Entre quem recebeu duas ligações ou mais, {percentual(taxa_minimo_duas)} compraram"
    lider_iv = SEGMENTOS[ranking.index[0]]
    maior_iv = numero(ranking["IV"].iloc[0], 4)
    grafico_iv = barras([
        (SEGMENTOS[coluna], linha["IV"], f'{numero(linha["IV"], 4)} · {linha["Classificação"]}')
        for coluna, linha in ranking.iterrows()
    ], escala=max(ranking["IV"].max(), .3), metrica="decimal", descricao="Information Value (IV)")
    kpis = indicadores([
        ("Taxa de compra", percentual(taxa_geral), f"{numero(compras)} compras em {numero(total)} clientes"),
        ("Não compraram", numero(total - compras), f"{percentual(100 - taxa_geral)} dos clientes"),
        ("IC de 95% · Wilson", wilson, "Incerteza amostral da taxa de compra"),
    ])
    kpis = kpis.replace('class="kpis"', 'class="kpis kpis-centralizados"')
    conteudo = f"""
    {kpis}
    <nav class="nav indice" aria-label="Perguntas sobre a conversão da campanha">
      <a href="#estimativa">Quantos clientes compraram?</a>
      <a href="#segmentos">Em quais grupos a taxa foi maior?</a>
      <a href="#ligacoes">Como a taxa varia com as ligações?</a>
      <a href="#associacao">Quais variáveis mais distinguem compradores?</a>
    </nav>
    <section id="estimativa" class="painel">
      <h2>{percentual(taxa_geral)} dos clientes analisados compraram o título</h2>
      <p>Foram {numero(compras)} compras entre {numero(total)} clientes. O intervalo de 95% de Wilson vai de {wilson}.</p>
      {frequencias(dados[ALVO].value_counts().reindex(["Sim", "Não"]), "Clientes por resultado de compra")}
      <p>Generalizar a estimativa exige uma amostra representativa e condições comparáveis de público, oferta e abordagem.</p>
      <details>
        <summary>Comparar métodos de intervalo de confiança</summary>
        {tabela_ic}
        <p>Em amostragens repetidas, um método com cobertura de 95% produz intervalos que contêm a proporção
        populacional em cerca de 95% das repetições, sob as premissas do método.</p>
      </details>
    </section>
    <section id="segmentos" class="painel">
      <h2>{titulo_segmentos}</h2>
      <p>A taxa de cada grupo divide o número de compras pelo total de clientes daquele grupo.
      A linha tracejada indica a taxa geral de <strong>{percentual(taxa_geral)}</strong>.</p>
      <div class="grade">
        <div>
          <h3>Na faixa de {faixa}, {percentual(melhor_idade["Taxa Evento (%)"])} compraram</h3>
          <p class="nota">Foram {numero(melhor_idade["Sim"])} compras em {numero(melhor_idade["Total"])} clientes,
          a maior taxa observada entre as faixas etárias.</p>
          {taxas_segmento(idades, taxa_geral, "Taxa de compra por faixa etária")}
        </div>
        <div>
          <h3>{titulo_hipoteca}</h3>
          {taxas_segmento(tabelas["Tem_Hipoteca?"], taxa_geral, "Taxa de compra por situação de hipoteca")}
        </div>
      </div>
      <details><summary>Faixa etária x Profissão x Taxa de Compra</summary>
        <p>O cruzamento ajuda a contextualizar as taxas mais altas entre estudantes e aposentados.
        Leia cada taxa junto ao tamanho do grupo. O traço indica combinações sem observações.</p>
        {mapa_calor(cruzamento)}
      </details>
      {segmentos}
      <details><summary>Detalhamento dos saldos a partir de R$ 5 mil</summary>
        <p>O corte em R$ 1.500 é exploratório. Acima dele, as taxas são semelhantes.
        O desdobramento em R$ 10 mil cria grupos menores, o que limita a leitura da diferença.</p>
        {taxas_segmento(tabelas["Saldo_Detalhado"], taxa_geral, "Taxa de compra com detalhamento dos saldos")}
      </details>
    </section>
    <section id="ligacoes" class="painel">
      <h2>{titulo_ligacoes}</h2>
      <div class="grade">
        <div><h3>Cada faixa reúne um grupo distinto de clientes</h3>
          {taxas_segmento(faixas_ligacoes, taxa_geral, "Taxa de compra por faixa de ligações")}
          <p class="nota">Cada cliente aparece em uma única faixa. O máximo observado foi
          de {numero(dados[LIGACOES].max())} ligações.</p></div>
        <div><h3>{titulo_acumulado}</h3>{curvas_ligacoes(ligacoes, taxa_geral)}
          <p class="nota">Os grupos por limiar se sobrepõem. “Até k” inclui quem recebeu k ligações ou menos.
          “k ou mais” inclui quem recebeu k ligações ou mais.</p></div>
      </div>
      <p class="destaque">A taxa observada é menor nos grupos com mais ligações. Clientes com menor interesse
      podem ter recebido mais tentativas, e as ligações podem ter cessado após a compra.</p>
    </section>
    <section id="associacao" class="painel">
      <h2>{lider_iv} teve o maior Information Value (IV), de {maior_iv}</h2>
      <div class="grade">
        <div>{grafico_iv}
          <p class="nota">O IV resume a capacidade de distinção observada de cada variável, isoladamente.
          As faixas e categorias adotadas influenciam essa medida.</p></div>
        <div>{destaques_woe(tabelas)}
          <p class="nota">WoE negativo indica maior representação proporcional entre compradores.
          WoE positivo indica maior representação proporcional entre quem não comprou.</p></div>
      </div>
      <p class="destaque">IV e WoE descrevem associações na base. Interprete os valores junto às frequências
      e à taxa de compra, principalmente quando o grupo é pequeno.</p>
    </section>
    """
    return pagina("conversao", "Qual foi a taxa de compra e como ela variou entre os grupos analisados?", conteudo)


def main() -> None:
    dados, total_bruto = carregar_campanha(RAIZ / "data" / "bank_marketing.xlsx")
    relatorios = RAIZ / "reports"
    paginas = {"perfil": perfil(dados, total_bruto), "conversao": conversao(dados)}
    relatorios.mkdir(exist_ok=True)
    for tipo, html in paginas.items():
        destino = relatorios / PAGINAS[tipo][1]
        destino.write_text(html, encoding="utf-8")
        print(destino.relative_to(RAIZ))


if __name__ == "__main__":
    main()
