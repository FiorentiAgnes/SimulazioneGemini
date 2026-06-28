import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._idMapA={}
        self._bestPath = []

    def getBestPath(self, source):
        self._bestPath = []

        # Inizializzo il cammino parziale con il nodo sorgente
        partial = [self._idMapA[int(source)]]

        # Innesco direttamente la ricorsione passando "infinito" come peso precedente
        self._ricorsione(partial, float('inf'))

        return self._bestPath

    def _ricorsione(self, partial, lastWeight):
        # 1. Aggiorno la soluzione migliore
        if len(partial) > len(self._bestPath):
            self._bestPath = copy.deepcopy(partial)

        # 2. Recupero il nodo corrente
        current = partial[-1]

        # 3. Esploro i vicini
        for _, successor, data in self._graph.edges(current, data=True):

            weight = data["weight"]

            # VINCOLO A: pesi strettamente decrescenti (Corretto: < invece di >)
            if weight < lastWeight:

                # VINCOLO B: cammino semplice
                if successor not in partial:
                    partial.append(successor)

                    # Chiamata ricorsiva
                    self._ricorsione(partial, weight)

                    # Backtracking
                    partial.pop()



    def getNazioni(self):
        return DAO.getCountry()

    def buildGraph(self, country):
        self._graph.clear()

        nodes = DAO.getAllNodes(country)
        self._graph.add_nodes_from(nodes)
        for a in nodes:
            self._idMapA[a.ArtistId] = a
        allEdges = DAO.getAllEdges(country, self._idMapA)
        for e in allEdges:
            self._graph.add_edge(e.a1, e.a2, weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getArtistaPiuAbbinato(self):
        bestArtist = None
        bestScore = None

        for v in self._graph.nodes():
            peso= 0
            for _, _, data in self._graph.edges(v, data=True):
                peso += data["weight"]

            score = peso

            if bestScore is None or score > bestScore:
                bestScore = score
                bestArtist = v

        return bestArtist.Name, bestScore


    def get5ArchiPesoMaggiore(self):
        edges = sorted(
            self._graph.edges(data=True),
            key=lambda x: x[2]["weight"]
            ,reverse=True
        )
        return edges[:5]

    def getAllNodes(self):
        return self._graph.nodes
    def getAllEdges(self):
        return self._graph.edges