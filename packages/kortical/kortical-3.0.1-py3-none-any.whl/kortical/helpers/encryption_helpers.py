from cryptography.fernet import Fernet
import json


def encrypt(dict, key):
    # Dictionary to encrypted b64
    decrypted_bytes = json.dumps(dict).encode('utf-8')
    encrypted_bytes = Fernet(key).encrypt(decrypted_bytes)
    encrypted_data = encrypted_bytes.decode('utf-8')
    return encrypted_data


def decrypt(encrypted_data, key):
    # Encrypted b64 to dict
    encrypted_bytes = encrypted_data.encode('utf-8')
    decrypted_bytes = Fernet(key).decrypt(encrypted_bytes)
    dict = json.loads(decrypted_bytes.decode('utf-8'))
    return dict
