# Prática – Grafos: Roteamento e Coloração em Redes

Implementação de dois problemas clássicos de grafos aplicados a infraestrutura de redes:

- **Parte 1** — Roteamento em rede de backbone: menor caminho em grafo direcionado com pesos (incluindo negativos)
- **Parte 2** — Alocação de canais Wi-Fi: coloração mínima de grafo não-direcionado

## Requisitos

Python 3.10 ou superior. Sem dependências externas.

## Como executar

### Parte 1 — Roteamento

```bash
python parte1/roteamento.py
```

Lê `entrada/grafo_rede_p.txt` e `entrada/grafo_rede_m.txt` e gera:

- `parte1/saida_parte1_p.txt`
- `parte1/saida_parte1_m.txt`

### Parte 2 — Coloração

```bash
python parte2/colocaracao.py
```

Lê `entrada/grafo_wifi_p.txt` e `entrada/grafo_wifi_m.txt` e gera:

- `parte2/saida_parte2_p.txt`
- `parte2/saida_parte2_m.txt`

## Estrutura do repositório

```
pratica-grafos/
├── README.md
├── comparativo.md
├── entrada/
│   ├── grafo_rede_p.txt     ← roteamento pequeno (5 vértices, sem pesos negativos)
│   ├── grafo_rede_m.txt     ← roteamento médio  (10 vértices, com pesos negativos)
│   ├── grafo_wifi_p.txt     ← Wi-Fi pequeno (5 vértices)
│   └── grafo_wifi_m.txt     ← Wi-Fi médio   (8 vértices)
├── parte1/
│   ├── roteamento.py        ← Dijkstra e Bellman-Ford
│   ├── saida_parte1_p.txt
│   └── saida_parte1_m.txt
└── parte2/
    ├── colocaracao.py       ← DSatur com backtracking exato
    ├── saida_parte2_p.txt
    └── saida_parte2_m.txt
```

## Equipe

- Willian Tcheldon
- Luiz Henrique
- Hércules Porfírio
- Pedro Satiro
- Davy Caetano
