from datetime import datetime


class Kitap:
    def __init__(self, kitap_id, ad, yazar):
        self.kitap_id = kitap_id
        self.ad = ad
        self.yazar = yazar
        self.durum = 'Müsait'  

    def durum_guncelle(self, yeni_durum):
        self.durum = yeni_durum

    def __str__(self):
        return f"Kitap(ID:{self.kitap_id}, Ad:{self.ad}, Yazar:{self.yazar}, Durum:{self.durum})"


class Uye:
    def __init__(self, uye_id, ad, soyad, telefon):
        self.uye_id = uye_id
        self.ad = ad
        self.soyad = soyad
        self.telefon = telefon

    def __str__(self):
        return f"Üye(ID:{self.uye_id}, Ad:{self.ad} {self.soyad}, Tel:{self.telefon})"


class Odunc:
    def __init__(self, odunc_id, kitap, uye):
        self.odunc_id = odunc_id
        self.kitap = kitap
        self.uye = uye
        self.odunc_tarihi = datetime.now()
        self.iade_tarihi = None

    def odunc_al(self):
        if self.kitap.durum == 'Müsait':
            self.kitap.durum_guncelle('Ödünçte')
            print(f"'{self.kitap.ad}' ödünç alındı.")
            return True
        else:
            print(f"'{self.kitap.ad}' şu anda ödünçte.")
            return False

    def iade_et(self):
        if self.kitap.durum == 'Ödünçte':
            self.kitap.durum_guncelle('Müsait')
            self.iade_tarihi = datetime.now()
            print(f"'{self.kitap.ad}' iade edildi.")
            return True
        else:
            print(f"'{self.kitap.ad}' zaten müsait.")
            return False

    def odunc_bilgisi(self):
        print(f"Ödünç ID: {self.odunc_id}")
        print(f"Kitap: {self.kitap.ad}")
        print(f"Üye: {self.uye.ad} {self.uye.soyad}")
        print(f"Ödünç Tarihi: {self.odunc_tarihi.strftime('%Y-%m-%d %H:%M:%S')}")
        if self.iade_tarihi:
            print(f"İade Tarihi: {self.iade_tarihi.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("Henüz iade edilmedi.")



kitaplar = {}
uyeler = {}
odunc_listesi = []
son_odunc_id = 0



def kitap_ekle():
    kitap_id = int(input("Kitap ID: "))
    if kitap_id in kitaplar:
        print("Bu ID ile kitap zaten var.")
        return
    ad = input("Kitap Adı: ")
    yazar = input("Yazar: ")
    kitaplar[kitap_id] = Kitap(kitap_id, ad, yazar)
    print("Kitap eklendi.")

def uye_ekle():
    uye_id = int(input("Üye ID: "))
    if uye_id in uyeler:
        print("Bu ID ile üye zaten var.")
        return
    ad = input("Üye Adı: ")
    soyad = input("Üye Soyadı: ")
    telefon = input("Telefon: ")
    uyeler[uye_id] = Uye(uye_id, ad, soyad, telefon)
    print("Üye eklendi.")

def kitap_listele():
    if not kitaplar:
        print("Kütüphanede kitap yok.")
        return
    for k in kitaplar.values():
        print(k)

def uye_listele():
    if not uyeler:
        print("Kütüphanede üye yok.")
        return
    for u in uyeler.values():
        print(u)

def odunc_al():
    global son_odunc_id
    kitap_id = int(input("Ödünç alınacak kitap ID: "))
    uye_id = int(input("Ödünç alan üye ID: "))

    if kitap_id not in kitaplar:
        print("Kitap bulunamadı.")
        return
    if uye_id not in uyeler:
        print("Üye bulunamadı.")
        return

    kitap = kitaplar[kitap_id]
    uye = uyeler[uye_id]

    odunc = Odunc(son_odunc_id + 1, kitap, uye)
    if odunc.odunc_al():
        odunc_listesi.append(odunc)
        son_odunc_id += 1

def iade_et():
    kitap_id = int(input("İade edilecek kitap ID: "))
    for odunc in odunc_listesi:
        if odunc.kitap.kitap_id == kitap_id and odunc.iade_tarihi is None:
            if odunc.iade_et():
                return
    print("Bu kitap şu anda ödünç değil ya da bulunamadı.")

def odunclari_listele():
    if not odunc_listesi:
        print("Hiç ödünç işlemi yok.")
        return
    for o in odunc_listesi:
        o.odunc_bilgisi()
        print("------")

def menu():
    print("""
    Kütüphane Yönetim Sistemi
    1. Kitap Ekle
    2. Üye Ekle
    3. Kitapları Listele
    4. Üyeleri Listele
    5. Ödünç Al
    6. İade Et
    7. Ödünç İşlemlerini Listele
    8. Çıkış
    """)

def main():
    while True:
        menu()
        secim = input("Seçiminiz: ")
        if secim == '1':
            kitap_ekle()
        elif secim == '2':
            uye_ekle()
        elif secim == '3':
            kitap_listele()
        elif secim == '4':
            uye_listele()
        elif secim == '5':
            odunc_al()
        elif secim == '6':
            iade_et()
        elif secim == '7':
            odunclari_listele()
        elif secim == '8':
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz seçim. Tekrar deneyin.")

if __name__ == "__main__":
    main()
