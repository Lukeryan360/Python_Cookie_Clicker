# get_coords.py
import pygame

def get_coords(width, height):
    x, y = pygame.mouse.get_pos()
    rel_x = x / width
    rel_y = y / height
    print(f"Cursor position: ({x}, {y})")
    print(f"Relative position: ({rel_x:.2f}, {rel_y:.2f})")
