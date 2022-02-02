import pygame
from Assets import Assets
from Blocks import Block
from Board import Board
from random import choice


class Bullet(pygame.sprite.Sprite):
    __assets = Assets()  # asset sinifindan bir uye olusturuyor
    __images = __assets.BULLET_IMAGES  # asset sinifindan gelen mermi resimleri
    _bullets = pygame.sprite.Group()  # sinifin uyelerini tutan degisken(sprite grubu)
    _configs = None  # ana ayarlar
    point = 0  # oyunda kazanilan puan
    game = None

    def __init__(self, color_value):
        super().__init__()  # kalitim yapilan sinifin constructorini calistiriyor
        self.color_value = color_value  # parametreye verilen renk degerini uye degeri yapiyor
        self.image = self.__images[color_value]['img']  # merminin resmi
        self.rect = self.image.get_rect()  # merminin alani ve koordinati
        self.vector = [choice([1, -1]), choice([1, -1])]  # merminin vectoru rastgele belirleniyor.

        if color_value == 1:  # eger beyaz ise
            self._bulletdamage = self._configs['white_bullet_damage']  # hasari ayarlama

        elif color_value == 2:  # eger kirmizi ise
            self._bulletdamage = self._configs['red_bullet_damage']  # hasari ayarlama

        elif color_value == 3:  # eger sari ise
            self._bulletdamage = self._configs['yellow_bullet_damage']  # hasari ayarlama

        elif color_value == 4:  # eger yesil ise
            self._bulletdamage = self._configs['green_bullet_damage']  # hasari ayarlama

        Bullet._bullets.add(self)  # olsuturulan yeni uyeyi sprite grubuna ekleme

    @classmethod
    def create(cls, color_value, x, y):  # sinif uzerinden yeni bir uye olusturma(mermi olusturma)
        new_bullet = cls(color_value)  # mermi olusturuyor
        new_bullet.rect.x = x  # merminin x koordinatini ayarliyor
        new_bullet.rect.y = y  # merminin y koordinatini ayarliyor

    @classmethod
    def add_bullet(cls, color_code):  # cephaneye mermi ekleme
        cls.game.bullets[color_code] += 1  # cephaneye mermi ekleme

    @classmethod
    def delete_all(cls):
        cls._bullets = pygame.sprite.Group()  # butun mermileri silme
        cls.point = 0  # puani sifirlama

    @classmethod
    def main(cls, screen):
        for bullet in cls._bullets:  # mermilerin carpisma kontrolu icin mermi dongusu
            collided = pygame.sprite.spritecollideany(bullet, Block._blocks)  # kutuyla carpismasini kontrol ediyor
            board_collision = pygame.sprite.spritecollide(bullet, Board._board, False)  #tahtayla carpismasini kontrol ediyor

            if board_collision:  # tahta ile carpisma yasandiysa
                Board._board.sprites()[0].image = Board._images[bullet.color_value]['img']  # tahta merminin rengini aliyor
                bullet.vector[1] = -bullet.vector[1]  # merminin y vektoru yukari yoneltiliyor

            elif collided:  # mermi kutulardan biriyle carpistiysa
                collided.health -= bullet._bulletdamage  # kutu topla carpistigi icin cani azaldi

                if collided.health <= 0:  # eger kutunun cani 0'dan az olduysa
                    cls.point += collided.point  # puani arttirma
                    cls.add_bullet(collided.color_value)  # yeni mermi ekleme
                    collided.kill()  # kutu oyundan siliniyor

                collided.text = Block._font.render(str(collided.health), False, (0, 0, 0))  # kutunun canini degistirme

                if collided.rect.x + collided.rect.width - 1 == bullet.rect.x:  # sagdan gelip sol tarafa carptiysa
                    bullet.vector[0] = 1  # x vektorunu saga yonlendirme

                if collided.rect.x == bullet.rect.x + bullet.rect.width - 1:  # soldan gelip sag tarafa carptiysa
                    bullet.vector[0] = -1  # x vektorunu sola yonlendirme

                if collided.rect.y + collided.rect.height - 1 == bullet.rect.y:  # asagidan yukari carpma
                    bullet.vector[1] = 1  # y vektorunu asagi yonlendirme

                if collided.rect.y == bullet.rect.y + bullet.rect.height - 1:  # yukaridan asagi carpma
                    bullet.vector[1] = -1  # y vektorunu yukari yonlendirme

            if bullet.rect.x >= cls._configs['width'] - 10:  # mermi ekranin sagina carptiysa
                bullet.vector[0] = -1  # merminin x vektoru sola yoneltiliyor

            elif bullet.rect.x <= 0:  # mermi ekranin soluna carptiysa
                bullet.vector[0] = 1  # merminin x vektoru saga yoneltiliyor

            if bullet.rect.y <= 0:  # mermi ekranin ustune carptiysa
                bullet.vector[1] = 1  # merminin y vektoru asagi yoneltiliyor
            if bullet.rect.y >= cls._configs['height']:  # mermi ekranin asagisina carptiysa
                bullet.kill()  # mermi oyundan siliniyor

            bullet.rect.x += bullet.vector[0]  # mermi x eksenin x vektoru kadar ilerletiliyor
            bullet.rect.y += bullet.vector[1]  # mermi y ekseninde y vektoru kadar ilerletiliyor

        cls._bullets.draw(screen)  # butun mermileri ekrana ciziyor
