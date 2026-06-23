"""Validação independente das saídas de coloração da Parte 2."""

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Grafo:
    numero_vertices: int
    numero_arestas: int
    arestas: frozenset[tuple[int, int]]


@dataclass(frozen=True)
class SaidaColoracao:
    algoritmo: str
    justificativa: str
    numero_cores: int
    coloracao: dict[int, int]


@dataclass(frozen=True)
class RelatorioValidacao:
    valida: bool
    numero_vertices: int
    numero_arestas: int
    numero_cores_utilizadas: int
    problemas: tuple[str, ...]


def ler_grafo(caminho: str | Path) -> Grafo:
    linhas = Path(caminho).read_text(encoding="utf-8").splitlines()
    linhas = [linha.strip() for linha in linhas if linha.strip()]
    numero_vertices, numero_arestas = map(int, linhas[0].split())
    arestas = frozenset(
        tuple(sorted(map(int, linha.split())))
        for linha in linhas[1:]
    )
    if len(arestas) != numero_arestas:
        raise ValueError(
            f"O cabecalho declara {numero_arestas} arestas, "
            f"mas possui {len(arestas)} arestas distintas."
        )
    return Grafo(numero_vertices, numero_arestas, arestas)


def ler_saida_coloracao(caminho: str | Path) -> SaidaColoracao:
    linhas = Path(caminho).read_text(encoding="utf-8").splitlines()
    linhas = [linha.strip() for linha in linhas if linha.strip()]

    if not 4 <= len(linhas) <= 6:
        raise ValueError(
            "A saida deve possuir os quatro campos e justificativa de ate tres linhas."
        )

    def extrair_valor(linha: str, rotulo: str) -> str:
        prefixo = f"{rotulo}:"
        if not linha.startswith(prefixo):
            raise ValueError(f"Formato invalido: esperado o rotulo {rotulo}.")
        return linha[len(prefixo):].strip()

    algoritmo = extrair_valor(linhas[0], "ALGORITMO")
    primeira_linha_justificativa = extrair_valor(linhas[1], "JUSTIFICATIVA")
    justificativa = "\n".join(
        (primeira_linha_justificativa, *linhas[2:-2])
    )
    numero_cores_texto = extrair_valor(linhas[-2], "NUM_CORES")
    coloracao_texto = extrair_valor(linhas[-1], "COLORACAO")
    numero_cores = int(numero_cores_texto)
    coloracao = {}
    for token in coloracao_texto.split():
        vertice_texto, cor_texto = token.split("=", 1)
        vertice = int(vertice_texto)
        if vertice in coloracao:
            raise ValueError(f"Vertice {vertice} aparece mais de uma vez na COLORACAO.")
        coloracao[vertice] = int(cor_texto)

    return SaidaColoracao(algoritmo, justificativa, numero_cores, coloracao)


def validar_coloracao(
    grafo: Grafo,
    saida: SaidaColoracao,
) -> RelatorioValidacao:
    cores_utilizadas = len(set(saida.coloracao.values()))
    problemas = []
    vertices_esperados = set(range(grafo.numero_vertices))
    vertices_informados = set(saida.coloracao)
    vertices_ausentes = sorted(vertices_esperados - vertices_informados)
    if vertices_ausentes:
        lista = ", ".join(map(str, vertices_ausentes))
        problemas.append(f"Vertices sem cor: {lista}.")

    vertices_extras = sorted(vertices_informados - vertices_esperados)
    if vertices_extras:
        lista = ", ".join(map(str, vertices_extras))
        problemas.append(f"Vertices inexistentes na coloracao: {lista}.")

    for vertice, cor in sorted(saida.coloracao.items()):
        if cor < 1:
            problemas.append(
                f"Vertice {vertice} usa a cor invalida {cor}; "
                "cores devem iniciar em 1."
            )

    if saida.numero_cores != cores_utilizadas:
        problemas.append(
            f"NUM_CORES informa {saida.numero_cores}, mas foram utilizadas "
            f"{cores_utilizadas} cores distintas."
        )

    for origem, destino in sorted(grafo.arestas):
        cor_origem = saida.coloracao.get(origem)
        cor_destino = saida.coloracao.get(destino)
        if cor_origem is not None and cor_origem == cor_destino:
            problemas.append(
                f"Vertices adjacentes {origem} e {destino} usam a cor {cor_origem}."
            )

    return RelatorioValidacao(
        valida=not problemas,
        numero_vertices=grafo.numero_vertices,
        numero_arestas=grafo.numero_arestas,
        numero_cores_utilizadas=cores_utilizadas,
        problemas=tuple(problemas),
    )


