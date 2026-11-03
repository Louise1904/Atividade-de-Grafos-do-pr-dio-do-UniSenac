# @unisenac Etapa 3: buscas no grafo do prédio
from collections import deque
import heapq
from grafo import carregar_grafo


def montar_caminho(anterior, origem, destino):
    # @unisenac volta do destino até a origem usando as anotações de "de onde cheguei"
    caminho = [destino]
    while caminho[-1] != origem:
        caminho.append(anterior[caminho[-1]])
    caminho.reverse()
    return caminho


def calcular_custo(grafo, caminho):
    # @unisenac soma o peso de cada aresta do caminho
    custo = 0
    for i in range(len(caminho) - 1):
        for vizinho, peso in grafo[caminho[i]]:
            if vizinho == caminho[i + 1]:
                custo += peso
                break
    return custo


def bfs(grafo, origem, destino):
    # @unisenac BFS: usa FILA (primeiro que entra, primeiro que sai)
    # @unisenac acha o caminho com MENOS PORTAS, ignorando os pesos
    fila = deque([origem])
    descobertas = {origem}   # @unisenac portas que já entraram na fila (evita andar em círculo)
    anterior = {}            # @unisenac de qual porta cheguei em cada uma
    visitados = 0            # @unisenac quantas portas foram examinadas

    while fila:
        atual = fila.popleft()
        visitados += 1

        # @unisenac chegou no destino: monta o caminho e calcula o custo
        if atual == destino:
            caminho = montar_caminho(anterior, origem, destino)
            return caminho, calcular_custo(grafo, caminho), visitados

        # @unisenac coloca na fila os vizinhos que ainda não foram descobertos
        for vizinho, peso in grafo[atual]:
            if vizinho not in descobertas:
                descobertas.add(vizinho)
                anterior[vizinho] = atual
                fila.append(vizinho)

    # @unisenac não existe caminho entre as portas
    return [], 0, visitados


def dfs(grafo, origem, destino):
    # @unisenac DFS: usa PILHA (último que entra, primeiro que sai)
    # @unisenac vai fundo no primeiro vizinho e só volta quando não tem mais saída
    pilha = [origem]
    finalizadas = set()   # @unisenac portas já examinadas (evita andar em círculo)
    anterior = {}         # @unisenac de qual porta cheguei em cada uma
    visitados = 0

    while pilha:
        atual = pilha.pop()   # @unisenac tira o ÚLTIMO da pilha

        # @unisenac a mesma porta pode ter sido empilhada duas vezes: ignora a repetida
        if atual in finalizadas:
            continue
        finalizadas.add(atual)
        visitados += 1

        if atual == destino:
            caminho = montar_caminho(anterior, origem, destino)
            return caminho, calcular_custo(grafo, caminho), visitados

        # @unisenac empilha ao contrário para explorar os vizinhos na ordem do arestas.txt
        for vizinho, peso in reversed(grafo[atual]):
            if vizinho not in finalizadas:
                anterior[vizinho] = atual
                pilha.append(vizinho)

    return [], 0, visitados


def gulosa(grafo, origem, destino):
    # @unisenac Gulosa: a cada passo vai para o vizinho MAIS PERTO (menor peso de aresta)
    # @unisenac não pensa no caminho todo, só na melhor escolha do momento
    caminho = [origem]      # @unisenac o caminho atual funciona como uma pilha
    vistas = {origem}       # @unisenac portas por onde já passou (evita andar em círculo)
    visitados = 1

    while caminho:
        atual = caminho[-1]

        if atual == destino:
            return caminho, calcular_custo(grafo, caminho), visitados

        # @unisenac vizinhos que ainda não foram visitados, como (peso, porta)
        candidatos = [(peso, vizinho) for vizinho, peso in grafo[atual]
                      if vizinho not in vistas]

        if candidatos:
            # @unisenac escolha gulosa: o de menor peso
            peso, proxima = min(candidatos)
            vistas.add(proxima)
            visitados += 1
            caminho.append(proxima)
        else:
            # @unisenac beco sem saída: volta uma porta e tenta o próximo mais perto
            caminho.pop()

    return [], 0, visitados


def dijkstra(grafo, origem, destino):
    # @unisenac Dijkstra: acha o caminho de MENOR PESO TOTAL (menos passos)
    # @unisenac passo 1: todas as portas começam com distância infinita; a origem com 0
    distancia = {p: float("inf") for p in grafo}
    anterior = {}         # @unisenac de onde cheguei
    distancia[origem] = 0
    fila = [(0, origem)]  # @unisenac fila de prioridade: (distância, porta)
    finalizadas = set()

    while fila:
        # @unisenac passo 2: o heapq sempre devolve a porta com a MENOR distância
        d, atual = heapq.heappop(fila)

        # @unisenac se já foi finalizada, esta entrada é antiga: ignora
        if atual in finalizadas:
            continue
        finalizadas.add(atual)

        # @unisenac passo 4: ao finalizar o destino, monta o caminho voltando pelas anotações
        if atual == destino:
            caminho = montar_caminho(anterior, origem, destino)
            return caminho, distancia[destino], len(finalizadas)

        # @unisenac passo 3: para cada vizinho, se achou um caminho mais curto, atualiza
        for vizinho, peso in grafo[atual]:
            nova = d + peso
            if nova < distancia[vizinho]:
                distancia[vizinho] = nova
                anterior[vizinho] = atual
                heapq.heappush(fila, (nova, vizinho))

    return [], 0, len(finalizadas)


if __name__ == "__main__":
    # @unisenac teste rápido das buscas
    grafo = carregar_grafo("arestas.txt")
    print("BFS:     ", bfs(grafo, "LABTEC", "CANTINAB"))
    print("DFS:     ", dfs(grafo, "LABTEC", "CANTINAB"))
    print("Gulosa:  ", gulosa(grafo, "LABTEC", "CANTINAB"))
    print("Dijkstra:", dijkstra(grafo, "LABTEC", "CANTINAB"))