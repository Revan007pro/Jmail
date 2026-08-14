import imaplib
import email
from email.message import EmailMessage
from email.header import decode_header
import smtplib
import flet as ft
from email.policy import default


ima_servidor="imap.gmail.com"
usuario_save:str=""
password_save:str=""

def leer_correos(usuario,password):
    global usuario_save, password_save
    try:
        usuario_save=usuario
        password_save=password
        mail=imaplib.IMAP4_SSL(ima_servidor)
        mail.login(usuario_save,password_save) # lo envia como parametro el from
        mail.select("inbox")

        status, messenger = mail.search(None,"X-GM-RAW",'"category:primary is:inbox"')
        mail_ids=messenger[0].split()

        ultimos_correos = mail_ids[-15:] if len(mail_ids) >= 15 else mail_ids

        lista_correo=[]

        for i in reversed(ultimos_correos):
            status,msg_data=mail.fetch(i, "(RFC822)")
            for j in msg_data:
                if not isinstance(j,tuple):
                    continue
                if isinstance(j,tuple):
                    msg=email.message_from_bytes(j[1],policy=default)
                    remitente=msg.get("From")
                    enviado=msg.get("To")
                    fecha=msg.get("Date")
                    asun= msg.get("Subject")
                    body_part = msg.get_body(preferencelist=('plain', 'html'))
                    cuerpo = body_part.get_content() if body_part else ""
                    if asun:
                        subject, encoding = decode_header(asun)[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8", errors="ignore")
                    else:
                        subject = "(Sin asunto)"


                    lista_correo.append({
                        "id": i.decode(),
                        "remitente":remitente,
                        "fecha": fecha,
                        "asunto": subject,
                        "Sent":enviado,
                        "Body":cuerpo
                    })
        
        mail.logout()

        return {"exito": True, "datos": lista_correo}
        
        #return requests.status_codes(status.).body(lista_correo)
    except Exception as e:
        print(f"Error en leer_correos: {e}")
        return {
            "exito": False,
            "datos": [],
            "error": str(e)
        }

async def mensaje_enviar(correo:str,asunto:str,cuerpo:str,mensaje,page):

    prefs = ft.SharedPreferences()
    usuario_guardado = await prefs.get("usuario_guardado")
    pass_guardada= await prefs.get("pass_guardada") #nota acepta la credencia guardada
    try:
        email_mensaje=EmailMessage()
        email_mensaje.set_content(cuerpo.value or "" ) 
        email_mensaje["Subject"]=asunto.value or ""
        email_mensaje["To"]=correo.value or ""
        email_mensaje["From"]=usuario_guardado
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as e:
            e.login(usuario_guardado,pass_guardada)
            e.send_message(email_mensaje)
            mensaje.value = "mensaje enviado correctamente"
            mensaje.color = ft.Colors.GREEN
            correo.value = ""
            asunto.value = ""
            cuerpo.value = ""
            page.update()
            
    except Exception as err:
        print(f"el error es: {err}")
        mensaje.value="error enviando el correo"


def file_enviados():
    try:
        mail=imaplib.IMAP4_SSL(ima_servidor)
        mail.login(usuario_save,password_save)
        mail.select('"[Gmail]/Enviados"')

        #status, messenger = mail.search(None,"X-GM-RAW",'"category:primary is:inbox"')
        status, messenger = mail.search(None, "ALL")
        mail_ids=messenger[0].split()

        ultimos_correos = mail_ids[-15:] if len(mail_ids) >= 15 else mail_ids

        lista_correo=[]

        for i in reversed(ultimos_correos):
            status, msg_data=mail.fetch(i, "(RFC822)")
            for j in msg_data:
                if not isinstance(j,tuple):
                    continue

                msg = email.message_from_bytes(j[1], policy=default)

                destino=msg.get("To")
                asun=msg.get("Subject")
                fech=msg.get("Date")

                if asun:
                    subject,encoding=decode_header(asun)[0]
                    if isinstance(subject,bytes):
                        subject = subject.decode(encoding or "utf-8", errors="ignore")
                    else:
                        subject="(Sin Asunto)"


                body_part = msg.get_body(preferencelist=('plain', 'html'))
                cuerpo = body_part.get_content() if body_part else ""

                lista_correo.append({
                    "destino":destino,
                    "asunto":asun,
                    "fecha": fech,
                    "Body":cuerpo
                })
        mail.logout
        return {"datos":lista_correo}
    except Exception as err:
        print(f"error al traer los correos enviados: {err}")


def file_spam():
    try:
        mail=imaplib.IMAP4_SSL(ima_servidor)
        mail.login(usuario_save,password_save)
        mail.select('"[Gmail]/Spam"')

        #status, messenger = mail.search(None,"X-GM-RAW",'"category:primary is:inbox"')
        status, messenger = mail.search(None, "ALL")
        mail_ids=messenger[0].split()

        ultimos_correos = mail_ids[-15:] if len(mail_ids) >= 15 else mail_ids

        lista_correo=[]

        for i in reversed(ultimos_correos):
            status, msg_data=mail.fetch(i, "(RFC822)")
            for j in msg_data:
                if not isinstance(j,tuple):
                    continue

                msg = email.message_from_bytes(j[1], policy=default)

                destino=msg.get("To")
                asun=msg.get("Subject")
                fech=msg.get("Date")
                fulano=msg.get("From")

                if asun:
                    subject,encoding=decode_header(asun)[0]
                    if isinstance(subject,bytes):
                        subject = subject.decode(encoding or "utf-8", errors="ignore")
                    else:
                        subject="(Sin Asunto)"


                body_part = msg.get_body(preferencelist=('plain', 'html'))
                cuerpo = body_part.get_content() if body_part else ""

                lista_correo.append({
                    "destino":destino,
                    "asunto":asun,
                    "fecha": fech,
                    "Body":cuerpo,
                    "de_parte":fulano
                })
        mail.logout
        return {"datos":lista_correo}
    except Exception as err:
        print(f"error al traer los correos enviados: {err}")




def file_borradores():
    try:
        mail=imaplib.IMAP4_SSL(ima_servidor)
        mail.login(usuario_save,password_save)
        mail.select('"[Gmail]/Borradores"')

        #status, messenger = mail.search(None,"X-GM-RAW",'"category:primary is:inbox"')
        status, messenger = mail.search(None, "ALL")
        mail_ids=messenger[0].split()

        ultimos_correos = mail_ids[-15:] if len(mail_ids) >= 15 else mail_ids

        lista_correo=[]

        for i in reversed(ultimos_correos):
            status, msg_data=mail.fetch(i, "(RFC822)")
            for j in msg_data:
                if not isinstance(j,tuple):
                    continue

                msg = email.message_from_bytes(j[1], policy=default)

                destino=msg.get("To")
                asun=msg.get("Subject")
                fech=msg.get("Date")
                fulano=msg.get("From")

                if asun:
                    subject,encoding=decode_header(asun)[0]
                    if isinstance(subject,bytes):
                        subject = subject.decode(encoding or "utf-8", errors="ignore")
                    else:
                        subject="(Sin Asunto)"


                body_part = msg.get_body(preferencelist=('plain', 'html'))
                cuerpo = body_part.get_content() if body_part else ""

                lista_correo.append({
                    "destino":destino,
                    "asunto":asun,
                    "fecha": fech,
                    "Body":cuerpo,
                    "de_parte":fulano
                })
        mail.logout
        return {"datos":lista_correo}
    except Exception as err:
        print(f"error al traer los correos enviados: {err}")

















""" @app.get("/correos")
def get_correos_api():
    resultado = leer_correos()
    if "error" in resultado:
        raise HTTPException(status_code=500, detail=f"error de conexion: {resultado['error']}")
    return resultado


    nota solo cuando se tenga un servidor dedicado
        
 """
            




