import flet as ft
#from backend import enviar_correo
from enviar_correo import send_correo
from read_correo import leer_correo




async def mostrar_bandeja(page: ft.Page, datos):
    #page = getattr(page_or_event, "page", page_or_event)
    page.clean()
    page.title = "Bandeja de entrada"
    page.padding = 10
    page.spacing = 0
    page.bgcolor = ft.Colors.BLACK
    prefs = ft.SharedPreferences()
    
    correos_cache = []
    for correo in datos:
        fila = ft.Button(
            visible=True,
            data=correo,
            on_click=lambda e:leer_correo(page,e.control.data),
            content=ft.Row(
                controls=[
                    ft.Checkbox(value=False),
                    ft.Icon(
                        ft.Icons.STAR_BORDER,
                        color=ft.Colors.GREEN_200
                    ),
                    ft.Container(
                        content=ft.Text(correo.get("fecha")),
                        width=50
                    ),
                    ft.Container(
                        content=ft.Text(correo.get("remitente")),
                        width=50
                    ),
                    ft.Container(
                        content=ft.Text(correo.get("asunto")),
                        expand=True
                    )
                ]
            )
        )       
        correos_cache.append(fila)
    lista = ft.Column(controls=correos_cache, scroll=ft.ScrollMode.AUTO, expand=True)

        

    es_movil = page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]
    nave_bar = ft.Container(
        padding=ft.Padding(top=10),
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.DEHAZE,
                    on_click=lambda e: print("Menú click")
                ),
                ft.TextField(
                    prefix_icon=ft.Icons.SEARCH,
                    label="Buscar",
                    on_click=lambda e: print("Buscar click")
                ),
                #ft.CircleAvatar(
                #    content=ft.Image(
                #        #src=
                #        fit=ft.BoxFit.COVER,
                #    ),
                #    radius=18
                #)
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND)
    )
    page.add(ft.Column(controls=[nave_bar]))
    #solo pc
    if not es_movil:
        page.title = "Jmail"
        page.theme_mode = ft.ThemeMode.DARK
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window.width = 800
        page.window.height = 900

        page.window.min_width = 900
        page.window.max_width = 1000
        page.window.min_height = 700
        page.window.max_height = 1000
    
        page.window.resizable = True
    

        
    async def limpiar_storange():
        await prefs.clear()

        print("saliendo")
        page.clean()

        await page.push_route("/main")



    async def cambiar_vista(e):
        botones=["Recibidos","Enviados","Spam","Borradores","Salir"]
        indice=e.control.selected_index
        match indice:
            case 4:
                await limpiar_storange()
            case _:
                print("toque el boton: ",botones[indice])
                await page.push_route(botones[indice])  

      
        

    if es_movil:
        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.INBOX, label="Recibidos"),
                ft.NavigationBarDestination(icon=ft.Icons.SEND, label="Enviados"),
                ft.NavigationBarDestination(icon=ft.Icons.WARNING, label="Spam"),
                ft.NavigationBarDestination(icon=ft.Icons.DRAFTS, label="Borradores"),
                ft.IconButton(icon=ft.Icons.EXIT_TO_APP, tooltip="Salir", on_click=limpiar_storange)
            ],
            on_change=cambiar_vista
        )
        page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.CREATE, tooltip="Redactar",on_click=lambda e: send_correo(e.page,"","")
        )
        page.add(lista)

    else:
        # PC: sidebar lateral
        side_bar = ft.NavigationRail(
            selected_index=0,
            on_change=cambiar_vista,
            #padding=ft.Padding.top(20),
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.INBOX_OUTLINED, label="Recibidos", selected_icon=ft.Icons.INBOX),
                ft.NavigationRailDestination(icon=ft.Icons.SEND, label="Enviados", selected_icon=ft.Icons.SEND_AND_ARCHIVE),
                ft.NavigationRailDestination(icon=ft.Icons.WARNING, label="Spam", selected_icon=ft.Icons.WARNING_AMBER),
                ft.NavigationRailDestination(icon=ft.Icons.DRAFTS, label="Borradores", selected_icon=ft.Icons.DOCUMENT_SCANNER),
                ft.NavigationRailDestination(icon=ft.Icons.EXIT_TO_APP, label="Salir", selected_icon=ft.Icons.CLOSE),

            ],
            trailing=ft.FloatingActionButton(
                icon=ft.Icons.CREATE,
                content=ft.Text("Redactar", color=ft.Colors.WHITE),
                on_click=lambda e: send_correo(e.page,"","")
            )
        )
        
        
        page.add(ft.Row(controls=[side_bar, lista], expand=True, spacing=0))



    page.update()
    

