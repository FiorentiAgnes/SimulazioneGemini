import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Esame 02/11/2022 - iTunes"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT

        self._controller = None

        self._title = None
        self._dd_genere = None
        self._txt_min = None
        self._txt_max = None

        self._btn_crea_grafo = None
        self._btn_playlist = None
        self.txt_result = None

    def load_interface(self):
        self._title = ft.Text("Esame 02/11/2022 iTunes", color="blue", size=24)
        self._page.controls.append(self._title)

        self._dd_genere = ft.Dropdown(label="Genere", hint_text="Seleziona un genere", width=300)
        self._btn_crea_grafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo,
                                                 width=200)

        row1 = ft.Row([self._dd_genere, self._btn_crea_grafo],
                      alignment=ft.MainAxisAlignment.CENTER,
                      vertical_alignment=ft.CrossAxisAlignment.END)
        self._page.controls.append(row1)

        self._txt_min = ft.TextField(label="Min (secondi)", hint_text="Durata minima", width=145)
        self._txt_max = ft.TextField(label="Max (secondi)", hint_text="Durata massima", width=145)
        self._btn_playlist = ft.ElevatedButton(text="La mia playlist", on_click=self._controller.handlePlaylist,
                                               width=200)

        row2 = ft.Row([self._txt_min, self._txt_max, self._btn_playlist],
                      alignment=ft.MainAxisAlignment.CENTER,
                      vertical_alignment=ft.CrossAxisAlignment.END)
        self._page.controls.append(row2)

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
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