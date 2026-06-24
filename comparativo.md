# Comparativo de Algoritmos

## Parte 1 — Roteamento em Rede de Backbone

### Algoritmos considerados

| Algoritmo | Pesos negativos | Detecta ciclo negativo | Complexidade | Observação |
|---|:---:|:---:|---|---|
| Dijkstra | Não | Não | O((V + E) log V) | Ótimo para grafos esparsos sem pesos negativos |
| Bellman-Ford | Sim | Sim | O(V × E) | Indicado quando há pesos negativos e fonte única |
| Floyd-Warshall | Sim | Sim | O(V³) | Calcula todos os pares; excessivo para fonte única |

### Decisão

**Grafo pequeno** (`grafo_rede_p.txt`): todos os pesos são positivos. Dijkstra é aplicável e
mais eficiente que Bellman-Ford para esse caso. Rota mínima: `0 → 1 → 3 → 4`, custo `7`.

**Grafo médio** (`grafo_rede_m.txt`): há arestas com peso negativo decorrentes de acordos de
SLA. Dijkstra não garante corretude nesse cenário. Floyd-Warshall seria excessivo para
fonte única. Bellman-Ford foi escolhido por suportar pesos negativos, detectar ciclos
negativos e ter custo proporcional a O(V × E) — adequado para o tamanho do grafo.
Rota mínima: `0 → 1 → 2 → 4 → 3 → 6 → 9`, custo `6`.

---

## Parte 2 — Coloração de Grafos

## Estrategia

A implementacao proposta para a Parte 2 utiliza **DSatur com backtracking
exato**. O DSatur escolhe primeiro o vertice com maior grau de saturacao, em caso de empate, a implementacao prioriza o vertice de maior
grau.
O backtracking testa quantidades crescentes de cores. Assim, a primeira
coloracao completa encontrada determina o numero cromatico do grafo.

| Estrategia | Caracteristica | Garante o minimo? | Observacao |
|---|---|---:|---|
| Guloso simples | Colore os vertices em uma ordem fixa | Nao | Rapido, mas pode usar mais cores que o necessario |
| DSatur guloso | Prioriza vertices com maior saturacao | Nao | Costuma produzir coloracoes melhores que o guloso simples |
| Backtracking | Explora combinacoes de cores | Sim | Possui custo exponencial no pior caso |
| DSatur + backtracking | Usa DSatur para orientar a busca exata | Sim | Estrategia adotada na implementacao analisada |

## Resultados

| Grafo | Vertices | Arestas | Cores encontradas | Conflitos | Arquivo final |
|---|---:|---:|---:|---:|---|
| Pequeno | 5 | 7 | 3 | 0 | Validado |
| Medio | 8 | 11 | 3 | 0 | Validado |

Nos dois grafos, os vertices 0, 1 e 2 formam um triangulo. Portanto, qualquer
coloracao valida precisa de pelo menos tres cores. Como a implementacao
analisada encontrou coloracoes validas com tres cores, esses resultados sao
otimos para as entradas atuais.

O grafo medio possui mais vertices e arestas, mas nao exige mais cores que o
grafo pequeno. Para essas instancias pequenas, o custo do backtracking e
baixo. Em grafos maiores, o tempo pode crescer exponencialmente, embora a
ordem DSatur normalmente reduza a quantidade de tentativas.
