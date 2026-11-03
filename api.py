from fastapi import FastAPI, HTTPException
from grafo import carregar_grafo
from buscas import bfs, dfs, gulosa, dijkstra

app = FastAPI(title="Rotas do Prédio - UniSenac")
grafo = carregar_grafo("arestas.txt")

# dicionário que liga o nome do algoritmo à função
ALGORITMOS = {
    "bfs": bfs,
    "dfs": dfs,
    "gulosa": gulosa,
    "dijkstra": dijkstra,
}
UNIDADE = "passos"


def conferir_porta(porta):
    # deixa em maiúsculas e devolve 404 se a porta não existir
    porta = porta.upper()
    if porta not in grafo:
        raise HTTPException(404, f"Porta não encontrada: {porta}")
    return porta


def executar(nome, origem, destino):
    # roda um algoritmo e monta a resposta no formato do PDF
    caminho, custo, visitados = ALGORITMOS[nome](grafo, origem, destino)
    return {
        "algoritmo": nome,
        "caminho": caminho,
        "custo": custo,
        "unidade": UNIDADE,
        "visitados": visitados,
    }


@app.get("/portas")
def portas():
    # lista todas as portas do prédio
    return sorted(grafo)


@app.get("/vizinhos/{porta}")
def vizinhos(porta: str):
    # vizinhos da porta e o peso de cada aresta
    porta = conferir_porta(porta)
    return [{"porta": p, "peso": w} for p, w in grafo[porta]]


@app.get("/rota")
def rota(origem: str, destino: str, algoritmo: str = "dijkstra"):
    # caminho, custo e visitados de UM algoritmo
    origem = conferir_porta(origem)
    destino = conferir_porta(destino)
    algoritmo = algoritmo.lower()
    if algoritmo not in ALGORITMOS:
        raise HTTPException(400, "Algoritmo inválido: use bfs, dfs, gulosa ou dijkstra")
    return executar(algoritmo, origem, destino)


@app.get("/comparar")
def comparar(origem: str, destino: str):
    # os quatro algoritmos lado a lado para comparar
    origem = conferir_porta(origem)
    destino = conferir_porta(destino)
    return [executar(nome, origem, destino) for nome in ALGORITMOS]
