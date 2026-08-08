import flet as ft
import yaml
from pathlib import Path
from backend import leer_correos
from bandeja import mostrar_bandeja
from token_script import crear_token
import requests

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
    
    version_instalada=""

    async def obtener_ultima_version():
        nonlocal version_instalada
        ver_guardada = await prefs.get("version_instada_guardada")
        version_instalada=ver_guardada
        print("la version en el localStorange es: ",ver_guardada)
        
        try:
            url = "https://api.github.com/repos/Revan007pro/Jmail/releases/latest"
            
            r=requests.get(url,timeout=10)
            r.raise_for_status()
    
            data=r.json()
            version_nube=data["tag_name"]
            apk=data["assets"][0]
            if version_nube !=ver_guardada:
                version_instalada=version_nube      
                print("hay una nueva version")
                texto_actualizar.visible=True
                page.update()
                
                await version_install()
            else:
                print("no hay nueva version")
        except Exception as err:
            print(f"error actualizando la app: {err}")

             
    async def version_install():
        await prefs.set("version_instada_guardada", version_instalada)
        print("la version instalada es: ",version_instalada)

    def actualizar():
        print("actualizando")

    texto_actualizar=ft.TextButton(
        "Hay una nueva version desea actualizar",
        visible=False,
        style=ft.ButtonStyle(color=ft.Colors.CYAN_300),
        on_click=actualizar
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

#ft.app(target=main) deprecada

ft.run(main)