import pygame
import random
import time

# === Настройки игры ===
WIDTH = 640
HEIGHT = 480
BLOCK_SIZE = 20
FPS = 15

# === Цвета ===
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# === Направления ===
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
    
    def get_head_position(self):
        return self.positions[0]
    
    def update_direction(self, new_dir):
        # Запрещаем разворот на 180 градусов
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir
    
    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new_pos = ((cur[0] + (x * BLOCK_SIZE)), (cur[1] + (y * BLOCK_SIZE)))
        
        # Проверка на столкновение с собой
        if new_pos in self.positions[2:]:
            self.reset()
            return False
            
        self.positions.insert(0, new_pos)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True
    
    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, 
                           (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))