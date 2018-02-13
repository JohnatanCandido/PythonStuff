import pygame
import random
import math

pygame.init()
gray = (200, 200, 200)
dark_gray = (100, 100, 100)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

block_width = 20
display_width, display_height, n_bomba = 0, 0, 0
clicados, marcados, timer = 0, 0, 0

in_game = True

gameDisplay = pygame.display.set_mode((270, 330))
pygame.display.set_caption('Campo Minado')
clock = pygame.time.Clock()


class Bomba(object):
    def __init__(self, x, y):
        self.is_bomb = False
        self.bombas = 0
        self.clicado = False
        self.marcado = False
        self.x = x
        self.y = y
        self.cor = gray

    def clica(self, bombas=None):
        if not self.marcado and not self.clicado:
            global clicados
            self.clicado = True
            if self.is_bomb:
                self.cor = red
                return True
            clicados += 1
            self.cor = dark_gray
            if self.bombas == 0 and bombas is not None:
                abrir_clareira(bombas, self)
            return False

    def marca(self):
        global marcados
        if not self.clicado and (marcados < n_bomba or self.marcado):
            self.marcado = not self.marcado
            if self.marcado:
                marcados += 1
            else:
                marcados -= 1

    def desenha(self):
        pygame.draw.rect(gameDisplay, self.cor, [self.x, self.y, block_width, block_width])
        n_cor = blue
        if self.bombas == 2:
            n_cor = green
        elif self.bombas >= 3:
            n_cor = red
        if (self.clicado or self.bombas > 5) and not self.is_bomb and self.bombas > 0:
            marca_bloco(self.x, self.y, n_cor, self.bombas)
        elif self.marcado:
            marca_bloco(self.x, self.y, red, "B")


def marca_bloco(x, y, cor, texto):
    large_text = pygame.font.Font('freesansbold.ttf', 15)
    txt_surf, text_rect = text_objects(str(texto), large_text, cor)
    text_rect.center = ((x + (block_width / 2)), (y + (block_width / 2)))
    gameDisplay.blit(txt_surf, text_rect)


def mostra_texto_final(text, color):
    large_text = pygame.font.Font('freesansbold.ttf', math.ceil((display_width*21)/7))
    txt_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (((display_width*21) / 2), ((display_height*21) / 2))
    gameDisplay.blit(txt_surf, text_rect)


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def mostra_texto(text, x, y, cor=black):
    large_text = pygame.font.Font('freesansbold.ttf', 30)
    txt_surf, text_rect = text_objects(text, large_text, cor)
    text_rect.center = (x, y)
    gameDisplay.blit(txt_surf, text_rect)


def novo_jogo(dificuldade=True):
    global display_width, display_height, n_bomba, gameDisplay, timer, clicados, marcados
    timer, clicados, marcados = 0, 0, 0

    if dificuldade:
        display_width, display_height, n_bomba = seta_dificuldade()
    gameDisplay = pygame.display.set_mode((display_width * 21, display_height * 21 + 63))

    bombas = []
    n_bombas = 0
    for i in range(display_height):
        bombas.append([])
        for j in range(display_width):
            bombas[i].append(Bomba((j * 20) + j, (i * 20) + i + 63))
    while n_bombas != n_bomba:
        for i in range(len(bombas)):
            for j in range(len(bombas[i])):
                if n_bombas == n_bomba:
                    break
                if random.randrange(100) % 7 == 1 and not max_bombas(bombas, i, j) and not bombas[i][j].is_bomb:
                    bombas[i][j].is_bomb = True
                    n_bombas += 1
                    numera_bombas(bombas, i, j)
            if n_bombas == n_bomba:
                break
    global in_game
    in_game = True
    return bombas


def max_bombas(bombas, i, j):
    if i > 0 and j > 0 and bombas[i-1][j-1].bombas > 4:
        return True
    elif i > 0 and bombas[i-1][j].bombas > 4:
        return True
    elif i > 0 and j < len(bombas[i])-1 and bombas[i-1][j+1].bombas > 4:
        return True
    elif j > 0 and bombas[i][j-1].bombas > 4:
        return True
    elif j < len(bombas[i])-1 and bombas[i][j+1].bombas > 4:
        return True
    elif i < len(bombas)-1 and j > 0 and bombas[i+1][j-1].bombas > 4:
        return True
    elif i < len(bombas)-1 and bombas[i+1][j].bombas > 4:
        return True
    elif i < len(bombas)-1 and j < len(bombas[i])-1 and bombas[i+1][j+1].bombas > 4:
        return True
    return False


