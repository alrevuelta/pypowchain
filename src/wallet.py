import json
from json.decoder import JSONDecodeError

import structlog
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
import base64
from cryptography.fernet import Fernet


logger = structlog.get_logger(__name__)

class Wallet:
    def __init__(self): 
        self.privatekey = ""
        self.publickey = ""
    
    def generate_wallet():
        password = input("\nSe necesita una contraseña, escriba una: ")   #Proposing a change 
        passws = password.encode('utf-8') #It is coded to be supported
        #Fernet asks for a length of 32 bytes, to the password used add as many '0's to complete it.
        while (passws.ljust(32)):
            passws = passws + b"0"
            
        pwd = base64.b64encode(passws)
        f = Fernet(pwd)
        private_key = SigningKey.generate()
        public_key = private_key.verify_key
        payload = {
            "private_key": private_key.encode(encoder=HexEncoder).decode(),
            "public_key": "<PERSONALIZABLE>" + public_key.encode(encoder=HexEncoder).decode(),
        }
        
        with open("wallet.json", "w") as file:  # Propose a change to wallet.json for other method
            json.dump(payload, file)
        logger.info("Genereada una nueva cartera: wallet.json")
        #return payload
        #At this point it encrypts the content, it is easy to see the private key in this format.
        with open('wallet.json', 'rb') as file:
                original = file.read()
                
        token = f.encrypt(original)
        
        with open('wallet.json', 'wb') as encrypted_file: # Propose a change to wallet.json for other method
            encrypted_file.write(token)
        logger.info("wallet.json ha sido asegurada, por el momento")

    def load_wallet():
        print("") #Search for a better solution
    try:
        #Decrypt the keys to be able to use them.
        #First you have to decrypt the content to be able to read and use it.
        #Then re-encrypt it so it remains secure
        passwd = input("\nSe necesita una contraseña, escriba una: ") #Proposing a change 
        passws = passwd.encode('utf-8') #It is coded to be supported
        #Fernet asks for a length of 32 bytes, to the password used add as many '0's to complete it.
        while (passws.ljust(32)):
            passws = passws + b"0"
        
        pwd = base64.b64encode(passws)
        f = Fernet(pwd)
        #The content is read
        with open('wallet.json', 'rb') as file: 
            encrypted = file.read()

        token = f.decrypt(encrypted)

        with open('wallet.json', 'wb') as dec_file:
            dec_file.write(token)
        #It is rewritten in its original form so that it can be read
        with open('wallet.json', 'r') as file:
            keys = json.load(file)
        #Re-encryption
        with open('wallet.json', 'rb') as file:
                original = file.read()
                
        token = f.encrypt(original)

        with open('wallet.json', 'wb') as encrypted_file:
            encrypted_file.write(token)
        
        logger.info("Keys cargadas desde wallet.json")
        privatekey = keys["private_key"]
        publickey = keys["public_key"]

    except (JSONDecodeError, FileNotFoundError):
        keys = generate_wallet()

#wallet.upload_wallet()
#print(wallet.PUBLIC_KEY)
