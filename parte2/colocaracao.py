import os
from pathlib import Path

class GrafoWiFi:
    def __init__(self):
        self.V = 0
        self.E = 0
        self.adj = {}

    def ler_arquivo(self, caminho_arquivo):
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
            
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            linhas = [linha.strip() for list_lin in f if (linha := list_lin.strip())]
        
        if not linhas:
            return
        
        # Leitura da primeira linha com número de vértices e arestas
        self.V, self.E = map(int, linhas[0].split('\t'))
        self.adj = {i: set() for i in range(self.V)}
        
        # Construção da lista de adjacência (Grafo não-direcionado)
        for linha in linhas[1:]:
            u, v = map(int, linha.split('\t'))
            self.adj[u].add(v)
            self.adj[v].add(u)

    def obter_graus(self):
        return {u: len(self.adj[u]) for u in range(self.V)}


class ColoracaoDSaturBacktracking:
    def __init__(self, grafo):
        self.grafo = grafo
        self.V = grafo.V
        self.adj = grafo.adj
        self.cores_finais = {}

    def _calcular_saturacao(self, vertice, coloridos):
        """Mede o grau de saturação contando as cores distintas nos vizinhos."""
        cores_vizinhos = set()
        for vizinho in self.adj[vertice]:
            if vizinho in coloridos:
                cores_vizinhos.add(coloridos[vizinho])
        return len(cores_vizinhos)

    def _escolher_proximo_vertice(self, coloridos, graus):
        """Heurística DSatur: maior grau de saturação, com desempate por maior grau original."""
        melhor_vertice = None
        max_sat = -1
        max_grau = -1

        for u in range(self.V):
            if u not in coloridos:
                sat = self._calcular_saturacao(u, coloridos)
                grau = graus[u]
                
                if (sat > max_sat) or (sat == max_sat and grau > max_grau):
                    max_sat = sat
                    max_grau = grau
                    melhor_vertice = u
                    
        return melhor_vertice

    def _eh_valido(self, vertice, cor, coloridos):
        """Garante que nenhum vizinho compartilhe a mesma cor."""
        for vizinho in self.adj[vertice]:
            if vizinho in coloridos and coloridos[vizinho] == cor:
                return False
        return True

    def _backtracking(self, coloridos, limite_cores, graus):
        if len(coloridos) == self.V:
            self.cores_finais = coloridos.copy()
            return True

        u = self._escolher_proximo_vertice(coloridos, graus)
        
        for cor in range(1, limite_cores + 1):
            if self._eh_valido(u, cor, coloridos):
                coloridos[u] = cor
                
                if self._backtracking(coloridos, limite_cores, graus):
                    return True
                
                del coloridos[u]  # Backtrack
                
        return False

    def resolver(self):
        if self.V == 0:
            return 0, {}

        graus = self.grafo.obter_graus()
        
        # Testa progressivamente limites de k-cores para achar o número cromático exato
        for limite in range(1, self.V + 1):
            coloridos_temporarios = {}
            if self._backtracking(coloridos_temporarios, limite, graus):
                return limite, self.cores_finais
        return self.V, self.cores_finais


def salvar_saida(caminho_saida, num_cores, coloracao_resultado):
    justificativa = (
        "O algoritmo DSatur com ordenacao por grau de saturacao dinamica "
        "foi combinado ao backtracking exato. Isso garante a descoberta do numero "
        "cromatico minimo para a alocacao de canais sem conflito entre vizinhos."
    )
    
    lista_coloracao = [f"{v}={cor}" for v, cor in sorted(coloracao_resultado.items())]
    str_coloracao = " ".join(lista_coloracao)
    
    conteudo = (
        f"ALGORITMO: DSatur com Backtracking Exato\n"
        f"JUSTIFICATIVA: {justificativa}\n"
        f"NUM_CORES: {num_cores}\n"
        f"COLORACAO: {str_coloracao}\n"
    )
    
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.write(conteudo)


if __name__ == "__main__":
    PASTA_RAIZ = Path(__file__).parent.parent
    arquivos_processar = [
        {"entrada": PASTA_RAIZ / "entrada" / "grafo_wifi_p.txt", "saida": PASTA_RAIZ / "parte2" / "saida_parte2_p.txt"},
        {"entrada": PASTA_RAIZ / "entrada" / "grafo_wifi_m.txt", "saida": PASTA_RAIZ / "parte2" / "saida_parte2_m.txt"}
    ]
    
    for par in arquivos_processar:
        if par["entrada"].exists():
            print(f"Processando {par['entrada']}...")
            
            g = GrafoWiFi()
            g.ler_arquivo(par["entrada"])
            
            solver = ColoracaoDSaturBacktracking(g)
            qtd_cores, resultado = solver.resolver()
            
            par["saida"].parent.mkdir(parents=True, exist_ok=True)
            salvar_saida(par["saida"], qtd_cores, resultado)
            print(f"Sucesso! Saída gerada em: {par['saida']}\n")
        else:
            print(f"Aviso: Arquivo de entrada {par['entrada']} não encontrado.")