import json
import sys
from units import Player, Enemy
from config import *

pygame.font.init()
pygame.init()

mouse_pos = pygame.mouse.get_pos()
keys = pygame.key.get_pressed()


def main_game():
    run = True
    lost = False
    lives = 10
    wave = 0
    score = 0

    enemy_speed = 4
    projectile_speed = 7

    enemies = []
    wave_length = 4

    clock = pygame.time.Clock()
    player = Player()

    def update():

        screen.blit(background, (0, 0))
        lives_label = main_font.render(str(lives), True, (255, 255, 255))
        wave_label = main_font.render(str(wave), True, (255, 255, 255))
        score_label = main_font.render(str(score), True, (255, 255, 255))

        screen.blit(stats_bg, (800, 33))
        screen.blit(score_label, (820, 42))
        screen.blit(score_symbol_high, (955, 12))
        screen.blit(stats_bg, (WIDTH - 490, 33))
        screen.blit(lives_label, (WIDTH - 470, 42))
        screen.blit(hp_symbol, (WIDTH - 330, 25))
        screen.blit(stats_bg, (190, 33))
        screen.blit(wave_label, (210, 42))

        for enemy in enemies:
            enemy.draw(screen)

        player.draw(screen)
        player.move()
        pygame.display.update()

    while run:
        clock.tick(FPS)
        update()
        lost_score_label_two = lost_font.render(f"{score}", True, (255, 255, 255))

        if lives <= 0:
            lost = True
            player_name = " "
            screen.blit(lost_screen, (0, 0))
            qoute()
            screen.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 200))
            screen.blit(lost_score_label, (WIDTH / 2 - lost_score_label.get_width() / 2, 600))
            screen.blit(lost_score_label_two, (WIDTH / 2 - lost_score_label_two.get_width() / 2, 700))
            screen.blit(return_key, (1700, 850))
            high_score = {}
            high_score["Scores"] = []
            high_score["Scores"].append({
                "Score": score
            })
            with open("highscore.json", "a+") as high_score_file:
                json.dump(high_score, high_score_file)
                high_score_file.write("\n")

        while lost:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        main_menu()
                        lost = False

            pygame.display.update()

        if len(enemies) == 0:
            wave += 1
            wave_length += 1
            for enemy in range(wave_length):
                enemy = Enemy()
                score = score + wave * 3
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                player.shoot()
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot()
            if keys[pygame.K_ESCAPE]:
                main_menu()

        for enemy in enemies[:]:
            enemy.move(enemy_speed, screen)

            if enemy.x <= 300:
                lives -= 1
                score += wave * 3 * - 1
                enemies.remove(enemy)

        player.projectile_control(projectile_speed, enemies)


def main_menu():
    run_mm = True
    screen.blit(mm_background, (0, 0))
    main_menu_label = menu_font.render("MAIN MENU", True, (0, 0, 0))
    screen.blit(main_menu_label, (240, 350))
    screen.blit(menu_item, (200, 500))
    high_score_label = menu_font.render("HIGH SCORE", True, (255, 255, 255))
    screen.blit(high_score_label, (235, 550))
    screen.blit(menu_item, (200, 700))

    screen.blit(menu_item, (200, 900))
    quit_label = menu_font.render("QUIT", True, (255, 0, 0))
    screen.blit(quit_label, (330, 950))
    high_scores_as_list = []

    hs_list = []
    for line in open("highscore.json", "r"):
        high_scores_as_list.append(json.loads(line))
        for item in high_scores_as_list:
            item_dict = item
            for key, value in item_dict.items():
                itemvalue = value
                for item_two in itemvalue:
                    i = item_two
                    for key, value in i.items():
                        hs_list.append(value)
                        hs_list.sort(reverse=True)
                        hs_list = list(dict.fromkeys(hs_list))

    while run_mm:
        mouse_pos = pygame.mouse.get_pos()
        show_high_score = False

        btn_x = 200
        btn_y = 500
        high_score_txt = "HIGH SCORES!"
        high_score_label = hs_font.render(high_score_txt, True, (0, 0, 0))
        high_score_failed = "Now dont you go snoopin where you dont belong! Play the game first cheif!"
        high_score_failed_label = menu_font.render(high_score_failed, True, (0, 0, 0))
        button(btn_x, btn_y, "Start Game", (255, 250, 250), (255, 0, 0))
        btn_y_2 = btn_y + 200
        button(btn_x, btn_y_2, "High Score", (255, 250, 250), (255, 0, 0))
        btn_y_3 = btn_y_2 + 200
        button(btn_x, btn_y_3, "QUIT", (255, 50, 50), (255, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_x <= mouse_pos[0] <= btn_x + 400:
                    if btn_y <= mouse_pos[1] <= btn_y + 150:
                        main_game()
                    elif btn_y_2 <= mouse_pos[1] <= btn_y_2 + 150:
                        show_high_score = True
                    elif btn_y_3 <= mouse_pos[1] <= btn_y_3 + 150:
                        run_mm = False
                        pygame.quit()
                        sys.exit()

        while show_high_score:
            screen.blit(lost_screen, (0, 0))

            try:
                screen.blit(high_score_label, (1200, 100))
                x = 1400
                y = 200
                local_num = 1
                high_score_to_display = hs_list[0:10]
                for value in high_score_to_display:
                    full_score = f"{local_num} : {value}"
                    score_label = main_font.render(full_score, True, (0, 0, 0))
                    screen.blit(score_label, (x, y))
                    local_num += 1
                    y += 80

            except:
                screen.blit(high_score_failed_label, (30, 200))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    show_high_score = False
                    main_menu()
                pygame.display.update()

        pygame.display.update()


def button(x, y, text_to_display, inactive, active):
    btn_texts = text_to_display
    image = menu_item
    width = image.get_width()
    height = image.get_height()
    screen.blit(image, (x, y))

    try:
        if x <= mouse_pos[0] <= x + 400:
            if y <= mouse_pos[1] <= y + 150:
                btn_texts = menu_font.render(btn_texts, True, active)
        else:
            btn_texts = menu_font.render(btn_texts, True, inactive)
    except:
        btn_texts = menu_font.render(btn_texts, True, inactive)
    screen.blit(btn_texts, (width - x/2 - 30, y + 50))


main_menu()
