# Comparativo Parte 2 - Coloracao de Grafos

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
