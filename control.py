import pygame, sys
from lazer import Lazer
import musor

def do_it(pyshka, lazers, events):
    """обработка нажатых клавиш при игре"""
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pyshka.m_right = True
            if event.key == pygame.K_LEFT:
                pyshka.m_left = True
            if event.key == pygame.K_SPACE:
                laz = Lazer(
                    x=pyshka.rect.centerx,
                    y=pyshka.rect.top,
                    shir=4,
                    wisota=10,
                    color=(255, 0, 0),
                    face=-1
                )
                lazers.append(laz)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                pyshka.m_right = False
            if event.key == pygame.K_LEFT:
                pyshka.m_left = False


def create_musor_army(screen, musor_list, debris_count=None):
    """создаем армию космического мусора"""
    temp_musor = musor.Musor(screen)
    width = temp_musor.rect.width
    height = temp_musor.rect.height

    # ИЗМЕНЕНО: если количество не передано, создаём полные ряды (по умолчанию)
    if debris_count is None:
        count_in_row = int(650 / width)
        count_rows = int(400 / height)
        all_width = count_in_row * width
        margin = (700 - all_width) // 2

        for row in range(count_rows):
            for col in range(count_in_row):
                musor_item = musor.Musor(screen)
                musor_item.x = margin + width * col
                musor_item.rect.x = musor_item.x
                musor_item.y = height * row
                musor_item.rect.y = musor_item.y
                musor_list.append(musor_item)
    else:
        #создаём указанное количество мусора рядами
        count_in_row = int(650 / width)
        margin = (700 - count_in_row * width) // 2
        
        for i in range(debris_count):
            musor_item = musor.Musor(screen)
            row = i // count_in_row
            col = i % count_in_row
            musor_item.x = margin + width * col
            musor_item.rect.x = musor_item.x
            musor_item.y = height * row
            musor_item.rect.y = musor_item.y
            musor_list.append(musor_item)


def update_musor_army(musor_list):
    """Обновляет позиции всего мусора."""
    for musor_item in musor_list:
        musor_item.update()


def chek_musor(lazers, musor_list):
    """проверка столкновения лазера с мусором"""
    point = 0
    for laz in lazers[:]:
        for musor_item in musor_list[:]:
            if (laz.x < musor_item.rect.x + musor_item.rect.width and
                laz.x + laz.shir > musor_item.rect.x and
                laz.y < musor_item.rect.y + musor_item.rect.height and
                laz.y + laz.wisota > musor_item.rect.y):
                lazers.remove(laz)
                musor_list.remove(musor_item)
                point += 10
                break
    return point


def chek_game_over(musor_list, pyshka):
    """проверка столкновения космического мусора и нашего корабля"""
    for musor_i in musor_list:
        if (musor_i.rect.x < pyshka.rect.x + pyshka.rect.width and
            musor_i.rect.x + musor_i.rect.width > pyshka.rect.x and
            musor_i.rect.y < pyshka.rect.y + pyshka.rect.height and
            musor_i.rect.y + musor_i.rect.height > pyshka.rect.y):
            return True
    return False