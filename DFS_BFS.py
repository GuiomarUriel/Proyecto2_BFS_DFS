from os import system
import random
import networkx as nx
import pydot
import m_arista
from collections import deque 

system('cls')

#==================Generar archivo .dot=======================
def generar_grafo_graphviz(lista_aristas,nombre_grafo):
    archivo=f"{nombre_grafo}.dot"
    try:
        with open(archivo, "x") as archivo_graphviz:
            archivo_graphviz.write("graph {\n")
            for arista in lista_aristas:
                archivo_graphviz.write(f"  {arista.nodo1} -- {arista.nodo2};\n")
            archivo_graphviz.write("}\n")
    except FileExistsError:
        print( "Archivo ya existente")

#====================DFS Forma Recursiva========================
def DFS_recursivo(grafo,nodo_actual,visitados,nuevo_grafo):
    visitados.add(nodo_actual)
    nodo1=nodo_actual
    #recorremos vecinos del nodo actual
    for vecino in grafo.neighbors(nodo_actual):
        if vecino not in visitados:
            nodo2=vecino
            nueva_arista=m_arista.arista(nodo1,nodo2)
            nuevo_grafo.append(nueva_arista)
            #print('nodo1R: ',nodo1,'Nodo2: ',nodo2)
            DFS_recursivo(grafo,vecino,visitados,nuevo_grafo)
    return nuevo_grafo

def DFS_start(grafo,nodo_raiz):
    visitados=set()
    nuevo_grafo=[]#set()
    grafo_dfs=DFS_recursivo(grafo,nodo_raiz,visitados,nuevo_grafo)
    grafo_dfs=list(grafo_dfs)
    return grafo_dfs

#====================DFS Forma Iterativa========================
def DFS_iterativo(grafo, nodo_raiz):
    visitados = set()
    pila = [(nodo_raiz, None)]  # Pila de tuplas: (nodo_actual, nodo_padre)
    nuevo_grafo = []

    while pila:
        nodo_actual, nodo_padre = pila.pop()

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            if nodo_padre is not None:
                nueva_arista = m_arista.arista(nodo_padre, nodo_actual)
                nuevo_grafo.append(nueva_arista)
                #print('nodo1: ', nodo_padre, 'Nodo2: ', nodo_actual)

            # Agregamos los vecinos no visitados a la pila
            for vecino in grafo.neighbors(nodo_actual):
                if vecino not in visitados:
                    pila.append((vecino, nodo_actual))
    return nuevo_grafo

def DFS_start_iterativo(grafo, nodo_raiz):
    grafo_dfs = DFS_iterativo(grafo, nodo_raiz)
    return grafo_dfs



#====================BFS Forma Recursiva========================
def BFS_recursivo(grafo, cola, visitados, nuevo_grafo):
    if not cola:
        return nuevo_grafo

    nodo_actual = cola.popleft()
    for vecino in grafo.neighbors(nodo_actual):
        if vecino not in visitados:
            visitados.add(vecino)
            nueva_arista = m_arista.arista(nodo_actual, vecino)
            nuevo_grafo.append(nueva_arista)
            cola.append(vecino)

    return BFS_recursivo(grafo, cola, visitados, nuevo_grafo)

def BFS_start(grafo, nodo_raiz):
    visitados = set()
    nuevo_grafo = []
    cola = deque()

    visitados.add(nodo_raiz)
    cola.append(nodo_raiz)

    grafo_bfs = BFS_recursivo(grafo, cola, visitados, nuevo_grafo)
    return list(grafo_bfs)

#====================BFS Forma Iterativa========================
def BFS_iterativo(grafo, nodo_raiz):
    visitados = set()
    cola = deque([nodo_raiz])  # Inicializamos la cola con el nodo raíz
    visitados.add(nodo_raiz)
    nuevo_grafo = []

    while cola:
        nodo_actual = cola.popleft()  # Dequeue el primer nodo

        for vecino in grafo.neighbors(nodo_actual):
            if vecino not in visitados:
                visitados.add(vecino)
                nueva_arista = m_arista.arista(nodo_actual, vecino)
                nuevo_grafo.append(nueva_arista)
                #print('nodo1B: ', nodo_actual, 'Nodo2B: ', vecino)
                cola.append(vecino)  # Enqueue los vecinos no visitados
    return nuevo_grafo



 #========Programa Principal=======

grafo_base='Malla50.dot'#lectura de grafo
grafo=nx.Graph(nx.nx_pydot.read_dot(grafo_base))
nodos=list(grafo.nodes())
nodo_raiz=random.choice(nodos)
print(nodo_raiz)

grafico_dfs_recursivo=DFS_start(grafo,nodo_raiz)
grafico_dfs_iterativo=DFS_iterativo(grafo,nodo_raiz)
grafico_bfs_iterativo=BFS_iterativo(grafo,nodo_raiz)
#grafico_bfs_recursivo=BFS_start(grafo,nodo_raiz)


generar_grafo_graphviz(grafico_dfs_recursivo,'Malla_500_DFS_recursivo')
generar_grafo_graphviz(grafico_dfs_iterativo,'Malla_500_DFS_iterativo')
generar_grafo_graphviz(grafico_bfs_iterativo,'Malla_500_BFS_iterativo')
#generar_grafo_graphviz(grafico_bfs_recursivo,'BFSrecursivo_Dorogovtsev200')

# nodos=list(grafo.nodes())
# aristas = grafo.edges()
# vecinos=list(grafo.neighbors(nodo_raiz))
# print(vecinos)


