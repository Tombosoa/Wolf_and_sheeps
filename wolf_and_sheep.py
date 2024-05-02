import pygame
import random
import math
import time

DIRECTIONS = ('up', 'down', 'left', 'right', 'up_left', 'up_right', 'down_left', 'down_right')

class Sheep:
    def __init__(self, x, y, speed=0.1):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction_index = random.randint(0, len(DIRECTIONS) - 1)
        self.max_speed = 1.0
        self.min_speed = 0.1
        self.fleeing = False
        self.image = pygame.transform.scale(pygame.image.load("sheep.png"), (60, 60))
        self.stop_chance = 0.02  
        self.stop_duration = 20
        self.stop_counter = 0 

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def walk(self):
        if self.stop_counter > 0:
            self.stop_counter -= 1
            return

        direction = DIRECTIONS[self.direction_index]
        if direction == 'up':
            self.y -= self.speed
        elif direction == 'down':
            self.y += self.speed
        elif direction == 'left':
            self.x -= self.speed
        elif direction == 'right':
            self.x += self.speed
        elif direction == 'up_left':
            self.x -= self.speed
            self.y -= self.speed
        elif direction == 'up_right':
            self.x += self.speed
            self.y -= self.speed
        elif direction == 'down_left':
            self.x -= self.speed
            self.y += self.speed
        elif direction == 'down_right':
            self.x += self.speed
            self.y += self.speed

    def check_limits(self, width, height):
        if self.x < 0 or self.x > width - 10:
            self.direction_index = random.randint(0, len(DIRECTIONS) - 1)
            self.x = min(max(self.x, 0), width - 10)
        if self.y < 0 or self.y > height - 10:
            self.direction_index = random.randint(0, len(DIRECTIONS) - 1)
            self.y = min(max(self.y, 0), height - 10)

    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    def scare(self):
        self.fleeing = True
        self.speed = self.max_speed

    def calm(self):
        self.fleeing = False
        self.speed = self.min_speed

    def flee(self, wolf, width, height):
        vector_x = self.x - wolf.x
        vector_y = self.y - wolf.y

        magnitude = math.sqrt(vector_x ** 2 + vector_y ** 2)

        if magnitude != 0:
            vector_x /= magnitude
            vector_y /= magnitude

        if vector_x > 0:
            self.direction_index = random.choice([0, 4, 5]) 
        else:
            self.direction_index = random.choice([1, 6, 7]) 

        if vector_y > 0:
            self.direction_index = random.choice([self.direction_index, 1, 7]) 
        else:
            self.direction_index = random.choice([self.direction_index, 0, 4])

        next_x = self.x + vector_x * self.speed
        next_y = self.y + vector_y * self.speed

        if next_x < 0 or next_x > width - 10 or next_y < 0 or next_y > height - 10:
            self.direction_index = random.randint(0, len(DIRECTIONS) - 1)
        else:
            self.x = next_x
            self.y = next_y

    def stop(self):
        if random.random() < self.stop_chance:
            self.stop_counter = self.stop_duration

class Wolf:
    def __init__(self, x, y, speed=1):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = 'right'
        self.image = pygame.transform.scale(pygame.image.load("wolf.png"), (50, 50))

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def walk(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_UP]:
            self.y -= self.speed
            self.direction = 'up'
        elif keys[pygame.K_DOWN]:
            self.y += self.speed
            self.direction = 'down'
        elif keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = 'left'
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = 'right'


    def check_limits(self, width, height):
        if self.x < 0 or self.x > width - 10:
            self.x = min(max(self.x, 0), width - 10)
        if self.y < 0 or self.y > height - 10:
            self.y = min(max(self.y, 0), height - 10)

pygame.init()
pygame.display.set_caption("Wolf and sheep")
width, height = 800, 600
window = pygame.display.set_mode((width, height))

background_image = pygame.transform.scale(pygame.image.load("28256.jpg"), (width, height))

sheep_list = [Sheep(random.randint(50, width - 50), random.randint(50, height - 50)) for _ in range(11)]

wolf = Wolf(random.randint(50, width - 50), random.randint(50, height - 50))

score = 0
start_time = time.time()
game_over = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        elapsed_time = 30 - (time.time() - start_time) 
        if elapsed_time <= 0: 
            game_over = True

    window.blit(background_image, (0, 0))

    for sheep in sheep_list:
        sheep.walk()
        sheep.check_limits(width, height)

        distance = sheep.distance(wolf)
        if distance < 100:
            sheep.scare()
            sheep.flee(wolf, width, height)
            if distance < 50:
                sheep_list.remove(sheep)
                score += 1 
        else:
            sheep.calm()
            sheep.speed = max(sheep.speed - 0.05, sheep.min_speed)

        sheep.draw(window)
        sheep.stop() 

    wolf.walk()
    wolf.check_limits(width, height)
    wolf.draw(window)

    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    if not game_over:
        timer_text = font.render("Time: " + str(int(elapsed_time)), True, (255, 255, 255))
        window.blit(timer_text, (width - 120, 10))
    else:
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        window.blit(game_over_text, (width // 2 - 80, height // 2))

        restart_text = font.render("Click anywhere to restart", True, (255, 255, 255))
        window.blit(restart_text, (width // 2 - 150, height // 2 + 50))


    pygame.display.flip()

    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_over = False
                score = 0
                start_time = time.time()
                sheep_list = [Sheep(random.randint(50, width - 50), random.randint(50, height - 50)) for _ in range(11)]

pygame.quit()
