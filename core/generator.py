import pygame

import core.config as cc
import core.funcs as cf


class Generator:
    def __init__(self, panel, order, text, base_price, cps, sprite = None):
        from run import game_state
        self.panel = panel
        self.order = order
        self.text = text
        self.base_price = base_price
        self.cps = cps
        self.sprite = sprite

        self.count = game_state["generators"][text]["owned"]
        self.level = game_state["generators"][text]["level"]
        self.base_upgrade_price = 10 * base_price
        self.button1_color = cc.COLOR["l_gray"]
        self.button2_color = cc.COLOR["l_gray"]

        # Buy button
        self.rect1size = [panel.size[0] * 0.7, panel.size[1] * 0.08]
        self.rect1pos = (
            panel.pos[0] + panel.size[0] * 0.03,
            panel.pos[1] + panel.size[1] * 0.1 * order
        )
        self.rect1 = pygame.Rect(self.rect1pos[0], self.rect1pos[1], self.rect1size[0], self.rect1size[1])

        # Upgrade button
        self.rect2size = [panel.size[1] * 0.13, panel.size[1] * 0.08]
        self.rect2pos = (
            panel.pos[0] + panel.size[0] * 0.75,
            panel.pos[1] + panel.size[1] * 0.1 * order
        )
        self.rect2 = pygame.Rect(self.rect2pos[0], self.rect2pos[1], self.rect2size[0], self.rect2size[1])

    def draw(self, pos, scale):
        """
        Draws the generator sprite at the given position with the given scale factor.
        """
        from run import SCREEN

        # Handle uniform or non-uniform scaling
        if isinstance(scale, (int, float)):
            width = int(self.sprite.get_width() * scale)
            height = int(self.sprite.get_height() * scale)
        else:
            width = int(self.sprite.get_width() * scale[0])
            height = int(self.sprite.get_height() * scale[1])

        scaled_image = pygame.transform.scale(self.sprite, (width, height))
        rect = scaled_image.get_rect(center=pos)
        SCREEN.blit(scaled_image, rect)

    def draw_buy_button(self):
        from run import SCREEN
        # button box
        pygame.draw.rect(SCREEN, self.button1_color, self.rect1, 0)
        # text
        cf.draw_text(
            f"{self.text} ({cf.custom_format(self.count)} | Cost: {cf.custom_format(self.buy_price())})",
            font_size=24,
            font_color="black",
            center=(
            self.rect1pos[0] + self.rect1size[0] * 0.5,
            self.rect1pos[1] + self.rect1size[1] * 0.5
            ),
        )

    def draw_upgrade_button(self):
        from run import SCREEN
        # button box
        pygame.draw.rect(SCREEN, self.button2_color, self.rect2, 0)
        # text
        cf.draw_text(
            f"L{self.level - 1}", # technically false, shift later
            font_size=36,
            font_color="black",
            center=(
                self.rect2pos[0] + self.rect2size[0] * 0.5,
                self.rect2pos[1] + self.rect2size[1] * 0.35
            ),
        )
        _text = f"L{self.level}: {cf.custom_format_2(self.upgrade_price())}" if self.level < 4 else "MAX"
        cf.draw_text(
            text= _text,
            font_size=24,
            font_color="black",
            center=(
                self.rect2pos[0] + self.rect2size[0] * 0.5,
                self.rect2pos[1] + self.rect2size[1] * 0.65
            ),
        )

    def total_cps(self):
        return self.count * self.cps * 2**(self.level - 1)

    def buy_price(self):
        return round(self.base_price * 1.15**self.count)

    def upgrade_price(self):
        if self.level == 1:
            return self.base_upgrade_price
        elif self.level == 2:
            return self.base_upgrade_price * 5
        elif self.level == 3:
            return self.base_upgrade_price * 10
        else:
            return 0

    def buy_is_clicked(self, point):
        return self.rect1.collidepoint(point)

    def upgrade_is_clicked(self, point):
        return self.rect2.collidepoint(point)

    def buy(self): # Buy one generator
        from run import game_state
        price = self.buy_price()
        if game_state["cookies"] >= price:
            self.count += 1
            game_state["cookies"] -= price
            game_state["generators"][f"{self.text}"]["owned"] += 1

    def buy_max(self): # Keep buying generators while we have enough cookies
        from run import game_state

        while True:
            price = self.buy_price()
            if game_state["cookies"] >= price:
                self.count += 1
                game_state["cookies"] -= price
                game_state["generators"][f"{self.text}"]["owned"] += 1
            else:
                break

    def upgrade(self):
        from run import game_state
        price = self.upgrade_price()
        if game_state["cookies"] >= price:
            if self.level == 1 and game_state["generators"][f"{self.text}"]["owned"] >= 1:
                game_state["cookies"] -= price
                self.level = game_state["generators"][f"{self.text}"]["level"] = 2
            elif self.level == 2 and game_state["generators"][f"{self.text}"]["owned"] >= 5:
                game_state["cookies"] -= price
                self.level = game_state["generators"][f"{self.text}"]["level"] = 3
            elif self.level == 3 and game_state["generators"][f"{self.text}"]["owned"] >= 25:
                game_state["cookies"] -= price
                self.level = game_state["generators"][f"{self.text}"]["level"] = 4