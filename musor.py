import pygame
import random
import os


class Musor():
    """класс одного объекта мусора"""

    def __init__(self, screen):
        """иницилизация мусора"""
        self.screen = screen

        # загружаем случайную картинку из папки image/musor
        self.image = self.load_random_image()
        self.rect = self.image.get_rect()

        # начальная позиция 
        self.rect.x = 0
        self.rect.y = 0
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # ВАЖНО: скорость должна быть ОДИНАКОВОЙ для всего мусора
        self.speed = 0.05  # Одинаковая скорость

    def load_random_image(self):
        """функция загрузки рандомного изображения"""
        folder_path = os.path.join("image", "musor")

        if not os.path.exists(folder_path):
            img = pygame.Surface((50, 50))
            img.fill((139, 69, 19))
            pygame.draw.rect(img, (255, 255, 255), (0, 0, 49, 49), 2)
            return img
        
        images = [i for i in os.listdir(folder_path) if i.lower().endswith('.png')]

        if images:
            random_image = random.choice(images)
            path = os.path.join(folder_path, random_image)
            try:
                img = pygame.image.load(path)
                return pygame.transform.scale(img, (50, 50))
            except:
                print(f"ошибка загрузки картинки {random_image}")
        
        img = pygame.Surface((50, 50))
        img.fill((139, 69, 19))
        pygame.draw.rect(img, (255, 255, 255), (0, 0, 49, 49), 2)
        return img
    
    def draw(self):
        """функция отрисовки мусора на экране"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """движение мусора вниз"""
        self.y += self.speed
        self.rect.y = self.y