import json
import tkinter as tk
import os
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime



class FinansYoneticisi:
    def __init__(self, dosya_yolu="veri.json"):
        self.dosya_yolu = dosya_yolu
        self.veri = {
            "gelir": [],
            "gider": [],
            "tasarruf_hedefi": 0
        }

    def verileri_yukle(self):
        try:
            with open(self.dosya_yolu, "r") as dosya:
                self.veri = json.load(dosya)
        except FileNotFoundError:
            self.verileri_kaydet() 

    def verileri_kaydet(self):
        with open(self.dosya_yolu, "w") as dosya:
            json.dump(self.veri, dosya)

    def verileri_sifirla(self):
        self.veri = {"gelir": [], "gider": [], "tasarruf_hedefi": 0}
        self.verileri_kaydet()

    def gelir_ekle(self, miktar, kaynak):
        self.veri["gelir"].append({"miktar": miktar, "kaynak": kaynak})
        self.verileri_kaydet()

    def gider_ekle(self, miktar, kategori):
        self.veri["gider"].append({"miktar": miktar, "kategori": kategori})
        self.verileri_kaydet()

    def tasarruf_hedefi_ayarla(self, miktar):
        self.veri["tasarruf_hedefi"] = miktar
        self.verileri_kaydet()

    def toplam_geliri_hesapla(self):
        return sum(item["miktar"] for item in self.veri["gelir"])

    def toplam_gideri_hesapla(self):
        return sum(item["miktar"] for item in self.veri["gider"])

    def tasarrufu_hesapla(self):
        return self.toplam_geliri_hesapla() - self.toplam_gideri_hesapla()


