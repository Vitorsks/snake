import random
import pygame
from sys import exit
import pygame.math


class SNAKE:
    def __init__(self):
        self.body = [pygame.math.Vector2(5, 10), pygame.math.Vector2(4, 10), pygame.math.Vector2(3, 10)]
        self.direct = pygame.math.Vector2(0, 0)
        self.new_body = False
        self.meat2 = MEAT2()

    def draw_snake(self):
        for elem in self.body:
            x_pos = elem.x * cell_size
            y_pos = elem.y * cell_size
            elem_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (50, 200, 200), elem_rect)

    def move(self):
        if self.new_body:
            body_copy = self.body[:]
            if self.body[0] == self.meat2.pos:
                # Bonus level
                for i in range(4):
                    body_copy.insert(0, body_copy[0] + self.direct)
            else:
                body_copy.insert(0, body_copy[0] + self.direct)
            self.body = body_copy[:]
            self.new_body = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direct)
            self.body = body_copy[:]

    def add_body(self):
        self.new_body = True

    def reset(self):
        self.body = [pygame.math.Vector2(5, 10), pygame.math.Vector2(4, 10), pygame.math.Vector2(3, 10)]
        self.direct = pygame.math.Vector2(0, 0)


class MEAT:
    def __init__(self):
        self.pos = None
        self.y = None
        self.x = None
        self.random_meat_position()

    def draw_meat(self):
        meat_recta = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(meat_image, meat_recta)
        # pygame.draw.rect(screen, (200, 0, 0), meat_recta,)

    def random_meat_position(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = pygame.math.Vector2(self.x, self.y)


class MEAT2:
    def __init__(self):
        self.pos = None
        self.y = None
        self.x = None
        self.random_meat_position()

    def draw_meat(self):
        meat2_recta = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(meat2_image, meat2_recta)
        # pygame.draw.rect(screen, (200, 0, 0), meat_recta,)

    def random_meat_position(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = pygame.math.Vector2(self.x, self.y)


class GAME:
    def __init__(self):
        self.snake = SNAKE()
        self.meat = MEAT()
        self.meat2 = MEAT2()
        # Bonus levels
        self.bonus = (5, 10, 15, 20, 25, 30, 35, 40, 45, 50)

    def game_over(self):
        self.snake.reset()

    def update(self):
        self.snake.move()
        self.check_colision()
        self.check_fails()

    def draw_elem(self):
        self.meat.draw_meat()
        if (len(self.snake.body) - 3) in self.bonus:
            self.meat2.draw_meat()
        self.snake.draw_snake()
        self.draw_score()

    def check_colision(self):
        if self.snake.body[0] == self.meat.pos:
            self.meat.random_meat_position()
            self.snake.add_body()
        if self.snake.body[0] == self.meat2.pos:
            self.snake.add_body()

    def check_fails(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for elem in self.snake.body[1:]:
            if elem == self.snake.body[0]:
                self.game_over()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = (cell_size * cell_number - 100)
        score_y = (cell_size * cell_number - 60)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)


pygame.init()
cell_size = 20
cell_number = 40
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
meat_image = pygame.image.load("img\morango.jpg").convert_alpha()
meat2_image = pygame.image.load("img\cereija.jpg").convert_alpha()
game_font = pygame.font.Font(None, 30)
# snake_image = pygame.image.load("").convert_alpha()
pygame.display.set_caption("SNAKE")

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

main_game = GAME()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                main_game.snake.direct = pygame.math.Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                main_game.snake.direct = pygame.math.Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                main_game.snake.direct = pygame.math.Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                main_game.snake.direct = pygame.math.Vector2(1, 0)
    screen.fill((150, 240, 50))
    main_game.draw_elem()
    pygame.display.update()
    clock.tick(60)
