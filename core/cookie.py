import math
import pygame

import core.config as cc

class Cookie:
    def __init__(self, size, pos, sprite):
        self.radius = self.base_radius = size
        self.pos = pygame.Vector2(pos)
        self.sprite = sprite

        # --- animation state ---
        self.bounce_time = 0.0
        self.bounce_duration = cc.BOUNCE_DURATION
        self.bounce_active = False

        self.bounce_amplitude = cc.BOUNCE_AMPLITUDE
        self.bounce_decay = cc.BOUNCE_DECAY
        self.bounce_frequency = cc.BOUNCE_FREQUENCY

        # --- sprite coordinates ---
        diameter = self.base_radius * 2
        self.base_sprite = pygame.transform.smoothscale(
            self.sprite, (diameter, diameter)
        )
        self.sprite = self.base_sprite
        self.rect = self.sprite.get_rect(center=self.pos)

    def draw(self):
        from run import SCREEN
        self.rect.center = self.pos
        SCREEN.blit(self.sprite, self.rect)

    def is_clicked(self, point):
        mouse_vec = pygame.Vector2(point)
        return mouse_vec.distance_squared_to(self.pos) <= self.radius ** 2 # circular hitbox

    def click(self):
        from run import game_state
        game_state["cookies"] += 2**(game_state["upgrades"]["click"]["level"] - 1)
        # initiate animation
        self.bounce_time = 0.0
        self.bounce_active = True

    # animation
    def update_sprite(self, dt):
        if not self.bounce_active:
            return

        self.bounce_time += dt
        t = self.bounce_time

        if t > self.bounce_duration:
            self.bounce_active = False
            self.radius = self.base_radius
            self.sprite = self.base_sprite
            self.rect = self.sprite.get_rect(center=self.pos)
            return

        scale = 1 + (
                self.bounce_amplitude *
                math.exp(-self.bounce_decay * t) *
                math.sin(self.bounce_frequency * t - math.pi / 2)
        )

        self.radius = self.base_radius * scale

        diameter = int(self.radius * 2)
        self.sprite = pygame.transform.smoothscale(
            self.base_sprite, (diameter, diameter)
        )

        # 🔑 Recreate rect from the NEW sprite
        self.rect = self.sprite.get_rect(center=self.pos)
