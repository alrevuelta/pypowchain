import json
import os
import structlog
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
import base64
from cryptography.fernet import Fernet


logger = structlog.get_logger(__name__)

class Wallet:
    def __init__(self, passw, file): 
        self.privatekey = ""
        self.publickey = ""
        self.wallet_pass = passw
        self.wallet_file = file

    def generate_wallet(self): 
        passws = self.wallet_pass.encode('utf-8') #It is coded to be supported
        #Fernet asks for a length of 32 bytes, to the password used add as many '0's to complete it.
            
        pwd = base64.b64encode(passws.ljust(32))
        f = Fernet(pwd)
        private_key = SigningKey.generate()
        public_key = private_key.verify_key
        payload = {
            "private_key": private_key.encode(encoder=HexEncoder).decode(),
            "public_key": "<CUSTOMIZABLE>" + public_key.encode(encoder=HexEncoder).decode(),
        }
        
        with open(self.wallet_file, "w") as file:
            json.dump(payload, file)
        logger.info("Generated a new wallet: " + self.wallet_file.)
        
        #At this point it encrypts the content, it is easy to see the private key in this format.
        with open(self.wallet_file, 'rb') as file:
                original = file.read()
                
        token = f.encrypt(original)
        
        with open(self.wallet_file, 'wb') as encrypted_file:
            encrypted_file.write(token)
        logger.info(self.wallet_file + " has been secured, for the time being.")

    def load_wallet(self):
        if os.path.exists(self.wallet_file):
            #Decrypt the keys to be able to use them.
            #First you have to decrypt the content to be able to read and use it.
            #Then re-encrypt it so it remains secure
            passws = self.wallet_pass.encode('utf-8') #It is coded to be supported
            #Fernet asks for a length of 32 bytes, to the password used add as many '0's to complete it.

            pwd = base64.b64encode(passws.ljust(32))
            f = Fernet(pwd)
            #The content is read
            with open(self.wallet_file, 'rb') as file:
                    encrypted = file.read()

            token = f.decrypt(encrypted)

             with open(self.wallet_file, 'wb') as dec_file:
                    dec_file.write(token)

            #It is rewritten in its original form so that it can be read
            with open(self.wallet_file, 'r') as file:
                    keys = json.load(file) #Now there is no more?

            #Re-encryption
            with open(self.wallet_file, 'rb') as file:
                        original = file.read()

            token = f.encrypt(original)

            with open(self.wallet_file, 'wb') as encrypted_file:
                    encrypted_file.write(token)

            logger.info("Keys cargadas desde wallet.json")
            privatekey = keys["private_key"]
            publickey = keys["public_key"]

            logger.info("Keys loaded from " + self.wallet_file)
                self.privatekey = keys["private_key"]
                self.publickey = keys["public_key"]
        else:
            Wallet.generate_wallet(self)

