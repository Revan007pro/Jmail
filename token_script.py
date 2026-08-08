#import bcrypt
import secrets #para generar token

#def crear_hash(password:str):
#    password_hash=bcrypt.hashpw(password.encode(),bcrypt.gensalt)
#    return password_hash

    #token=secrets.token_hex(32)


def crear_token(correo:str,password:str):
    payload=correo,password
    payload=secrets.token_hex(32)
    return payload

