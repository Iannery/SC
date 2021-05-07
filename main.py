import math
import json
import random
import time
import hashlib
import base64
import sympy
import sys
import string

# X, Y = "", ""

sys.setrecursionlimit(1000000)
data = {}
data['debug']   = []
data['public']  = []
data['private'] = []


def millerRabin(n, k):
    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def countTotalBits(n):
    binary = bin(n)[2:]
    return len(binary)

def euclideanExtendedGCD(a, b):
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = euclideanExtendedGCD(b%a, a)

    x = y1 - (b//a) * x1
    y = x1
    return gcd, x, y


def jsonDump():
    with open('debug.json', 'w+') as debugFile:
        json.dump(data['debug'][0], debugFile, indent=4)
    with open('public.json', 'w+') as publicFile:
        json.dump(data['public'][0], publicFile, indent=4)
    with open('private.json', 'w+') as privateFile:
        json.dump(data['private'][0], privateFile, indent=4)

def genKey():
    print("Generating Random Prime Numbers \"P\" and \"Q\"")
    p = sympy.randprime(2**511, 2**512)
    q = sympy.randprime(2**511, 2**512)
    # q = random.randrange(2**511, 2**512)
    # p = random.randrange(2**511, 2**512)
    print(p)
    print("Calculating valid \"P\" value...", end="", flush=True)
    while not millerRabin(p, 40):
        print(".", end="", flush=True)
        time.sleep(0.01)
        p = random.randrange(2**511, 2**512)
    print("\nDone")
    print("Calculating valid \"Q\" value...", end="", flush=True)
    while not millerRabin(q, 40):
        print(".", end="", flush=True)
        time.sleep(0.01)
        q = random.randrange(2**511, 2**512)

    print("\nDone")
    if millerRabin(p, 40) and millerRabin(q, 40):
        print("Random P and Q generated.")
    n = p * q
    phi = (p-1)*(q-1)



    print("Calculating valid \"e\" value...", end="", flush=True)
    e = 65537

    print("\nDone")
    print("Calculating valid \"d\" value...")
    _, d, _ = euclideanExtendedGCD(e, phi)
    if d < 0:
        d = (d + phi) % phi
    print("Done")

    data['debug'].append({
        'p' : {
            'value' : p,
            'length' : countTotalBits(p)
        },
        'q' : {
            'value' : q,
            'length' : countTotalBits(q)
        },
        'n' : {
            'value' : n,
            'length' : countTotalBits(n)
        },
        'phi' : {
            'value' : phi,
        },
        'e' : {
            'value' : e,
        },
        'd' : {
            'value' : d,
        },
    })
    data['public'].append({
        'n' : {
            'value' : n,
        },
        'e' : {
            'value' : e,
        },
    })
    data['private'].append({
        'p' : {
            'value' : p,
        },
        'q' : {
            'value' : q,
        },
        'd' : {
            'value' : d,
        },
    })

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
    msg_hash_padd = padded(msg_hash, r, t)

    #pega o resultado do padding e transforma em inteiro
    cypher = int(msg_hash_padd, 16)

    signature = pow(cypher,d,n)

    return signature, msg_hash_padd

def xor(xs, ys):
    return "".join(chr(ord(x)^ord(y)) for x, y in zip(xs, ys))

def gen_random_str(length = 8): # k0
    result = ''.join((random.choice(string.ascii_letters) for x in range(length)))
    return result

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

def unpadded(msg_padded):
    Y = msg_padded[-8:]
    X = msg_padded[:-8]

    g = hashlib.sha3_256(X.encode('ascii')).hexdigest()
    r = xor(Y, g)
    h = hashlib.sha3_256(r.encode('ascii')).hexdigest()

    msg_unpadded = xor(X, h)
    return msg_unpadded



def verify(msg, signature):
    pblc_key = json.load(open('public.json', 'r'))
    n = pblc_key['n']['value']
    e = pblc_key['e']['value']

    #para comparar ao final
    correct_hash = hashlib.sha3_256(msg.encode("ascii")).hexdigest()

    #desfaz o rsa
    decrpt_int = pow(signature, e, n)
    #transforma de numero de volta para bytes
    msg_padded = int(decrpt_int, 16)

    #desfaz o padding
    msg_hash = unpadded(msg_padded)

    if (correct_hash == msg_hash):
        print("Valid signature!")
    else:
        print("Invalid signature!")

# genKey()
# jsonDump()
msg = "attack now"
sigature, msg = sign(msg)
verify(msg, sigature)
