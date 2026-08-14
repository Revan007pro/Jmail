import flet as ft
from enviar_correo import send_correo

def leer_correo(page_or_event,datos):
    # Obtener el objeto page de forma segura
    page = getattr(page_or_event, "page", page_or_event)

    page.clean()
    page.title = "Leer Correo"
    page.padding = 0
    page.spacing = 0
    page.bgcolor = ft.Colors.BLACK
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.window.resizable = True
    #print("el remitente es: ",datos) 

    es_movil = page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]

    if es_movil:
        def retroceso(e: ft.ViewPopEvent):
            if len(page.views) > 1:
                print("devolviendome")
                page.views.pop()
                page.go(page.views[-1].route)
        page.on_view_pop = retroceso


    correo = ft.TextField(
        label="Correo",
        value=datos.get("remitente"),
        width=300,
        border_color=ft.Colors.BLUE_400,
        focused_border_color=ft.Colors.BLUE_ACCENT,
        prefix_icon=ft.Icons.EMAIL_OUTLINED
    )
    
    asunto = ft.TextField(
        label="Asunto",
        value=datos.get("asunto"),
        width=300,
        border_color=ft.Colors.BLUE_400,
        focused_border_color=ft.Colors.BLUE_ACCENT,
        prefix_icon=ft.Icons.SUBJECT
    )
    
    cuerpo = ft.TextField(
        label="Cuerpo",
        value=datos.get("Body"),
        width=300,
        multiline=True,
        min_lines=5,
        max_lines=8,
        border_color=ft.Colors.BLUE_400,
        focused_border_color=ft.Colors.BLUE_ACCENT,
    )



    container_botones = ft.Row(
        controls=[
            ft.TextButton(
                "Reenviar",
                
            ),
            ft.TextButton(
                "Responder",
                on_click=lambda e: send_correo(e.page,correo.value,asunto.value)
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
