# Plano de Implementação — Prática de Grafos

**Equipe:** 4 membros | **Prazo:** ver enunciado | **Nota máxima:** 10.0

---

## Dependências globais

```
T-01 (infraestrutura) → desbloqueia T-02 e T-03
T-02 (parser P1)      → desbloqueia T-04
T-03 (parser P2)      → desbloqueia T-07
T-04 (Bellman-Ford)   → desbloqueia T-05 e T-10
T-05 (caminho)        → desbloqueia T-06
T-06 (saída P1)       → desbloqueia T-11
T-07 (DSatur)         → desbloqueia T-08 e T-10
T-08 (verificação)    → desbloqueia T-09
T-09 (saída P2)       → desbloqueia T-11
T-10 (justificativas) → parte de T-11
T-11 (comparativo)    → desbloqueia T-12
T-12 (README final)   → entrega
```

---

## Membro 1 — Infraestrutura & Parsers

**Responsabilidade:** estrutura do repositório, leitura dos arquivos de entrada, integração final.

### T-01 · Estrutura do repositório
- **Depende de:** —
- **Entrega:** pastas `parte1/` e `parte2/` criadas, `README.md` com placeholder de instruções
- **Critério de conclusão:** `git push` com estrutura inicial, todos os membros conseguem clonar e enxergar os arquivos de entrada

### T-02 · Parser para grafo dirigido ponderado (Parte 1)
- **Depende de:** T-01
- **Entrega:** função/módulo que lê `grafo_rede_p.txt` e `grafo_rede_m.txt` e retorna `(V, E, S, T, lista_adjacencia)`
- **Formato de entrada:**
  ```
  Linha 1: V E
  Linha 2: S T
  Linhas seguintes: u v w  (aresta dirigida de u para v com peso w)
  ```
- **Teste obrigatório:** imprimir o grafo lido e conferir contra o arquivo. `grafo_rede_p.txt` deve produzir V=5, E=6, S=0, T=4.
- **Critério de conclusão:** Membro 2 consegue importar a função sem modificação

### T-03 · Parser para grafo não-dirigido sem peso (Parte 2)
- **Depende de:** T-01
- **Entrega:** função/módulo que lê `grafo_wifi_p.txt` e `grafo_wifi_m.txt` e retorna `(V, E, lista_adjacencia)`
- **Formato de entrada:**
  ```
  Linha 1: V E
  Linhas seguintes: u v  (aresta não-dirigida)
  ```
- **Teste obrigatório:** `grafo_wifi_p.txt` deve produzir V=5, E=7. Lista de adjacência deve ser simétrica (se u-v existe, v-u também).
- **Critério de conclusão:** Membro 3 consegue importar a função sem modificação

---

## Membro 2 — Parte 1: Caminho Mínimo

**Responsabilidade:** implementar Bellman-Ford e gerar os arquivos de saída da Parte 1.

### T-04 · Implementar Bellman-Ford com rastreamento de predecessores
- **Depende de:** T-02
- **Entrega:** função `bellman_ford(grafo, S, T)` que retorna `(dist, predecessores)`
- **Algoritmo:**
  1. `dist[i] = ∞` para todo i; `dist[S] = 0`
  2. Repetir V-1 vezes: para cada aresta (u, v, w), se `dist[u] + w < dist[v]`, atualize `dist[v] = dist[u] + w` e `pred[v] = u`
  3. (Opcional bônus) Na V-ésima iteração, se ainda houver relaxamento, reportar ciclo negativo
- **Teste interno:** `grafo_rede_p.txt` → dist[4] deve ser 8; caminho esperado: 0 → 1 → 2 → 4
- **Critério de conclusão:** teste passa nos dois grafos antes de prosseguir para T-05

### T-05 · Reconstrução do caminho e formatação de saída
- **Depende de:** T-04
- **Entrega:** função `reconstruir_caminho(pred, S, T)` → lista de vértices na ordem S...T; função `formatar_saida_p1(algoritmo, justificativa, rota, custo)` → string no formato exato
- **Formato obrigatório:**
  ```
  ALGORITMO: Bellman-Ford
  JUSTIFICATIVA: <texto em até 3 linhas>
  ROTA: 0 1 2 4
  CUSTO: 8
  ```
- **Critério de conclusão:** saída gerada bate exatamente com `docs/exemplo_saida_parte1.txt`

### T-06 · Gerar saida_parte1_p.txt e saida_parte1_m.txt
- **Depende de:** T-05
- **Entrega:** arquivos `parte1/saida_parte1_p.txt` e `parte1/saida_parte1_m.txt` commitados
- **Critério de conclusão:** ambos os arquivos presentes no repositório, formato conferido pelo Membro 4

---

## Membro 3 — Parte 2: Coloração de Grafos

**Responsabilidade:** implementar DSatur e gerar os arquivos de saída da Parte 2.

