import pygame
import random
import time
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((800, 900))
pygame.display.set_caption("Snake")

class Game():
    def __init__(self, width, height):
        self.width = width
        self.height = height 
        self.snake = [(i, 0) for i in range(2)]
        self.x, self.y = pygame.display.get_surface().get_size()
        self.sqsize = self.x / self.width
        self.direction = [0, 0]
        self.apple = None
        self.game_over = False
        self.high_score = 2

    def draw_score(self):
        myfont = pygame.font.SysFont("Trebuchet MS", 30)
        htext = myfont.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        ctext = myfont.render(f"Current Score: {len(self.snake)}", True, (255, 255, 255))
        screen.blit(ctext, (self.x // 2, (100 - ctext.get_height()) // 2 + 800))
        screen.blit(htext, (30, (100 - htext.get_height()) // 2 + 800))

    def draw_apple(self):
        red = (231, 71, 29)
        asqsize = int(self.sqsize * 0.6)
        apple = pygame.Rect(self.apple[0] * self.sqsize + (self.sqsize - asqsize) // 2, self.apple[1] * self.sqsize + (self.sqsize - asqsize) // 2, asqsize, asqsize) 
        pygame.draw.rect(screen, red, apple)

    def gen_new_apple(self):
        self.apple = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        while self.apple in set(self.snake):
            self.apple = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))

    def draw_background(self):
        ogreen = (87, 138, 52)
        bg = pygame.Rect(0, 0, self.x, self.y)
        pygame.draw.rect(screen, ogreen, bg)
        lgreen = (167, 217, 70)
        dgreen = (141, 204, 53)
        for i in range(self.width):
            for j in range(self.height):
                square = pygame.Rect(i * self.sqsize, j * self.sqsize, self.sqsize, self.sqsize)
                pygame.draw.rect(screen, lgreen if i % 2 == j % 2 else dgreen, square)

    def draw_snake(self):
        sncolor = (77, 119, 247)
        for i in self.snake:
            xloc, yloc = i 
            body = pygame.Rect(xloc * self.sqsize, yloc * self.sqsize, self.sqsize, self.sqsize)
            pygame.draw.rect(screen, sncolor, body)

    def update_snake(self):
        if self.direction == [0, 0]:
            return 
        
        tail = self.snake.pop(0)
        new_head_loc = self.add_coords(self.snake[-1], self.direction)
        if new_head_loc in set(self.snake) or self.is_out_of_bounds(new_head_loc):
            self.high_score = max(self.high_score, len(self.snake))
            self.game_over = True
        else:
            self.snake += [new_head_loc]
            if new_head_loc == self.apple:
                self.snake = [tail] + self.snake
                if len(self.snake) == self.width * self.height:
                    self.high_score = max(self.high_score, len(self.snake))
                    self.draw_background()
                    self.draw_apple()
                    self.draw_snake()
                    self.game_over = True 
                else:
                    self.gen_new_apple()

    def is_out_of_bounds(self, head):
        x, y = head
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True 
        else:
            return False

    @staticmethod
    def add_coords(old, update):
        return (old[0] + update[0], old[1] + update[1])
    
    @staticmethod
    def multiply_coords(coords, multi):
        return (coords[0] * multi, coords[1] * multi)
    
    def set_direction(self, new_direction):
        if self.multiply_coords(self.direction, -1) != new_direction:
            self.direction = new_direction


bg = Game(20, 20)
bg.gen_new_apple()
running = True
frame = 0
while running:

    if not bg.game_over:
        bg.draw_background()
        bg.draw_apple()
        bg.draw_snake()
        bg.draw_score()

        if frame % 20 == 0:
            bg.update_snake()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 119: # W
                bg.set_direction((0, -1))
            elif event.key == 97: # A
                bg.set_direction((-1, 0))
            elif event.key == 115: # S
                bg.set_direction((0, 1))
            elif event.key == 100: # D
                bg.set_direction((1, 0))

    frame += 1
    pygame.display.update()
    time.sleep(1/300)

pygame.quit()