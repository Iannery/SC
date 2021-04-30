import math
import json
import random
import time
import hashlib
import base64
import sympy
import sys
sys.setrecursionlimit(1000000)
data = {}
data['debug']   = []
data['public']  = []
data['private'] = []
rsakey = 'Mpk7gvtqIADk7O8a6eqS5Fk6ARPAqXEWyewFa+8qiUOUwIiFqfWbFRD7JjMqwtY0tO6Os7c7GjbpNJ9M5OEXZPVA+Qw/CqhD7GUzMC5s0YjN5aJ1GuTa2+373NpGJaHsq9OTKc/ILQ/U8ap8DaZ5NgueoWk5gTXKZbDOjxF0AHSfJQFwbv0XCFHCOe8Lmw8FkBzQQddIkVVANwPvakw6k/vul1fwQTNmACZ84ZAFq2M='


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
    # e = random.randrange(1, phi)
    # gcd, _, _ = euclideanExtendedGCD(e, phi)
    # while gcd != 1:
    #     print(".", end="",flush=True)
    #     time.sleep(0.01)
    #     e = random.randrange(1, phi)
    #     gcd, _, _ = euclideanExtendedGCD(e, phi)
    e = 65537 #common value for e (https://www.johndcook.com/blog/2018/12/12/rsa-exponent/)

    print("\nDone")
    print("Calculating valid \"d\" value...")
    _, d, _ = euclideanExtendedGCD(e, phi)
    # d = modInv(e, phi)
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

def sign(message):
    prvt_key = json.load(open('private.json', 'r'))
    p = prvt_key['p']['value']
    q = prvt_key['q']['value']
    d = prvt_key['d']['value']
    n = p * q
    sha3 = hashlib.sha3_256()
    message_bytes = message.encode('ascii')

    sha3.update(message_bytes)
    cypher = sha3.digest()
    hexcypher = sha3.hexdigest()
    deccypher = int(hexcypher, 16)

    signature = pow(deccypher,d,n)

    return signature


def verify(message, signature):
    pblc_key = json.load(open('public.json', 'r'))
    n = pblc_key['n']['value']
    e = pblc_key['e']['value']

    sha3 = hashlib.sha3_256()
    message_bytes = message.encode('ascii')
    sha3.update(message_bytes)
    hexcypher = sha3.hexdigest()
    deccypher = int(hexcypher, 16)

    if (deccypher == pow(signature, e, n)):
        print("Valid signature!")
    else:
        print("Invalid signature!")

# genKey()
# jsonDump()
msg = "attack now"
sigature = sign(msg)
verify(msg, sigature)
