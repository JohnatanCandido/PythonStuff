import pygame
import random
from Pife.validador import validar


class Jogador:
    def __init__(self, cartas):
        self.cartas = cartas
        self.xs = []
        self.carta_selecionada = None
        self.carta_lixo = None

        for i in range(10):
            self.xs.append([i*80+283, i*80+283+71])

    def printa_mao(self, display):
        x = 283
        for carta in self.cartas:
            img = pygame.image.load(carta.url)
            if carta == self.carta_selecionada:
                display.blit(img, (x, 570))
            else:
                display.blit(img, (x, 580))
            x += 80

    def encontra_carta(self, x):
        for i in range(10):
            if self.xs[i][0] < x < self.xs[i][1] and self.cartas[i].naipe != '-':
                return self.cartas[i]
        return None

    def compra_bolo(self, baralho, carta_vazia):
        if len([c for c in self.cartas if c.naipe == '-']) == 1:
            carta = baralho[random.randrange(len(baralho))]
            self.cartas.remove(carta_vazia)
            self.cartas.append(carta)
            baralho.remove(carta)

    def compra_lixo(self, lixo, carta_vazia):
        if len([c for c in self.cartas if c.naipe == '-']) == 1:
            carta = lixo[-1]
            lixo.remove(carta)
            self.cartas.remove(carta_vazia)
            self.cartas.append(carta)
            self.carta_lixo = carta

    def descartar(self, x, carta_vazia):
        carta = self.encontra_carta(x)
        if carta is not None and len([c for c in self.cartas if c.naipe == '-']) == 0:
            if carta != self.carta_lixo:
                self.cartas.remove(carta)
                self.cartas.append(carta_vazia)
                self.carta_lixo = None
                return carta
            else:
                raise ValueError
        return None

    def seleciona_carta(self, x):
        if self.carta_selecionada is None:
            self.carta_selecionada = self.encontra_carta(x)
        else:
            i = self.cartas.index(self.carta_selecionada)
            segunda_carta = self.encontra_carta(x)
            if segunda_carta is not None:
                j = self.cartas.index(segunda_carta)
                self.cartas[i] = segunda_carta
                self.cartas[j] = self.carta_selecionada
                self.carta_selecionada = None

    def checar_mao(self):
        v1 = validar([self.cartas[0], self.cartas[1], self.cartas[2]])
        v2 = validar([self.cartas[3], self.cartas[4], self.cartas[5]])
        v3 = validar([self.cartas[6], self.cartas[7], self.cartas[8]])

        return v1 and v2 and v3

if __name__ == '__main__':
    pass