def cabecalho():
    pygame.draw.rect(gameDisplay, (255, 255, 255), [0, 0, display_width*21, 62])
    pygame.draw.rect(gameDisplay, black, [display_width*21-100, 15, 90, 40])
    pygame.draw.rect(gameDisplay, black, [10, 15, 50, 40])
    mostra_texto(str(n_bomba - marcados), 35, 37, red)
    mostra_texto(tempo_formatado(), display_width*21-55, 37, red)


def tempo_formatado():
    segundos = str((math.floor(timer/5) % 60))
    segundos = segundos if int(segundos) > 9 else "0"+segundos
    retorno = str(math.floor((timer/5)/60))+":"+segundos
    return retorno


def seta_dificuldade():
    global gameDisplay
    gameDisplay = pygame.display.set_mode((270, 330))
    while True:
        gameDisplay.fill(gray)
        pygame.draw.rect(gameDisplay, dark_gray, [20, 40, 230, 40])  # x y width height
        mostra_texto("Fácil", 135, 63)
        pygame.draw.rect(gameDisplay, dark_gray, [20, 100, 230, 40])
        mostra_texto("Intermediário", 135, 123)
        pygame.draw.rect(gameDisplay, dark_gray, [20, 160, 230, 40])
        mostra_texto("Difícil", 135, 183)
        pygame.draw.rect(gameDisplay, dark_gray, [20, 220, 230, 40])
        mostra_texto("Profissional", 135, 243)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 20 < event.dict.get('pos')[0] < 250 and 40 < event.dict.get('pos')[1] < 80:
                    return 15, 8, 10
                if 20 < event.dict.get('pos')[0] < 250 and 100 < event.dict.get('pos')[1] < 140:
                    pass
                if 20 < event.dict.get('pos')[0] < 250 and 160 < event.dict.get('pos')[1] < 200:
                    pass
                if 20 < event.dict.get('pos')[0] < 250 and 220 < event.dict.get('pos')[1] < 260:
                    return 30, 16, 99
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()


def game_loop():
    global timer, in_game
    bombas = novo_jogo()
    while True:
        if in_game:
            timer += 1
        gameDisplay.fill(black)
        cabecalho()
        for b in bombas:
            for bo in b:
                bo.desenha()
        if clicados == (display_width * display_height) - n_bomba:
            mostra_texto_final("Você ganhou", green)
            in_game = False
        pygame.display.update()
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                bombas = novo_jogo(False)
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                bombas = novo_jogo()
                break
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            achou = False
            if event.type == pygame.MOUSEBUTTONDOWN and in_game:
                for bomba in bombas:
                    for b in bomba:
                        if achou:
                            break
                        if b.x < event.dict.get('pos')[0] < (b.x + 20) and b.y < event.dict.get('pos')[1] < (b.y+20):
                            achou = True
                            if event.dict.get('button') == 1:
                                if b.clica():
                                    end_game(bombas)
                                    break
                                if b.bombas == 0:
                                    abrir_clareira(bombas, b)
                            elif event.dict.get('button') == 3:
                                b.marca()
                    if achou:
                        break
                break


def end_game(bombas):
    for bomba in bombas:
        for b in bomba:
            if b.is_bomb:
                b.clica()
    global in_game
    in_game = False


def numera_bombas(bombas, i, j):
    if j > 0:
        bombas[i][j-1].bombas += 1
    if j < (len(bombas[i])-1):
        bombas[i][j+1].bombas += 1
    if i > 0:
        bombas[i-1][j].bombas += 1
    if i < (len(bombas)-1):
        bombas[i+1][j].bombas += 1
    if i > 0 and j > 0:
        bombas[i-1][j-1].bombas += 1
    if i > 0 and j < (len(bombas[i])-1):
        bombas[i-1][j+1].bombas += 1
    if i < (len(bombas)-1) and j < (len(bombas[i])-1):
        bombas[i+1][j+1].bombas += 1
    if i < (len(bombas)-1) and j > 0:
        bombas[i+1][j-1].bombas += 1


def abrir_clareira(bombas, b):
    for i in range(0, len(bombas)):
        for j in range(0, len(bombas[i])):
            if bombas[i][j] == b:
                if j > 0:
                    bombas[i][j - 1].clica(bombas)
                if j < display_width-1:
                    bombas[i][j + 1].clica(bombas)
                if i > 0:
                    bombas[i - 1][j].clica(bombas)
                if i < display_height-1:
                    bombas[i + 1][j].clica(bombas)
                if i > 0 and j > 0:
                    bombas[i - 1][j - 1].clica(bombas)
                if i > 0 and j < display_width-1:
                    bombas[i - 1][j + 1].clica(bombas)
                if i < display_height-1 and j < display_width-1:
                    bombas[i + 1][j + 1].clica(bombas)
                if i < display_height-1 and j > 0:
                    bombas[i + 1][j - 1].clica(bombas)

if __name__ == "__main__":
    game_loop()

pygame.quit()
quit()