"""Автоматические тесты CryptoLab (unittest)."""
import unittest
from программы.классические_шифры import *
from программы.криптоанализ import *
from программы.стеганография import *
from программы.современные_примитивы import *
from программы.электронная_подпись import *
from программы.анализ_журнала import *
from программы.контрольные_дефекты import выполнить_контрольные_дефекты

class CryptoLabTests(unittest.TestCase):
    def test01_caesar_ru_roundtrip(self): self.assertEqual(расшифровать_цезарем(зашифровать_цезарем("ВСТРЕЧА",3,"русский")["результат"],3,"русский")["результат"],"ВСТРЕЧА")
    def test02_caesar_en_roundtrip(self): self.assertEqual(расшифровать_цезарем(зашифровать_цезарем("Hello!",5)["результат"],5)["результат"],"Hello!")
    def test03_caesar_full_cycle(self): self.assertEqual(зашифровать_цезарем("ABC",26)["результат"],"ABC")
    def test04_caesar_large_shift(self): self.assertEqual(зашифровать_цезарем("ABC",53)["результат"],"BCD")
    def test05_caesar_empty_rejected(self): self.assertEqual(зашифровать_цезарем("",1)["статус"],"ошибка")
    def test06_caesar_bad_key_rejected(self): self.assertEqual(зашифровать_цезарем("ABC","x")["статус"],"ошибка")
    def test07_atbash_en_involution(self): self.assertEqual(атбаш(атбаш("CRYPTO")["результат"])["результат"],"CRYPTO")
    def test08_atbash_ru_involution(self): self.assertEqual(атбаш(атбаш("ТЕСТ","русский")["результат"],"русский")["результат"],"ТЕСТ")
    def test09_polybius_j_i(self): self.assertEqual(полибий_декодировать(полибий_кодировать("JIG")["результат"])["результат"],"IIG")
    def test10_polybius_invalid_symbol(self): self.assertEqual(полибий_кодировать("HELLO!")["статус"],"ошибка")
    def test11_vigenere_roundtrip(self): self.assertEqual(виженер(виженер("ATTACK AT DAWN","LEMON")["результат"],"LEMON",decrypt=True)["результат"],"ATTACK AT DAWN")
    def test12_vigenere_empty_key(self): self.assertEqual(виженер("ABC","")["статус"],"ошибка")
    def test13_vigenere_wrong_alphabet(self): self.assertEqual(виженер("ABC","КЛЮЧ")["статус"],"ошибка")
    def test14_transposition_roundtrip_with_padding(self):
        src="ABCDEG"; key=[2,0,1]; enc=перестановка_блоков(src,key); dec=перестановка_блоков(enc["результат"],key,True,len(src)); self.assertEqual(dec["результат"],src)
    def test15_transposition_invalid_key(self): self.assertEqual(перестановка_блоков("ABC",[0,0])["статус"],"ошибка")
    def test16_transposition_requires_original_length(self): self.assertEqual(перестановка_блоков("ABC",[1,0],True)["статус"],"ошибка")
    def test17_playfair_preparation(self): self.assertEqual(плейфер_подготовить("BALLOON"),"BALXLOON")
    def test18_playfair_roundtrip_prepared(self):
        src=плейфер_подготовить("HIDE THE GOLD"); enc=плейфер(src,"MONARCHY"); dec=плейфер(enc["результат"],"MONARCHY",True); self.assertEqual(dec["результат"],src)
    def test19_playfair_invalid_key(self): self.assertEqual(плейфер("HELLO","ключ")["статус"],"ошибка")
    def test20_cardano_roundtrip(self):
        mask=[[1,1,1,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]]; src="HELLO CRYPTO LAB"; enc=кардано_шифровать(src,mask); dec=кардано_расшифровать(enc["результат"],mask,len(src)); self.assertEqual(dec["результат"],src)
    def test21_cardano_invalid_mask(self): self.assertEqual(кардано_шифровать("TEXT",[[1,0],[1,0]])["статус"],"ошибка")
    def test_cardano_capacity_rejected(self): self.assertEqual(кардано_шифровать("A"*17,[[1,1,1,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]])["статус"],"ошибка")
    def test22_frequency_count(self): self.assertEqual(частоты("AAB")["количество"],3)
    def test23_caesar_bruteforce_count(self): self.assertEqual(len(перебор_цезаря("ABC")),26)
    def test24_lsb_utf8_roundtrip(self): self.assertEqual(извлечь_lsb(встроить_lsb([100]*500,"тест")),"тест")
    def test25_lsb_capacity(self):
        with self.assertRaises(ValueError): встроить_lsb([0]*10,"слишком длинно")
    def test26_lsb_corrupt_length_detected(self):
        p=встроить_lsb([100]*300,"A"); p[0]^=1
        with self.assertRaises(ValueError): извлечь_lsb(p)
    def test27_sha256_known_vector(self): self.assertEqual(вычислить_хеш("abc"),"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
    def test28_hash_integrity(self):
        h=вычислить_хеш("doc"); self.assertTrue(проверить_целостность("doc",h)); self.assertFalse(проверить_целостность("Doc",h))
    def test29_aes_gcm_roundtrip(self):
        p=aes_gcm_зашифровать("secret"); self.assertEqual(aes_gcm_расшифровать(p["шифротекст"],p["ключ"],p["nonce"])["данные"],"secret")
    def test30_aes_gcm_tampering_detected(self):
        p=aes_gcm_зашифровать("secret"); b=p["шифротекст"][:-1]+bytes([p["шифротекст"][-1]^1]); self.assertEqual(aes_gcm_расшифровать(b,p["ключ"],p["nonce"])["статус"],"ошибка_аутентификации")
    def test31_signature_valid(self):
        pr,pu=создать_пару_ключей(); sig=подписать_документ("doc",pr); self.assertEqual(проверить_подпись("doc",sig,pu)["статус"],"действительна")
    def test32_signature_modified_document(self):
        pr,pu=создать_пару_ключей(); sig=подписать_документ("doc",pr); self.assertEqual(проверить_подпись("Doc",sig,pu)["статус"],"недействительна")
    def test33_signature_wrong_key(self):
        pr,_=создать_пару_ключей(); _,pu=создать_пару_ключей(); sig=подписать_документ("doc",pr); self.assertEqual(проверить_подпись("doc",sig,pu)["статус"],"недействительна")
    def test34_log_anomalies(self): self.assertGreaterEqual(len(анализировать_журнал(создать_журнал())["подозрительные"]),3)
    def test35_tls_demo(self):
        from программы.tls_модель import учебный_tls_сеанс
        self.assertEqual(учебный_tls_сеанс("hello")["обмен"],"hello")
    def test36_three_control_defects(self):
        r=выполнить_контрольные_дефекты(); self.assertEqual(r["всего"],3); self.assertEqual(r["пройдено"],3)

if __name__=="__main__": unittest.main(verbosity=2)
