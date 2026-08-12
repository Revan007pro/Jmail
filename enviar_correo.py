import flet as ft
from backend import mensaje_enviar

def send_correo(page_or_event):
    # Obtener el objeto page de forma segura
    page = getattr(page_or_event, "page", page_or_event)

    page.clean()
    page.title = "Enviar Correo"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = ft.Colors.BLACK
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.window.resizable = True

    correo = ft.TextField(
        label="Correo",
        width=300,
        border_color=ft.Colors.BLUE_400,
        focused_border_color=ft.Colors.BLUE_ACCENT,
        prefix_icon=ft.Icons.EMAIL_OUTLINED
    )
    
    asunto = ft.TextField(
        label="Asunto",
        width=300,
        border_color=ft.Colors.BLUE_400,
        focused_border_color=ft.Colors.BLUE_ACCENT,
        prefix_icon=ft.Icons.SUBJECT
    )
    
    cuerpo = ft.TextField(
        label="Cuerpo",
        width=300,
        multiline=True,
        min_lines=5,
        max_lines=8,
        border_color=ft.Colors.BLUE_400,
        focused_border_color=ft.Colors.BLUE_ACCENT,
    )

    # Texto de estado para el backend
    mensaje = ft.Text("", size=14, text_align=ft.TextAlign.CENTER)

    container_botones = ft.Row(
        controls=[
            ft.TextButton(
                "Cancelar",
                on_click=lambda _: page.update()
            ),
            ft.TextButton(
                "Enviar",
                on_click=lambda _:page.run_task(
                    mensaje_enviar,
                    correo,
                    asunto,
                    cuerpo,
                    mensaje,
                    page
                )
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    # Contenedor principal centrado con Shadow Box
    main_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.MAIL_ROUNDED, size=50, color=ft.Colors.BLUE_400),
                ft.Text("Enviar Correo", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                correo,
                asunto,
                cuerpo,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                container_botones,
                mensaje 
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        padding=5,
        bgcolor=ft.Colors.GREY_900,
        border_radius=20,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            offset=ft.Offset(0, 10),
        ),
        width=380, # Ancho del contenedor para que los campos de 300 luzcan centrados
    )

    # Añadir a la página centrado utilizando Row y Column con expand
    page.add(
        ft.Column(
            [
                ft.Row(
                    [main_card],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
    )

    page.update()