### T-07 · Implementar DSatur com saturação dinâmica
- **Depende de:** T-03
- **Entrega:** função `dsatur(grafo)` que retorna `(num_cores, coloracao[])` onde `coloracao[i]` é a cor do vértice i
- **Algoritmo:**
  1. Inicializar `cor[i] = -1`, `saturacao[i] = 0`, `grau[i]` para todos
  2. Enquanto houver vértice não-colorido:
     - Selecione o vértice `u` com maior `saturacao[u]` (empate: maior `grau[u]`)
     - Atribua a `u` a menor cor inteira ≥ 1 não usada por nenhum vizinho
     - Para cada vizinho `v` não-colorido de `u`, recalcule `saturacao[v]` como o número de cores distintas entre os vizinhos de `v` já coloridos
- **Estrutura de dados sugerida:** conjunto de cores dos vizinhos para cada vértice, atualizado incrementalmente
- **Teste obrigatório:** `grafo_wifi_p.txt` → NUM_CORES = 3 (5-ciclo com diagonais exige 3 cores)
- **Critério de conclusão:** teste passa nos dois grafos

### T-08 · Verificação de validade e formatação de saída
- **Depende de:** T-07
- **Entrega:** função `validar_coloracao(grafo, coloracao)` que verifica se nenhum par adjacente tem a mesma cor (retorna True/False); função `formatar_saida_p2(algoritmo, justificativa, num_cores, coloracao)` → string no formato exato
- **Formato obrigatório:**
  ```
  ALGORITMO: DSatur
  JUSTIFICATIVA: <texto em até 3 linhas>
  NUM_CORES: 3
  COLORACAO: 0=1 1=2 2=3 3=1 4=2
  ```
- **Critério de conclusão:** validação retorna True para ambos os grafos; saída bate com `docs/exemplo_saida_parte2.txt`

### T-09 · Gerar saida_parte2_p.txt e saida_parte2_m.txt
- **Depende de:** T-08
- **Entrega:** arquivos `parte2/saida_parte2_p.txt` e `parte2/saida_parte2_m.txt` commitados
- **Critério de conclusão:** ambos presentes, validação passou, formato conferido pelo Membro 4

---

## Membro 4 — Documentação & Entrega

**Responsabilidade:** justificativas técnicas, comparativo de algoritmos, README final, conferência dos arquivos.

### T-10 · Redigir justificativas de algoritmo (Partes 1 e 2)
- **Depende de:** T-04 (para entender Bellman-Ford em prática), T-07 (para entender DSatur em prática)
- **Entrega:** textos de justificativa (máx. 3 linhas cada) que serão inseridos nas saídas pelos Membros 2 e 3
- **Parte 1 deve mencionar:** pesos negativos no grafo, por que Dijkstra é inválido, por que Bellman-Ford é correto
- **Parte 2 deve mencionar:** critério de saturação, vantagem sobre greedy simples, comportamento próximo do ótimo sem backtracking
- **Critério de conclusão:** texto aprovado e entregue antes da geração das saídas finais

### T-11 · Escrever comparativo.md com trade-offs
- **Depende de:** T-06 (saídas P1 prontas), T-09 (saídas P2 prontas)
- **Entrega:** arquivo `comparativo.md` na raiz do repositório
- **Conteúdo mínimo:**
  - Seção Parte 1: tabela com Dijkstra, Bellman-Ford, Floyd-Warshall — complexidade, suporte a pesos negativos, escopo, motivo da escolha
  - Seção Parte 2: tabela com Greedy, DSatur, Backtracking — complexidade, qualidade da solução, garante ótimo, motivo da escolha
  - Parágrafo de conclusão por parte explicando a decisão final
- **Critério de conclusão:** cobre os três algoritmos candidatos de cada parte com argumentação técnica

### T-12 · README final com instruções de compilação e execução
- **Depende de:** T-11 (projeto finalizado)
- **Entrega:** `README.md` atualizado na raiz
- **Conteúdo obrigatório:**
  - Linguagem e versão (ex: Python 3.11, C++17, Java 17)
  - Como compilar (se aplicável): comando exato
  - Como executar Parte 1: `./programa parte1 grafo_rede_p.txt` (ou equivalente)
  - Como executar Parte 2: `./programa parte2 grafo_wifi_p.txt` (ou equivalente)
  - Dependências externas (se houver)
- **Critério de conclusão:** qualquer pessoa consegue clonar e reproduzir todos os 4 arquivos de saída seguindo apenas o README

---

## Cronograma sugerido

| Fase | Tasks | Membros bloqueados até concluir |
|------|-------|---------------------------------|
| Kick-off | T-01 | Todos |
| Parsers | T-02, T-03 (paralelo) | M2 espera T-02; M3 espera T-03 |
| Algoritmos | T-04, T-07 (paralelo) | M2 e M3 independentes aqui |
| Formatação | T-05, T-08 (paralelo) | M4 pode iniciar T-10 quando T-04 e T-07 existem |
| Saídas | T-06, T-09 (paralelo) | M4 inicia T-11 após ambos |
| Docs | T-11 → T-12 | Entrega final |

---

## Checklist de entrega

- [ ] `parte1/saida_parte1_p.txt`
- [ ] `parte1/saida_parte1_m.txt`
- [ ] `parte2/saida_parte2_p.txt`
- [ ] `parte2/saida_parte2_m.txt`
- [ ] `comparativo.md` (ou `.pdf`)
- [ ] `README.md` com instruções funcionais
- [ ] Commits de todos os 4 membros no histórico git
