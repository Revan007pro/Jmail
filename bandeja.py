import flet as ft


def mostrar_bandeja(page: ft.Page,datos):
    page.title="Bandeja de entrada"
    page.padding=0
    page.spacing=0
    page.bgcolor=ft.Colors.BLACK

    coreos_cache=[]

    lista = ft.Column(controls=coreos_cache, scroll=ft.ScrollMode.AUTO, expand=True)

    if page.platform in [ft.PagePlatform.WINDOWS, ft.PagePlatform.LINUX]:
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window.resizable=False
        page.window.maximized=False
        page.window.full_screem=False   
        page.window.width = 1000
        page.window.height = 500    
        page.window.min_width = 400
        page.window.max_width = 400
        page.window.min_height = 500
        page.window.max_height = 500    
        page.window.resizable = True

    elif page.platform in [ft.PagePlatform.ANDROID]:
        page.window.width = 400
        page.window.height = 500
    
        page.window.min_width = 400
        page.window.max_width = 400
        page.window.min_height = 500
        page.window.max_height = 500
    
        page.window.resizable = True

        page.nave_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.INBOX, label="Recibidos"),
                ft.NavigationBarDestination(icon=ft.Icons.SEND, label="Enviados"),
                ft.NavigationBarDestination(icon=ft.Icons.ARCHIVE, label="Archivados"),
                ft.NavigationBarDestination(icon=ft.Icons.ARCHIVE, label="Archivados")
            ]
        )
        page.redactar=ft.FloatingActionButton(
            icon=ft.Icons.CREATE, tooltip="Redactar"
        )

    
    side_bar=ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        #bgcolor=ft.Colors.SURFACE_CONTAINER,
        group_alignment=-1.0, #centra los elementos al final o al principio
        destinations=[
        ft.NavigationRailDestination(
            icon=ft.Icons.INBOX_OUTLINED, 
            label="Recibidos",
            selected_icon=ft.Icons.INBOX, 
        ),
        ft.NavigationBarDestination(
            icon=ft.Icons.SEND,
            label="Enviados",
            selected_icon=ft.Icons.SEND_AND_ARCHIVE #icono cuando se le hace click
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.ARCHIVE,
            label="Archivados",
            selected_icon=ft.Icons.ALL_INBOX #icono cuando se le hace click
            ),
        ft.NavigationRailDestination(
            icon=ft.Icons.DRAFTS,
            label="Borradores",
            selected_icon=ft.Icons.DOCUMENT_SCANNER #icono cuando se le hace click
            ),
        ],
        trailing=ft.FloatingActionButton(
            icon=ft.Icons.CREATE,
            content=ft.Text("Redactar", color=ft.Colors.WHITE),
            #style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_GREY_900),
        )    
    )

    
    for i in datos:
        fila=ft.Row(
            controls=[
                ft.Checkbox(value=False),
                ft.Icon(ft.Icons.STAR_BORDER, color=ft.Colors.GREEN_200),
                ft.Container(
                    content=ft.Text(i.get("id")),
                    expand=True
                ),
                ft.Container(
                    content=ft.Text(i.get("remitente")),
                    expand=True
                    ),
                ft.Container(
                    content=ft.Text(i.get("asunto")),
                    expand=True
                    ),
            
            ]
        )
        coreos_cache.append(fila)
    container=ft.Container(
        #bgcolor=ft.Colors.BLACK,
        content=ft.Column(
            controls=coreos_cache,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )
    )

    

    page.add(
        ft.Row(
            controls=[
                side_bar,
                container
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
        )
    )
    page.update()

