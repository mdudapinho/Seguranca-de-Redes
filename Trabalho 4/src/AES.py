from Crypto.Cipher import AES
import ast
import json

DEBUG = True

def EncryptMsg(msg, k):
    k = k.encode()
    msg = msg.encode()
    cipher = AES.new(k, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg)

    hex_ciphertext = ciphertext.hex()
    hex_tag = tag.hex()
    hex_nonce = nonce.hex()

    enc_msg = {"ciphertext": hex_ciphertext, "tag": hex_tag, "nonce": hex_nonce}
    if(DEBUG):
        print("Encrpting: ", msg, "with key: ", k)
        print("\tciphertext: ", enc_msg["ciphertext"])
        print("\ttag: ", enc_msg["tag"])
        print("\tnonce: ", enc_msg["nonce"])

    return enc_msg
    # return msg

def DecryptMsg(enc_msg, k):
    enc_msg = enc_msg.replace("\'", "\"")
    enc_msg = json.loads(enc_msg)

    k = k.encode()
    
    if(DEBUG):
        print("Decrpting with key: ", k)
        print("\tciphertext: ", enc_msg["ciphertext"])
        print("\ttag: ", enc_msg["tag"])
        print("\tnonce: ", enc_msg["nonce"])

    ciphertext = bytes.fromhex(enc_msg["ciphertext"])
    tag = bytes.fromhex(enc_msg["tag"])
    nonce = bytes.fromhex(enc_msg["nonce"])

    cipher = AES.new(k, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext).decode()
    try:
        cipher.verify(tag)
        return plaintext
    except ValueError:
        return False
