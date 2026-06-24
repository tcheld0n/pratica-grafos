import unittest

from roteamento import (
    bellman_ford,
    dijkstra,
    ler_grafo,
    tem_peso_negativo,
    validar_rota,
)


class TestesParte1(unittest.TestCase):
    def test_leitura_grafo_pequeno(self):
        num_vertices, num_arestas, origem, destino, _, _ = ler_grafo(
            "grafo_rede_p.txt"
        )

        self.assertEqual(num_vertices, 5)
        self.assertEqual(num_arestas, 6)
        self.assertEqual(origem, 0)
        self.assertEqual(destino, 4)

    def test_dijkstra_grafo_pequeno(self):
        num_vertices, _, origem, destino, grafo, _ = ler_grafo(
            "grafo_rede_p.txt"
        )

        rota, custo = dijkstra(num_vertices, origem, destino, grafo)

        self.assertEqual(rota, [0, 1, 3, 4])
        self.assertEqual(custo, 7)
        self.assertTrue(validar_rota(rota, custo, origem, destino, grafo))

    def test_bellman_ford_grafo_medio(self):
        num_vertices, _, origem, destino, grafo, arestas = ler_grafo(
            "grafo_rede_m.txt"
        )

        rota, custo, tem_ciclo_negativo = bellman_ford(
            num_vertices, origem, destino, arestas
        )

        self.assertFalse(tem_ciclo_negativo)
        self.assertEqual(rota, [0, 1, 2, 4, 3, 6, 9])
        self.assertEqual(custo, 6)
        self.assertTrue(validar_rota(rota, custo, origem, destino, grafo))

    def test_pesos_negativos(self):
        _, _, _, _, _, arestas_p = ler_grafo("grafo_rede_p.txt")
        _, _, _, _, _, arestas_m = ler_grafo("grafo_rede_m.txt")

        self.assertFalse(tem_peso_negativo(arestas_p))
        self.assertTrue(tem_peso_negativo(arestas_m))

    def test_deteccao_de_ciclo_negativo(self):
        arestas = [
            (0, 1, 1),
            (1, 2, -2),
            (2, 1, -2),
        ]

        _, _, tem_ciclo_negativo = bellman_ford(3, 0, 2, arestas)
        self.assertTrue(tem_ciclo_negativo)


if __name__ == "__main__":
    unittest.main()
