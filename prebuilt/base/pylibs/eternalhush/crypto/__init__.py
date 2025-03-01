import _eternalhush

def ImportRsaKey(path, type):
    return _eternalhush.ctxObj.import_rsa_key(path, type)

def DecryptRsaData(key, encrypted_data):
    return _eternalhush.ctxObj.decrypt_rsa_data(key, encrypted_data)

def EncryptRsaData(key, encrypted_data):
    return _eternalhush.ctxObj.decrypt_rsa_data(key, encrypted_data)
    
def DecryptAesData(key, iv, encrypted_data):
    return _eternalhush.ctxObj.decrypt_aes_data(key, iv, encrypted_data)    
    
def EncryptAesData(key, iv, encrypted_data):
    return _eternalhush.ctxObj.encrypt_aes_data(key, iv, encrypted_data)