"""Preparação e métricas dos dashboards a partir da planilha da campanha."""

from math import sqrt
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import beta, norm, t

from src.analise_IV import AnaliseIV

ALVO = "Cliente_Comprou_o_Titulo?"
SALDO = "Saldo_Conta_Corrente"
LIGACOES = "Qte_de_Ligações_Feitas"
PERFIL = {
    "Profissão": "Profissão",
    "Formação": "Formação",
    "Estado_Civil": "Estado civil",
    "Cliente_Devedor?": "Inadimplência",
    "Tem_Hipoteca?": "Hipoteca",
    "Tem_Emprestimo?": "Empréstimo pessoal",
}
SEGMENTOS = {
    "Faixa_Idade": "Faixa etária",
    **PERFIL,
    "Faixa_Saldo": "Saldo em conta corrente",
    "Faixa_Qtd_Ligações": "Quantidade de ligações",
}
ORDEM_FORMACAO = ["Fundamental", "Ensino Médio", "Ensino Superior", "Desconhecido"]


def carregar_campanha(arquivo: Path) -> tuple[pd.DataFrame, int]:
    """Lê a planilha, valida as colunas usadas e remove duplicatas exatas."""
    dados = pd.read_excel(arquivo, sheet_name="bank_marketing", header=1, usecols="B:K")
    colunas = {*PERFIL, ALVO, "Idade", SALDO, LIGACOES}
    if set(dados.columns) != colunas:
        raise ValueError("As colunas da planilha não correspondem ao esquema da campanha.")
    if dados.empty or dados.isna().any().any():
        raise ValueError("A planilha deve conter observações sem valores ausentes.")
    for coluna in (ALVO, "Cliente_Devedor?", "Tem_Hipoteca?", "Tem_Emprestimo?"):
        if not dados[coluna].isin(["Sim", "Não"]).all():
            raise ValueError(f"A coluna {coluna!r} deve conter apenas 'Sim' ou 'Não'.")
    if dados[ALVO].nunique() != 2:
        raise ValueError("A conversão requer observações das duas classes de compra.")
    if not dados["Formação"].isin(ORDEM_FORMACAO).all():
        raise ValueError("A planilha contém uma categoria de formação fora do esquema.")
    for coluna in ("Idade", SALDO, LIGACOES):
        if not pd.api.types.is_numeric_dtype(dados[coluna]) or not np.isfinite(dados[coluna]).all():
            raise ValueError(f"A coluna {coluna!r} deve conter números finitos.")
    if dados["Idade"].lt(18).any() or dados[LIGACOES].lt(1).any():
        raise ValueError("Idade abaixo de 18 anos ou quantidade de ligações abaixo de 1.")

    return dados.drop_duplicates(ignore_index=True), len(dados)


def tabelas_conversao(dados: pd.DataFrame) -> tuple[dict[str, pd.DataFrame], pd.DataFrame, pd.DataFrame]:
    """Reproduz as faixas do notebook e calcula as tabelas e o ranking de IV."""
    idade = pd.cut(dados["Idade"], [0, 25, 35, 45, 55, 65, np.inf],
                   labels=["18–25", "26–35", "36–45", "46–55", "56–65", "66+"])
    saldo = pd.cut(dados[SALDO], [-np.inf, 499, 1499, 4999, np.inf],
                   labels=["Até R$ 499", "R$ 500 a 1.499", "R$ 1.500 a 4.999", "R$ 5 mil ou mais"])
    ligacoes = pd.cut(dados[LIGACOES], [0, 1, 2, 3, 4, np.inf], labels=["1", "2", "3", "4", "5+"])
    segmentados = dados.assign(Faixa_Idade=idade, Faixa_Saldo=saldo, Faixa_Qtd_Ligações=ligacoes)
    analise = AnaliseIV(segmentados, list(SEGMENTOS), ALVO, event_value="Sim")
    tabelas = {coluna: analise.get_freq_table(coluna).drop(index="Total") for coluna in SEGMENTOS}
    ranking = analise.get_iv_list()

    saldo_detalhado = pd.cut(dados[SALDO], [-np.inf, 499, 1499, 4999, 9999, np.inf],
                            labels=[*saldo.cat.categories[:3], "R$ 5 mil a 9.999", "R$ 10 mil ou mais"])
    detalhado = AnaliseIV(segmentados.assign(Saldo_Detalhado=saldo_detalhado), ["Saldo_Detalhado"], ALVO)
    tabelas["Saldo_Detalhado"] = detalhado.get_freq_table("Saldo_Detalhado").drop(index="Total")

    cruzamento = (
        segmentados.assign(Compra=segmentados[ALVO].eq("Sim").astype(int))
        .groupby(["Faixa_Idade", "Profissão"], observed=True)["Compra"]
        .agg(compras="sum", total="size")
    )
    return tabelas, ranking, cruzamento


def probabilidades_ligacoes(dados: pd.DataFrame) -> pd.DataFrame:
    """Calcula P(compra | ligações ≤ k) e P(compra | ligações ≥ k)."""
    linhas = []
    for limiar in range(2, 6):
        for condicao, mascara in [
            ("Até k ligações", dados[LIGACOES].le(limiar)),
            ("k ou mais ligações", dados[LIGACOES].ge(limiar)),
        ]:
            total = int(mascara.sum())
            compras = int(dados.loc[mascara, ALVO].eq("Sim").sum())
            linhas.append((condicao, limiar, total, compras, 100 * compras / total if total else np.nan))
    return pd.DataFrame(linhas, columns=["condicao", "limiar", "total", "compras", "taxa"])


def intervalos_conversao(compras: int, total: int) -> dict[str, tuple[float, float]]:
    """Devolve os limites dos três intervalos de 95% comparados no notebook."""
    p = compras / total
    z = norm.ppf(0.975)
    denominador = 1 + z**2 / total
    centro = (p + z**2 / (2 * total)) / denominador
    margem = z * sqrt(p * (1 - p) / total + z**2 / (4 * total**2)) / denominador
    margem_t = t.ppf(0.975, df=total - 1) * sqrt(p * (1 - p) / (total - 1))
    return {
        "Wilson": (centro - margem, centro + margem),
        "Clopper–Pearson": (beta.ppf(0.025, compras, total - compras + 1),
                            beta.ppf(0.975, compras + 1, total - compras)),
        "t de Student": (p - margem_t, p + margem_t),
    }
