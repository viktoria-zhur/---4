import hashlib,os
def вычислить_хеш(данные):
 if isinstance(данные,str):данные=данные.encode()
 if not isinstance(данные,(bytes,bytearray)):raise TypeError("Ожидаются str или bytes")
 return hashlib.sha256(данные).hexdigest()
def проверить_целостность(данные,ожидаемый_хеш):return вычислить_хеш(данные)==ожидаемый_хеш
def _aes():
 try:from cryptography.hazmat.primitives.ciphers.aead import AESGCM; return AESGCM
 except ImportError as e:raise RuntimeError("Установите cryptography из requirements.txt") from e
def aes_gcm_зашифровать(данные,ключ=None):
 A=_aes(); key=ключ or A.generate_key(bit_length=256); nonce=os.urandom(12); raw=данные.encode() if isinstance(данные,str) else bytes(данные); return {"шифротекст":A(key).encrypt(nonce,raw,None),"ключ":key,"nonce":nonce}
def aes_gcm_расшифровать(шифротекст,ключ,nonce):
 try:return {"статус":"успешно","данные":_aes()(ключ).decrypt(nonce,шифротекст,None).decode()}
 except Exception:return {"статус":"ошибка_аутентификации","данные":None,"пояснение":"Неверный ключ, шифротекст или тег"}
