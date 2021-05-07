import hashlib
import json
import random
import string

def gen_random_str(length = 8): # k0
    result = ''.join((random.choice(string.ascii_letters) for x in range(length)))
    return result

def xor(xs, ys):
    return "".join(chr(ord(x)^ord(y)) for x, y in zip(xs, ys))

def padded(msg, r, t):
    #expande msg com k1 zeros ( t = '00000' - k1 vezes)
    msg = msg + t

    #pega a string aleatoria r, transforma em bytes e faz o hash
    h = hashlib.sha3_256(r.encode('ascii')).hexdigest()

    X = xor(msg, h)

    #pega a string X, transforma em bytes e faz o hash
    g = hashlib.sha3_256(X.encode('ascii')).hexdigest()

    Y = xor(r, g)

    msg_padded =  (X + Y).encode('ascii')
    return msg_padded

def sign(msg):
    prvt_key = json.load(open('private.json', 'r'))
    p = prvt_key['p']['value']
    q = prvt_key['q']['value']
    d = prvt_key['d']['value']
    n = p * q

    #pega a mensagem, transforma em bytes e faz o hash
    msg_hash = hashlib.sha3_256(msg.encode('ascii')).hexdigest()

    #pega o hash e faz o padding
    t = '00000000'
    r = gen_random_str()
    # print("MSG_HASH = ", msg_hash)
    msg_hash_padd = padded(msg_hash, r, t)
    # print("MSG_HASH_PADDED = ", msg_hash_padd)
    #pega o resultado do padding e transforma em inteiro
    cypher = int.from_bytes(msg_hash_padd, "big")
    # print("MSG HASH PADDED INT = ", cypher)
    signature = pow(cypher,d,n)

    return signature


class SignHandler:
    def __init__(self):
        pass
    
    def run(self, msg):
        return sign(msg)