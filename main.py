import flet as ft
import yaml
from pathlib import Path
from backend import leer_correos
from bandeja import mostrar_bandeja

def main(page: ft.Page): #solo debe haber un main.py para que la aplicaion funcione y le diga a flet cual compilar
    page.title = "Jmail"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.resizable=False
    page.window.maximized=False
    page.window.full_screem=False

    page.window.width = 400
    page.window.height = 500

    page.window.min_width = 400
    page.window.max_width = 400
    page.window.min_height = 500
    page.window.max_height = 500

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

    def guardar_correo_user():
        if check_box.value:
            carpeta = Path(__file__).parent / "save"
            archivo = carpeta / "save_user.yaml"
            with open(archivo,"w",encoding="utf-8") as f:
                yaml.dump(usuario.value,f,allow_unicode=True,sort_keys=False)
    
    def ingresar_usuario(e):
        resultado=leer_correos(
            usuario=usuario.value,
            servidor_imap=credencial.value #se le pasa al backend como parametro
        )
        if  usuario.value=="" or credencial.value=="":
            mensaje.value="porfavor llenar todos los campos"
            mensaje.color=ft.Colors.RED
            page.update()
            return       
        if resultado["exito"]:
            mensaje.value="conexion establecida"
            mensaje.color=ft.Colors.GREEN
            page.clean()
            vista_nueva=mostrar_bandeja(page,resultado["datos"])
        else:
            mensaje.value=f"error: {resultado['error']}"
            mensaje.color=ft.Color.RED
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
                mensaje
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )

    traer_correo_save()
#ft.app(target=main) deprecada

ft.run(main)