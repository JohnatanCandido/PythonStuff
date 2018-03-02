import random
import pygame
from Pife.validador import validar


class JogadorBase:
    def __init__(self, cartas, mostra_jogo, y):
        self.cartas = cartas
        self.carta_lixo = None
        self.xs = []
        self.y = int(y)
        self.carta_selecionada = None
        self.mostra_jogo = mostra_jogo

        for i in range(10):
            self.xs.append([i*80+283, i*80+283+71])

    def compra(self, bolo, is_lixo, carta_vazia):
        if len([c for c in self.cartas if c.naipe == '-']) == 1:
            if is_lixo:
                carta = bolo[-1]
                self.carta_lixo = carta
            else:
                carta = bolo[random.randrange(len(bolo))]
            bolo.remove(carta)
            self.cartas.remove(carta_vazia)
            self.cartas.append(carta)

    def descartar(self, carta, carta_vazia):
        if carta is not None and len([c for c in self.cartas if c.naipe == '-']) == 0:
            if carta != self.carta_lixo:
                self.cartas.remove(carta)
                self.cartas.append(carta_vazia)
                self.carta_lixo = None
                return carta
            else:
                raise ValueError
        return None

    def printa_mao(self, display):
        for i in range(10):
            img = pygame.image.load(self.cartas[i].url)
            if self.cartas[i] == self.carta_selecionada:
                display.blit(img, (self.xs[i][0], self.y - 10))
            elif self.mostra_jogo and self.cartas[i].url != '-':
                display.blit(img, (self.xs[i][0], self.y))
            else:
                img = pygame.image.load('img_cartas//fundo_carta.png')
                display.blit(img, (self.xs[i][0], self.y))

    def checar_mao(self):
        v1 = validar([self.cartas[0], self.cartas[1], self.cartas[2]])
        v2 = validar([self.cartas[3], self.cartas[4], self.cartas[5]])
        v3 = validar([self.cartas[6], self.cartas[7], self.cartas[8]])

        return v1 and v2 and v3