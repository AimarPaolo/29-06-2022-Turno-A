import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._nodi = []
        self._idMap = {}
        self._dizionario_bilancio = {}
        self.tupla_DD = []
        self._bestPath = []

    def buildGraph(self, nItems):
        self._grafo.clear()
        self._nodi = DAO.getAlbums(nItems)
        self._grafo.add_nodes_from(self._nodi)
        for f in self._nodi:
            self._idMap[f.AlbumId] = f
        for album1 in self._nodi:
            for album2 in self._nodi:
                numeroCanzoni1 = album1.NumeroCanzoni
                numeroCanzoni2 = album2.NumeroCanzoni
                if album2.AlbumId != album1.AlbumId and album2.AlbumId and numeroCanzoni1 - numeroCanzoni2 != 0:
                    if numeroCanzoni1 - numeroCanzoni2 > 0:
                        self._grafo.add_edge(album2, album1, weight=numeroCanzoni1 - numeroCanzoni2)
                    else:
                        self._grafo.add_edge(album1, album2, weight=-(numeroCanzoni1 - numeroCanzoni2))

    def definizione_dizionario(self):
        self._dizionario_bilancio = {}
        for s in self._grafo.nodes:
            successori = 0
            predecessori = 0
            for suc in list(self._grafo.successors(s)):
                successori += self._grafo[s][suc]['weight']
            for pred in list(self._grafo.predecessors(s)):
                predecessori += self._grafo[pred][s]['weight']
            self._dizionario_bilancio[s.AlbumId] = predecessori - successori
        return self._dizionario_bilancio

    def getVicini(self, nodoSorgente):
        nodoSource = self._idMap[int(nodoSorgente)]
        return self._grafo.neighbors(nodoSource)

    def tuplaDD(self):
        self.tuple_DD = []
        for r in self._grafo.nodes:
            self.tuple_DD.append((r.AlbumId, r.Title))
        return self.tuple_DD

    def getBestPath(self, numero_percorso, a1, a2):
        nodo1Source = self._idMap[int(a1)]
        nodo2Source = self._idMap[int(a2)]
        parziale = [nodo1Source]
        self.ricorsione(parziale, numero_percorso, nodo2Source)
        print(self._bestPath)
        return self._bestPath

    def ricorsione(self, parziale, peso_min, a2):
        if parziale[-1].AlbumId == a2.AlbumId:
            if len(parziale) > len(self._bestPath):
                self._bestPath = copy.deepcopy(parziale)
        print(list(self._grafo.successors(parziale[-1])))
        for v in self._grafo.successors(parziale[-1]):
            print("entrato")
            if v not in parziale:
                if self._grafo[parziale[-1]][v]['weight'] >= peso_min:
                    if self._dizionario_bilancio[v.AlbumId] > self._dizionario_bilancio[parziale[0].AlbumId]:
                        parziale.append(v)
                        self.ricorsione(parziale, peso_min, a2)
                        parziale.pop()
                    else:
                        if v.AlbumId == a2.AlbumId:
                            if len(parziale) + 1 > len(self._bestPath):
                                parziale.append(v)
                                self._bestPath = copy.deepcopy(parziale)
                                return
                else:
                    if v.AlbumId == a2.AlbumId:
                        if len(parziale) + 1 > len(self._bestPath):
                            parziale.append(v)
                            self._bestPath = copy.deepcopy(parziale)
                            return


    def getValuesGraph(self):
        return len(self._grafo.nodes), len(self._grafo.edges)
