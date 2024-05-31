import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._ddA1 = None
        self._btn_adiacenze = None
        self._ddA2 = None
        self._btn_calcola_percorso = None
        self.ddyear = None
        self.ddcountry = None
        self.txtN = None

        self.txt_view = None
        self.btn_graph = None
        self.txt_result = None
        self.txtOut2 = None
        self.txtOut3 = None
        self._text_2 = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("Tema d'esame", color="blue", size=24)
        self._page.controls.append(self._title)

        self.txt_view = ft.TextField(label="Numero canzoni")

        self.btn_graph = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handle_graph)

        row1 = ft.Row([self.txt_view, self.btn_graph],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)
        self._ddA1 = ft.Dropdown(label="Album a1", disabled=True)
        self._btn_adiacenze = ft.ElevatedButton(text="Stampa adiacenze", disabled=True, on_click=self._controller.handle_adiacenze)
        row2 = ft.Row([self._ddA1, self._btn_adiacenze], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)
        self._ddA2 = ft.Dropdown(label="Album a2", disabled=True)
        self._btn_calcola_percorso = ft.ElevatedButton(text="Calcola percorso", disabled=True, on_click=self._controller.handle_calcola_percorso)
        row3 = ft.Row([self._ddA2, self._btn_calcola_percorso], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)
        self._text_2 = ft.TextField(label="Soglia x", disabled=True)
        row4 = ft.Row([self._text_2], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row4)
        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=0, spacing=5, padding=5, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()



    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
