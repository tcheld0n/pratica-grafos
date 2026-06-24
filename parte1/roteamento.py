import heapq
from pathlib import Path


PASTA_RAIZ = Path(__file__).parent.parent


def ler_grafo(nome_arquivo):
    """
    Le um grafo direcionado e ponderado no formato:

    numero_vertices numero_arestas
    origem destino
    u v peso
    ...

    Retorna os dados do grafo, a lista de adjacencia e a lista de arestas.
    """
    caminho_arquivo = PASTA_RAIZ / "entrada" / nome_arquivo

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

    if len(arestas) != num_arestas:
        raise ValueError(
            f"O arquivo informa {num_arestas} arestas, "
            f"mas foram lidas {len(arestas)}."
        )

    return num_vertices, num_arestas, origem, destino, grafo, arestas


def reconstruir_caminho(pai, origem, destino):
    """Reconstrói o caminho da origem ate o destino usando o vetor de pais."""
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
    """Calcula o menor caminho quando todos os pesos sao nao negativos."""
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


def bellman_ford(num_vertices, origem, destino, arestas):
    """
    Calcula o menor caminho mesmo quando existem pesos negativos.

    Retorna a rota, o custo e um valor booleano que indica se existe
    ciclo negativo alcancavel a partir da origem.
    """
    distancia = [float("inf")] * num_vertices
    pai = [None] * num_vertices
    distancia[origem] = 0

    for _ in range(num_vertices - 1):
        houve_alteracao = False

        for u, v, peso in arestas:
            if distancia[u] == float("inf"):
                continue

            nova_distancia = distancia[u] + peso

            if nova_distancia < distancia[v]:
                distancia[v] = nova_distancia
                pai[v] = u
                houve_alteracao = True

        if not houve_alteracao:
            break

    tem_ciclo_negativo = False

    for u, v, peso in arestas:
        if distancia[u] != float("inf") and distancia[u] + peso < distancia[v]:
            tem_ciclo_negativo = True
            break

    if tem_ciclo_negativo:
        return [], float("-inf"), True

    caminho = reconstruir_caminho(pai, origem, destino)
    return caminho, distancia[destino], False


def tem_peso_negativo(arestas):
    """Retorna True quando o grafo possui pelo menos uma aresta negativa."""
    return any(peso < 0 for _, _, peso in arestas)


def calcular_custo_rota(rota, grafo):
    """Soma os pesos das arestas percorridas por uma rota."""
    if not rota:
        return float("inf")

    custo_total = 0

    for i in range(len(rota) - 1):
        atual = rota[i]
        proximo = rota[i + 1]

        peso_encontrado = None
        for vizinho, peso in grafo[atual]:
            if vizinho == proximo:
                peso_encontrado = peso
                break

        if peso_encontrado is None:
            return float("inf")

        custo_total += peso_encontrado

    return custo_total


def validar_rota(rota, custo_informado, origem, destino, grafo):
    """Confere os extremos, as arestas e o custo total da rota."""
    if not rota:
        return False

    if rota[0] != origem or rota[-1] != destino:
        return False

    custo_calculado = calcular_custo_rota(rota, grafo)
    return custo_calculado == custo_informado


def formatar_saida(algoritmo, justificativa, rota, custo):
    """Monta o texto no formato exigido pelo enunciado."""
    rota_texto = " ".join(map(str, rota))

    return (
        f"ALGORITMO: {algoritmo}\n"
        f"JUSTIFICATIVA: {justificativa}\n"
        f"ROTA: {rota_texto}\n"
        f"CUSTO: {custo}\n"
    )


def salvar_saida(nome_arquivo, conteudo):
    """Salva um arquivo de saida dentro da pasta parte1."""
    caminho_saida = Path(__file__).parent / nome_arquivo

    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)


def processar_grafo_pequeno():
    """Processa o grafo pequeno, que nao possui pesos negativos."""
    num_vertices, _, origem, destino, grafo, arestas = ler_grafo(
        "grafo_rede_p.txt"
    )

    if tem_peso_negativo(arestas):
        raise ValueError("O grafo pequeno deveria possuir apenas pesos nao negativos.")

    rota, custo = dijkstra(num_vertices, origem, destino, grafo)

    if not validar_rota(rota, custo, origem, destino, grafo):
        raise ValueError("A rota calculada para o grafo pequeno e invalida.")

    justificativa = (
        "O grafo pequeno nao possui arestas com peso negativo. "
        "Dijkstra e aplicavel e encontra a rota minima de forma eficiente."
    )

    conteudo = formatar_saida("Dijkstra", justificativa, rota, custo)
    salvar_saida("saida_parte1_p.txt", conteudo)

    return rota, custo


def processar_grafo_medio():
    """Processa o grafo medio, que possui pesos negativos."""
    num_vertices, _, origem, destino, grafo, arestas = ler_grafo(
        "grafo_rede_m.txt"
    )

    rota, custo, tem_ciclo_negativo = bellman_ford(
        num_vertices, origem, destino, arestas
    )

    if tem_ciclo_negativo:
        raise ValueError("O grafo medio possui ciclo negativo alcancavel.")

    if not validar_rota(rota, custo, origem, destino, grafo):
        raise ValueError("A rota calculada para o grafo medio e invalida.")

    justificativa = (
        "O grafo possui arestas com peso negativo, o que torna Dijkstra "
        "inadequado. Bellman-Ford suporta pesos negativos e detecta ciclos negativos."
    )

    conteudo = formatar_saida("Bellman-Ford", justificativa, rota, custo)
    salvar_saida("saida_parte1_m.txt", conteudo)

    return rota, custo


def main():
    rota_p, custo_p = processar_grafo_pequeno()
    rota_m, custo_m = processar_grafo_medio()

    print("Arquivos da Parte 1 gerados com sucesso.")
    print("Grafo pequeno:", " -> ".join(map(str, rota_p)), "| custo =", custo_p)
    print("Grafo medio:", " -> ".join(map(str, rota_m)), "| custo =", custo_m)
    print("Saidas criadas em parte1/saida_parte1_p.txt e parte1/saida_parte1_m.txt")


if __name__ == "__main__":
    main()
