from данные.параметры_алгоритмов import АЛФАВИТЫ,РАЗДЕЛИТЕЛИ
def нормализовать_текст(текст,регистр="upper"):
 if not isinstance(текст,str): raise TypeError("Текст должен быть строкой")
 if регистр not in ("upper","lower","keep"): raise ValueError("Неизвестное правило регистра")
 return текст.upper() if регистр=="upper" else текст.lower() if регистр=="lower" else текст
def определить_алфавит(текст):
 letters=[c.upper() for c in текст if c.isalpha()]
 if not letters:return "не определён"
 if all(c in АЛФАВИТЫ["русский"] for c in letters):return "русский"
 if all(c in АЛФАВИТЫ["латиница"] for c in letters):return "латиница"
 return "смешанный/неподдерживаемый"
def проверить_символы(текст,алфавит):
 if алфавит not in АЛФАВИТЫ:return False,["Неизвестный алфавит"]
 allowed=set(АЛФАВИТЫ[алфавит]+АЛФАВИТЫ[алфавит].lower()+РАЗДЕЛИТЕЛИ+"0123456789")
 bad=sorted(set(c for c in текст if c not in allowed)); return not bad,bad
def восстановить_формат(исходный,преобразованные_буквы):
 it=iter(преобразованные_буквы); return "".join(next(it) if c.isalpha() else c for c in исходный)
