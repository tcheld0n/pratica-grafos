import heapq
from pathlib import Path


PASTA_ATUAL = Path(__file__).parent


def ler_grafo(nome_arquivo):
    """
    Le o grafo no formato:

    num_vertices num_arestas
    origem destino
    u v peso
    u v peso
    ...

    Retorna:
    - numero de vertices
    - numero de arestas
    - vertice de origem
    - vertice de destino
    - grafo em lista de adjacencia
    - lista de arestas
    """
    caminho_arquivo = PASTA_ATUAL / nome_arquivo

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip().split() for linha in arquivo if linha.strip()]

    num_vertices = int(linhas[0][0])
    num_arestas = int(linhas[0][1])

    origem = int(linhas[1][0])
    destino = int(linhas[1][1])

    grafo = [[] for _ in range(num_vertices)]
    arestas = []

    for linha in linhas[2:]:
        u = int(linha[0])
        v = int(linha[1])
        peso = int(linha[2])

        grafo[u].append((v, peso))
        arestas.append((u, v, peso))

    return num_vertices, num_arestas, origem, destino, grafo, arestas


def reconstruir_caminho(pai, origem, destino):
    """
    Reconstrói o caminho da origem até o destino usando o vetor de pais.
    """
    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = pai[atual]

    caminho.reverse()

    if not caminho or caminho[0] != origem:
        return []

    return caminho


def dijkstra(num_vertices, origem, destino, grafo):
    """
    Aplica Dijkstra somente como teste inicial no grafo pequeno.
    """
    distancia = [float("inf")] * num_vertices
    pai = [None] * num_vertices

    distancia[origem] = 0
    fila = [(0, origem)]

    while fila:
        dist_atual, vertice = heapq.heappop(fila)

        if dist_atual > distancia[vertice]:
            continue

        for vizinho, peso in grafo[vertice]:
            nova_distancia = dist_atual + peso

            if nova_distancia < distancia[vizinho]:
                distancia[vizinho] = nova_distancia
                pai[vizinho] = vertice
                heapq.heappush(fila, (nova_distancia, vizinho))

    caminho = reconstruir_caminho(pai, origem, destino)

    return caminho, distancia[destino]


def exibir_informacoes_grafo(nome_arquivo):
    """
    Mostra informações básicas para validar a leitura e a representação do grafo.
    """
    num_vertices, num_arestas, origem, destino, grafo, arestas = ler_grafo(
        nome_arquivo)

    print(f"\nArquivo lido: {nome_arquivo}")
    print(f"Numero de vertices: {num_vertices}")
    print(f"Numero de arestas: {num_arestas}")
    print(f"Origem: {origem}")
    print(f"Destino: {destino}")
    print("Representacao do grafo em lista de adjacencia:")

    for vertice, vizinhos in enumerate(grafo):
        print(f"{vertice}: {vizinhos}")

    return num_vertices, num_arestas, origem, destino, grafo, arestas


def testar_grafo_pequeno():
    """
    Primeiro teste da Parte 1 com o grafo pequeno.

    Responsabilidade do Integrante 2:
    - ler o arquivo grafo_rede_p.txt;
    - representar o grafo;
    - aplicar um teste inicial com Dijkstra;
    - reconstruir a rota S -> T.
    """
    num_vertices, _, origem, destino, grafo, _ = ler_grafo("grafo_rede_p.txt")

    rota, custo = dijkstra(num_vertices, origem, destino, grafo)

    print("\nTeste inicial com grafo pequeno:")
    print("ALGORITMO: Dijkstra")
    print("ROTA:", " ".join(map(str, rota)))
    print("CUSTO:", custo)


def main():
    print("Parte 1 - Base do roteamento")
    print("Responsabilidade: Integrante 2")

    exibir_informacoes_grafo("grafo_rede_p.txt")
    testar_grafo_pequeno()

    exibir_informacoes_grafo("grafo_rede_m.txt")

    print("\nObservacao:")
    print(
        "A implementacao do Bellman-Ford, a validacao final e a geracao "
        "dos arquivos de saida ficam para o Integrante 3."
    )


if __name__ == "__main__":
    main()
