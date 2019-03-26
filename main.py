import argparse
import Cryptor as cry

from CryptorMachine import CryptorMachine

parser = argparse.ArgumentParser()
parser.add_argument('algorithm', choices=['elgamal' , 'ecceg'], help='algoritma kriptografi yang akan dipakai')

group1 = parser.add_mutually_exclusive_group()
group1.add_argument(
    '--generate', metavar='nama_file',
    help='opsi untuk membangkitkan file kunci, diisi dengan nama file kunci')
group1.add_argument(
    '--load', metavar='nama_file',
    help='opsi untuk memuat file kunci, diisi dengan nama file kunci')

group2 = parser.add_mutually_exclusive_group()
group2.add_argument(
    '--encrypt', nargs=2, metavar=('plain_file', 'cipher_file'),
    help='opsi untuk melakukan enkripsi, diisi dengan nama file input (plain) dan output (cipher)')
group2.add_argument(
    '--decrypt', nargs=2, metavar=('cipher_file', 'plain_file'),
    help='opsi untuk melakukan dekripsi, diisi dengan nama file input (cipher) dan output (plain)')

args = parser.parse_args()

if args.algorithm == 'elgamal' :
    cryptor = cry.ElGamalCryptor()
else :
    cryptor = cry.ECCEGCryptor()

if args.generate :
    if args.algorithm == 'elgamal' :
        p = input('Masukkan sebuah bilangan prima : ')
        cryptor.generate_key(int(p))
    else :
        print('Masukkan parameter kurva eliptik')
        a = input('a : ')
        b = input('b : ')
        p = input('p (bilangan prima) : ')
        cryptor.generate_key(int(a), int(b), int(p))
    file_name = args.generate
    cryptor.save_key(file_name)

if args.load :
    file_name = args.load
    cryptor.load_key(file_name)

if args.encrypt :
    plain_file = args.encrypt[0]
    cipher_file = args.encrypt[1]

    machine = CryptorMachine(cryptor)
    machine.encrypt(plain_file, cipher_file)

if args.decrypt:
    cipher_file = args.decrypt[0]
    plain_file = args.decrypt[1]

    machine = CryptorMachine(cryptor)
    machine.decrypt(cipher_file, plain_file)
