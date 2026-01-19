from database.dao import DAO
from model.team import Team


class Model:
    def __init__(self):
        self._best_soluzione = None
        self._best_pesi = None
        self._max_peso = None
        self.K = 3
        self.G = None

    def get_years(self):
        return DAO.get_year()

    def get_team_by_year(self, year):
        return DAO.get_team_by_year(year)

    def calcola_peso(self, nodo1: Team, nodo2: Team):
        return DAO.calcola_peso(nodo1, nodo2)

    def get_neighbors(self, team: Team):
        """Ritorna lista (vicino, peso) ordinata per peso decrescente"""
        vicini = []
        for n in self.G.neighbors(team):
            w = self.G[team][n]["weight"]
            vicini.append((n, w))
        return sorted(vicini, key=lambda x: x[1], reverse=True)

    def calcola_percorso(self, team_partenza: Team, grafo):
        """Percorso di peso massimo con archi strettamente decrescenti,
        esplorando al più i primi K vicini (per peso)."""
        self.G = grafo
        self._best_soluzione = []
        self._max_peso = 0

        self.ricorsione([team_partenza], 0, float("inf"))  # last_edge_weight = +inf
        return self._max_peso, self._best_soluzione

    def ricorsione(self, parziale, peso, ultimo_peso_arco):
        last = parziale[-1]

        if peso > self._max_peso:
            self._max_peso = peso
            self._best_soluzione = parziale.copy()

        # prendo vicini ordinati
        vicini = self.get_neighbors(last)
        neighbors = []
        counter = 0
        for nodo, peso_arco in vicini:
            if nodo in parziale: #primo vincolo
                continue
            if peso_arco <= ultimo_peso_arco:
                neighbors.append((nodo, peso_arco))
                counter += 1
                if counter == self.K:
                    break

        for nodo, peso_arco in neighbors:
            parziale.append(nodo)
            self.ricorsione(parziale, peso + peso_arco, peso_arco )
            parziale.pop()

