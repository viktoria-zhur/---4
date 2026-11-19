def в_биты(s):
 b=s.encode("utf-8"); return f"{len(b):032b}"+"".join(f"{x:08b}" for x in b)
def встроить_lsb(пиксели,сообщение):
 if not isinstance(сообщение,str):raise TypeError("Сообщение должно быть строкой")
 if any(not isinstance(x,int) or not 0<=x<=255 for x in пиксели):raise ValueError("Значения должны быть 0..255")
 bits=в_биты(сообщение)
 if len(bits)>len(пиксели):raise ValueError(f"Недостаточная ёмкость: требуется {len(bits)}, доступно {len(пиксели)}")
 out=list(пиксели)
 for i,b in enumerate(bits):out[i]=(out[i]&254)|int(b)
 return out
def извлечь_lsb(p):
 if len(p)<32:raise ValueError("Носитель слишком короткий")
 n=int("".join(str(x&1) for x in p[:32]),2); end=32+n*8
 if end>len(p):raise ValueError("Повреждена длина или недостаточно данных")
 bits="".join(str(x&1) for x in p[32:end])
 try:return bytes(int(bits[i:i+8],2) for i in range(0,len(bits),8)).decode("utf-8")
 except Exception as e:raise ValueError("Данные повреждены") from e
