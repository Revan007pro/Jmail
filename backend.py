import imaplib
import email
from email.header import decode_header

#from fastapi import FastAPI, HTTPException

#app=FastAPI()

ima_servidor="imap.gmail.com"


def leer_correos(usuario: str,servidor_imap:str):
    try:
        mail=imaplib.IMAP4_SSL(ima_servidor)
        mail.login(usuario,servidor_imap) # lo envia como parametro el from
        mail.select("inbox")

        #status,messenger=mail.search(None,"ALL") trae todo los correo
        status, messenger = mail.search(None, "X-GM-RAW", '"category:primary is:inbox"') # solo trae la vandeja principal
        mail_ids=messenger[0].split()

        ultimos_correos = mail_ids[-15:] if len(mail_ids) >= 15 else mail_ids

        lista_correo=[]

        for i in reversed(ultimos_correos):
            res,msg_data=mail.fetch(i, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part,tuple):
                    msg=email.message_from_bytes(response_part[1])

                    # Corregido "Subjesct" a "Subject"
                    subject_header = msg["Subject"]
                    if subject_header:
                        subject, encoding = decode_header(subject_header)[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8", errors="ignore")
                    else:
                        subject = "(Sin asunto)"

                    remitente=msg.get("From")

                    lista_correo.append({
                        "id": i.decode(),
                        "remitente":remitente,
                        "asunto": subject
                    })
        mail.logout()
        return {"exito": True, "datos": lista_correo}
    except Exception as e:
        print(f"Error en leer_correos: {e}")
        return {"error": str(e)}

""" @app.get("/correos")
def get_correos_api():
    resultado = leer_correos()
    if "error" in resultado:
        raise HTTPException(status_code=500, detail=f"error de conexion: {resultado['error']}")
    return resultado


    nota solo cuando se tenga un servidor dedicado
        
 """
            




