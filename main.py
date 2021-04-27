
import json
import random

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
    if (x < 0):
        x = x + b
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
    p = random.randrange(2**511, 2**512)
    q = random.randrange(2**511, 2**512)
    print("Calculating valid \"P\" value...", end="")
    while not millerRabin(p, 40):
        print(".", end="")
        p = random.randrange(2**511, 2**512)
    print("\nDone")
    print("Calculating valid \"Q\" value...", end="")
    while not millerRabin(q, 40):
        print(".", end="")
        q = random.randrange(2**511, 2**512)
    print("\nDone")
    if millerRabin(p, 40) and millerRabin(q, 40):
        print("Random P and Q generated.")
    n = p * q
    phi = (p-1)*(q-1)
    
    
    print("Calculating valid \"e\" value...", end="")
    e = random.randrange(1, phi)
    gcd, _, _ = euclideanExtendedGCD(e, phi)
    while gcd != 1:
        print(".", end="")
        e = random.randrange(1, phi)
        gcd, _, _ = euclideanExtendedGCD(e, phi)
    print("\nDone")
    print("Calculating valid \"d\" value...")
    _, d, _ = euclideanExtendedGCD(e, phi)
    if d < 0:
        d = d + phi
    print("\nDone")
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

genKey()
jsonDump()