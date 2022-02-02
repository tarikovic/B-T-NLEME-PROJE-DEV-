import os
from os.path import join
import pygame


class Assets:  # tum assetleri(resimleri) iceren sinif
    __COLORS = {'beyaz': 1, 'kirmizi': 2, 'sari': 3, 'yesil': 4}  # renklerin isimleri ve degerleri
    __IMAGES_PATH = join(os.getcwd(), 'resimler\\')  # tum resimlerin klasorunun konumu
    __BULLET_IMG_PATH = join(__IMAGES_PATH, 'mermiler\\')  # mermi resimlerinin klasorunun konumu
    __BLOCK_IMG_PATH = join(__IMAGES_PATH, 'kutular\\')  # kutu resimlerinin klasorunun konumu
    __BOARD_IMG_PATH = join(__IMAGES_PATH, 'tahtalar\\')  # tahta resimlerinin klasorunun konumu

    def __init__(self):  # tum assetleri iceren sinifin constructori
        self.BULLET_IMAGES = {value: {'img': pygame.image.load(self.__BULLET_IMG_PATH + color + '.png'), 'color': color}
                              for color, value in self.__COLORS.items()}  # mermi resimlerinin {renk:{konum:, deger:}}

        self.BLOCK_IMAGES = {value: {'img': pygame.image.load(self.__BLOCK_IMG_PATH + color + '.png'), 'color': color}
                             for color, value in self.__COLORS.items()}  # kutu resimlerinin {renk:{konum:, deger:}}

        self.BOARD_IMAGES = {value: {'img': pygame.transform.scale(
                                             pygame.image.load(self.__BOARD_IMG_PATH + color + '.png'), (128, 12)),
                                     'color': color}
                             for color, value in self.__COLORS.items()}  # tahta resimlerinin {renk:{konum:, deger:}}

    @property
    def color_codes(self):
        return {value: key for key, value in self.__COLORS.items()}  # renk sozlugunu {sayi:renk} olarak disari aktarma
