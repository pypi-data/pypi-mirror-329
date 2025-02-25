import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

# Segmentation encryption
def encrypt(data,public_key):
    data = data.encode()
    try:
        public_key=RSA.import_key(public_key)
        cipher_rsa = PKCS1_v1_5.new(public_key)
        res = []
        for i in range(0, len(data), 64):
            enc_tmp = cipher_rsa.encrypt(data[i : i + 64])
            res.append(enc_tmp)
        cipher_text = b"".join(res)
    except Exception as e:
        print(e)
    else:
        return base64.b64encode(cipher_text).decode()