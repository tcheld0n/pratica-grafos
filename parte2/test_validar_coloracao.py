from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from parte2.validar_coloracao import (
    SaidaColoracao,
    ler_grafo,
    ler_saida_coloracao,
    main,
    validar_arquivo,
    validar_coloracao,
)


RAIZ_PROJETO = Path(__file__).resolve().parents[1]


class LeituraGrafoTests(unittest.TestCase):
    def test_le_grafo_pequeno_com_quantidades_declaradas(self):
        grafo = ler_grafo(RAIZ_PROJETO / "entrada" / "grafo_wifi_p.txt")

        self.assertEqual(grafo.numero_vertices, 5)
        self.assertEqual(grafo.numero_arestas, 7)
        self.assertEqual(len(grafo.arestas), 7)

    def test_rejeita_quantidade_de_arestas_diferente_do_cabecalho(self):
        with TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "grafo.txt"
            caminho.write_text("3 2\n0 1\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "declara 2 arestas, mas possui 1"):
                ler_grafo(caminho)


class ValidacaoColoracaoTests(unittest.TestCase):
    def test_aceita_coloracao_valida_e_conta_cores(self):
        grafo = ler_grafo(RAIZ_PROJETO / "entrada" / "grafo_wifi_p.txt")
        conteudo = (
            "ALGORITMO: DSatur com Backtracking Exato\n"
            "JUSTIFICATIVA: Busca uma coloracao valida com o menor numero de cores.\n"
            "NUM_CORES: 3\n"
            "COLORACAO: 0=1 1=2 2=3 3=1 4=2\n"
        )

        with TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "saida.txt"
            caminho.write_text(conteudo, encoding="utf-8")
            saida = ler_saida_coloracao(caminho)

        relatorio = validar_coloracao(grafo, saida)

        self.assertTrue(relatorio.valida)
        self.assertEqual(relatorio.numero_cores_utilizadas, 3)
        self.assertEqual(relatorio.problemas, ())

    def test_aceita_resultado_revisado_para_o_grafo_medio(self):
        grafo = ler_grafo(RAIZ_PROJETO / "entrada" / "grafo_wifi_m.txt")
        saida = SaidaColoracao(
            algoritmo="DSatur com Backtracking Exato",
            justificativa="Resultado revisado antes da integracao da saida.",
            numero_cores=3,
            coloracao={0: 1, 1: 2, 2: 3, 3: 1, 4: 2, 5: 1, 6: 2, 7: 1},
        )

        relatorio = validar_coloracao(grafo, saida)

        self.assertTrue(relatorio.valida)
        self.assertEqual(relatorio.numero_vertices, 8)
        self.assertEqual(relatorio.numero_arestas, 11)
        self.assertEqual(relatorio.numero_cores_utilizadas, 3)

    def test_rejeita_vertices_adjacentes_com_a_mesma_cor(self):
        grafo = ler_grafo(RAIZ_PROJETO / "entrada" / "grafo_wifi_p.txt")
        saida = SaidaColoracao(
            algoritmo="DSatur",
            justificativa="Teste de conflito.",
            numero_cores=3,
            coloracao={0: 1, 1: 1, 2: 2, 3: 3, 4: 2},
        )

        relatorio = validar_coloracao(grafo, saida)

        self.assertFalse(relatorio.valida)
        self.assertIn("Vertices adjacentes 0 e 1 usam a cor 1.", relatorio.problemas)

    def test_rejeita_coloracao_com_vertice_ausente(self):
        grafo = ler_grafo(RAIZ_PROJETO / "entrada" / "grafo_wifi_p.txt")
        saida = SaidaColoracao(
            algoritmo="DSatur",
            justificativa="Teste de cobertura.",
            numero_cores=3,
            coloracao={0: 1, 1: 2, 2: 3, 3: 1},
        )

        relatorio = validar_coloracao(grafo, saida)

        self.assertFalse(relatorio.valida)
        self.assertIn("Vertices sem cor: 4.", relatorio.problemas)

    def test_rejeita_coloracao_com_vertice_extra(self):
        grafo = ler_grafo(RAIZ_PROJETO / "entrada" / "grafo_wifi_p.txt")
        saida = SaidaColoracao(
            algoritmo="DSatur",
            justificativa="Teste de cobertura.",
            numero_cores=3,
            coloracao={0: 1, 1: 2, 2: 3, 3: 1, 4: 2, 5: 3},
        )

        relatorio = validar_coloracao(grafo, saida)

        self.assertFalse(relatorio.valida)
        self.assertIn("Vertices inexistentes na coloracao: 5.", relatorio.problemas)

    def test_rejeita_cor_menor_que_um(self):
        grafo = ler_grafo(RAIZ_PROJETO / "entrada" / "grafo_wifi_p.txt")
        saida = SaidaColoracao(
            algoritmo="DSatur",
            justificativa="Teste de cor invalida.",
            numero_cores=3,
            coloracao={0: 0, 1: 1, 2: 2, 3: 3, 4: 1},
        )

        relatorio = validar_coloracao(grafo, saida)

        self.assertFalse(relatorio.valida)
        self.assertIn("Vertice 0 usa a cor invalida 0; cores devem iniciar em 1.", relatorio.problemas)

    def test_rejeita_num_cores_diferente_das_cores_utilizadas(self):
        grafo = ler_grafo(RAIZ_PROJETO / "entrada" / "grafo_wifi_p.txt")
        saida = SaidaColoracao(
            algoritmo="DSatur",
            justificativa="Teste de contagem.",
            numero_cores=4,
            coloracao={0: 1, 1: 2, 2: 3, 3: 1, 4: 2},
        )

        relatorio = validar_coloracao(grafo, saida)

        self.assertFalse(relatorio.valida)
        self.assertIn(
            "NUM_CORES informa 4, mas foram utilizadas 3 cores distintas.",
            relatorio.problemas,
        )


class FormatoSaidaTests(unittest.TestCase):
    def test_aceita_justificativa_com_ate_tres_linhas(self):
        conteudo = (
            "ALGORITMO: DSatur\n"
            "JUSTIFICATIVA: DSatur prioriza vertices saturados.\n"
            "O backtracking garante o menor numero de cores.\n"
            "NUM_CORES: 2\n"
            "COLORACAO: 0=1 1=2\n"
        )

        with TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "saida.txt"
            caminho.write_text(conteudo, encoding="utf-8")

            saida = ler_saida_coloracao(caminho)

        self.assertEqual(saida.numero_cores, 2)
        self.assertIn("backtracking", saida.justificativa)

    def test_rejeita_rotulo_diferente_do_formato_esperado(self):
        conteudo = (
            "ALGORITMO: DSatur\n"
            "JUSTIFICATIVA: Teste.\n"
            "CORES: 3\n"
            "COLORACAO: 0=1 1=2\n"
        )

        with TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "saida.txt"
            caminho.write_text(conteudo, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "esperado o rotulo NUM_CORES"):
                ler_saida_coloracao(caminho)

    def test_rejeita_vertice_repetido_na_coloracao(self):
        conteudo = (
            "ALGORITMO: DSatur\n"
            "JUSTIFICATIVA: Teste.\n"
            "NUM_CORES: 2\n"
            "COLORACAO: 0=1 0=2\n"
        )

        with TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "saida.txt"
            caminho.write_text(conteudo, encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Vertice 0 aparece mais de uma vez"):
                ler_saida_coloracao(caminho)


class RelatorioArquivoTests(unittest.TestCase):
    def test_valida_as_duas_saidas_finais(self):
        for tamanho in ("p", "m"):
            with self.subTest(tamanho=tamanho):
                grafo = RAIZ_PROJETO / "entrada" / f"grafo_wifi_{tamanho}.txt"
                saida = RAIZ_PROJETO / "parte2" / f"saida_parte2_{tamanho}.txt"

                sucesso, relatorio = validar_arquivo(grafo, saida)

                self.assertTrue(sucesso, relatorio)
                self.assertIn("STATUS: VALIDA", relatorio)
                self.assertIn("CORES_UTILIZADAS: 3", relatorio)

    def test_informa_saida_pendente_sem_criar_arquivo(self):
        grafo = RAIZ_PROJETO / "entrada" / "grafo_wifi_p.txt"

        with TemporaryDirectory() as diretorio:
            saida = Path(diretorio) / "saida_inexistente.txt"

            sucesso, relatorio = validar_arquivo(grafo, saida)

            self.assertFalse(sucesso)
            self.assertFalse(saida.exists())

        self.assertIn("STATUS: PENDENTE", relatorio)
        self.assertIn("VERTICES: 5", relatorio)
        self.assertIn("ARESTAS: 7", relatorio)
        self.assertIn("CORES_UTILIZADAS: N/A", relatorio)

    def test_cli_retorna_erro_quando_saida_esta_pendente(self):
        grafo = RAIZ_PROJETO / "entrada" / "grafo_wifi_p.txt"

        with TemporaryDirectory() as diretorio:
            saida = Path(diretorio) / "saida_inexistente.txt"
            texto = StringIO()
            with redirect_stdout(texto):
                codigo = main(["--grafo", str(grafo), "--saida", str(saida)])

        self.assertEqual(codigo, 1)
        self.assertIn("STATUS: PENDENTE", texto.getvalue())


if __name__ == "__main__":
    unittest.main()
