import hashlib
import base64

msg = "Oi mundo!"

msg_bytes = msg.encode('utf-8');

sha3 = hashlib.sha3_256()
sha3.update(msg_bytes)
cypher = sha3.digest()
hexcypher = sha3.hexdigest()

print(cypher)
print(hexcypher)
