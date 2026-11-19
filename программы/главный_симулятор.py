"""Точка входа учебного комплекса CryptoLab."""
import argparse, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from данные.документы_для_подписи import ДОКУМЕНТЫ
from программы.классические_шифры import зашифровать_цезарем, расшифровать_цезарем, плейфер, кардано_шифровать, кардано_расшифровать
from программы.криптоанализ import перебор_цезаря
from программы.стеганография import встроить_lsb, извлечь_lsb
from программы.современные_примитивы import вычислить_хеш, проверить_целостность
from программы.электронная_подпись import создать_пару_ключей, подписать_документ, проверить_подпись
from программы.tls_модель import учебный_tls_сеанс
from программы.анализ_журнала import создать_журнал, анализировать_журнал
from программы.инциденты import ИНЦИДЕНТЫ
from программы.контрольные_дефекты import выполнить_контрольные_дефекты
O=ROOT/"отчёты"; O.mkdir(exist_ok=True)
def save(name, content): (O/name).write_text(content,encoding="utf-8")
def классика():
    t="ВСТРЕЧА УЧЕБНОЙ ГРУППЫ В ДЕСЯТЬ ЧАСОВ"; e=зашифровать_цезарем(t,3,"русский"); d=расшифровать_цезарем(e["результат"],3,"русский")
    play=плейфер("HIDE THE GOLD","MONARCHY"); mask=[[1,1,1,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]]; card=кардано_шифровать("HELLO CRYPTO LAB",mask); card_dec=кардано_расшифровать(card["результат"],mask,16)
    s=(f"Цезарь\nОткрытый текст: {t}\nКлюч: 3\nШифротекст: {e['результат']}\nРасшифрование: {d['результат']}\n\n"
       f"Плейфер (подготовка убирает пробелы, J=I): {play['результат']}\nКардано: {card['результат']}\nКардано, восстановление: {card_dec['результат']}\n")
    save("отчёт_классические_шифры.txt",s); print(s)
def анализ():
    c=зашифровать_цезарем("THE QUICK BROWN FOX",7)["результат"]; s="\n".join(f"{x['ключ']}: {x['вариант']} | оценка {x['оценка']}" for x in перебор_цезаря(c)); save("отчёт_криптоанализа.txt",s); print(s)
def стего():
    m="Скрытое учебное сообщение"; p=встроить_lsb([120]*1000,m); s=f"Исходное: {m}\nИзвлечено: {извлечь_lsb(p)}\nLSB не обеспечивает шифрование и криптографическую целостность.\n"; save("отчёт_стеганография.txt",s); print(s)
def хеш():
    d=ДОКУМЕНТЫ["DOC-001"]; h=вычислить_хеш(d); s=f"SHA-256: {h}\nОригинал: {проверить_целостность(d,h)}\nИзменён: {проверить_целостность(d+'X',h)}\n"; save("отчёт_хеширование.txt",s); print(s)
def подпись():
    d=ДОКУМЕНТЫ["DOC-001"]; pr,pu=создать_пару_ключей(); sig=подписать_документ(d,pr); s=f"Оригинал: {проверить_подпись(d,sig,pu)}\nИзменённый: {проверить_подпись(d+'X',sig,pu)}\nЗакрытый ключ не сохраняется и не выводится.\n"; save("отчёт_электронная_подпись.txt",s); print(s)
def tls():
    s=json.dumps(учебный_tls_сеанс("Тест TLS-модели"),ensure_ascii=False,indent=2); save("отчёт_tls.txt",s); print(s)
def инциденты():
    s="\n\n".join(f"{x['название']} ({x['год']}): {x['тип']}\n{x['роль']}\nМеры: {x['меры']}\nИсточник: {x['источник']}" for x in ИНЦИДЕНТЫ); save("анализ_инцидентов.txt",s)
    log=анализировать_журнал(создать_журнал()); save("отчёт_сетевой_журнал.json",json.dumps(log,ensure_ascii=False,indent=2)); print(s); print(json.dumps(log,ensure_ascii=False,indent=2))
def дефекты():
    r=выполнить_контрольные_дефекты(); save("отчёт_контрольные_дефекты.json",json.dumps(r,ensure_ascii=False,indent=2)); print(json.dumps(r,ensure_ascii=False,indent=2)); return r["пройдено"]==r["всего"]
