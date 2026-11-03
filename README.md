Rotas do Prédio com Grafos

Trabalho de Algoritmos e Estruturas de Dados II com o professor Pablo De Chiaro.

Mapeamos o prédio a partir do LabTec, que é o ponto zero: cada porta é um nó, cada ligação entre portas vizinhas é uma aresta, e o peso da aresta é a distância medida. Uma API recebe duas portas e devolve o caminho calculado por BFS, DFS, busca gulosa e Dijkstra.

Integrantes
Louise Vahal
Unidade do peso

Todos os pesos estão em passos. Cada peso é a distância só entre duas portas vizinhas, e não a distância acumulada desde o LabTec.

Arquivos
Arquivo	O que faz
desenho.png	Foto do desenho do caderno, com o LabTec marcado como ponto zero
arestas.txt	Uma aresta por linha: PORTA PORTA PESO. São 38 portas e 43 arestas
grafo.py	Lê o arestas.txt e monta a lista de adjacência nos dois sentidos
buscas.py	BFS, DFS, gulosa e Dijkstra, todas devolvendo caminho, custo, visitados
api.py	API em FastAPI com os endpoints /portas, /vizinhos, /rota e /comparar

No desenho, o P1 é só a entrada do corredor da coordenação, não uma porta. Por isso ele não aparece no arestas.txt.

Como rodar

O projeto usa Python 3 e o uv. No terminal, dentro da pasta do projeto:

uv venv
uv pip install fastapi uvicorn

Conferir o grafo (deve mostrar 38 portas e 43 arestas, e que a BFS a partir do LABTEC alcança todas):

.venv\Scripts\python grafo.py

Testar as buscas:

.venv\Scripts\python buscas.py

Subir a API:

.venv\Scripts\python -m uvicorn api:app --reload

Depois é só abrir http://127.0.0.1:8000/docs no navegador para testar cada endpoint.

No Linux ou macOS, troque .venv\Scripts\python por .venv/bin/python.

Endpoints
Endpoint	Devolve
GET /portas	Todas as portas
GET /vizinhos/{porta}	Vizinhos e peso de cada aresta
GET /rota?origem=&destino=&algoritmo=	Caminho, custo e visitados (bfs, dfs, gulosa ou dijkstra)
GET /comparar?origem=&destino=	Os quatro algoritmos lado a lado

Uma porta inexistente devolve 404 com mensagem, e um algoritmo inválido devolve 400.

Par em que BFS e Dijkstra discordam: LABTEC → CANTINAB
Algoritmo	Caminho	Portas	Custo
BFS	LABTEC → PATIOA → PATIOB → CANTINAB	4	78 passos
Dijkstra	LABTEC → LAB201 → LAB202 → PATIOB → CANTINAB	5	47 passos

Por que os dois discordam:

A BFS explora o grafo em camadas: primeiro os vizinhos da origem, depois os vizinhos deles, e assim por diante. Por isso ela encontra o caminho com menos portas, mas ignora os pesos. O PATIOB está a só 2 portas do LABTEC passando pelo PATIOA, então ela escolhe esse caminho, mesmo com a aresta PATIOA–PATIOB pesando 50 passos:

14 + 50 + 14 = 78 passos

O Dijkstra soma os pesos e sempre continua pela porta com a menor distância acumulada. Ele percebe que contornar pelo LAB201 e pelo LAB202 é mais curto:

5 + 20 + 8 + 14 = 47 passos

O Dijkstra passa por uma porta a mais, mas anda 31 passos a menos. Menos portas nem sempre quer dizer menor distância.

Decisão sobre a busca gulosa

A busca gulosa sempre vai para o vizinho mais perto, ou seja, o de menor peso de aresta. Testamos a versão que nunca volta atrás e ela travava em 79% dos pares de portas, porque caía em becos sem saída como ESTUDOS1, CRECHE e LAB210. Por isso, quando não há saída, ela volta uma porta e tenta o próximo vizinho mais perto. Fora isso, continua sempre fazendo a escolha gulosa. Assim ela encontra caminho para todos os pares, mas não garante o menor custo: de LABTEC até CANTINAB, por exemplo, ela anda 167 passos.
