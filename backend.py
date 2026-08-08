import imaplib
import email
from email.header import decode_header
#import smtplib

#from fastapi import FastAPI, HTTPException

#app=FastAPI()

ima_servidor="imap.gmail.com"


def leer_correos(usuario: str,password:str):
    try:
        mail=imaplib.IMAP4_SSL(ima_servidor)
        mail.login(usuario,password) # lo envia como parametro el from
        mail.select("inbox")

        #status,messenger=mail.search(None,"ALL") trae todo los correo
        #status,messenger = mail.search(None, "X-GM-RAW", '"category:primary is:inbox"') # solo trae la vandeja principal
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
                    msg=email.message_from_bytes(j[1])
                    remitente=msg.get("From")
                    fecha=msg.get("Date")
                    asun= msg.get("Subject")
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
                        "asunto": subject
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

""" @app.get("/correos")
def get_correos_api():
    resultado = leer_correos()
    if "error" in resultado:
        raise HTTPException(status_code=500, detail=f"error de conexion: {resultado['error']}")
    return resultado


    nota solo cuando se tenga un servidor dedicado
        
 """
            
















""" @app.get("/correos")
def get_correos_api():
    resultado = leer_correos()
    if "error" in resultado:
        raise HTTPException(status_code=500, detail=f"error de conexion: {resultado['error']}")
    return resultado


    nota solo cuando se tenga un servidor dedicado
        
 """
            




