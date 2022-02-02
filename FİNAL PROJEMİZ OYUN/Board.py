import pygame
from Assets import Assets
pygame.init()


class Board(pygame.sprite.Sprite):
    __assets = Assets()  # asset sinifindan bir uye olsuturuyor
    _images = __assets.BOARD_IMAGES  # asset sinifindan gelen tahta resimleri
    _board = pygame.sprite.Group()  # sinifin uyelerini tutan degisken(sprite grubu)
    _configs = None  # ana ayarlar

    def __init__(self, board_speed, board_length):  # bu sinifin constructori
        super().__init__()  # kalitim yapilan sinifin constructorini calistiriyor
        self.board_speed = board_speed  # tahtanin hizi
        self.board_length = board_length  # tahtanin uzunlugu
        self.__image = pygame.transform.scale(self.__assets.BOARD_IMAGES[1]['img'], (board_length, 12))  # tahtanin resmi
        self.rect = self.image.get_rect()  # tahtanin alani ve koordinati
        self.rect.y = self._configs['height'] - 12  # tahtanin y koordinatini en asagiya getiriyor
        Board._board.add(self)  # tahta sprite grubuna ekliyor

    @property
    def image(self):
        return self.__image  # resim cagrildiginda private resmi dondurme

    @image.setter  # resim degistiginde tekrar boyutlandirma fonksiyonu
    def image(self, value):
        self.__image = pygame.transform.scale(value, (self.board_length, 12))  # tekrar boyutlandirma

    def move(self, direction):  # tahtanin hareket fonksiyonu
        if direction == 'right':  # eger parametre right ise
            if self.rect.x <= self._configs['width'] - self.board_length - 5:  # eger tahta ekranin sagindan disari cikmiyorsa
                self.rect.x += self.board_speed  # tahtanin x konumunu 1 pixel saga kaydiriyor
        elif direction == 'left':  # eger parametre left ise
            if self.rect.x > 0:  # eger tahta ekranin solundan disari cikmiyorsa
                self.rect.x -= self.board_speed  # tahtanin x konumunu 1 pixel sola kaydiriyor

    def main(self, screen):  # her ekran yenilenmesinde calisacak fonksiyonu
        screen.blit(self.image, self.rect)  # ekrana tahtayi cizdiriyor
