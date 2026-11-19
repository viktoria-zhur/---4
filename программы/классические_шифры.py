"""Учебные классические шифры. Не использовать для защиты реальных данных."""
from данные.параметры_алгоритмов import АЛФАВИТЫ, ПОЛИБИЙ_АЛФАВИТ


def _r(a, o, s, res, k, status="успешно", note=""):
    return {"алгоритм": a, "операция": o, "исходное_сообщение": s,
            "результат": res, "ключ_или_параметры": k, "статус": status, "пояснение": note}


def _shift(t, k, alpha, dec=False):
    if not isinstance(t, str) or not t:
        return _r("Цезарь", "расчёт", t, None, k, "ошибка", "Текст должен быть непустой строкой")
    if not isinstance(k, int) or isinstance(k, bool):
        return _r("Цезарь", "расчёт", t, None, k, "ошибка", "Сдвиг должен быть целым числом")
    if alpha not in АЛФАВИТЫ:
        return _r("Цезарь", "расчёт", t, None, k, "ошибка", "Неизвестный алфавит")
    a = АЛФАВИТЫ[alpha]; q = (-k if dec else k) % len(a); out = []
    for c in t:
        u = c.upper()
        if u in a:
            v = a[(a.index(u) + q) % len(a)]
            out.append(v.lower() if c.islower() else v)
        else: out.append(c)
    return _r("Цезарь", "расшифрование" if dec else "шифрование", t, "".join(out), {"сдвиг": k, "алфавит": alpha})


def зашифровать_цезарем(текст, сдвиг, алфавит="латиница"): return _shift(текст, сдвиг, алфавит)
def расшифровать_цезарем(текст, сдвиг, алфавит="латиница"): return _shift(текст, сдвиг, алфавит, True)


def атбаш(текст, алфавит="латиница"):
    if not isinstance(текст, str) or not текст or алфавит not in АЛФАВИТЫ:
        return _r("Атбаш", "преобразование", текст, None, алфавит, "ошибка", "Проверьте текст и алфавит")
    a = АЛФАВИТЫ[алфавит]; out = []
    for c in текст:
        u = c.upper(); v = a[-1-a.index(u)] if u in a else c
        out.append(v.lower() if c.islower() and u in a else v)
    return _r("Атбаш", "преобразование", текст, "".join(out), алфавит)


def полибий_кодировать(текст):
    if not isinstance(текст, str) or not текст:
        return _r("Полибий", "кодирование", текст, None, None, "ошибка", "Текст должен быть непустой строкой")
    out = []
    for c in текст.upper():
        x = "I" if c == "J" else c
        if x in ПОЛИБИЙ_АЛФАВИТ:
            i = ПОЛИБИЙ_АЛФАВИТ.index(x); out.append(f"{i//5+1}{i%5+1}")
        elif c.isspace(): out.append("/")
        else: return _r("Полибий", "кодирование", текст, None, None, "ошибка", f"Символ {c!r} отсутствует в таблице")
    return _r("Полибий", "кодирование", текст, " ".join(out), "5x5; I/J объединены")


def полибий_декодировать(код):
    try:
        if not isinstance(код, str) or not код: raise ValueError
        out = []
        for x in код.split():
            if x == "/": out.append(" "); continue
            if len(x) != 2 or any(c not in "12345" for c in x): raise ValueError
            out.append(ПОЛИБИЙ_АЛФАВИТ[(int(x[0])-1)*5+int(x[1])-1])
        return _r("Полибий", "декодирование", код, "".join(out), None)
    except (ValueError, TypeError): return _r("Полибий", "декодирование", код, None, None, "ошибка", "Некорректные координаты")


def виженер(текст, ключ, алфавит="латиница", decrypt=False):
    if not isinstance(текст, str) or not текст or not isinstance(ключ, str) or not ключ:
        return _r("Виженер", "расчёт", текст, None, ключ, "ошибка", "Текст и ключ должны быть непустыми строками")
    if алфавит not in АЛФАВИТЫ or any(c.upper() not in АЛФАВИТЫ.get(алфавит, "") for c in ключ):
        return _r("Виженер", "расчёт", текст, None, ключ, "ошибка", "Неверный алфавит или ключ")
    a = АЛФАВИТЫ[алфавит]; out=[]; j=0
    for c in текст:
        u=c.upper()
        if u in a:
            q=a.index(ключ[j % len(ключ)].upper()) * (-1 if decrypt else 1)
            v=a[(a.index(u)+q) % len(a)]; out.append(v.lower() if c.islower() else v); j += 1
        else: out.append(c)
    return _r("Виженер", "расшифрование" if decrypt else "шифрование", текст, "".join(out), {"ключ":ключ,"алфавит":алфавит})


def перестановка_блоков(текст, порядок, decrypt=False, длина_исходного=None):
    if not isinstance(текст, str) or not isinstance(порядок, (list, tuple)) or not порядок or sorted(порядок) != list(range(len(порядок))):
        return _r("Перестановка", "расчёт", текст, None, порядок, "ошибка", "Ключ — перестановка индексов 0..n-1")
    n=len(порядок)
    if decrypt:
        if длина_исходного is None or not isinstance(длина_исходного,int) or not 0 <= длина_исходного <= len(текст) or len(текст)%n:
            return _r("Перестановка", "расшифрование", текст, None, порядок, "ошибка", "Для точного восстановления укажите длину исходного текста; шифротекст должен состоять из полных блоков")
        out=[]
        for i in range(0,len(текст),n):
            b=текст[i:i+n]; r=[""]*n
            for j,p in enumerate(порядок): r[p]=b[j]
            out.extend(r)
        result="".join(out)[:длина_исходного]
    else:
        out=[]
        for i in range(0,len(текст),n):
            b=текст[i:i+n].ljust(n," "); out.extend(b[p] for p in порядок)
        result="".join(out)
    return _r("Перестановка", "расшифрование" if decrypt else "шифрование", текст, result,
              {"порядок":list(порядок),"длина_исходного":длина_исходного if decrypt else len(текст)},
              note="Последний блок дополняется пробелами; исходная длина хранится отдельно")


