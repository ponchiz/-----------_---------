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
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
    
    def reset(self):
        self.change_direction()

    def change_direction(self):
        if self.direction == UP:
            self.direction = DOWN
        elif self.direction == DOWN:
            self.direction = UP
        elif self.direction == LEFT:
            self.direction = RIGHT
        else:
            self.direction = LEFT
    
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
            
class Food:
    def __init__(self):
        self.color = RED
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (
            random.randint(0, (WIDTH-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE,
            random.randint(0, (HEIGHT-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        )
    
    def check_position(self, snake_positions):
        while self.position in snake_positions:
            self.randomize_position()
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color,
                        (self.position[0], self.position[1],
                         BLOCK_SIZE, BLOCK_SIZE))

def draw_score(surface, score):
    font = pygame.font.SysFont('arial', 30)
    text = font.render(f"Очки: {score}", True, WHITE)
    surface.blit(text, (10, 10))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Змейка - Парное программирование")
    clock = pygame.time.Clock()
    
    snake = Snake()
    food = Food()
    score = 0
    
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.update_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.update_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.update_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.update_direction(RIGHT)
        
        # Игровая логика
        if not snake.move():
            score = 0  # Сброс при столкновении
        
        # Сбор еды
        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1
            food.randomize_position()
            food.check_position(snake.positions)
        
        # Проверка границ
        head = snake.get_head_position()
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            snake.reset()
        
        # Отрисовка
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        draw_score(screen, score)
        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()