import json
from json.decoder import JSONDecodeError

import structlog
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
import base64
from cryptography.fernet import Fernet


logger = structlog.get_logger(__name__)


def generate_wallet():
    password = input("\nSe necesita una contraseña, escriba una: ")    
    passws = passwd.encode('utf-8') #Se codifica para que lo admita
    #Fernet pide una longitud de 32 bytes, a la contraseña que se usa
    #se añaden tantos '0' hasta completarlo
    while (len(passws) < 32):
        passws = passws + b"0"
        
    pwd = base64.b64encode(passws)
    f = Fernet(pwd)
    private_key = SigningKey.generate()
    public_key = private_key.verify_key
    payload = {
        "private_key": private_key.encode(encoder=HexEncoder).decode(),
        "public_key": "<SI SE QUIERE PERSONALIZAR>" + public_key.encode(encoder=HexEncoder).decode(),
    }
    
    with open("wallet.json", "w") as file:
        json.dump(payload, file)
    logger.info("Genereada una nueva cartera: wallet.json")
    return payload
    #En este momento encripta el contenido, es facil ver la clave privada en
    #este formato
    with open('wallet.json', 'rb') as file:
            original = file.read()
            
    token = f.encrypt(original)
    
    with open('wallet.json', 'wb') as encrypted_file:
        encrypted_file.write(token)
    logger.info("wallet.json ha sido asegurada, por el momento")

try:
    #Desencripta las claves para poder usarlas
    #Primero tiene que desencriptar el contenido para poder leerlo y usarlo, luego vuleve a encriptarlo para que siga estando seguro
    passwd = input("\nSe necesita una contraseña, escriba una: ")
    passws = passwd.encode('utf-8') #Se codifica para que lo admita
    #Fernet pide una longitud de 32 bytes, a la contraseña que se usa
    #se añaden tantos '0' hasta completarlo
    while (len(passws) < 32):
        passws = passws + b"0"
    
    pwd = base64.b64encode(passws)
    f = Fernet(pwd)
    #Se lee elcontenido
    with open('wallet.json', 'rb') as file:
        encrypted = file.read()

    token = f.decrypt(encrypted)

    with open('wallet.json', 'wb') as dec_file:
        dec_file.write(token)
    #Se reescribe en su forma original para que se pueda leer
    with open("wallet.json", "r") as file:
        keys = json.load(file)
    #Se vuelve a encriptar
    with open('wallet.json', 'rb') as file:
            original = file.read()
            
    token = f.encrypt(original)
    
    with open('wallet.json', 'wb') as encrypted_file:
        encrypted_file.write(token)
    logger.info("Keys cargadas desde wallet.json")
except (JSONDecodeError, FileNotFoundError):
    keys = generate_wallet()

PRIVATE_KEY = keys["private_key"]
PUBLIC_KEY = keys["public_key"]
