import pygame
import os
import random

pygame.font.init()
pygame.init()
WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Island Invaders")
FPS = 60

# Fonts
main_font = pygame.font.SysFont("ForgottenDream.otf", 50)
hs_font = pygame.font.SysFont("ForgottenDream.otf", 100, True)
menu_font = pygame.font.SysFont("ForgottenDream.otf", 75)
lost_font = pygame.font.SysFont("ForgottenDream.otf", 70)
qoute_font = pygame.font.SysFont("ForgottenDream.otf", 70)

# Labels
lost_label = lost_font.render("Bring bigger guns next time!", True, (50, 55, 55))
lost_score_label = lost_font.render("Your final score:", True, (55, 55, 55))


# Backgrounds
mm_background = pygame.image.load(os.path.join("assets", "mm_bg.jpg")).convert()
background = pygame.image.load(os.path.join("assets", "background.jpg")).convert()
stats_bg = pygame.image.load(os.path.join("assets", "score_hp_background.png")).convert_alpha()
menu_item = pygame.image.load(os.path.join("assets", "menu_btn.png")).convert_alpha()
lost_screen = pygame.image.load(os.path.join("assets", "lostscreen.png")).convert()

# Score Symbols
score_symbol_low = pygame.image.load(os.path.join("assets", "score_symbol_low.png")).convert_alpha()
score_symbol_mid = pygame.image.load(os.path.join("assets", "score_symbol_mid.png")).convert_alpha()
score_symbol_high = pygame.image.load(os.path.join("assets", "score_symbol_high.png")).convert_alpha()

# Health symbol
hp_symbol = pygame.image.load(os.path.join("assets", "hpSymbol.png")).convert_alpha()

# Return Key
return_key = pygame.image.load(os.path.join("assets", "return_key.png")).convert_alpha()

# Player and player projectiles:
player_tower = pygame.image.load(os.path.join("assets/towers", "ct1.png")).convert_alpha()
player_tower_base = pygame.image.load(os.path.join("assets/towers", "tower_base.png")).convert_alpha()
projectile_image_one = pygame.image.load(os.path.join("assets/projectiles", "projectileOneOne.png")).convert_alpha()

# Enemies and their explosions:
enemy_explosion = pygame.image.load(os.path.join("assets", "explosion.png")).convert_alpha()
red_ship = pygame.image.load(os.path.join("assets/enemies/red_ship", "enemyOne.png")).convert_alpha()
orange_ship = pygame.image.load(os.path.join("assets/enemies/orange_ship", "enemyTwo.png")).convert_alpha()

# Lost qoutes:
qoutes = {
    "butbut": "But but, its not only only",
    "empty cup": "Its better with a full cup then an empty cup... unless your boat is sinking",
    "fart": "Its not the fart that kills you... its the smell"
}

q_one = qoute_font.render("Bring bigger guns next time!", True, (255, 255, 255))
q_two = qoute_font.render("But, but its not only only!", True, (255, 255, 255))
q_three = qoute_font.render("Its not the fart that kills you, its the smell", True, (255, 255, 255))


def qoute():

    qoutes = {
        "end_one": q_one,
        "end_two": q_two,
        "end_three": q_three
    }
    qoute_time = 0
    qoute_time += 1
    if qoute_time == 1:
        qoute_choice = random.choice(["end_one", "end_two", "end_three"])
        screen.blit(qoutes[qoute_choice], (50, 900))
