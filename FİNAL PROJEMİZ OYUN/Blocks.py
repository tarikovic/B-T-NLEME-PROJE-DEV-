import pygame
from Assets import Assets
pygame.init()


class Block(pygame.sprite.Sprite):  # kutularin sinifi
    __assets = Assets()  # asset sinifindan bir uye olusturuyor
    __images = __assets.BLOCK_IMAGES  # asset sinifindan gelen kutu resimleri
    _blocks = pygame.sprite.Group()  # sinifin uyelerini tutan degisken(sprite grubu)
    _font = pygame.font.SysFont('Comic Sans MS', 10)  # can bilgilerinin fontu
    _configs = None  # ana ayarlar

    def __init__(self, color_value):  # bu sinifin constructori
        super().__init__()  # kalitim yapilan sinifin constructorini calistiriyor
        self.color_value = color_value  # parametreye verilen renk degerini uye degeri yapiyor
        self.image = self.__images[color_value]['img']  # kutunun resmi
        self.rect = self.image.get_rect()  # kutunun alani ve koordinati
        if color_value == 1:
            self.health = self._configs['white_box_health']  # kutunun cani
            self.point = self._configs['white_box_point']  # kutunun verdigi puan
        elif color_value == 2:
            self.health = self._configs['red_box_health']
            self.point = self._configs['red_box_point']
        elif color_value == 3:
            self.health = self._configs['yellow_box_health']
            self.point = self._configs['yellow_box_point']
        elif color_value == 4:
            self.health = self._configs['green_box_health']
            self.point = self._configs['green_box_point']
        self.text = self._font.render(str(self.health), False, (0, 0, 0))  # kutunun caninin render edilmesi
        Block._blocks.add(self)  # olsuturulan yeni uyeyi sprite grubuna ekleme

    @classmethod
    def delete_all(cls):  # tum kutulari silme fonksiyonu
        cls._blocks = pygame.sprite.Group()  # tum kutulari silme

    @classmethod
    def create(cls, color_value, x, y):  # sinif uzerinden yeni bir uye olusturma(kutu olusturma)
        new = cls(color_value)  # uye olusturma
        new.rect.x = x  # uyenin x koordinatini ayarlama
        new.rect.y = y  # uyenin y koordinatini ayarlama

    @classmethod
    def main(cls, screen):  # her ekran yenilenmesinde calisacak sinif fonksiyonu
        Block._blocks.draw(screen)  # butun kutulari ekrana cizdirme
        for block in cls._blocks:  # kutularda dongu olusturma
            screen.blit(block.text, (block.rect.x+2, block.rect.y))  # kutunun canini ekrana ekleme