def тесты():
    from программы.тестирование import CryptoLabTests
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(CryptoLabTests)
    def flatten(items):
        for item in items:
            if isinstance(item, unittest.TestSuite):
                yield from flatten(item)
            else:
                yield item
    test_cases=list(flatten(suite))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    lines=["Результаты автоматических тестов CryptoLab",f"Всего: {result.testsRun}",f"Ошибок: {len(result.errors)}",f"Провалов: {len(result.failures)}","", "Подробный протокол (входные данные / ожидаемый / фактический результат):"]
    failed={t.id():msg for t,msg in result.failures+result.errors}
    catalog={
      "test01_caesar_ru_roundtrip":("ВСТРЕЧА; сдвиг 3; русский алфавит","после расшифрования исходная строка","ВСТРЕЧА"),
      "test02_caesar_en_roundtrip":("Hello!; сдвиг 5","после расшифрования исходная строка","Hello!"),
      "test03_caesar_full_cycle":("ABC; сдвиг 26","ABC","ABC"),
      "test04_caesar_large_shift":("ABC; сдвиг 53","BCD","BCD"),
      "test05_caesar_empty_rejected":("пустой текст","статус ошибка","ошибка"),
      "test06_caesar_bad_key_rejected":("ABC; ключ x","статус ошибка","ошибка"),
      "test07_atbash_en_involution":("CRYPTO; Атбаш дважды","CRYPTO","CRYPTO"),
      "test08_atbash_ru_involution":("ТЕСТ; русский Атбаш дважды","ТЕСТ","ТЕСТ"),
      "test09_polybius_j_i":("JIG; Полибий","IIG (I/J объединены)","IIG"),
      "test10_polybius_invalid_symbol":("HELLO!; Полибий","статус ошибка","ошибка"),
      "test11_vigenere_roundtrip":("ATTACK AT DAWN; ключ LEMON","исходная строка","ATTACK AT DAWN"),
      "test12_vigenere_empty_key":("ABC; пустой ключ","статус ошибка","ошибка"),
      "test13_vigenere_wrong_alphabet":("ABC; ключ КЛЮЧ","статус ошибка","ошибка"),
      "test14_transposition_roundtrip_with_padding":("ABCDEG; ключ [2,0,1]","точное восстановление длины 6","ABCDEG"),
      "test15_transposition_invalid_key":("ABC; ключ [0,0]","статус ошибка","ошибка"),
      "test16_transposition_requires_original_length":("ABC; ключ [1,0]; длина не задана","статус ошибка","ошибка"),
      "test17_playfair_preparation":("BALLOON","подготовка биграмм BALXLOON","BALXLOON"),
      "test18_playfair_roundtrip_prepared":("HIDE THE GOLD; ключ MONARCHY","после расшифрования подготовленный текст","подготовленная строка восстановлена"),
      "test19_playfair_invalid_key":("HELLO; кириллический ключ","статус ошибка","ошибка"),
      "test20_cardano_roundtrip":("HELLO CRYPTO LAB; решётка 4x4","восстановление исходного текста","HELLO CRYPTO LAB"),
      "test21_cardano_invalid_mask":("маска с повторным покрытием","статус ошибка","ошибка"),
      "test_cardano_capacity_rejected":("17 символов; решётка 4x4","статус ошибка из-за ёмкости 16","ошибка"),
      "test22_frequency_count":("AAB","количество букв 3","3"),
      "test23_caesar_bruteforce_count":("ABC","26 вариантов ключа","26"),
      "test24_lsb_utf8_roundtrip":("сообщение тест; массив 500 байт","извлечено тест","тест"),
      "test25_lsb_capacity":("носитель 10 значений; длинное сообщение","ValueError","ValueError"),
      "test26_lsb_corrupt_length_detected":("изменён первый LSB","ValueError при извлечении","ValueError"),
      "test27_sha256_known_vector":("строка abc","известный SHA-256","ba7816bf…15ad"),
      "test28_hash_integrity":("doc и изменённое Doc","True для исходника; False для изменения","True / False"),
      "test29_aes_gcm_roundtrip":("secret; AES-GCM","исходный открытый текст","secret"),
      "test30_aes_gcm_tampering_detected":("изменён последний байт шифротекста","ошибка_аутентификации","ошибка_аутентификации"),
      "test31_signature_valid":("doc; подпись RSA-PSS","действительна","действительна"),
      "test32_signature_modified_document":("подпись doc; проверка Doc","недействительна","недействительна"),
      "test33_signature_wrong_key":("подпись одним ключом; проверка другим","недействительна","недействительна"),
      "test34_log_anomalies":("24 синтетических события журнала","не менее 3 подозрительных событий","обнаружены"),
      "test35_tls_demo":("hello","обмен hello","hello"),
      "test36_three_control_defects":("три негативных сценария","3 из 3 пройдены","3 из 3 пройдены")}
    for test in test_cases:
        short=test.id().split(".")[-1]; inp,expected,actual=catalog.get(short,(short,"проверка без исключений","успешно")); full=test.id()
        if full in failed: actual="ОШИБКА: "+failed[full].splitlines()[-1]
        lines += [f"\n{short}",f"  Вход: {inp}",f"  Ожидалось: {expected}",f"  Фактически: {actual}"]
    save("результаты_тестов.txt","\n".join(lines)); return result.wasSuccessful()
def все():
    for f in (классика,анализ,стего,хеш,подпись,tls,инциденты): f()
    ok_def=дефекты(); ok_tests=тесты()
    summary=f"CryptoLab — итоговый прогон\nКонтрольные дефекты: {'пройдены' if ok_def else 'ошибка'}\nАвтотесты: {'пройдены' if ok_tests else 'ошибка'}\n"
    save("статус_проверки.txt",summary); print(summary)
    if not (ok_def and ok_tests): raise SystemExit(1)
def main():
    acts={"все":все,"классика":классика,"анализ":анализ,"стего":стего,"хеш":хеш,"подпись":подпись,"tls":tls,"инциденты":инциденты,"дефекты":дефекты,"тесты":тесты}
    p=argparse.ArgumentParser(description="Учебный симулятор CryptoLab"); p.add_argument("команда",nargs="?",choices=["меню",*acts],default="меню"); c=p.parse_args().команда
    if c=="меню":
        print("Команды: "+", ".join(acts)+", выход")
        while True:
            try: x=input("CryptoLab> ").strip().lower()
            except (EOFError,KeyboardInterrupt): break
            if x in ("выход","exit"): break
            if x not in acts: print("Неизвестная команда"); continue
            acts[x]()
    else: acts[c]()
if __name__=="__main__": main()
