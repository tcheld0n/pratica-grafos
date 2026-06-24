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

## Parte 2 — Alocação de Canais Wi-Fi

### Algoritmos considerados

| Estratégia | Garante o mínimo? | Observação |
|---|:---:|---|
| Guloso simples | Não | Rápido, mas pode usar mais cores que o necessário |
| DSatur guloso | Não | Prioriza vértices com maior saturação; produz resultados melhores |
| Backtracking puro | Sim | Custo exponencial no pior caso |
| DSatur + backtracking | Sim | DSatur orienta a busca exata, reduzindo tentativas |

### Decisão

A implementação utiliza **DSatur com backtracking exato**. O DSatur escolhe o próximo
vértice pelo maior grau de saturação (número de cores distintas já usadas pelos vizinhos),
com desempate pelo maior grau original. O backtracking testa limites crescentes de cores
até encontrar a primeira coloração válida, garantindo o número cromático χ(G).

### Resultados

| Grafo | Vértices | Arestas | Cores encontradas | Válida |
|---|:---:|:---:|:---:|:---:|
| Pequeno | 5 | 7 | 3 | Sim |
| Médio | 8 | 11 | 3 | Sim |

Nos dois grafos os vértices 0, 1 e 2 formam um triângulo, impondo χ(G) ≥ 3. Como a
implementação encontrou colorações com exatamente 3 cores, os resultados são ótimos.
