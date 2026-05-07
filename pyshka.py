import pygame

class Pyshka:
    def __init__(self, screen):
        """иницилизация пушки"""
        self.screen = screen #атрибут экрана
        self.image = pygame.image.load("image/pyshka.png") #загрузка нашей пушки
        self.rect = self.image.get_rect() # отрисовка
        self.rect.centerx = self.screen.get_rect().centerx #расположим нашу пушку по центру экрана
        self.screen_rect = screen.get_rect()
        self.rect.bottom = self.screen_rect.bottom  #расположим пушку по низу экрана
        self.m_right = False # при запуске наш корабль остаётся без  движения
        self.m_left = False #
    
    def output(self):
        """функция отрисовки пушки на экране"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """функция изменеия координат пушки"""
        if self.m_right:
            if self.rect.right < self.screen_rect.right:
                self.rect.x += 1
        if self.m_left:
            if self.rect.left > 0:
                self.rect.x -= 1