def _playfair_table(key):
    alphabet="ABCDEFGHIKLMNOPQRSTUVWXYZ"; seen=[]
    for c in (key.upper().replace("J","I")+alphabet):
        if c in alphabet and c not in seen: seen.append(c)
    return [seen[i:i+5] for i in range(0,25,5)]


def плейфер_подготовить(текст):
    s="".join(c for c in текст.upper().replace("J","I") if c.isalpha())
    pairs=[]; i=0
    while i<len(s):
        a=s[i]
        if i+1>=len(s): b="X" if a!="X" else "Q"; i+=1
        elif s[i+1]==a: b="X" if a!="X" else "Q"; i+=1
        else: b=s[i+1]; i+=2
        pairs.append(a+b)
    return "".join(pairs)


def плейфер(текст, ключ, decrypt=False):
    if not isinstance(текст,str) or not isinstance(ключ,str) or not ключ or any(not c.isalpha() or ord(c)>127 for c in ключ):
        return _r("Плейфер","расчёт",текст,None,ключ,"ошибка","Нужны текст и латинский ключ")
    table=_playfair_table(ключ); pos={c:(r,col) for r,row in enumerate(table) for col,c in enumerate(row)}
    s="".join(c for c in текст.upper().replace("J","I") if c.isalpha()) if decrypt else плейфер_подготовить(текст)
    if len(s)%2: return _r("Плейфер","расчёт",текст,None,ключ,"ошибка","Для расшифрования требуется чётное число букв")
    out=[]; step=-1 if decrypt else 1
    for i in range(0,len(s),2):
        a,b=s[i],s[i+1]
        if a not in pos or b not in pos: return _r("Плейфер","расчёт",текст,None,ключ,"ошибка","Поддерживаются только латинские буквы")
        ra,ca=pos[a]; rb,cb=pos[b]
        if ra==rb: out.extend((table[ra][(ca+step)%5],table[rb][(cb+step)%5]))
        elif ca==cb: out.extend((table[(ra+step)%5][ca],table[(rb+step)%5][cb]))
        else: out.extend((table[ra][cb],table[rb][ca]))
    return _r("Плейфер","расшифрование" if decrypt else "шифрование",текст,"".join(out),ключ,note="J объединяется с I; при подготовке вставляются X/Q, пробелы и пунктуация удаляются")


def кардано_шифровать(текст, маска):
    """Учебная решётка Кардано: квадратная бинарная маска, поворот на 90°."""
    if not isinstance(текст,str) or not isinstance(маска,list) or not маска or any(not isinstance(row,list) for row in маска):
        return _r("Кардано","шифрование",текст,None,маска,"ошибка","Маска должна быть квадратной матрицей списков")
    n=len(маска)
    if n%2 or any(len(row)!=n for row in маска) or any(v not in (0,1) for row in маска for v in row):
        return _r("Кардано","шифрование",текст,None,маска,"ошибка","Нужна чётная квадратная бинарная маска")
    if len(текст)>n*n:
        return _r("Кардано","шифрование",текст,None,маска,"ошибка",f"Недостаточная ёмкость решётки: максимум {n*n} символов")
    coords=[]; cur=[row[:] for row in маска]
    for _ in range(4):
        coords.extend((r,c) for r in range(n) for c in range(n) if cur[r][c])
        cur=[list(row) for row in zip(*cur[::-1])]
    if len(coords)!=n*n or len(set(coords))!=n*n:
        return _r("Кардано","шифрование",текст,None,маска,"ошибка","Отверстия маски при четырёх поворотах должны покрыть каждую клетку ровно один раз")
    s=текст.ljust(n*n,"X"); grid=[["" for _ in range(n)] for _ in range(n)]
    for (r,c),ch in zip(coords,s): grid[r][c]=ch
    return _r("Кардано","шифрование",текст,"".join("".join(row) for row in grid),{"маска":маска,"размер":n,"длина_исходного":len(текст)},note="Учебная решётка; сообщение дополняется X до размера квадрата")


def кардано_расшифровать(шифротекст, маска, длина_исходного):
    if not isinstance(шифротекст,str) or not isinstance(маска,list) or not маска or not isinstance(длина_исходного,int):
        return _r("Кардано","расшифрование",шифротекст,None,маска,"ошибка","Неверные параметры")
    n=len(маска)
    if n%2 or any(not isinstance(row,list) or len(row)!=n for row in маска) or len(шифротекст)!=n*n or not 0<=длина_исходного<=n*n:
        return _r("Кардано","расшифрование",шифротекст,None,маска,"ошибка","Размер шифротекста, маски или длина не согласованы")
    coords=[]; cur=[row[:] for row in маска]
    for _ in range(4):
        coords.extend((r,c) for r in range(n) for c in range(n) if cur[r][c])
        cur=[list(row) for row in zip(*cur[::-1])]
    if len(coords)!=n*n or len(set(coords))!=n*n:
        return _r("Кардано","расшифрование",шифротекст,None,маска,"ошибка","Некорректная решётка: клетки не покрываются ровно один раз")
    grid=[list(шифротекст[i*n:(i+1)*n]) for i in range(n)]
    result="".join(grid[r][c] for r,c in coords)[:длина_исходного]
    return _r("Кардано","расшифрование",шифротекст,result,{"маска":маска,"длина_исходного":длина_исходного})
