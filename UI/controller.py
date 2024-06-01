import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []
        self.listaOrdinata = []

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        stringa_canzoni = self._view.txt_view.value
        try:
            numero_canzoni = int(stringa_canzoni)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Hai inserito una stringa, devi inserire un intero!"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._model.buildGraph(numero_canzoni)
        nNodes, nEdges = self._model.getValuesGraph()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nNodes} nodi e {nEdges} vertici"))
        self._view._btn_adiacenze.disabled = False
        self.fillDD(self._model.tuplaDD())
        self._view._text_2.disabled = False
        self._view._btn_calcola_percorso.disabled = False
        self._view.update_page()

    def handle_adiacenze(self, e):
        self.listaOrdinata = []
        self._view.txt_result.controls.clear()
        nodoSorgente = self._view._ddA1.value
        if nodoSorgente is None:
            self._view.txt_result.controls.append(ft.Text("ERRORE"))
            self._view.update_page()
            return
        dizionario_bilancio = self._model.definizione_dizionario()
        vicini = self._model.getVicini(nodoSorgente)
        for vic in vicini:
            self.listaOrdinata.append((self._model._idMap[int(vic.AlbumId)].Title, dizionario_bilancio[vic.AlbumId]))
        self.listaOrdinata = sorted(self.listaOrdinata, key=lambda x: x[1], reverse=True)
        for titolo, bilancio in self.listaOrdinata:
            self._view.txt_result.controls.append(ft.Text(f"{titolo}, bilancio={bilancio}"))
        self._view.update_page()

    def handle_calcola_percorso(self, e):
        self._view.txt_result.controls.clear()
        stringa_percorso = self._view._text_2.value
        try:
            numero_percorso = int(stringa_percorso)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Hai inserito una stringa, devi inserire un intero!"))
            self._view.update_page()
            return
        nodoPartenza = self._view._ddA1.value
        nodoArrivo = self._view._ddA2.value
        miglior_cammino = self._model.getBestPath(numero_percorso, nodoPartenza, nodoArrivo)
        for i in range(len(miglior_cammino)):
                self._view.txt_result.controls.append(ft.Text(f"{miglior_cammino[i].Title}"))
        self._view.update_page()

    def fillDD(self, tupla):
        self._view._ddA1.options.clear()
        self._view._ddA2.options.clear()
        ordinata = sorted(tupla, key=lambda x: x[1])
        for key, value in ordinata:
            self._view._ddA1.options.append(ft.dropdown.Option(text=value, key=key))
            self._view._ddA2.options.append(ft.dropdown.Option(text=value, key=key))
        self._view.update_page()
