import flet as ft
import networkx as nx

from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

        self._lista_years = []

        self.G = None
        self.teams = {}

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        self.G = nx.Graph()

        year = self._view.dd_anno.value
        lista_team = self._model.get_team_by_year(year)

        for team in lista_team:
            self.teams[team.id] = team
            self.G.add_node(team)

        for nodo1 in self.G:
            print(nodo1)
            for nodo2 in self.G:
                print(nodo2)
                if nodo1.id < nodo2.id:
                    risultato = self._model.calcola_peso(nodo1, nodo2)

                    if risultato is None:
                        continue  # non creare arco

                    # opzionale: se vuoi evitare archi inutili
                    if risultato <= 0:
                        continue

                    print(risultato)
                    self.G.add_edge(nodo1, nodo2, weight=risultato)

        self._view.txt_risultato.controls.clear()
        if self.G.number_of_nodes() > 0 and self.G.number_of_edges() > 0:
            self._view.txt_risultato.controls.append(ft.Text("Grafo creato correttamente"))
            self._view.txt_risultato.controls.append(ft.Text(f"Numero nodi {self.G.number_of_nodes()}"))
            self._view.txt_risultato.controls.append(ft.Text(f"Numero archi {self.G.number_of_edges()}"))
            self._view.update()
        else:
            self._view.show_alert("La creazione del grafo ha riscontrato dei problemi")


    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        id_team_selezionato = int(self._view.dd_squadra.value)
        team = self.teams[id_team_selezionato]
        print(team)

        self._view.txt_risultato.controls.clear()

        vicini = []
        for nodo in self.G.neighbors(team):
            peso = self.G[team][nodo].get("weight",0)
            vicini.append((nodo, peso))

        #ordino per peso decrescente
        vicini.sort(key=lambda x: x[1], reverse=True)

        for nodo, peso in vicini:
            self._view.txt_risultato.controls.append(ft.Text(f"{nodo.team_code} ({nodo.name}) - peso {peso}"))

        self._view.update()


    def get_years(self):
        self._lista_years = [ft.dropdown.Option("Nessun filtro")]
        db_years = self._model.get_years()
        for year in db_years:
            self._lista_years.append(
                ft.dropdown.Option(year)
            )
        return self._lista_years


    def get_team_by_year(self, e):
        year = self._view.dd_anno.value
        lista_team = self._model.get_team_by_year(year)

        self._view.txt_out_squadre.controls.clear()

        numero_squadre = len(lista_team)

        self._view.txt_out_squadre.controls.append(ft.Text(f"Numero squadre: {numero_squadre}"))

        for team in lista_team:
            self._view.txt_out_squadre.controls.append(ft.Text(f"{team.team_code} {team.name}"))

        options = [ft.dropdown.Option(key= team.id, text=f"{team.team_code} ({team.name})") for team in lista_team]
        self._view.dd_squadra.options = options



        self._view.update()


        # vertice di partenza
        # ogni vertice può comparire una sola volta
        # dal peso del vertice le soluzioni buone sono quelle diciamo con peso massimo uguale al primo e via via cosi
        # si ferma a k = 3 archi vicini quindi 4 nodi
        #

    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        id_team_selezionato = int(self._view.dd_squadra.value)
        team_partenza = self.teams[id_team_selezionato]

        miglior_peso , miglior_sequenza = self._model.calcola_percorso(team_partenza, self.G)
        self._view.txt_risultato.controls.clear()

        for i in range(len(miglior_sequenza)-1):
            a = miglior_sequenza[i]
            b = miglior_sequenza[i + 1]
            w = self.G[a][b]["weight"]
            self._view.txt_risultato.controls.append(ft.Text(f"{a.team_code} ({a.name}) -> {b.team_code} ({b.name}) (peso {w})"))

        self._view.txt_risultato.controls.append(ft.Text(f"Peso totale: {miglior_peso}"))
        self._view.update()

