import tkinter as tk
import json
from string import digits


class UI:
    def __init__(self):
        self.configs = self.get_curr()  # dosyadaki verileri uyeye aktarma
        self.entries = dict()  # arayuzdeki girdilerin sozlugu
        self.window = tk.Tk()  # tkinter arayuzu olusturma
        self.window.geometry("300x620+650+120")  # arayuzu boyutlandirma
        self.window.resizable(False, False)  # arayuz boyutunu sabit hale getirme
        self.create_interface()  # arayuzu baslatma

    def get_curr(self):  # dosyadaki bilgileri okuyan fonksiyon
        with open('config.json', mode='r') as f:  # dosyayi acma
            json_data = f.read()  # dosyadaki verileri okuma
            py_obj = json.loads(json_data)  # verileri python nesnesi haline getirme
            py_obj = {key.lower(): value for key, value in py_obj.items()}  # anahtarlari kucuk harfe cevirme
            return py_obj.copy()  # python nesnesini disari aktarma

    def create_interface(self):  # arayuzu olusturan ve baslatan fonksiyon
        for index, (key, value) in enumerate(self.configs.items()):  # ayarlarda dongu olusturma
            default_value = tk.StringVar(value=value)  # girdi kutucuklarina degisken atama
            label = tk.Label(self.window, text=key, anchor='w', width=25)  # anahtarin adinin text widgetini olusturma
            label.grid(row=index, pady=2)  # yaziyi ekrana yerlestirme
            entry = tk.Entry(self.window, width=17, name=key, textvariable=default_value)  # girdi kutusu olusturma
            entry.grid(row=index, column=1, columnspan=2)  # girdi kutusunu ekrana yerlestirme
            self.entries[entry.winfo_name()] = default_value  # girdiler sozlugune ekleme

        save_button = tk.Button(self.window, text='kaydet', command=self.save_configs, anchor='e')  # arayuzu kaydetme
        save_button.grid(row=index + 1, column=1)  # kaydetme butonunu ekrana yerlestirme

        start_button = tk.Button(self.window, text='Başlat', command=self.window.destroy)  # oyunu baslatma butonu
        start_button.grid(row=index + 1, column=2, pady=30)  # baslatma butonunu ekrana yerlestirme

        tk.mainloop()  # arayuzu baslatma

    def save_configs(self):  # arayuzdeki degerleri kaydetme fonksiyonu
        new_configs = {key.upper(): int(value.get()) for key, value in self.entries.items()}  # arayuzdekileri sozluk yapma
        with open('config.json', mode='w') as f:  # ayarlar dosyasini acma
            json.dump(new_configs, f, indent=4)  # dosyaya yeni degerleri kaydetme
        self.configs = self.get_curr()  # ilk basta gelen verileri yeni verilerle degistirme

