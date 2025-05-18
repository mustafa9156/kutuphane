import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

import tkinter as tk
from tkinter import messagebox

USERS = {"admin": "1234", "user": "pass"}

class GirisEkrani(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kütüphane Yönetim Sistemi - Giriş")
        self.geometry("400x350")
        self.configure(bg="#2C3E50")
        self.resizable(False, False)

        self._build_login_ui()

    def _build_login_ui(self):
        label_baslik = tk.Label(self, text="Kütüphane Yönetim Sistemi", fg="white", bg="#2C3E50", font=("Helvetica", 20, "bold"))
        label_baslik.pack(pady=30)

        label_kullanici = tk.Label(self, text="Kullanıcı Adı", fg="white", bg="#2C3E50", font=("Arial", 14))
        label_kullanici.pack(pady=(10, 5))
        self.entry_kullanici = tk.Entry(self, font=("Arial", 14))
        self.entry_kullanici.pack(pady=5, ipadx=10, ipady=5)

        label_sifre = tk.Label(self, text="Şifre", fg="white", bg="#2C3E50", font=("Arial", 14))
        label_sifre.pack(pady=(15, 5))
        self.entry_sifre = tk.Entry(self, show="*", font=("Arial", 14))
        self.entry_sifre.pack(pady=5, ipadx=10, ipady=5)
        self.entry_sifre.bind("<Return>", lambda e: self._giris_yap())

        btn_giris = tk.Button(self, text="Giriş Yap", font=("Arial", 14, "bold"), bg="#27AE60", fg="white",
                              relief="flat", command=self._giris_yap)
        btn_giris.pack(pady=10, ipadx=20, ipady=8)

    def _giris_yap(self):
        kullanici_adi = self.entry_kullanici.get()
        sifre = self.entry_sifre.get()

        if USERS.get(kullanici_adi) == sifre:
            messagebox.showinfo("Başarılı", f"Hoşgeldiniz, {kullanici_adi}!")
            # Burada giriş başarılı sonrası yapılacak işlemler (ana pencere açma vs) yapılabilir
            self.destroy()  # Örneğin pencereyi kapatıyoruz
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış.")
            self.entry_sifre.delete(0, tk.END)

if __name__ == "__main__":
    app = GirisEkrani()
    app.mainloop()


# --- Sınıflar ---

class Kitap:
    def __init__(self, kitap_id, ad, yazar):
        self.kitap_id = kitap_id
        self.ad = ad
        self.yazar = yazar
        self.durum = 'Müsait'

    def durum_guncelle(self, yeni_durum):
        self.durum = yeni_durum

    def __str__(self):
        return f"{self.kitap_id} - {self.ad} ({self.yazar}) [{self.durum}]"

class Uye:
    def __init__(self, uye_id, ad, soyad, telefon):
        self.uye_id = uye_id
        self.ad = ad
        self.soyad = soyad
        self.telefon = telefon

    def __str__(self):
        return f"{self.uye_id} - {self.ad} {self.soyad}"

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
            return True
        else:
            return False

    def iade_et(self):
        if self.kitap.durum == 'Ödünçte':
            self.kitap.durum_guncelle('Müsait')
            self.iade_tarihi = datetime.now()
            return True
        else:
            return False

# --- Veri Yapıları ---
kitaplar = {}
uyeler = {}
odunc_listesi = []

# --- GUI Uygulaması ---
class KutuphaneApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kütüphane Yönetim Sistemi")
        self.geometry("700x500")
        self.son_odunc_id = 0

        self.tab_control = ttk.Notebook(self)
        self.tab_kitap = ttk.Frame(self.tab_control)
        self.tab_uye = ttk.Frame(self.tab_control)
        self.tab_odunc = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_kitap, text='Kitaplar')
        self.tab_control.add(self.tab_uye, text='Üyeler')
        self.tab_control.add(self.tab_odunc, text='Ödünç İşlemleri')

        self.tab_control.pack(expand=1, fill='both')

        self.create_kitap_tab()
        self.create_uye_tab()
        self.create_odunc_tab()

    def create_kitap_tab(self):
        frame = self.tab_kitap
        
        self.kitap_listbox = tk.Listbox(frame, height=15)
        self.kitap_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.kitap_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.kitap_listbox.yview)

        frame_ekle = tk.Frame(frame)
        frame_ekle.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        tk.Label(frame_ekle, text="Kitap ID:").pack()
        self.entry_kitap_id = tk.Entry(frame_ekle)
        self.entry_kitap_id.pack()

        tk.Label(frame_ekle, text="Kitap Adı:").pack()
        self.entry_kitap_ad = tk.Entry(frame_ekle)
        self.entry_kitap_ad.pack()

        tk.Label(frame_ekle, text="Yazar:").pack()
        self.entry_kitap_yazar = tk.Entry(frame_ekle)
        self.entry_kitap_yazar.pack()

        tk.Button(frame_ekle, text="Kitap Ekle", command=self.kitap_ekle).pack(pady=5)
        tk.Button(frame_ekle, text="Kitapları Yenile", command=self.kitaplari_goster).pack()

        self.kitaplari_goster()

    def kitap_ekle(self):
        try:
            kitap_id = int(self.entry_kitap_id.get())
            if kitap_id in kitaplar:
                messagebox.showerror("Hata", "Bu ID ile kitap zaten var.")
                return
            ad = self.entry_kitap_ad.get()
            yazar = self.entry_kitap_yazar.get()
            if not ad or not yazar:
                messagebox.showerror("Hata", "Kitap adı ve yazar boş olamaz.")
                return
            kitaplar[kitap_id] = Kitap(kitap_id, ad, yazar)
            messagebox.showinfo("Başarılı", "Kitap eklendi.")
            self.kitaplari_goster()
        except ValueError:
            messagebox.showerror("Hata", "Kitap ID sayısal olmalıdır.")

    def kitaplari_goster(self):
        self.kitap_listbox.delete(0, tk.END)
        for k in kitaplar.values():
            self.kitap_listbox.insert(tk.END, str(k))

    def create_uye_tab(self):
        frame = self.tab_uye
        
        self.uye_listbox = tk.Listbox(frame, height=15)
        self.uye_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.uye_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.uye_listbox.yview)

        frame_ekle = tk.Frame(frame)
        frame_ekle.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        tk.Label(frame_ekle, text="Üye ID:").pack()
        self.entry_uye_id = tk.Entry(frame_ekle)
        self.entry_uye_id.pack()

        tk.Label(frame_ekle, text="Ad:").pack()
        self.entry_uye_ad = tk.Entry(frame_ekle)
        self.entry_uye_ad.pack()

        tk.Label(frame_ekle, text="Soyad:").pack()
        self.entry_uye_soyad = tk.Entry(frame_ekle)
        self.entry_uye_soyad.pack()

        tk.Label(frame_ekle, text="Telefon:").pack()
        self.entry_uye_tel = tk.Entry(frame_ekle)
        self.entry_uye_tel.pack()

        tk.Button(frame_ekle, text="Üye Ekle", command=self.uye_ekle).pack(pady=5)
        tk.Button(frame_ekle, text="Üyeleri Yenile", command=self.uyeleri_goster).pack()

        self.uyeleri_goster()

    def uye_ekle(self):
        try:
            uye_id = int(self.entry_uye_id.get())
            if uye_id in uyeler:
                messagebox.showerror("Hata", "Bu ID ile üye zaten var.")
                return
            ad = self.entry_uye_ad.get()
            soyad = self.entry_uye_soyad.get()
            tel = self.entry_uye_tel.get()
            if not ad or not soyad or not tel:
                messagebox.showerror("Hata", "Tüm alanlar doldurulmalı.")
                return
            uyeler[uye_id] = Uye(uye_id, ad, soyad, tel)
            messagebox.showinfo("Başarılı", "Üye eklendi.")
            self.uyeleri_goster()
        except ValueError:
            messagebox.showerror("Hata", "Üye ID sayısal olmalıdır.")

    def uyeleri_goster(self):
        self.uye_listbox.delete(0, tk.END)
        for u in uyeler.values():
            self.uye_listbox.insert(tk.END, str(u))

    def create_odunc_tab(self):
        frame = self.tab_odunc

        odunc_al_frame = tk.LabelFrame(frame, text="Ödünç Alma")
        odunc_al_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(odunc_al_frame, text="Kitap ID:").grid(row=0, column=0)
        self.entry_odunc_kitap = tk.Entry(odunc_al_frame, width=10)
        self.entry_odunc_kitap.grid(row=0, column=1, padx=5)

        tk.Label(odunc_al_frame, text="Üye ID:").grid(row=0, column=2)
        self.entry_odunc_uye = tk.Entry(odunc_al_frame, width=10)
        self.entry_odunc_uye.grid(row=0, column=3, padx=5)

        tk.Button(odunc_al_frame, text="Ödünç Al", command=self.odunc_al).grid(row=0, column=4, padx=5)

        iade_frame = tk.LabelFrame(frame, text="İade Etme")
        iade_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(iade_frame, text="Kitap ID:").grid(row=0, column=0)
        self.entry_iade_kitap = tk.Entry(iade_frame, width=10)
        self.entry_iade_kitap.grid(row=0, column=1, padx=5)

        tk.Button(iade_frame, text="İade Et", command=self.iade_et).grid(row=0, column=2, padx=5)

        self.odunc_tree = ttk.Treeview(frame, columns=("kitap", "uye", "odunc_tarihi", "iade_tarihi"), show='headings')
        self.odunc_tree.heading("kitap", text="Kitap")
        self.odunc_tree.heading("uye", text="Üye")
        self.odunc_tree.heading("odunc_tarihi", text="Ödünç Tarihi")
        self.odunc_tree.heading("iade_tarihi", text="İade Tarihi")
        self.odunc_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.odunclari_goster()

    def odunc_al(self):
        try:
            kitap_id = int(self.entry_odunc_kitap.get())
            uye_id = int(self.entry_odunc_uye.get())
        except ValueError:
            messagebox.showerror("Hata", "IDler sayısal olmalı.")
            return

        if kitap_id not in kitaplar:
            messagebox.showerror("Hata", "Kitap bulunamadı.")
            return
        if uye_id not in uyeler:
            messagebox.showerror("Hata", "Üye bulunamadı.")
            return

        kitap = kitaplar[kitap_id]
        uye = uyeler[uye_id]

        if kitap.durum == 'Ödünçte':
            messagebox.showwarning("Uyarı", "Kitap zaten ödünçte.")
            return

        self.son_odunc_id += 1
        odunc = Odunc(self.son_odunc_id, kitap, uye)
        if odunc.odunc_al():
            odunc_listesi.append(odunc)
            messagebox.showinfo("Başarılı", "Kitap ödünç alındı.")
            self.odunclari_goster()
        else:
            messagebox.showerror("Hata", "Ödünç alma işlemi başarısız.")

    def iade_et(self):
        try:
            kitap_id = int(self.entry_iade_kitap.get())
        except ValueError:
            messagebox.showerror("Hata", "Kitap ID sayısal olmalı.")
            return

        for odunc in odunc_listesi:
            if odunc.kitap.kitap_id == kitap_id and odunc.iade_tarihi is None:
                if odunc.iade_et():
                    messagebox.showinfo("Başarılı", "Kitap iade edildi.")
                    self.odunclari_goster()
                    return
        messagebox.showwarning("Uyarı", "Kitap şu anda ödünç değil veya bulunamadı.")

    def odunclari_goster(self):
        for i in self.odunc_tree.get_children():
            self.odunc_tree.delete(i)
        for o in odunc_listesi:
            iade_tarihi = o.iade_tarihi.strftime('%Y-%m-%d %H:%M:%S') if o.iade_tarihi else "Ödünçte"
            self.odunc_tree.insert('', tk.END, values=(
                f"{o.kitap.ad} ({o.kitap.kitap_id})",
                f"{o.uye.ad} {o.uye.soyad} ({o.uye.uye_id})",
                o.odunc_tarihi.strftime('%Y-%m-%d %H:%M:%S'),
                iade_tarihi
            ))

if __name__ == "__main__":
    app = KutuphaneApp()
    app.mainloop()
