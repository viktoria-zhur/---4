def создать_пару_ключей():
 from cryptography.hazmat.primitives.asymmetric import rsa
 p=rsa.generate_private_key(public_exponent=65537,key_size=2048); return p,p.public_key()
def подписать_документ(документ,закрытый_ключ):
 from cryptography.hazmat.primitives import hashes
 from cryptography.hazmat.primitives.asymmetric import padding
 d=документ.encode() if isinstance(документ,str) else bytes(документ); return закрытый_ключ.sign(d,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
def проверить_подпись(документ,подпись,открытый_ключ):
 from cryptography.hazmat.primitives import hashes
 from cryptography.hazmat.primitives.asymmetric import padding
 try:
  d=документ.encode() if isinstance(документ,str) else bytes(документ); открытый_ключ.verify(подпись,d,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256()); return {"статус":"действительна","пояснение":"Криптографическая проверка успешна; сертификат отдельно"}
 except Exception:return {"статус":"недействительна","пояснение":"Подпись не подтверждена"}
