import json
import random as rd

from abc import ABC, abstractmethod
from CryptorLib import EllipticCurve
from CryptorLib import modular_inv

class Cryptor(ABC) :
    def __init__(self) :
        self.public_key = {}
        self.private_key = {}
        self.name = ''

    def save_key(self, file_name):
        with open('{}.pbl'.format(file_name), 'w') as outfile:
            json.dump(self.public_key, outfile)

        with open('{}.prv'.format(file_name), 'w') as outfile:
            json.dump(self.private_key, outfile)

    def load_key(self, file_name):
        with open('{}.pbl'.format(file_name), 'r') as infile:
            self.public_key = json.load(infile)

        with open('{}.prv'.format(file_name), 'r') as infile:
            self.private_key = json.load(infile)

    @abstractmethod
    def encrypt(self, m) :
        pass
    
    @abstractmethod
    def decrypt(self, c):
        pass

class ElGamalCryptor(Cryptor) :
    def __init__(self) :
        rd.seed(None)
        self.name = 'elgamal'
    
    def generate_key(self, p) :
        g, x = rd.randrange(0, p), rd.randrange(1, p - 1)
        y = (g ** x) % p
        self.public_key = {'y': y, 'g': g, 'p': p}
        self.private_key = {'x': x, 'p': p}

    def encrypt(self, m) :
        y, g, p = self.public_key['y'], self.public_key['g'], self.public_key['p']
        
        k = rd.randrange(1, p - 1)
        a = (g ** k) % p
        b = ((y ** k) * m) % p
        return a, b
    
    def decrypt(self, c) :
        x, p = self.private_key['x'], self.private_key['p']
        
        a = c[0]
        b = c[1]
        m = (b * modular_inv(a ** x, p)) % p
        return m

class ECCEGCryptor(Cryptor) :
    def __init__(self) :
        rd.seed(None)
        self.name = 'ecceg'

    def generate_key(self, a, b, p) :
        curve = EllipticCurve(a, b, p)
        basis = curve.get_basis()

        k = rd.randrange(1, p)
        key_point = curve.multiply(k, basis)

        self.public_key = {'a' : curve.a, 'b' : curve.b, 'p' : curve.p, 'basis' : list(basis), 'y' : list(key_point)}
        self.private_key = {'x' : k}

    def encrypt(self, m) :
        a, b, p = self.public_key['a'], self.public_key['b'], self.public_key['p']
        basis = tuple(self.public_key['basis'])
        y = tuple(self.public_key['y'])

        k = rd.randrange(1, p)
        curve = EllipticCurve(a, b, p)
        pc1 = curve.multiply(k, basis)
        pc2 = curve.add(curve.encode(m), curve.multiply(k, y))
        return pc1, pc2

    def decrypt(self, c) :
        pc1 = c[0]
        pc2 = c[1]
        a, b, p = self.public_key['a'], self.public_key['b'], self.public_key['p']
        x = self.private_key['x']
        curve = EllipticCurve(a, b, p)
        return curve.decode(curve.subtract(pc2, curve.multiply(x, pc1)))
