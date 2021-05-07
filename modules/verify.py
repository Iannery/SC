import hashlib
import json
import math as m

def xor(xs, ys):
    return "".join(chr(ord(x)^ord(y)) for x, y in zip(xs, ys))


def unpadded(msg_padded):
    X = msg_padded.decode('ascii')[:-8]
    Y = msg_padded.decode('ascii')[-8:]
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

    correct_hash = hashlib.sha3_256(msg.encode('ascii')).hexdigest()
    #desfaz o rsa
    decrpt_int = pow(signature, e, n)
    #transforma de numero de volta para bytes
    number_of_bytes = int(m.ceil(decrpt_int.bit_length() / 8))

    msg_padded = decrpt_int.to_bytes(number_of_bytes, byteorder='big')
    # msg_padded = msg_padded.decode('ascii')

    #desfaz o padding
    msg_hash = unpadded(msg_padded)

    if (correct_hash == msg_hash):
        print("Valid signature!")
    else:
        print("Invalid signature!")
        
class VerifyHandler:
    def __init__(self):
        pass
    def run(self, msg, signature):
        verify(msg, signature)