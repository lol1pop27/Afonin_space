import pygame, random, os

class Musor():
  """класс одного обьекта мусора"""

  def __init__(self, screen):
    """иницилизация мусора"""

    self.screen = screen
    
    self.image = self.load_random_image()
    self.rect = self.image.get_rect()


    self.rect.x = 0
    self.rect.y = 0
    self.x = float(self.rect.x)
    self.y = float(self.rect.y)




    self.speed = 0.5


  def load_random_image(self):
    """функция загрузки рандомного изображения"""
    if not os.path.exists("/image")