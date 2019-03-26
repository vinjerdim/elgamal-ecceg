import Cryptor
import struct

class CryptorMachine():
    def __init__(self, cryptor) :
        self.cryptor = cryptor

    def read_bytes(self, filename) :
        with open(filename, 'rb') as infile :
            return infile.read()

    def write_bytes(self, filename, message):
        with open(filename, 'wb') as outfile:
            outfile.write(message)

    def encrypt(self, plain_file, cipher_file) :
        plain_bytes = self.read_bytes(plain_file)
        
        if plain_bytes :
            cryptor = self.cryptor
            cipher_bytes = bytes()
            print(cipher_bytes)
            for m in plain_bytes :
                cipher = cryptor.encrypt(m)
                cipher_bytes = cipher_bytes + struct.pack('h', cipher[0])
                cipher_bytes = cipher_bytes + struct.pack('h', cipher[1])
            self.write_bytes(cipher_file, cipher_bytes)
            
    def decrypt(self, plain_file, cipher_file):
        pass

cryptor = Cryptor.ElGamalCryptor()
cryptor.load_key('coba')

machine = CryptorMachine(cryptor)
machine.encrypt('plain/index.php', 'cipher/index.cip')
