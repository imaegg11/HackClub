import pygame
import random
import time
from pygame.locals import *
pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Snake")

class Game():
    def __init__(self, width, height):
        self.width = width
        self.height = height 
        self.snake = [(i, 0) for i in range(5)]
        self.x, self.y = pygame.display.get_surface().get_size()
        self.sqsize = self.x / self.width
        self.direction = [1, 0]
        self.apple = ()
        self.game_over = False

    def draw_background(self):
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
        self.snake.pop(0)
        new_head_loc = self.update_coords(self.snake[-1], self.direction)
        if new_head_loc in set(self.snake) or self.is_out_of_bounds(new_head_loc):
            print("Game Over")
            self.game_over = True
        else:
            self.snake += [new_head_loc]

    def is_out_of_bounds(self, head):
        x, y = head
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True 
        else:
            return False

    @staticmethod
    def update_coords(old, update):
        return (old[0] + update[0], old[1] + update[1])
    
    def set_direction(self, new_direction):
        self.direction = new_direction


bg = Game(20, 20)

running = True
frame = 0
while running:

    if not bg.game_over:
        bg.draw_background()
        bg.draw_snake()

        if frame % 20 == 0:
            bg.update_snake()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 119: # W
                bg.set_direction([0, -1])
            elif event.key == 97: # A
                bg.set_direction([-1, 0])
            elif event.key == 115: # S
                bg.set_direction([0, 1])
            elif event.key == 100: # D
                bg.set_direction([1, 0])

    frame += 1
    pygame.display.update()
    time.sleep(1/360)

pygame.quit()