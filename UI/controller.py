import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._model.buildGraph()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodes()} "
                                                      f"Numero di archi: {self._model.getNumEdges()}"))
        min = self._model.getArcoMin()
        max = self._model.getArcoMax()
        self._view.txt_result.controls.append(ft.Text(f"Informazioni sui pesi degli archi - "
                                                      f"valore minimo: {min} e valore massimo: {max}"))
        self._view.update_page()

    def handle_countedges(self, e):
        soglia = self._view.txt_name.value
        try:
            sogliaFloat = float(soglia)
        except ValueError:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Attenzione soglia inserita non numerica."))
            self._view.update_page()
            return

        nMin = self._model.numArchiMinori(sogliaFloat)
        nMag = self._model.numArchiMaggiori(sogliaFloat)

        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso maggiore della soglia: {nMag}\n"
                                                       f"Numero archi con peso minore della soglia: {nMin}"))
        self._view.update_page()

    def handle_search(self, e):
        threshold = float(self._view.txt_name.value)
        self._model.searchPath(threshold)

        self._view.txt_result3.controls.append(ft.Text(f"Peso cammino massimo: "
                                                       f"{str(self._model.computeWeightPath(self._model.solBest))}"))

        for ii in self._model.solBest:
            self._view.txt_result3.controls.append(ft.Text(
                f"{ii[0]} --> {ii[1]}: {str(ii[2]["weight"])}"))

        self._view.update_page()