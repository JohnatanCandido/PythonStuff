import pygame
import time
import random
import math

pygame.init()
width_blocks = 15
heigth_blocks = 10
display_width = width_blocks*22
display_height = heigth_blocks*22

black = (0, 0, 0)
gray = (240, 240, 240)
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)

block_width = 20

children = []

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Jogo da Cobrinha')
clock = pygame.time.Clock()


class Square(object):
    def __init__(self, x, y, move, parent):
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 0
        self.move = move
        self.parent = parent
        self.child = None

    def do_move(self):
        self.x += self.x_change
        self.y += self.y_change
        if self.child is not None:
            self.child.do_move()
            self.child.change_move(self.move)
        pygame.draw.rect(gameDisplay, black, [self.x, self.y, block_width, block_width])

    def create_child(self):
        if self.child is None:
            if self.move == 1:  # LEFT
                child_x = self.x + 22
                child_y = self.y
            elif self.move == 2:  # RIGHT
                child_x = self.x - 22
                child_y = self.y
            elif self.move == 3:  # UP
                child_y = self.y + 22
                child_x = self.x
            else:                 # DOWN
                child_y = self.y - 22
                child_x = self.x

            self.child = Square(child_x, child_y, self.move, self)
            children.append(self.child)
            self.child.change_move(self.move)
        else:
            self.child.create_child()

    def change_move(self, move):
        if self.parent is not None:
            if self.parent.move < 3 and self.y == self.parent.y:
                self.move = self.parent.move
                self.x_change = self.parent.x_change
                self.y_change = self.parent.y_change
            elif self.parent.move > 2 and self.x == self.parent.x:
                self.move = self.parent.move
                self.x_change = self.parent.x_change
                self.y_change = self.parent.y_change
        else:
            self.move = move
            if self.move == 1:  # LEFT
                self.x_change = -22
                self.y_change = 0
            elif self.move == 2:  # RIGHT,
                self.x_change = 22
                self.y_change = 0
            elif self.move == 3:  # UP
                self.y_change = -22
                self.x_change = 0
            elif self.move == 4:  # DOWN
                self.y_change = 22
                self.x_change = 0

        if self.child is not None:
            self.child.change_move(self.move)


class Food(object):
    def __init__(self, x, y, food_radius, color):
        self.x = x
        self.y = y
        self.color = color
        self.food_radius = food_radius

    def draw_food(self):
        pygame.draw.circle(gameDisplay, yellow, (self.x, self.y), self.food_radius)


def eat(player, food):
    if player.x < food.x < (player.x + block_width) and player.y < food.y < (player.y + block_width):
        player.create_child()
        nova_coordenada(food)
        food.draw_food()


def nova_coordenada(food):
    food.x = (random.randrange(1, math.ceil(display_width / 22)) * 22) - 11
    food.y = (random.randrange(1, math.ceil(display_height / 22)) * 22) - 11
    for n in children:
        if n.x < food.x and n.y < food.y and n.x + block_width > food.x and n.y + block_width > food.y:
            food.x = (random.randrange(1, math.ceil((display_width+22) / 22)) * 22) - 11
            food.y = (random.randrange(1, math.ceil((display_height+22) / 22)) * 22) - 11


def checa_colisao(player):
    if not (0 <= player.x < display_width and 0 <= player.y < display_height):
        return True
    node = player.child
    while True:
        if player.x == node.x and player.y == node.y:
            return True
        if node.child is None:
            return False
        node = node.child


def mostra_texto_final(text, color):
    large_text = pygame.font.Font('freesansbold.ttf', math.ceil(display_width/6))
    txt_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(txt_surf, text_rect)
    pygame.display.update()

    time.sleep(2)

    game_loop()


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def game_loop():
    player = Square(5*22, 5*22, 2, None)
    children.append(player)
    for _ in range(5):
        player.create_child()

    food_x = (random.randrange(1, math.ceil((display_width+22)/22))*22)-11
    food_y = (random.randrange(1, math.ceil((display_height+22)/22))*22)-11
    food_radius = 10
    food = Food(food_x, food_y, food_radius, yellow)

    game_exit = False

    while not game_exit:
        if len(children) == (width_blocks*heigth_blocks):
            mostra_texto_final('You Win!', green)
        eat(player, food)
        gameDisplay.fill(gray)
        food.draw_food()
        player.do_move()
        if checa_colisao(player):
            mostra_texto_final('Game Over!', red)
        player.change_move(player.move)
        pygame.display.update()
        clock.tick(3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player.x_change == 0:
                    player.change_move(1)
                    break
                if event.key == pygame.K_RIGHT and player.x_change == 0:
                    player.change_move(2)
                    break
                if event.key == pygame.K_UP and player.y_change == 0:
                    player.change_move(3)
                    break
                if event.key == pygame.K_DOWN and player.y_change == 0:
                    player.change_move(4)
                    break

game_loop()
pygame.quit()
quit()
