import copy

import networkx as nx

from database.DAO import DAO
from model.order import Order


class Model:

    def __init__(self):
        self._graph=nx.DiGraph() # diretto e pesato
        self._idMapOrders={}
        for o in DAO.getAllOrders():
            self._idMapOrders[o.order_id]=o
        self._bestPath=[]
        self._bestWeight=0

    def getAllStores(self):
        return DAO.getAllStores()

    def buildGraph(self, id: int, k: int):
        self._nodes=[]
        self._graph.clear()
        self._nodes=DAO.getAllNodes(id)
        self._graph.add_nodes_from(self._nodes)
        for ordine1, q1, ordine2, q2, diff in DAO.getAllWeightedEdges(id, k, self._idMapOrders):
            if ordine1 in self._nodes and ordine2 in self._nodes:
                peso=(q1+q2)/diff
                self._graph.add_edge(ordine1, ordine2, weight=peso)

    def getNodes(self):
        return self._nodes

    def getMaxEdges(self):
        archi=list(self._graph.edges(data="weight"))
        archi.sort(key=lambda x: x[2], reverse=True)
        return archi[0:5]

    def getMaxPath(self, source: Order):
        # il cammino più lungo possibile partendo da source
        longest_path = []
        tree=nx.dfs_tree(self._graph, source) # albero di visita
        for n in tree.nodes(): # tutti i nodi raggiunti dal cammino
            path=nx.shortest_path(tree, source=source, target=n)
            # il cammino più breve da source a n
            if len(path) > len(longest_path):
                longest_path=copy.deepcopy(path)
        return longest_path

    def getNNodes(self):
        return len(self._nodes)

    def getNEdges(self):
        return len(self._graph.edges)

    def getBestPath(self, source: Order):
        self._bestPath=[]
        self._bestWeight=0
        parziale=[source]
        for n in self._graph.successors(source):
            parziale.append(n)
            self._ricorsione(parziale)
            parziale.pop() #backtracking
        return self._bestPath, self._bestWeight

    def _ricorsione(self, parziale):
        if self.calcolaPeso(parziale)>self._bestWeight:
            self._bestPath=copy.deepcopy(parziale)
            self._bestWeight=self.calcolaPeso(parziale)
        # condizione terminale
        if len(list(self._graph.successors(parziale[-1])))==0:
            # se il nodo non ha successori
            return
        for n in self._graph.successors(parziale[-1]):
            if self._graph[parziale[-1]][n]["weight"]<self._graph[parziale[-2]][parziale[-1]]["weight"] and n not in parziale:
                # peso arco strett decrescente e nodo non già inserito
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop() #backtracking

    def calcolaPeso(self, parziale):
        peso=0
        for i in range(0, len(parziale)-1):
            peso+=self._graph[parziale[i]][parziale[i+1]]["weight"]
        return peso