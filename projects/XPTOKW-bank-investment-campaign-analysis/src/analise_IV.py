"""Análise de Information Value para variáveis categóricas ou discretizadas."""

import numpy as np
import pandas as pd


class AnaliseIV:
    """Calcula tabelas de frequência, WoE e IV para um alvo binário.

    Os percentuais da tabela são exibidos de 0 a 100. O WoE segue a
    convenção ln(proporção de não eventos / proporção de eventos).
    """

    def __init__(
        self,
        df: pd.DataFrame,
        use_cols: list[str],
        target: str,
        event_value: str | int | bool = "Sim",
    ) -> None:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df deve ser um pandas.DataFrame.")
        if isinstance(use_cols, str) or not use_cols:
            raise ValueError("use_cols deve conter ao menos uma coluna.")
        if len(use_cols) != len(set(use_cols)):
            raise ValueError("use_cols não pode conter colunas repetidas.")
        if target in use_cols:
            raise ValueError("A variável target não pode estar em use_cols.")

        missing_cols = [col for col in [*use_cols, target] if col not in df.columns]
        if missing_cols:
            raise KeyError(f"Colunas não encontradas no DataFrame: {missing_cols}")
        if df.empty:
            raise ValueError("O DataFrame não pode estar vazio.")
        if df[target].isna().any():
            raise ValueError("A variável target não pode conter valores ausentes.")
        if df[target].nunique() != 2:
            raise ValueError("A variável target deve conter exatamente duas classes.")
        if not df[target].eq(event_value).any():
            raise ValueError(f"O valor do evento {event_value!r} não aparece em target.")

        cols_with_nulls = [col for col in use_cols if df[col].isna().any()]
        if cols_with_nulls:
            raise ValueError(
                f"Trate os valores ausentes antes da análise: {cols_with_nulls}"
            )

        self.use_cols = list(use_cols)
        self.target = target
        self.event_value = event_value
        self._data = df[[*self.use_cols, target]].copy()

    @staticmethod
    def classificar_iv(iv: float) -> str:
        """Classifica o IV por faixas usuais em scorecards de crédito."""
        if not np.isfinite(iv) or iv < 0:
            raise ValueError("iv deve ser um número finito e não negativo.")
        if iv < 0.02:
            return "Muito fraco"
        if iv < 0.1:
            return "Fraco"
        if iv < 0.3:
            return "Médio"
        if iv <= 0.5:
            return "Forte"
        return "Suspeito / Muito Alto - Verifique"

    def get_freq_table(self, col: str) -> pd.DataFrame:
        """Retorna frequências observadas, percentuais, WoE e IV por categoria.

        Se alguma categoria não tiver evento ou não evento, adiciona 0,5
        a todas as células somente para calcular WoE e IV. As contagens,
        percentuais e taxas exibidos permanecem observados.
        """
        if col not in self.use_cols:
            raise KeyError(f"{col!r} não está em use_cols.")

        target_labels = pd.Series(
            np.where(self._data[self.target].eq(self.event_value), "Sim", "Não"),
            index=self._data.index,
        )
        counts = pd.crosstab(self._data[col], target_labels)
        counts = counts.reindex(columns=["Não", "Sim"], fill_value=0)
        counts = counts.loc[counts.sum(axis=1) > 0].astype(int)

        total = counts.sum(axis=1)
        table = counts.copy()
        table["Total"] = total
        table["Freq Rel (%)"] = total / total.sum() * 100
        table["% Não"] = counts["Não"] / counts["Não"].sum() * 100
        table["% Sim"] = counts["Sim"] / counts["Sim"].sum() * 100
        table["Taxa Evento (%)"] = counts["Sim"] / total * 100

        correction = 0.5 if counts.eq(0).any().any() else 0.0
        adjusted = counts.astype(float) + correction
        non_event_share = adjusted["Não"] / adjusted["Não"].sum()
        event_share = adjusted["Sim"] / adjusted["Sim"].sum()
        table["WoE"] = np.log(non_event_share / event_share)
        table["IV Parcial"] = (non_event_share - event_share) * table["WoE"]

        if "Total" in table.index:
            raise ValueError(
                f"A categoria 'Total' existe em {col!r} e conflita com a linha de totais."
            )

        iv_total = table["IV Parcial"].sum()
        table.loc["Total", ["Não", "Sim", "Total"]] = [
            counts["Não"].sum(),
            counts["Sim"].sum(),
            total.sum(),
        ]
        table.loc["Total", ["Freq Rel (%)", "% Não", "% Sim"]] = 100.0
        table.loc["Total", "Taxa Evento (%)"] = (
            counts["Sim"].sum() / total.sum() * 100
        )
        table.loc["Total", "WoE"] = np.nan
        table.loc["Total", "IV Parcial"] = iv_total

        count_cols = ["Não", "Sim", "Total"]
        table[count_cols] = table[count_cols].astype("Int64")
        table['% Não'] = table['% Não'].round(2)
        table['% Sim'] = table['% Sim'].round(2)
        table["Taxa Evento (%)"] = table["Taxa Evento (%)"].round(2)
        table["Freq Rel (%)"] = table["Freq Rel (%)"].round(2)
        decimal_cols = ["% Não", "% Sim", "Taxa Evento (%)", "WoE", "IV Parcial"]
        table[decimal_cols] = table[decimal_cols].round(4)
        return table

    def get_iv_list(self) -> pd.DataFrame:
        """Retorna as variáveis de use_cols ordenadas por IV decrescente."""
        values = {
            col: self.get_freq_table(col).loc["Total", "IV Parcial"]
            for col in self.use_cols
        }
        ranking = pd.DataFrame.from_dict(values, orient="index", columns=["IV"])
        ranking["Classificação"] = ranking["IV"].map(self.classificar_iv)
        ranking.index.name = "Variável"
        return ranking.sort_values("IV", ascending=False)
