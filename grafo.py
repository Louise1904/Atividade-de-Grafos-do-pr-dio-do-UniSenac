from collections import deque


def carregar_grafo(caminho):
    # @unisenac dicionário: chave = porta, valor = lista de (vizinho, peso)
    grafo = {}
    with open(caminho, encoding="utf-8") as arq:
        for linha in arq:
            
            if not linha.strip():
                continue
            a, b, peso = linha.split()
            peso = int(peso)
            # @unisenac cada linha gera duas entradas: anda-se nos dois sentidos
            grafo.setdefault(a, []).append((b, peso))
            grafo.setdefault(b, []).append((a, peso))
    return grafo


def contar_arestas(grafo):
    # @unisenac cada aresta aparece duas vezes (ida e volta), por isso divide por 2
    return sum(len(v) for v in grafo.values()) // 2


def alcancaveis(grafo, origem):
    # @unisenac BFS simples só para conferir se todas as portas são alcançadas
    visitados = {origem}
    fila = deque([origem])
    while fila:
        atual = fila.popleft()
        for vizinho, _ in grafo[atual]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)
    return visitados


if __name__ == "__main__":
    grafo = carregar_grafo("arestas.txt")
    print("Portas:", len(grafo))
    print("Arestas:", contar_arestas(grafo))
    faltando = set(grafo) - alcancaveis(grafo, "LABTEC")
    if faltando:
        print("Portas NÃO alcançadas a partir do LABTEC:", sorted(faltando))
    else:
        print("BFS a partir do LABTEC alcança todas as portas.")