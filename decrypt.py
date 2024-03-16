import os
import ctypes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import nacl

class Decrypt(object):                                     
    def __init__(self, Target, BoxM):     
        self.Target = Target          
        self.BoxM = BoxM            

    def decrypt_file(self):
        DeFileN = self.Target.strip(".locked") 
        EnFileN = self.Target
        with open(EnFileN, "rb") as File:
            Date = File.read()
        Decrypted = self.BoxM.decrypt(Date)
        with open(DeFileN, "wb") as File:
            File.write(Decrypted)
        os.remove(EnFileN)

User = os.getlogin()
encrypted_key_file = "C:/Users/"+User+"/appdata/local/temp/encrypted_key.txt"
key_file = input('Enter the path to private key file : ')
hexed_key = open(encrypted_key_file, "rb").read()
private_key = RSA.import_key(open(key_file).read())
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
                    Decrypt(FilePath, box).decrypt_file()             

ctypes.windll.user32.SystemParametersInfoW(20, 0, f'C:\\Users\\{User}\\wallpaper.jpg', 3)
os.remove('private.pem') 
