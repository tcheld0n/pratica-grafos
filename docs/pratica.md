# Prática 1 – Grafos: Roteamento e Coloração em Redes

Nesta atividade exploraremos dois problemas clássicos de grafos aplicados a infraestrutura de redes de computadores. A atividade pode ser feita em equipes de até 3 pessoas.

## Contexto geral

Uma empresa de telecomunicações gerencia duas redes distintas: (1) uma rede de backbone que interliga roteadores de diferentes cidades e (2) uma rede Wi-Fi interna de um campus universitário. Vocês irão resolver um problema em cada uma dessas redes.

---

## Parte 1 – Roteamento em Rede de Backbone

A rede de backbone é modelada como um **grafo direcionado com pesos**, onde cada vértice representa um roteador e cada aresta representa um enlace com custo associado (em unidades de latência acumulada). Alguns enlaces possuem acordos de nível de serviço (SLA) que resultam em **custo negativo** — o tráfego por esse enlace "ganha" prioridade e reduz o custo total da rota.

### Tarefa

Dado o grafo, determine o **caminho de menor custo** do roteador de origem (`S`) até o roteador de destino (`T`), indicando:

- Qual algoritmo foi escolhido (**Dijkstra**, **Bellman-Ford** ou **Floyd-Warshall**) e **por quê** (justifique em função das características do grafo);
- A sequência de vértices do caminho mínimo;
- O custo total do caminho.

> **OBS:** Para o grafo médio (`grafo_rede_m.txt`), verifique se o algoritmo escolhido suporta arestas com peso negativo. Justifique sua escolha.

### Formato de entrada

```
<num_vertices>\t<num_arestas>
<S>\t<T>
<vertice_u>\t<vertice_v>\t<custo>    ← repetir para cada aresta
```

Arquivos de exemplo: **`grafo_rede_p.txt`** (pequeno, sem pesos negativos) e **`grafo_rede_m.txt`** (médio, com pesos negativos). O separador é TAB (`\t`).

### Formato de saída — `saida_parte1_p.txt` e `saida_parte1_m.txt`

```
ALGORITMO: <nome do algoritmo>
JUSTIFICATIVA: <texto livre, até 3 linhas>
ROTA: <v0> <v1> <v2> ... <vn>
CUSTO: <valor inteiro ou decimal>
```

Exemplo (fictício):
```
ALGORITMO: Dijkstra
JUSTIFICATIVA: Todos os pesos sao positivos, portanto Dijkstra e aplicavel e mais eficiente.
ROTA: 0 2 3 4
CUSTO: 11
```

---

## Parte 2 – Alocação de Canais Wi-Fi

A rede Wi-Fi do campus é modelada como um **grafo não-direcionado sem pesos**, onde cada vértice representa um ponto de acesso (AP) e cada aresta indica que dois APs se interferem mutuamente (estão próximos o suficiente para usar o mesmo canal causar colisão de sinais). APs adjacentes **não podem** operar no mesmo canal.

### Tarefa

Determine uma atribuição de canais aos APs que:

- Seja **válida** (nenhum par de APs adjacentes usa o mesmo canal);
- Use o **menor número possível de canais** (número cromático χ(G)).

Indique qual algoritmo de coloração foi utilizado (Guloso, DSatur, Backtracking, etc.) e justifique.

> **Dica:** Algoritmos gulosos simples raramente garantem a solução ótima. Pesquise DSatur ou coloração com backtracking para obter χ(G) exato.

### Formato de entrada

```
<num_vertices>\t<num_arestas>
<vertice_u>\t<vertice_v>    ← repetir para cada aresta (sem peso)
```

Arquivos de exemplo: **`grafo_wifi_p.txt`** (pequeno) e **`grafo_wifi_m.txt`** (médio).

### Formato de saída — `saida_parte2_p.txt` e `saida_parte2_m.txt`

```
ALGORITMO: <nome do algoritmo>
JUSTIFICATIVA: <texto livre, até 3 linhas>
NUM_CORES: <k>
COLORACAO: <v0>=<cor> <v1>=<cor> ... <vn>=<cor>
```

- Cores são inteiros iniciando em **1**.
- `NUM_CORES` deve ser igual ao número de cores distintas efetivamente usadas na `COLORACAO`.

Exemplo (fictício):
```
ALGORITMO: DSatur
JUSTIFICATIVA: DSatur ordena vertices pelo grau de saturacao, tendendo a coloracao proxima ao otimo.
NUM_CORES: 3
COLORACAO: 0=1 1=2 2=3 3=1 4=2
```

---

## Estrutura do repositório esperada

```
repositorio/
├── README.md
├── parte1/
│   ├── <código-fonte>
│   └── saida_parte1_p.txt
│   └── saida_parte1_m.txt
├── parte2/
│   ├── <código-fonte>
│   └── saida_parte2_p.txt
│   └── saida_parte2_m.txt
└── comparativo.pdf   (ou comparativo.md, ou seção no README)
```

O README deve conter instruções claras de **compilação e execução** para cada parte.

---

## Entrega

Apenas o link do repositório **público** no GitHub ou GitLab.

**Aviso:** Os commits ficam registrados com autoria e data. Em equipes de 2 ou 3 pessoas, todos os membros devem ter commits no repositório — não apenas um. Isso será observado.

---

## Rubrica

| Critério | Pontos |
|---|---|
| Parte 1 – `grafo_rede_p.txt` correto (rota válida + custo mínimo) | 1,5 |
| Parte 1 – `grafo_rede_m.txt` correto (rota válida + custo mínimo) | 2,0 |
| Parte 2 – `grafo_wifi_p.txt` correto (coloração válida + mínima) | 1,5 |
| Parte 2 – `grafo_wifi_m.txt` correto (coloração válida + mínima) | 2,0 |
| Justificativa dos algoritmos (ambas as partes) | 1,0 |
| README com instruções funcionais | 1,0 |
| Commits de todos os membros | 1,0 |
| **Total** | **10,0** |

> Coloração com mais cores que o ótimo, mas válida, recebe **metade** dos pontos do critério de correção.
> Rota válida mas com custo não-mínimo recebe **metade** dos pontos do critério de correção.
