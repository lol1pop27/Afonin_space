import pygame, control          # Подключаем pygame и наш файл control.py с управлением
from pyshka import Pyshka      # Импортируем класс пушки (нашего корабля)
import musor                   # Импортируем класс мусора (врагов)
import sys                     # Для выхода из игры
import random                  # Для генерации случайных чисел

# функция запуска нашей игры
def run():
    # Инициализируем pygame - без этого ничего работать не будет
    pygame.init()
    
    # Создаём окно игры размером 700 на 800 пикселей
    screen = pygame.display.set_mode((700, 800))
    
    # Устанавливаем заголовок окна
    pygame.display.set_caption("Космические исследователи")
    
    # Цвет фона - чёрный 
    bg_color = (0, 0, 0)
    
    # Создаём объект пушки (нашего корабля)
    pyshka = Pyshka(screen)

    # Список для хранения всех лазеров, которые выпустила пушка
    lazers = []
    
    # Список для хранения всего мусора на экране
    musor_list = []
    
    # Счёт игрока - сколько очков набрано
    score = 0
    
    # Количество жизней - начинаем с 3
    lives = 3

    # Генерируем случайное количество мусора 
    debris_count = random.randint(20, 150)
    
    # Создаём армию мусора с этим случайным количеством
    control.create_musor_army(screen, musor_list, debris_count)

    # Шрифт для крупного текста (например, GAME OVER)
    font = pygame.font.Font(None, 72)
    
    # Шрифт для мелкого текста (счёт, жизни)
    smal_font = pygame.font.Font(None, 36)
    
    # Флаг окончания игры - False значит играем, True значит игра закончена
    game_over = False
    
    # Флаг паузы - False значит играем, True значит игра на паузе
    paused = False

    # ГЛАВНЫЙ ИГРОВОЙ ЦИКЛ - здесь происходит всё самое интересное
    while True:
        # Получаем все события от игрока (нажатия клавиш, закрытие окна и т.д.)
        events = pygame.event.get()
        
        # Обрабатываем каждое событие по очереди
        for event in events:
            # Если игрок нажал крестик закрытия окна
            if event.type == pygame.QUIT:
                pygame.quit()   # Закрываем pygame
                sys.exit()      # Полностью выходим из программы
                
            # Если игрок нажал какую-либо клавишу на клавиатуре
            elif event.type == pygame.KEYDOWN:
                # Проверяем, какая именно клавиша нажата
                
                # Если нажата клавиша R 
                if event.key == pygame.K_r:
                    # Перезапускаем игру только если не на паузе и игра не окончена
                    if not paused and not game_over:
                        game_over = False      # Игра продолжается
                        paused = False         # Снимаем паузу
                        lazers = []            # Очищаем список лазеров
                        musor_list = []        # Очищаем список мусора
                        score = 0              # Обнуляем счёт
                        lives = 3              # Восстанавливаем 3 жизни
                        pyshka = Pyshka(screen)  # Создаём новую пушку
                        debris_count = random.randint(20, 50)  # Новое случайное количество мусора
                        control.create_musor_army(screen, musor_list, debris_count)  # Создаём армию
                        
                # Если нажата клавиша ESC
                elif event.key == pygame.K_ESCAPE:
                    # Если игра уже окончена, ESC закрывает программу
                    if game_over:
                        pygame.quit()
                        sys.exit()
                    else:
                        # Если игра идёт, ESC переключает паузу 
                        paused = not paused

        # Если игра не окончена
        if not game_over:
            # Если игра не на паузе
            if not paused:
                # Передаём управление в функцию do_it 
                control.do_it(pyshka, lazers, events)
                
                # Обновляем позицию пушки (движение влево/вправо)
                pyshka.update()

                # Обновляем позиции всех лазеров и удаляем улетевшие за экран
                for i in lazers[:]:
                    i.update()    
                    # Если лазер улетел за верхнюю или нижнюю границу экрана
                    if i.is_offscreen(800):
                        lazers.remove(i)   # Удаляем его из списка

                # Обновляем позиции всего мусора (он летит вниз)
                control.update_musor_army(musor_list)
                
                # ПРОВЕРКА: не улетел ли мусор за нижнюю границу экрана
                # Проходим по копии списка, чтобы безопасно удалять
                for musor_item in musor_list[:]:
                    # Если мусор упал ниже 800 пикселей 
                    if musor_item.rect.y > 800:
                        musor_list.remove(musor_item)   # Удаляем этот мусор
                        lives -= 1                      # Отнимаем одну жизнь
                        
                        # Если жизни кончились - игра окончена
                        if lives <= 0:
                            game_over = True
                            break
                        else:
                            # Если жизни ещё есть - создаём новую армию вместо улетевшего мусора
                            debris_count = random.randint(20, 50)
                            musor_list.clear()                                # Очищаем старый мусор
                            control.create_musor_army(screen, musor_list, debris_count)  # Создаём новую армию
                            break   # Выходим из цикла, чтобы не проверять дальше

                # Добавляем очки за уничтоженный лазерами мусор
                score += control.chek_musor(lazers, musor_list)

                # ПРОВЕРКА: столкновение мусора с кораблём
                collision = False   # Флаг: было ли столкновение
                # Проверяем каждый объект мусора
                for musor_item in musor_list[:]:
                    # Условие пересечения прямоугольников мусора и пушки
                    if (musor_item.rect.x < pyshka.rect.x + pyshka.rect.width and      # Левый край мусора левее правого края пушки
                        musor_item.rect.x + musor_item.rect.width > pyshka.rect.x and  # Правый край мусора правее левого края пушки
                        musor_item.rect.y < pyshka.rect.y + pyshka.rect.height and     # Верхний край мусора выше нижнего края пушки
                        musor_item.rect.y + musor_item.rect.height > pyshka.rect.y):   # Нижний край мусора ниже верхнего края пушки
                        collision = True    # Столкновение произошло!
                        break               # Выходим из цикла, достаточно одного столкновения
                
                # Если было столкновение
                if collision:
                    lives -= 1   # Отнимаем жизнь
                    
                    # Если жизни кончились - игра окончена
                    if lives <= 0:
                        game_over = True
                    else:
                        # Если жизни ещё есть - очищаем старую армию и создаём новую
                        musor_list.clear()
                        debris_count = random.randint(20, 50)
                        control.create_musor_army(screen, musor_list, debris_count)

                # ПРОВЕРКА: если весь мусор уничтожен (лазерами), создаём новую армию
                if len(musor_list) == 0 and not game_over:
                    debris_count = random.randint(5, 100)   # Случайное количество от 5 до 100
                    control.create_musor_army(screen, musor_list, debris_count)

                # НАЧИНАЕМ ОТРИСОВКУ ВСЕГО НА ЭКРАНЕ
                
                # Заливаем фон чёрным цветом (стираем всё, что было нарисовано в прошлом кадре)
                screen.fill(bg_color)
                
                # Рисуем пушку на экране
                pyshka.output()

                # Рисуем все лазеры
                for i in lazers:
                    i.draw(screen)

                # Рисуем весь мусор
                for musor_item in musor_list:
                    musor_item.draw()

                # Отображаем счёт игрока в левом верхнем углу
                score_text = smal_font.render(f"Счёт: {score}", True, (255, 255, 255))
                screen.blit(score_text, (10, 10))
                
                # Отображаем количество жизней ниже счёта (красным цветом)
                lives_text = smal_font.render(f"Жизни: {lives}", True, (255, 0, 0))
                screen.blit(lives_text, (10, 50))
            
            else:
                # РЕЖИМ ПАУЗЫ - игра не активна, показываем затемнённый экран с надписью
                
                # Заливаем фон чёрным
                screen.fill(bg_color)
                
                # Создаём полупрозрачную поверхность для затемнения экрана
                paused_surface = pygame.Surface((700, 800))
                paused_surface.set_alpha(128)    # Полупрозрачность (0 - прозрачный, 255 - непрозрачный)
                paused_surface.fill((0, 0, 0))   # Заливаем чёрным
                screen.blit(paused_surface, (0, 0))   # Накладываем затемнение на весь экран

                # Большая надпись "ПАУЗА" по центру
                paused_text = font.render("ПАУЗА", True, (255, 255, 255))
                paused_rect = paused_text.get_rect(center=(350, 200))
                screen.blit(paused_text, paused_rect)

                # Подсказка для игрока, как снять паузу
                pod_text = smal_font.render("Нажмите ESC для продолжения", True, (255, 255, 255))
                pod_rect = pod_text.get_rect(center=(350, 300))
                screen.blit(pod_text, pod_rect)
                
                # Показываем текущий счёт на экране паузы
                score_on_pause = smal_font.render(f"Счёт: {score}", True, (255, 255, 255))
                score_on_pause_rect = score_on_pause.get_rect(center=(350, 400))
                screen.blit(score_on_pause, score_on_pause_rect)
                
                # Показываем количество жизней на экране паузы
                lives_on_pause = smal_font.render(f"Жизни: {lives}", True, (255, 0, 0))
                lives_on_pause_rect = lives_on_pause.get_rect(center=(350, 450))
                screen.blit(lives_on_pause, lives_on_pause_rect)
            
        else:
            # ЭКРАН GAME OVER - игра завершена
            
            # Заливаем фон чёрным
            screen.fill(bg_color)
            
            # Большая красная надпись "GAME OVER" в верхней части экрана
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(350, 150))
            screen.blit(game_over_text, game_over_rect)

            # Показываем финальный счёт игрока
            final_score_text = smal_font.render(f"Ваш счёт: {score}", True, (255, 255, 255))
            final_score_rect = final_score_text.get_rect(center=(350, 250))
            screen.blit(final_score_text, final_score_rect)
            
            # Инструкция для игрока: как перезапустить игру или выйти
            restart_text = smal_font.render("Нажмите R для перезапуска или ESC для выхода", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(350, 350))
            screen.blit(restart_text, restart_rect)

        # Обновляем экран - показываем всё, что нарисовали
        # Без этой строки ничего не будет видно на экране!
        pygame.display.flip()

# Запускаем игру - это точка входа
run()