def validar_arquivo(
    caminho_grafo: str | Path,
    caminho_saida: str | Path,
) -> tuple[bool, str]:
    grafo = ler_grafo(caminho_grafo)
    caminho_saida = Path(caminho_saida)

    if not caminho_saida.exists():
        relatorio = "\n".join(
            (
                f"ARQUIVO: {caminho_saida}",
                "STATUS: PENDENTE",
                f"VERTICES: {grafo.numero_vertices}",
                f"ARESTAS: {grafo.numero_arestas}",
                "CORES_UTILIZADAS: N/A",
                "PROBLEMAS:",
                "- Arquivo de saida ainda nao foi gerado.",
            )
        )
        return False, relatorio

    try:
        saida = ler_saida_coloracao(caminho_saida)
    except (OSError, ValueError) as erro:
        relatorio = "\n".join(
            (
                f"ARQUIVO: {caminho_saida}",
                "STATUS: INVALIDA",
                f"VERTICES: {grafo.numero_vertices}",
                f"ARESTAS: {grafo.numero_arestas}",
                "CORES_UTILIZADAS: N/A",
                "PROBLEMAS:",
                f"- Formato da saida invalido: {erro}",
            )
        )
        return False, relatorio

    resultado = validar_coloracao(grafo, saida)
    linhas = (
        f"ARQUIVO: {caminho_saida}",
        f"STATUS: {'VALIDA' if resultado.valida else 'INVALIDA'}",
        f"VERTICES: {resultado.numero_vertices}",
        f"ARESTAS: {resultado.numero_arestas}",
        f"CORES_UTILIZADAS: {resultado.numero_cores_utilizadas}",
        "PROBLEMAS:",
    )
    problemas = resultado.problemas or ("Nenhum problema encontrado.",)
    relatorio = "\n".join((*linhas, *(f"- {problema}" for problema in problemas)))
    return resultado.valida, relatorio


def main(argumentos: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Valida as coloracoes geradas para os grafos da Parte 2."
    )
    parser.add_argument("--grafo", type=Path, help="Caminho do arquivo de grafo.")
    parser.add_argument("--saida", type=Path, help="Caminho da saida de coloracao.")
    opcoes = parser.parse_args(argumentos)

    if (opcoes.grafo is None) != (opcoes.saida is None):
        parser.error("--grafo e --saida devem ser informados juntos")

    if opcoes.grafo is not None:
        pares = ((opcoes.grafo, opcoes.saida),)
    else:
        raiz_projeto = Path(__file__).resolve().parent.parent
        diretorio_entrada = raiz_projeto / "entrada"
        diretorio_saida = raiz_projeto / "parte2"
        pares = (
            (
                diretorio_entrada / "grafo_wifi_p.txt",
                diretorio_saida / "saida_parte2_p.txt",
            ),
            (
                diretorio_entrada / "grafo_wifi_m.txt",
                diretorio_saida / "saida_parte2_m.txt",
            ),
        )

    todos_validos = True
    for indice, (grafo, saida) in enumerate(pares):
        if indice:
            print()
        sucesso, relatorio = validar_arquivo(grafo, saida)
        print(relatorio)
        todos_validos = todos_validos and sucesso

    return 0 if todos_validos else 1


if __name__ == "__main__":
    raise SystemExit(main())
