# buttonpanel.py
import pygame

class ButtonPanel:
    def __init__(self, pos, size, color="white"):
        """
        pos: (x, y) top-left corner
        size: (width, height)
        color: RGB tuple
        """
        self.pos = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)
        self.color = color

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def draw(self):
        from run import SCREEN
        pygame.draw.rect(SCREEN, self.color, self.rect)