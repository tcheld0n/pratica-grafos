# Validação da Parte 1 — Roteamento

## Grafo pequeno

O arquivo `grafo_rede_p.txt` não possui pesos negativos. Por isso, o algoritmo de Dijkstra pode ser usado.

Rota mínima encontrada:

```text
0 -> 1 -> 3 -> 4
```

Conferência do custo:

```text
0 -> 1 = 2
1 -> 3 = 3
3 -> 4 = 2
Total = 2 + 3 + 2 = 7
```

A rota alternativa `0 -> 1 -> 2 -> 4` custa `2 + 1 + 5 = 8`, portanto não é a mínima.

## Grafo médio

O arquivo `grafo_rede_m.txt` possui arestas negativas, como `1 -> 2` com peso `-3`, `4 -> 3` com peso `-2` e `7 -> 6` com peso `-1`. Por isso, Dijkstra não é adequado. Foi usado Bellman-Ford, que suporta pesos negativos e também detecta ciclos negativos.

Rota mínima encontrada:

```text
0 -> 1 -> 2 -> 4 -> 3 -> 6 -> 9
```

Conferência do custo:

```text
0 -> 1 = 4
1 -> 2 = -3
2 -> 4 = 2
4 -> 3 = -2
3 -> 6 = 3
6 -> 9 = 2
Total = 4 - 3 + 2 - 2 + 3 + 2 = 6
```

Os testes automáticos verificam a leitura dos arquivos, as rotas, os custos, a presença de pesos negativos e a detecção de ciclo negativo.
