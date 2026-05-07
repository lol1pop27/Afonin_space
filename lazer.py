import pygame


class Lazer:
    """класс лазера. Управление выстрелом"""
    def __init__(self, x, y, shir, wisota, color, face):
        self.x = x # координаты
        self.y = y # координаты
        self.shir = shir # ширина
        self.wisota = wisota # высота
        self.color = color # цвет лазера
        self.face = face # направление движения (1 - вверх, -1 - вниз)
        self.speed = 2 

    def draw(self, screen):
        """отрисовка лазера на экране"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.shir, self.wisota))
    
    def update(self):
        """обновление координаты"""
        self.y += self.speed * self.face

    def is_offscreen(self, screen_height):
        """проверка вылета лазера за экран"""
        return (self.y + self.wisota < 0) or (self.y > screen_height)
