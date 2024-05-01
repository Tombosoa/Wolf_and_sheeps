import pygame
import random
import math

DIRECTIONS = ('up', 'down', 'left', 'right', 'up_left', 'up_right', 'down_left', 'down_right')

class Sheep:
    def __init__(self, x, y, speed = 0.1):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction_index = random.randint(0, len(DIRECTIONS) - 1)
        self.max_speed = 1.0
        self.min_speed = 0.1
        self.fleeing = False

    def draw(self, window):
        pygame.draw.circle(window, (255, 255, 0), (self.x, self.y), 10)

    def walk(self):
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

class Wolf:
    def __init__(self, x, y, speed=0.7):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = 'right'
        self.is_moving = False

    def draw(self, window):
        pygame.draw.circle(window, (255, 0, 0), (self.x, self.y), 10)

    def walk(self):
        if self.is_moving:
            if self.direction == 'up':
                self.y -= self.speed
            elif self.direction == 'down':
                self.y += self.speed
            elif self.direction == 'left':
                self.x -= self.speed
            elif self.direction == 'right':
                self.x += self.speed
            elif self.direction == 'up_left':
                self.x -= self.speed
                self.y -= self.speed
            elif self.direction == 'up_right':
                self.x += self.speed
                self.y -= self.speed
            elif self.direction == 'down_left':
                self.x -= self.speed
                self.y += self.speed
            elif self.direction == 'down_right':
                self.x += self.speed
                self.y += self.speed

    def catch(self):
        print("The wolf catches a sheep!")

    def check_limits(self, width, height):
        if self.x < 0 or self.x > width - 10:
            self.direction = 'up' if self.direction != 'up' else 'down'
        if self.y < 0 or self.y > height - 10:
            self.direction = 'left' if self.direction != 'left' else 'right'


pygame.init()
pygame.display.set_caption("Wolf and sheep")
width, height = 800, 600
window = pygame.display.set_mode((width, height))

sheep_list = [Sheep(random.randint(50, width - 50), random.randint(50, height - 50)) for _ in range(11)]

wolf = Wolf(random.randint(50, width - 50), random.randint(50, height - 50))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                wolf.direction = 'up'
                wolf.is_moving = True
            elif event.key == pygame.K_DOWN:
                wolf.direction = 'down'
                wolf.is_moving = True
            elif event.key == pygame.K_LEFT:
                wolf.direction = 'left'
                wolf.is_moving = True
            elif event.key == pygame.K_RIGHT:
                wolf.direction = 'right'
                wolf.is_moving = True

    for sheep in sheep_list:
        sheep.walk()
        sheep.check_limits(width, height)

        distance = sheep.distance(wolf)
        if distance < 150:
            sheep.scare()
            sheep.flee(wolf, width, height)
        else:
            sheep.calm()
            sheep.speed = max(sheep.speed - 0.05, sheep.min_speed)

    wolf.walk()
    wolf.check_limits(width, height)

    window.fill((0, 0, 0))
    for sheep in sheep_list:
        sheep.draw(window)
    wolf.draw(window)

    pygame.display.flip()

pygame.quit()
