import flet as ft
import yaml
from pathlib import Path
from backend import leer_correos
from bandeja import mostrar_bandeja
from token_script import crear_token
import requests
import flet_permission_handler as fph


async def main(page: ft.Page): #solo debe haber un main.py para que la aplicaion funcione y le diga a flet cual compilar

    prefs = ft.SharedPreferences()
    page.title = "Jmail"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.maximized=False
    page.window.full_screem=False

    page.window.width = 400
    page.window.height = 700

    page.window.min_width = 400
    page.window.max_width = 400
    page.window.min_height = 700
    page.window.max_height = 800

    page.window.resizable = True

    es_movil = page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]
    

    usuario = ft.TextField(
        label="Usuario",
        width=300
    )
    credencial =ft.TextField(
        label="Credencial",
        width=300,
        password=True,
        can_reveal_password=True,
    )

    mensaje = ft.Text(
        "",
        size=16,
        color=ft.Colors.RED,
    )

    check_box=ft.Checkbox(
        label="Desea Guardar el Usuario",
        value=False
    )
    def redireccionar():
        print("redireccionando a: mi pagina")
        #page.launch_url("mi futura pagina.com")
    link = ft.TextButton(
        content=ft.Text(
            "¿Desea Registrarse?",
            color=ft.Colors.BLUE_300,
            size=16,
            weight=ft.FontWeight.BOLD,
        ),
        on_click=redireccionar
    )

    async def route_change(e):

        #page.views.clear()

        if e.route == "/main":
            print("volviendo a main")
            await main(page)

            
        page.update()


    page.on_route_change = route_change


    cuadro_imagen = ft.Container(
        width=150,
        height=150,
        border_radius=15,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Image(
            src="./imagenes_proyecto/Logotipo.webp",
            width=150,
            height=150,
            fit=ft.BoxFit.COVER,
        )
    )
    
    
    version_nube=""
    version_instalada="" #se debe cambiar cuando se suba la aplicacion 
    data_nube=None

    async def set_version():
        await prefs.set("version_instada_guardada", version_instalada)
        print("la version instalada es: ",version_instalada)

    async def obtener_ultima_version():
        ver_guardada = await prefs.get("version_instada_guardada")
        nonlocal version_nube, data_nube
        
        try:
            url = "https://api.github.com/repos/Revan007pro/Jmail/releases/latest"
            
            r=requests.get(url,timeout=10)
            r.raise_for_status()
    
            data_nube=r.json()
            version_nube=data_nube["tag_name"]
            print("la version de la nube es: ",version_nube)
            if version_nube !=ver_guardada:   
                print("hay una nueva version")
                texto_actualizar.visible=True
                page.update()
                
                
            else:
                print("no hay nueva version")
        except Exception as err:
            print(f"error actualizando la app: {err}")


    async def actualizar(e):    
        version_instalada=version_nube
        try:
            if es_movil:
                url = "https://github.com/Revan007pro/Jmail/releases"
                await ft.UrlLauncher().launch_url(url)
            else:
                print("funcion para actualizar en escritorio")

            print("Instalación lanzada. El usuario debe confirmar la instalación.")
        except Exception as err:
            print(f"error actualizando: {err}")
        print("actualizando")
        print("despues de la actualizacion la version es: ",version_instalada)

    texto_actualizar=ft.TextButton(
        "Hay una nueva version desea actualizar",
        visible=False,
        style=ft.ButtonStyle(color=ft.Colors.CYAN_300),
        on_click=lambda e: page.run_task(actualizar, e)
    )

    token_guardado = await prefs.get("mi_token_guardado")
    usuario_guardado = await prefs.get("usuario_guardado")
    pass_guardada = await prefs.get("pass_guardada")


    if token_guardado and usuario_guardado and pass_guardada:
        resultado = leer_correos(usuario=usuario_guardado, password=pass_guardada)
        if resultado["exito"]:
            mostrar_bandeja(page, resultado["datos"])
            return  # ← sale para no renderizar el login
    def guardar_correo_user():
        if check_box.value:
            carpeta = Path(__file__).parent / "save"
            archivo = carpeta / "save_user.yaml"
            with open(archivo,"w",encoding="utf-8") as f:
                yaml.dump(usuario.value,f,allow_unicode=True,sort_keys=False)
    async def guardar_token(resultado):
        correo=usuario.value
        password=credencial.value
        hash_contrasenia=crear_token(correo,password)
        if hash_contrasenia:
            await prefs.set("mi_token_guardado", hash_contrasenia)
            await prefs.set("usuario_guardado", correo)
            await prefs.set("pass_guardada", password)
            print("token guardado:", hash_contrasenia)

    if es_movil:

        #permisos_handler = fph.PermissionHandler()
#
        #async def pedir_permisos_runtime():
        #    status = await permisos_handler.request(
        #        #fph.Permission.MANAGE_EXTERNAL_STORAGE
        #        await permisos_handler.open_app_settings()
        #    )
#
        #    print(f"Permiso de almacenamiento: {status}")
#
        #def cerrar_dialogo(e):
        #    dialogo.open = False
        #    page.update()
#
        #def aceptar_permisos(e):
        #    dialogo.open = False
        #    page.update()
#
        #    # haya pulsado "Sí"
        #    page.run_task(pedir_permisos_runtime)
#
        #dialogo = ft.AlertDialog(
        #    modal=True,
        #    title=ft.Text("Permisos de almacenamiento"),
        #    content=ft.Text(
        #        "Jmail necesita permisos de almacenamiento "
        #        "para poder guardar y acceder a tus archivos."
        #    ),
        #    actions=[
        #        ft.TextButton(
        #            "No",
        #            on_click=cerrar_dialogo
        #        ),
        #        ft.Button(
        #            "Sí",
        #            on_click=aceptar_permisos
        #        ),
        #    ],
        #    actions_alignment=ft.MainAxisAlignment.END,
        #)
#
        #page.overlay.append(dialogo)
#
        #def mostrar_dialogo():
        #    dialogo.open = True
        #    page.update()
#
        #mostrar_dialogo()
#
        #page.update()
        pass


    async def ingresar_usuario(e):
        resultado=leer_correos(
            usuario=usuario.value,
            password=credencial.value #se le pasa al backend como parametro
            )
        if  usuario.value=="" or credencial.value=="":
            mensaje.value="porfavor llenar todos los campos"
            mensaje.color=ft.Colors.RED
            page.update()
            return       
        elif resultado["exito"]:
            page.clean()
            mostrar_bandeja(page,resultado["datos"])
            await guardar_token(resultado)

        else:
            mensaje.value=f"error: {resultado['error']}"
            mensaje.color=ft.Colors.RED
        guardar_correo_user()


    def traer_correo_save():
        file=Path(__file__).parent / "save" / "save_user.yaml"
        if file.exists:
            with open(file,"r",encoding="utf-8") as e:
                usuario.value=yaml.safe_load(e)




    page.update()

    boton = ft.Button(
        content=ft.Text("Ingresar"),
        width=200,
        on_click=ingresar_usuario
    )

    page.add(
        ft.Column(
            [
                cuadro_imagen,
                usuario,
                credencial,
                boton,
                check_box,
                link,
                texto_actualizar,
                mensaje
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )
    traer_correo_save()
    await obtener_ultima_version()
    await set_version()


ft.run(main)