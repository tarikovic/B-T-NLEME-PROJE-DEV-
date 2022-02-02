from sys import exit
from time import time
from random import choice
import json
from Bullets import Bullet
from Blocks import Block
from Board import Board
from Assets import Assets
from Config import UI
import pygame


class Game:
    pygame.init()  # pygame ozelliklerini iceri aktarma
    config_interface = UI()  # ayarlar arayuzunu acma
    configs = config_interface.configs  # ayarlari ice aktarma
    wbullet = configs['white_bullet_count']  # ilk bastaki beyaz mermi sayisi
    rbullet = configs['red_bullet_count']  # ilk bastaki kirmizi mermi sayisi
    ybullet = configs['yellow_bullet_count']  # ilk bastaki sari mermi sayisi
    gbullet = configs['green_bullet_count']  # ilk bastaki yesil mermi sayisi
    default_bullets = {1: wbullet, 2: rbullet, 3: ybullet, 4: gbullet}  # cephane

    grid_count = configs['width'] // 50
    w = '10' * grid_count  # beyaz kutulardan olusan satir stringi
    r = '20' * grid_count  # kirmizi kutulardan olusan satir stringi
    y = '30' * grid_count  # sari kutulardan olusan satir stringi
    g = '40' * grid_count  # yesil kutulardan olusan satir stringi
    n = '-'  # yeni satira gecme karakteri
    all_lines = [w, r, y, g]  # tum renk satirlarini iceren liste

    def __init__(self):
        self.running = False  # oyunun devam edip etmemesi(start/pause)
        self.fps = self.configs['fps']  # oyunun fpsi(hizi)
        self.width = self.configs['width']  # ekranin genisligi
        self.height = self.configs['height']  # ekranin yuksekligi
        self.window = pygame.display.set_mode((self.width, self.height))  # oyun ekraninin buyuklugu
        self.clock = pygame.time.Clock()  # fps icin kullanilan sinif
        self.board_speed = self.configs['board_speed']  # tahtanin hizi
        self.board_length = self.configs['board_length']  # tahtanin uzunlugu
        self.__seed = '--'  # map stringi
        self.font = pygame.font.SysFont('', size=28)  # pygame font ozelligi
        self.bullets = self.default_bullets.copy()  # mermi sayilari
        self.start_time = None  # oyunun baslama zamani
        self.time_passed = 0  # toplam gecen sure
        self.pause_time = 0  # oyun durdurulma zamani
        self.add_lines = 1  # eklenen satir sayisi
        self.new_line_time = self.configs['new_line_time']  # yeni satir ekleme suresi (saniye)
        self.hpoint = 0  # en yuksek skor
        self.get_highest_score()  # en yuksek skoru bulma
        Bullet.game = self  # mermi sinifina bu sinifin referansini gonderme
        Bullet._configs = self.configs  # mermi sinifina ayarlari gonderme
        Block._configs = self.configs  # kutu sinifina ayarlari gonderme
        Board._configs = self.configs  # tahta sinifina ayarlari gonderme
        self.board = Board(self.board_speed, self.board_length)  # oyunda kullanilacak tahtayi olusturma
        self.main()  # oyunu baslatma

    @property
    def seed(self):  # map stringinin property fonskyonu
        return self.__seed  # map stringini dondurme

    @seed.setter  # map stringi degistirildiginde calisacak fonksiyon(setter)
    def seed(self, value):  # value = (seed, grid_size)
        x, y = 0, 0  # koordinat baslangici
        seed_, grid_size = value  # map stringi ve gridlerin boyutlari
        for block in seed_:  # stringdeki her bir karakterin dongusu
            if block not in ["0", "-"]:  # eger bir kutu olusturma karakteri ise
                Block.create(int(block), x, y)  # kutu olusturma
                x += grid_size  # bir yandaki gride gecme
            elif block == "0":  # eger kutu olsuturulmayacaksa
                x += grid_size  # bir sagdaki gride gecme
            else:  # eger alt gride gecilecekse
                y += grid_size  # alt gride gecme
                x = 0  # satirda en bastaki gride gecme
        self.__seed = seed_  # private stringi degistirme

    def reset(self):  # oyunu bastan baslatma fonksiyonu
        self.add_new_score()  # mevcut skoru dosyaya ekleme
        self.get_highest_score()  # ekleme yapildiktan sonra yeni en yuksek skoru cekme
        Block.delete_all()  # butun kutulari silme
        Bullet.delete_all()  # butun mermileri silme
        self.__init__()  # oyunu sifirdan olusturma

    def did_end(self):  # oyunun bitip bitmedigini kontrol eden fonksiyon
        if not Bullet._bullets and not any(self.bullets.values()):  # eger mermilerin hepsi bittiyse(cephane ve ekran)
            self.reset()  # oyunu sifirlama
        for block in Block._blocks.sprites():  # kutularda dongu olusturma
            if block.rect.y >= self.height - 25:  # eger kutulardan biri ekranin en altina geldiyse
                self.reset()  # oyunu sifirlama

    @staticmethod
    def add_new_score():  # dosyaya yeni skoru yazma fonksiyonu
        with open('scores.json', mode='r+') as f:  # dosyayi okuma
            json_data = f.read()  # dosyadaki verileri cekme
            py_obj = json.loads(json_data)  # verileri python nesnesi haline getirme

        with open('scores.json', mode='w') as f:  # dosyaya yazma
            if Bullet.point > py_obj['highest_score']:  # eger mevcut puan en yuksek puandan fazla ise
                py_obj['highest_score'] = Bullet.point  # dosyaya yazilacak en yuksek puani degistirme
            py_obj['scores'].append(Bullet.point)  # dosyaya yazilacak skorlara mevcut skoru ekleme
            json.dump(py_obj, f, indent=4)  # dosyaya yazma

    def get_highest_score(self):  # dosyadan en yuksek skoru cekme fonksiyonu
        with open('scores.json', mode='r') as f:  # dosyayi okuma
            json_data = f.read()  # verileri cekme
            py_obj = json.loads(json_data)  # verileri python nesnesi haline getirme
            self.hpoint = py_obj['highest_score']  # en yuksek puani ayarlama

    def fire(self, color_code):  # tahtadan mermi firlatma fonksiyonu
        if self.bullets[color_code]:  # eger herhangi renkte bir mermi varsa
            mx, my = self.board.rect.x + self.board_length / 2, self.board.rect.y - 12  # tahtanin koordinatlari
            Bullet.create(color_code, mx, my)  # mermi olusturma
            self.bullets[color_code] -= 1  # tahtadaki mermi sayisini azaltma

    def add_newline(self):  # oyuna yeni bir kutu satiri ekleme fonksiyonu
        if not Block._blocks or int(self.time_passed / self.new_line_time) == self.add_lines:  # kutu kalmadiysa veya sure gectiyse
            self.seed = ('--' + choice(self.all_lines), 25)  # yeni mapi ekleme
            for block in Block._blocks.sprites():  # kutularda dongu olusturma
                block.rect.y += 25  # eski kutulari 25 pixel asagi indirme
            self.add_lines += 1  # eklenen satir sayisini 1 arttirma

    def highest_point(self):
        text = self.font.render('En Yüksek Puan: ' + str(self.hpoint), False, (255, 255, 255))  # en yuksek puan yazisi
        self.window.blit(text, (self.width / 2 + 30, 10))  # en yuksek puani ekrana ekleme

    def point(self):
        text = self.font.render('Puan: ' + str(Bullet.point), False, (255, 255, 255))  # puan yazisi olusturma
        self.window.blit(text, (self.width / 2 + 270, 10))  # puan yazisini ekrana ekleme

    def time(self):  # sure sayaci fonksiyonu
        text = self.font.render('Süre: ' + str(round(self.time_passed, 2)), False, (205, 0, 205))  # surenin yazisi
        self.window.blit(text, (self.width/2 - 70, 10))  # sureyi ekrana renderlama

    def bullets_left(self):  # kalan mermi sayaci fonksiyonu
        white_bullets = self.bullets[1]  # beyaz mermilerin sayisi
        red_bullets = self.bullets[2]  # kirmizi mermilerin sayisi
        yellow_bullets = self.bullets[3]  # sari mermilerin sayisi
        green_bullets = self.bullets[4]  # yesil mermilerin sayisi
        wtext = self.font.render(str(white_bullets), False, (255, 255, 255))  # mermilerin sayilarini olusturma
        rtext = self.font.render(str(red_bullets), False, (255, 0, 0))
        ytext = self.font.render(str(yellow_bullets), False, (255, 255, 0))
        gtext = self.font.render(str(green_bullets), False, (0, 255, 0))
        self.window.blit(wtext, (self.width/2 - 235, 10))  # mermi sayilarini ekrana ekleme
        self.window.blit(rtext, (self.width/2 - 200, 10))
        self.window.blit(ytext, (self.width/2 - 165, 10))
        self.window.blit(gtext, (self.width/2 - 130, 10))

    def render(self):
        self.highest_point()  # en yuksek puani ekrana ekleme
        self.point()  # puani ekrana ekleme
        self.time()  # sureyi ekrana ekleme
        self.bullets_left()  # kalan mermi sayisini ekrana ekleme
        self.add_newline()  # eger yeterli kutu kirildiysa ekrana yeni kutu satiri ekleme

    def update(self):  # yeni bir frame olusturma
        self.window.fill((0, 0, 0))  # ekrani temizleme
        Bullet.main(self.window)  # butun mermileri ekrana ekleme
        self.board.main(self.window)  # tahtayi ekrana ekleme
        self.render()  # bu siniftan gelen ozellikleri ekrana ekleme
        Block.main(self.window)  # butun kutulari ekrana ekleme
        pygame.display.update()  # ekrani yeni eklenenlerle guncelleme
        self.clock.tick(self.fps)  # fps'e gore bekleme (time.sleep gibi)

    def main(self):  # oyunun isleme kismi
        self.seed = (self.__seed, 25)  # kutularin mapini cizme
        self.update()  # ekrani guncelleme
        while True:  # oyun dongusu
            for event in pygame.event.get():  # pygame hareket dinleyici
                if event.type == pygame.QUIT:  # eger carpiya basildiysa
                    pygame.quit()  # pygameden cikis yapma
                    exit()  # scripti tamamen durdurma

                if event.type == pygame.KEYDOWN:  # eger bir tusa basildiysa
                    if event.key == pygame.K_SPACE:  # eger bosluk tusu ise
                        if self.start_time is None:  # eger oyun baslamamis ise
                            self.start_time = time()  # baslama zamanini ayarlama
                            self.running = True  # oyunu baslatma

                        elif self.running:  # eger oyun devam ediyor ise
                            self.pause_time = time()  # durduruldugu zamani ayarlama
                            self.running = False  # oyunu durdurma

                        elif not self.running:  # eger oyun durmussa
                            self.start_time += time() - self.pause_time  # gecen sureyi durdurulan sureye gore ayarlama
                            self.running = True  # oyunu baslatma

                    if self.running:  # eger oyun devam ediyorsa
                        if event.key == pygame.K_q:  # eger q tusuna basilmissa
                            self.fire(1)  # beyaz mermi atesleme

                        elif event.key == pygame.K_w:  # eger w tusuna basilmissa
                            self.fire(2)  # kirmizi mermi atesleme

                        elif event.key == pygame.K_e:  # eger e tusuna basilmissa
                            self.fire(3)  # sari mermi atesleme

                        elif event.key == pygame.K_r:  # eger r tusuna basilmissa
                            self.fire(4)  # yesil mermi atesleme

            if self.running:  # eger oyun devam ediyorsa
                self.time_passed = time() - self.start_time  # gecen zamani degistirme
                keys = pygame.key.get_pressed()  # basili olan tuslarin listesi

                if keys[pygame.K_RIGHT]:  # eger sag ok tusuna basili tutuluyorsa
                    self.board.move('right')  # tahtayi saga hareket ettirme

                elif keys[pygame.K_LEFT]:  # eger sol ok tusuna basili tutuluyorsa
                    self.board.move('left')  # tahtayi sola hareket ettirme
                self.did_end()  # oyunun bitip bitmedigini kontrol etme
                self.update()  # ekrani guncelleme


if __name__ == '__main__':  # eger bu script calistirilirsa
    Game()  # oyunu baslatma