class FinansUygulamasi:
    def __init__(self, ana_pencere, finans_yoneticisi):
        self.fy = finans_yoneticisi
        self.fy.verileri_yukle()

        ana_pencere.title("Finans Yöneticisi")
        ana_pencere.geometry("500x500")
        ana_pencere.resizable(True, True)

        tk.Label(ana_pencere, text="Gelir Miktarı:").grid(row=0, column=0, padx=10, pady=10)
        self.gelir_giris = tk.Entry(ana_pencere)
        self.gelir_giris.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(ana_pencere, text="Gelir Kaynağı:").grid(row=1, column=0)
        self.gelir_kaynak_giris = tk.Entry(ana_pencere)
        self.gelir_kaynak_giris.grid(row=1, column=1)

        tk.Button(ana_pencere, text="Gelir Ekle", command=self.gelir_ekle).grid(row=2, column=1)

        tk.Label(ana_pencere, text="Gider Miktarı:").grid(row=3, column=0, padx=10, pady=10)
        self.gider_miktar_giris = tk.Entry(ana_pencere)
        self.gider_miktar_giris.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(ana_pencere, text="Gider Kategorisi:").grid(row=4, column=0)
        self.gider_kategori_giris = tk.Entry(ana_pencere)
        self.gider_kategori_giris.grid(row=4, column=1)

        tk.Button(ana_pencere, text="Gider Ekle", command=self.gider_ekle).grid(row=5, column=1, pady=10)

        tk.Label(ana_pencere, text="Tasarruf Hedefi:").grid(row=6, column=0)
        self.tasarruf_hedefi_giris = tk.Entry(ana_pencere)
        self.tasarruf_hedefi_giris.grid(row=6, column=1)

        tk.Button(ana_pencere, text="Hedef Ayarla", command=self.tasarruf_hedefi_ayarla).grid(row=7, column=1)

        tk.Button(ana_pencere, text="Rapor Oluştur  ", command=self.raporu_olustur).grid(row=8, column=1, pady=10)

        tk.Button(ana_pencere, text="Verileri Sıfırla", command=self.verileri_sifirla).grid(row=9, column=1, pady=10)

        tk.Button(ana_pencere, text="Geri Bildirim Al", command=self.geri_bildirim_ver).grid(row=10, column=1, pady=10)

    def gelir_ekle(self):
        try:
            miktar = float(self.gelir_giris.get())
            kaynak = self.gelir_kaynak_giris.get()
            if not kaynak:
                kaynak = "Genel"
            self.fy.gelir_ekle(miktar, kaynak)
            messagebox.showinfo("Başarılı", "Gelir başarıyla eklendi!")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir miktar girin.")

    def gider_ekle(self):
        try:
            miktar = float(self.gider_miktar_giris.get())
            kategori = self.gider_kategori_giris.get()
            if not kategori:
                kategori = "Genel"
            self.fy.gider_ekle(miktar, kategori)
            messagebox.showinfo("Başarılı", "Gider başarıyla eklendi!")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir miktar girin.")

            self.gider_miktar_giris.delete(0, tk.END)
            self.gider_kategori_giris.delete(0, tk.END)

    def tasarruf_hedefi_ayarla(self):
        try:
            miktar = float(self.tasarruf_hedefi_giris.get())
            self.fy.tasarruf_hedefi_ayarla(miktar)
            messagebox.showinfo("Başarılı", "Tasarruf hedefi başarıyla ayarlandı!")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir miktar girin.")

    def raporu_olustur(self):
        toplam_gelir = self.fy.toplam_geliri_hesapla()
        toplam_gider = self.fy.toplam_gideri_hesapla()
        tasarruf = self.fy.tasarrufu_hesapla()
        hedef = self.fy.veri["tasarruf_hedefi"]
        rapor = (
            f"Toplam Gelir: {toplam_gelir}\n"
            f"Toplam Gider: {toplam_gider}\n"
            f"Mevcut Tasarruf: {tasarruf}\n"
            f"Tasarruf Hedefi: {hedef}\n"
        )
        gelir_kaynaklari = [item['kaynak'] for item in self.fy.veri["gelir"]]
        gelir_miktarlari = [item['miktar'] for item in self.fy.veri["gelir"]]
        gider_kategorileri = [item['kategori'] for item in self.fy.veri["gider"]]
        gider_miktarlari = [item['miktar'] for item in self.fy.veri["gider"]]

        
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))  
        ax[0].bar(gelir_kaynaklari, gelir_miktarlari, label="Gelir", alpha=0.7, color='green')
        ax[0].bar(gider_kategorileri, gider_miktarlari, label="Gider", alpha=0.7, color='red')

        ax[0].set_xlabel("Kategori")
        ax[0].set_ylabel("Miktar")
        ax[0].set_title("Gelir ve Giderler")
        ax[0].legend()

       
        ax[1].pie(
            gider_miktarlari,
            labels=gider_kategorileri,
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.Paired.colors
        )
        ax[1].set_title("Gider Dağılımı")

        plt.tight_layout()  # Grafikleri düzenler
        plt.show()

         
        grafik_klasoru = os.path.join(os.path.expanduser("~"), "Masaüstü")  # Masaüstü yolunu oluştur
        os.makedirs(grafik_klasoru, exist_ok=True)  # Klasör mevcut değilse oluştur
        grafik_dosya_adi = os.path.join("grafik.png")
        plt.savefig(grafik_dosya_adi)
        plt.close()
        messagebox.showinfo("Başarılı", "Grafik başarıyla oluşturuldu ve kaydedildi!")

    def geri_bildirim_ver(self):
        toplam_gelir = self.fy.toplam_geliri_hesapla()
        toplam_gider = self.fy.toplam_gideri_hesapla()
        tasarruf_hedefi = self.fy.veri["tasarruf_hedefi"]

    
        gider_kategorileri = [item["kategori"] for item in self.fy.veri["gider"]]
        gider_miktarlari = [item["miktar"] for item in self.fy.veri["gider"]]
        if gider_miktarlari:
            max_gider_index = gider_miktarlari.index(max(gider_miktarlari))
            en_cok_harcama_kategorisi = gider_kategorileri[max_gider_index]
            en_cok_harcama_miktari = gider_miktarlari[max_gider_index]
            harcama_yuzdesi = (en_cok_harcama_miktari / toplam_gelir) * 100

        else:
            en_cok_harcama_kategorisi = "Yok"
            en_cok_harcama_miktari = 0
            harcama_yuzdesi = 0

        kalan_tasarruf = tasarruf_hedefi-toplam_gider

    
        if toplam_gider > tasarruf_hedefi:
            mesaj = (
            f"Tasarruf hedefini aştınız! "
            f"Toplam gider: {toplam_gider} TL, Tasarruf hedefi: {tasarruf_hedefi} TL.\n"
            f"En çok harcama yaptığınız kategori: {en_cok_harcama_kategorisi} ({en_cok_harcama_miktari} TL).\n"
            f"({en_cok_harcama_miktari} TL), bu gelirinizin %{harcama_yuzdesi:.2f}'sini oluşturuyor.\n"
            f"Tasarruf etmek için bu kategoride harcamalarınızı azaltabilirsiniz."
        )
        elif toplam_gider == tasarruf_hedefi:
            mesaj = "Harcamalarınız tam tasarruf hedefinizde! Dikkatli şekilde devam edin."
        else:
            kalan_tasarruf=toplam_gider-tasarruf_hedefi
        mesaj = (
            f"Tebrikler! Tasarruf hedefinize yaklaşıyorsunuz.\n"
            f"Toplam gider: {toplam_gider} TL, Tasarruf hedefi: {tasarruf_hedefi} TL.\n"
            f"Kalan tasarruf hedefi: {kalan_tasarruf} TL.\n"
            f"En çok harcama yaptığınız kategori: {en_cok_harcama_kategorisi} ({en_cok_harcama_miktari} TL).\n"
            f"({en_cok_harcama_miktari} TL), bu gelirinizin %{harcama_yuzdesi:.2f}'sini oluşturuyor.\n"
            f"Harcamalarınızı aynı şekilde kontrol altında tutabilirsiniz."
        )

        messagebox.showinfo("Tasarruf Geri Bildirimi", mesaj)

    def verileri_sifirla(self):
        self.fy.verileri_sifirla()
        messagebox.showinfo("Başarılı", "Tüm veriler sıfırlandı!")


if __name__ == "__main__":
    yonetici = FinansYoneticisi()
    kok = tk.Tk()
    uygulama = FinansUygulamasi(kok, yonetici)
    kok.mainloop()