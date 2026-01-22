import sys

import pygame
from pygame.locals import *

from core.cookie import Cookie
from core.generator import Generator
from core.buttonpanel import ButtonPanel

from core.funcs import *
from core.util.get_coords import get_coords
import core.config as cc

#============================================================
# Initializing pygame

pygame.init()
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("sysfont", 24)

# Sprites
sprites = {
    "cookie" : pygame.image.load(f"{cc.SPRITES["cookie"]}"),
    "cursor" : pygame.image.load(f"{cc.SPRITES["cursor"]}"),
}

# Game window
WIDTH, HEIGHT = cc.RESOLUTION
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(cc.WINDOW_NAME)
pygame.display.set_icon(sprites["cookie"])
background = pygame.Surface(SCREEN.get_size())
background = background.convert()
background.fill(cc.COLOR["bg_blue"])

#============================================================
# Prepping gamestate

game_state = load()
running = True

#============================================================
# Initializing assets

#-- cookie button
cookie = Cookie(
    size = WIDTH * 0.1, # 80px on 800x600 screen
    pos = (WIDTH*0.15, HEIGHT*0.5),
    sprite = pygame.image.load("sprites/cookie.png").convert_alpha()
    )

#-- generator buttons
buy_panel = ButtonPanel(
    (WIDTH * 0.67, HEIGHT * 0.02),
    (WIDTH * 0.32, HEIGHT * 0.96),
    color = cc.COLOR["d_gray"])

cursor = Generator(
    panel = buy_panel,
    order = 1,
    text = "Cursor",
    base_price = 15,
    cps = 0.1,
    sprite = sprites["cursor"]
    )
cursor.base_upgrade_price = 100 # in base game it deviates from the formula

grandma = Generator(
    panel=buy_panel,
    order=2,
    text = "Grandma",
    base_price = 100,
    cps = 1,
    )
farm = Generator(
    panel=buy_panel,
    order=3,
    text = "Farm",
    base_price = 1100,
    cps = 8,
    )
mine = Generator(
    panel=buy_panel,
    order=4,
    text = "Mine",
    base_price = 12000,
    cps = 47,
    )
factory = Generator(
    panel=buy_panel,
    order=5,
    text = "Factory",
    base_price = 130000,
    cps = 260,
    )
bank = Generator(
    panel=buy_panel,
    order=6,
    text = "Bank",
    base_price = 1400000,
    cps = 1400,
    )
temple = Generator(
    panel=buy_panel,
    order=7,
    text = "Temple",
    base_price = 20000000,
    cps = 7800,
    )

generators = [cursor, grandma, farm, mine, factory, bank, temple]

#-- generator sprites

#============================================================

# Game-run loop
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            # add keybinds here
            if event.key == K_1:
                game_state["cookies"] += cheat_cookies()
                game_state["stats"]["total_cookies_earned"] += cheat_cookies()

            if event.key == K_c:
                get_coords(WIDTH, HEIGHT)

        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            mouse_button = event.button

            shift_held = pygame.key.get_mods() & pygame.KMOD_SHIFT

            # left-click
            if mouse_button == 1 or mouse_button == 3:
                for button in generators:
                    if button.buy_is_clicked(mouse_pos):
                        if shift_held:
                            button.buy_max()
                        else:
                            button.buy()
                    if button.upgrade_is_clicked(mouse_pos):
                        if cc.DEBUG:
                            print(f"{button.text} upgrade clicked")
                            print("current level: ",button.level, "|", game_state["generators"][button.text]["level"])
                            print("current upgrade price: ", button.upgrade_price())
                        button.upgrade()

                if cookie.is_clicked(mouse_pos):
                    cookie.click()
                    game_state["stats"]["total_clicks"] += 1
                    game_state["stats"]["total_cookies_earned"] += 1

    delta_time = clock.tick(cc.FPS) / 1000.0

    # Generation
    cps = calculate_cps()
    game_state["cookies"] += cps / cc.FPS
    game_state["stats"]["total_cookies_earned"] += cps / cc.FPS

    # Display
    SCREEN.blit(background, (0, 0))

    #-- cookie
    cookie.update_sprite(delta_time)
    cookie.draw()
    draw_text(
        f"Cookies: {custom_format(game_state["cookies"], decimals=3)}",
        font_size=36, font_color="white",
        center=(cookie.pos[0], cookie.pos[1] - cookie.base_radius * 2),
    )
    draw_text(
        f"{cps:,.1f} per second",
        font_size=24, font_color="white",
        center=(cookie.pos[0], cookie.pos[1] - cookie.base_radius * 1.75),
    )

    #-- generator buttons
    buy_panel.draw()
    draw_text(
        "Generators",
        font_size=56, font_color="white",
        center=(
            buy_panel.pos[0] + buy_panel.size[0] * 0.5,
            (buy_panel.pos[1] + buy_panel.size[1] * 0.05)
        ))

    for generator in generators:
        # Buy button
        generator.draw_buy_button()
        #-- sprites
        if generator.sprite is not None:
            generator.draw(
                pos=(generator.rect1pos[0] + generator.rect1size[0] * 0.1, generator.rect1pos[1] + generator.rect1size[1] * 0.5),
                scale=(2, 2)
            )

        if generator.buy_price() > game_state["cookies"]: # grays out generators that are too expensive
            generator.button1_color = cc.COLOR["gray"]
        else:
            generator.button1_color = cc.COLOR["l_gray"]

        # Upgrade button
        if generator.count >= 1:
            generator.draw_upgrade_button()

        if generator.upgrade_price() > game_state["cookies"] or generator.count < 1:
            generator.button2_color = cc.COLOR["gray"]
        elif generator.level >= 4:
            generator.button2_color = cc.COLOR["l_green"]
        else:
            generator.button2_color = cc.COLOR["l_gray"]

    pygame.display.update()

#============================================================

save(game_state)
pygame.quit()
sys.exit()