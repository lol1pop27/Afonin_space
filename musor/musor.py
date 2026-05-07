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
    if not os.path.exists("/image/musor"):
      img = pygame.Surface((50, 50))
      img.fill((139, 69, 19))
      return img
    


    image = [i for i in os.listdir("/image/musor") if i.lower().endswith('png')]


    if image:
      random_image = random.choice(image)

      path = os.path.join("/image/musor", random_image)

      try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (50, 50))
      except:
        print(f"ошибка загрузки картинки {random_image}")


        img = pygame.Surface((50, 50))
        img.fill((139,69,19))



    def draw(self):
      """функция отрисовки мусора на экране"""
      self.screen.blit(self.image, self.rect)

    def update(self):
      """движение мусора в низ"""

      self.y += self.speed
      self.rect.y = self.y
      