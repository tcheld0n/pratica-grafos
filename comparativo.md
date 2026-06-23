# Comparativo da Parte 2 - Coloracao de Grafos

## Estrategia utilizada

A implementacao proposta para a Parte 2 utiliza **DSatur com backtracking
exato**. O DSatur escolhe primeiro o vertice com maior grau de saturacao,
isto e, aquele que possui mais cores distintas entre seus vizinhos ja
coloridos. Em caso de empate, a implementacao prioriza o vertice de maior
grau.

O backtracking testa quantidades crescentes de cores. Assim, a primeira
coloracao completa encontrada determina o numero cromatico do grafo. Essa
estrategia combina uma ordem de busca eficiente com a garantia de uma
solucao minima.

| Estrategia | Caracteristica | Garante o minimo? | Observacao |
|---|---|---:|---|
| Guloso simples | Colore os vertices em uma ordem fixa | Nao | Rapido, mas pode usar mais cores que o necessario |
| DSatur guloso | Prioriza vertices com maior saturacao | Nao | Costuma produzir coloracoes melhores que o guloso simples |
| Backtracking | Explora combinacoes de cores | Sim | Possui custo exponencial no pior caso |
| DSatur + backtracking | Usa DSatur para orientar a busca exata | Sim | Estrategia adotada na implementacao analisada |

## Validacao independente

O arquivo `parte2/validar_coloracao.py` realiza a verificacao sem importar
nem modificar o algoritmo de coloracao. Para cada par formado pelo grafo e
por sua saida, o validador:

1. confere o numero declarado de vertices e arestas;
2. verifica os quatro rotulos obrigatorios da saida;
3. confirma que cada vertice aparece exatamente uma vez;
4. exige cores inteiras iniciando em 1;
5. compara `NUM_CORES` com a quantidade de cores distintas;
6. verifica se vertices adjacentes receberam cores diferentes;
7. informa todos os problemas encontrados em um relatorio textual.

Execucao para os dois grafos:

```powershell
python parte2/validar_coloracao.py
```

Tambem e possivel validar caminhos informados explicitamente:

```powershell
python parte2/validar_coloracao.py --grafo entrada/grafo_wifi_p.txt --saida parte2/saida_parte2_p.txt
```

Execucao dos testes automaticos:

```powershell
python -m unittest parte2.test_validar_coloracao -v
```

## Resultados

Os numeros abaixo foram confirmados pela execucao do algoritmo integrado e
pela validacao automatica dos arquivos finais.

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

## Checklist final da Parte 2

- [x] Validador independente criado.
- [x] Leitura dos grafos pequeno e medio verificada.
- [x] Contagem de cores distintas implementada.
- [x] Verificacao de conflitos entre vertices adjacentes implementada.
- [x] Formato obrigatorio das saidas verificado.
- [x] Testes automaticos do validador criados.
- [x] `parte2/saida_parte2_p.txt` integrado e validado.
- [x] `parte2/saida_parte2_m.txt` integrado e validado.
- [x] Relatorio final atualizado apos a integracao das saidas.
