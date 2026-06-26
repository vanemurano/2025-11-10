import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._store=None
        self._order = None

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        store=self._store
        if store is None:
            self._view.txt_result.controls.append(
                ft.Text(f"Selezionare prima uno store!", color="red"))
            self._view.update_page()
            return
        k=self._view._txtIntK.value
        if k is None:
            self._view.txt_result.controls.append(
                ft.Text(f"Inserire numero minimo di giorni!", color="red"))
            self._view.update_page()
            return
        try:
            intK=int(k)
        except ValueError:
            self._view.txt_result.controls.append(
                ft.Text(f"k deve essere un numero intero positivo!", color="red"))
            self._view.update_page()
            return
        if intK<0:
            self._view.txt_result.controls.append(
                ft.Text(f"k deve essere un numero intero positivo!", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(store.store_id, intK)
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato:\n"
                    f"Numero di nodi: {self._model.getNNodes()}\n"
                    f"Numero di archi: {self._model.getNEdges()}\n"
                    f"5 archi di peso maggiore:")
        )
        for a in self._model.getMaxEdges():
            self._view.txt_result.controls.append(
                ft.Text(f"Arco: {a[0].order_id} -> {a[1].order_id} - Peso: {a[2]}"))
        self.fillDDNodes()
        self._view._ddNode.disabled=False
        self._view._btnCerca.disabled=False
        self._view._btnRicorsione.disabled = False
        self._view.update_page()

    def handleCerca(self, e):
        if self._model.getNNodes()==0:
            self._view.txt_result.controls.append(
                ft.Text(f"Creare prima il grafo!", color="red"))
            self._view.update_page()
            return
        if self._order is None:
            self._view.txt_result.controls.append(
                ft.Text(f"Selezionare nodo di partenza!", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino più lungo partendo dall'ordine {self._order}:"))
        for n in self._model.getMaxPath(self._order):
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()

    def handleRicorsione(self, e):
        if self._model.getNNodes() == 0:
            self._view.txt_result.controls.append(
                ft.Text(f"Creare prima il grafo!", color="red"))
            self._view.update_page()
            return
        if self._order is None:
            self._view.txt_result.controls.append(
                ft.Text(f"Selezionare nodo di partenza!", color="red"))
            self._view.update_page()
            return
        cammino, peso=self._model.getBestPath(self._order)
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino migliore partendo dall'ordine {self._order} (peso {peso}):"))
        for n in cammino:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()

    def fillDDStores(self):
        self._view._ddStore.options.clear()
        stores=self._model.getAllStores()
        storesOpt=list(map(lambda x: ft.dropdown.Option(text=x.store_name,
                                                        key=x.store_id,
                                                        data=x,
                                                        on_click=self.readDDStore), stores))
        self._view._ddStore.options=storesOpt
        self._view.update_page()

    def readDDStore(self, e):
        self._store=e.control.data

    def fillDDNodes(self):
        self._view._ddNode.options.clear()
        nodi=self._model.getNodes()
        nodiOpt=list(map(lambda x: ft.dropdown.Option(text=x.order_id,
                                                      data=x,
                                                      on_click=self.readDDOrder), nodi))
        self._view._ddNode.options=nodiOpt
        self._view.update_page()

    def readDDOrder(self, e):
        self._order=e.control.data