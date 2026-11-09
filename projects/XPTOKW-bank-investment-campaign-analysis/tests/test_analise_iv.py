import math
import unittest

import pandas as pd

from src.analise_IV import AnaliseIV


class AnaliseIVTests(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame(
            {
                "faixa": ["A", "A", "A", "A", "B", "B", "B", "B"],
                "constante": ["única"] * 8,
                "comprou": ["Não", "Não", "Não", "Sim", "Não", "Sim", "Sim", "Sim"],
            }
        )

    def test_tabela_exibe_frequencias_reais_e_woe_consistente(self):
        analise = AnaliseIV(self.df, ["faixa"], "comprou")

        tabela = analise.get_freq_table("faixa")

        self.assertEqual(
            list(tabela.columns),
            ["Não", "Sim", "Total", "Freq_Relativa", "% Não", "% Sim", "Taxa Evento", "WoE", "IV Parcial"],
        )
        self.assertEqual(tabela.loc["A", ["Não", "Sim", "Total"]].tolist(), [3, 1, 4])
        self.assertEqual(tabela.loc["A", "Freq_Relativa"], 50)
        self.assertEqual(tabela.loc["A", "% Não"], 75)
        self.assertEqual(tabela.loc["A", "% Sim"], 25)
        self.assertEqual(tabela.loc["A", "Taxa Evento"], 25)
        self.assertAlmostEqual(tabela.loc["A", "WoE"], math.log(3))
        self.assertAlmostEqual(tabela.loc["A", "IV Parcial"], math.log(3) / 2)

    def test_ranking_ordena_iv_e_classifica(self):
        analise = AnaliseIV(self.df, ["constante", "faixa"], "comprou")

        ranking = analise.get_iv_list()

        self.assertEqual(list(ranking.index), ["faixa", "constante"])
        self.assertEqual(list(ranking.columns), ["IV", "Classificação"])
        self.assertAlmostEqual(ranking.loc["faixa", "IV"], math.log(3))
        self.assertEqual(ranking.loc["faixa", "Classificação"], "Suspeito / muito alto")
        self.assertEqual(ranking.loc["constante", "IV"], 0)
        self.assertEqual(ranking.loc["constante", "Classificação"], "Muito fraco")

    def test_contagem_zero_recebe_suavizacao_sem_alterar_frequencias(self):
        df = pd.DataFrame(
            {"faixa": ["A", "A", "B", "B"], "comprou": ["Não", "Não", "Sim", "Sim"]}
        )

        tabela = AnaliseIV(df, ["faixa"], "comprou").get_freq_table("faixa")

        self.assertEqual(tabela.loc["A", ["Não", "Sim", "Taxa Evento"]].tolist(), [2, 0, 0])
        self.assertAlmostEqual(tabela.loc["A", "WoE"], math.log(5))
        self.assertAlmostEqual(tabela["IV Parcial"].sum(), 4 * math.log(5) / 3)
        self.assertTrue(tabela[["WoE", "IV Parcial"]].map(math.isfinite).all().all())

    def test_evento_pode_ser_informado_para_alvo_zero_um(self):
        df = self.df.assign(comprou=self.df["comprou"].eq("Sim").astype(int))

        tabela = AnaliseIV(df, ["faixa"], "comprou", event_value=1).get_freq_table("faixa")

        self.assertEqual(tabela.loc["A", ["Não", "Sim"]].tolist(), [3, 1])

    def test_entradas_invalidas_geram_erros_claros(self):
        with self.assertRaises(ValueError):
            AnaliseIV(self.df.assign(comprou="Sim"), ["faixa"], "comprou")
        with self.assertRaises(ValueError):
            AnaliseIV(self.df.assign(faixa=None), ["faixa"], "comprou")
        with self.assertRaises(KeyError):
            AnaliseIV(self.df, ["inexistente"], "comprou")

        analise = AnaliseIV(self.df, ["faixa"], "comprou")
        with self.assertRaises(KeyError):
            analise.get_freq_table("constante")


if __name__ == "__main__":
    unittest.main()
