import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleCreaGrafo(self, e):
        if self._view._ddNazione.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare una nazione", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.controls.clear()
        self._model.buildGraph(self._view._ddNazione.value)
        self.fillDDArtist()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato", color="green"))
        nodi, archi=self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {nodi}, Numero archi: {archi}"))
        bestArtista, bestScore = self._model.getArtistaPiuAbbinato()
        self._view.txt_result.controls.append(
            ft.Text(f"Artista con Maggiore influenza {bestArtista}: {bestScore}", color="blue"))

        topEdges = self._model.get5ArchiPesoMaggiore()
        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))
        for u, v, data in topEdges:
            self._view.txt_result.controls.append(
                ft.Text(f"{u.Name} -> {v.Name} : {data['weight']}"))
        self._view.update_page()


    def handleCammino(self, e):
        bestPath = self._model.getBestPath(self._view._ddArtist.value)
        self._view.txt_result.controls.append(ft.Text(f"Cammino massimo trovato ({len(bestPath)} nodi):"))
        for a in bestPath:
            self._view.txt_result.controls.append(ft.Text(a.Name))
        self._view.update_page()

    def fillDDArtist(self):
        self._view._ddArtist.options.clear()
        artists = self._model.getAllNodes()
        for artist in artists:
            self._view._ddArtist.options.append(ft.dropdown.Option(key=artist.ArtistId, text=artist.Name))
        self._view.update_page()


    def fillDDNazioni(self):
        self._view._ddNazione.options.clear()
        nazioni = self._model.getNazioni()
        for n in nazioni:
            self._view._ddNazione.options.append(ft.dropdown.Option(key=n, text=n))
        self._view.update_page()