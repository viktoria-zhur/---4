from collections import Counter
from данные.параметры_алгоритмов import АЛФАВИТЫ
from программы.классические_шифры import расшифровать_цезарем
def частоты(текст,алфавит="латиница"):
 a=АЛФАВИТЫ[алфавит]; c=Counter(x.upper() for x in текст if x.upper() in a); n=sum(c.values()); return {"количество":n,"частоты":{x:c[x]/n for x in a} if n else {},"по_убыванию":c.most_common()}
def перебор_цезаря(шифротекст,алфавит="латиница"):
 if алфавит not in АЛФАВИТЫ:return []
 common=set("ETAOINSHRDLU" if алфавит=="латиница" else "ОЕАИНТСРВЛКМДПУЯЫЬГЗБЧЙХЖШЮЦЩЭФЪ"); out=[]
 for k in range(len(АЛФАВИТЫ[алфавит])):
  t=расшифровать_цезарем(шифротекст,k,алфавит)["результат"]; letters=[c.upper() for c in t if c.upper() in АЛФАВИТЫ[алфавит]]
  out.append({"ключ":k,"вариант":t,"оценка":round(sum(c in common for c in letters)/len(letters),3) if letters else 0})
 return out
def пространство_ключей(n=26,m=3,p=5):
 import math
 return {"Цезарь":n-1,"Виженер":n**m,"Перестановка":math.factorial(p)}
