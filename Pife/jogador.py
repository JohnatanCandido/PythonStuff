from Pife.jogador_base import JogadorBase


class Jogador(JogadorBase):
    def __init__(self, cartas):
        JogadorBase.__init__(self, cartas, True, 580)

    def encontra_carta(self, x):
        for i in range(10):
            if self.xs[i][0] < x < self.xs[i][1] and self.cartas[i].naipe != 'Vazia':
                return self.cartas[i]
        return None

    def descartar(self, x, carta_vazia):
        carta = self.encontra_carta(x)
        return JogadorBase.descartar(self, carta, carta_vazia)

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


if __name__ == '__main__':
    pass