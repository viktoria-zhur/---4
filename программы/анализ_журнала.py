from datetime import datetime,timedelta
DOC=["192.0.2.10","198.51.100.20","203.0.113.7","203.0.113.44"]
def создать_журнал():
 rows=[]; base=datetime(2026,11,19,9)
 for i in range(24):rows.append({"время":(base+timedelta(minutes=3*i)).isoformat(),"назначение":DOC[i%4],"протокол":"HTTPS" if i%3 else "DNS","исходящий_байт":1200+(i%5)*350,"процесс":"browser.exe","проверка":"успешна"})
 rows[17]["исходящий_байт"]=85000000; rows[20]["процесс"]="unknown-helper.exe"; rows[21]["назначение"]="203.0.113.99"; return rows
def анализировать_журнал(rows):
 out=[]
 for r in rows:
  f=[]
  if r.get("исходящий_байт",0)>10000000:f.append("необычно большой исходящий объём")
  if r.get("процесс")=="unknown-helper.exe":f.append("новый/неизвестный процесс")
  if r.get("назначение") not in DOC:f.append("неизвестный узел")
  if f:out.append({"событие":r,"признаки":f,"оценка":"требует проверки; не доказательство атаки"})
 return {"всего_событий":len(rows),"подозрительные":out}
