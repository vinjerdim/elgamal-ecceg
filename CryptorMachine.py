import binascii
import Cryptor
import os
import struct
import time

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
        cryptor = self.cryptor
        plain_bytes = self.read_bytes(plain_file)
        cipher_bytes = bytes()

        print('Enkripsi dimulai')
        print('Algoritma:', cryptor.name)
        print()

        start = time.time()
        for m in plain_bytes :
            cipher = cryptor.encrypt(m)
            
            if cryptor.name == 'ecceg' :
                cipher = list(cipher[0]) + list(cipher[1])

            for c in cipher :
                x = struct.pack('>h', c)
                cipher_bytes = cipher_bytes + x
        end = time.time()
        duration = end - start

        print('Plaintext:')
        print(plain_bytes[:30])
        print()

        print('Ciphertext:')
        print(binascii.hexlify(cipher_bytes[:30]))
        print()

        print('Durasi enkripsi:', duration, ' detik')
        print('File plaintext:', plain_file, ', ukuran:',
              os.path.getsize(plain_file), 'bytes')
        self.write_bytes(cipher_file, cipher_bytes)
        print('File ciphertext:', cipher_file, ', ukuran:',
              os.path.getsize(cipher_file), 'bytes')
            
    def decrypt(self, cipher_file, plain_file):
        cryptor = self.cryptor
        cipher_bytes = self.read_bytes(cipher_file)
        plain_bytes = bytes()

        print('Dekripsi dimulai')
        print('Algoritma:', cryptor.name)
        print()

        start = time.time()
        if cryptor.name == 'elgamal' :
            for i in range(0, len(cipher_bytes), 4) :
                c = cipher_bytes[i : i + 4]
                x = struct.unpack('>hh', c)
                plain_bytes = plain_bytes + bytes([cryptor.decrypt(x)])
        else :
            for i in range(0, len(cipher_bytes), 8):
                c = cipher_bytes[i: i + 8]
                x = struct.unpack('>hhhh', c)
                x = ((x[0], x[1]), (x[2], x[3]))
                plain_bytes = plain_bytes + bytes([cryptor.decrypt(x)])
        end = time.time()
        duration = end - start
        
        print('Ciphertext:')
        print(binascii.hexlify(cipher_bytes[:30]))
        print()

        print('Plaintext:')
        print(plain_bytes[:30])
        print()

        print('Durasi dekripsi:', duration, ' detik')
        print('File ciphertext:', cipher_file, ', ukuran:',
              os.path.getsize(cipher_file), 'bytes')
        self.write_bytes(plain_file, plain_bytes)
        print('File plaintext:', plain_file, ', ukuran:',
              os.path.getsize(plain_file), 'bytes')
