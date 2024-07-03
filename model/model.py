import networkx as nx
from database.DAO import DAO


class Model:

    def __init__(self):
        self._listChromosomes = []
        self._listGenes = []
        self._listConnessioni = []

        self._graph = nx.DiGraph()
        self._nodes = []
        self._edges = []

        self.solBest = []

        self.loadChromosomes()
        self.loadGenes()
        self.loadConnessioni()

    def loadChromosomes(self):
        self._listChromosomes = DAO.getAllChromosomes()

    def loadGenes(self):
        self._listGenes = DAO.getAllGenes()

    def loadConnessioni(self):
        self._listConnessioni = DAO.getAllConnessioni()

    def buildGraph(self):
        self._graph.clear()

        for c in self._listChromosomes:
            self._nodes.append(c)
        self._graph.add_nodes_from(self._nodes)

        self.idMap = {}
        for g in self._listGenes:
            self.idMap[g.GeneID] = g.Chromosome

        edges = {}
        for g1, g2, corr in self._listConnessioni:
            if (self.idMap[g1], self.idMap[g2]) not in edges:
                edges[(self.idMap[g1], self.idMap[g2])] = float(corr)
            else:
                edges[(self.idMap[g1], self.idMap[g2])] += float(corr)

        for k, v in edges.items():
            self._edges.append((k[0], k[1], v))
        self._graph.add_weighted_edges_from(self._edges)

    def searchPath(self, t):

        for n in self._nodes:
            parziale = []
            parziale_archi = []
            parziale.append(n)
            self.ricorsione(parziale, parziale_archi, t)

        print("final", len(self.solBest), [i[2]["weight"] for i in self.solBest])

    def ricorsione(self, parziale, parziale_archi, t):
        nodoLast = parziale[-1]
        vicino = self.getVicinoAmmissibile(nodoLast, parziale_archi, t)

        #stop
        if len(vicino) == 0:
            weightPath = self.computeWeightPath(parziale_archi)
            bestWeightPath = self.computeWeightPath(self.solBest)
            if weightPath > bestWeightPath:
                self.solBest = parziale_archi[:]
            return

        for v in vicino:
            parziale.append(v)
            parziale_archi.append(((nodoLast, v, self._graph.get_edge_data(nodoLast, v))))
            self.ricorsione(parziale, parziale_archi, t)
            parziale.pop()
            parziale_archi.pop()

    def getVicinoAmmissibile(self, nodoLast, parziale_archi, t):
        listVicini = self._graph.edges(nodoLast, data=True)
        result = []
        for e in listVicini:
            if e[2]["weight"] > t:
                e_inv = (e[1], e[0], e[2])
                if (e_inv not in parziale_archi) and (e not in parziale_archi):
                    result.append(e[1])
        return result

    def computeWeightPath(self, list):
        peso = 0
        for e in list:
            peso += e[2]["weight"]
        return peso

    def getNodes(self):
        return self._graph.nodes()

    def getEdges(self):
        return list(self._graph.edges(data=True))

    def getNumNodes(self):
        return len(self._nodes)

    def getNumEdges(self):
        return len(self._edges)

    def getArcoMin(self):
        return min([a[2]['weight'] for a in self.getEdges()])

    def getArcoMax(self):
        return max([a[2]['weight'] for a in self.getEdges()])

    def numArchiMinori(self, soglia):
        minori = 0
        for a in self.getEdges():
            if a[2]['weight'] < soglia:
                minori += 1
        return minori

    def numArchiMaggiori(self, soglia):
        maggiori = 0
        for a in self.getEdges():
            if a[2]['weight'] > soglia:
                maggiori += 1
        return maggiori



"""

Grafo orientato
Query che restituisce due geni e il peso. Nel model ciclo i valori 
ottenuti e metto in un dizionario: se arco gia nel dizionario 
(coppia di nodi gia presente nell'idMap) sommo il peso se no aggiungo
nuova chave con nuovo valore.
Per prendere arco con peso minore: min([a[2]['weight'] for a in self.getEdges()])
Per prendere arco con peso maggiore: max([a[2]['weight'] for a in self.getEdges()])
Per sapere numero di archi minori e maggiori di una soglia metodi: def numArchiMinori, def numArchiMaggiori

"""
