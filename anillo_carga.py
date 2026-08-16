
import flet as ft

def anillo_charge(page_or_event):
    page = getattr(page_or_event, "page", page_or_event)
    page.clean()
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.maximized=False
    page.window.full_screem=False

    page.window.width = 400
    page.window.height = 700

    page.window.min_width = 400
    page.window.max_width = 400
    page.window.min_height = 700
    page.window.max_height = 800

    page.window.resizable = True
    
    anillo_carga = ft.ProgressRing(
        width=50,
        height=50,
        color=ft.Colors.GREEN_200,
        )

    cargando = ft.Column(
        controls=[
            anillo_carga,
            ft.Text("Cargando datos...")
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )
    page.add(
        ft.Column(
            [
                cargando
                
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )
        
    page.update()
    #resultado = await asyncio.to_thread(file_enviados)