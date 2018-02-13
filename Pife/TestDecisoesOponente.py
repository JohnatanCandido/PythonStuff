import unittest
from Pife.oponente import Oponente


class Carta:
    def __init__(self, id_carta, valor, naipe, url):
        self.id_carta = id_carta
        self.valor = valor
        self.naipe = naipe
        self.url = url

cartaVazia = Carta(99, '99', '-', '-')


class TestDecisoesOponente(unittest.TestCase):

    def test_deveCriarTrincaAsesESequencia456(self):
        mao = [
            Carta(1, '1', 'Espadas', 'Teste'),
            Carta(5, '5', 'Copas', 'Teste'),
            Carta(27, '1', 'Ouro', 'Teste'),
            Carta(48, '9', 'Espadas', 'Teste'),
            Carta(36, '10', 'Ouro', 'Teste'),
            Carta(4, '4', 'Copas', 'Teste'),
            Carta(14, '1', 'Paus', 'Teste'),
            Carta(6, '6', 'Copas', 'Teste'),
            Carta(24, '11', 'Paus', 'Teste')
        ]

        oponente = Oponente(mao)

        oponente.cria_jogos()

        self.assertEqual(len(oponente.jogos), 2)

        jogo1 = oponente.jogos[0]
        self.assertEqual(jogo1[0].valor, '4')
        self.assertEqual(jogo1[1].valor, '5')
        self.assertEqual(jogo1[2].valor, '6')

        jogo2 = oponente.jogos[1]
        self.assertEqual(jogo2[0].valor, '1')
        self.assertEqual(jogo2[1].valor, '1')
        self.assertEqual(jogo2[2].valor, '1')

    def test_deveComprarDoLixo(self):
        mao = [
            Carta(1, '1', 'Espadas', 'Teste'),
            Carta(5, '5', 'Copas', 'Teste'),
            Carta(27, '1', 'Ouro', 'Teste'),
            Carta(48, '9', 'Espadas', 'Teste'),
            Carta(36, '10', 'Ouro', 'Teste'),
            Carta(4, '4', 'Copas', 'Teste'),
            Carta(26, '13', 'Paus', 'Teste'),
            Carta(6, '6', 'Copas', 'Teste'),
            Carta(24, '11', 'Paus', 'Teste'),
            cartaVazia
        ]

        lixo = [Carta(14, '1', 'Paus', 'Teste')]
        oponente = Oponente(mao)

        oponente.jogar([], lixo, cartaVazia)

        self.assertEqual(len(lixo), 0)

    def test_deveTransformarUmJogoEmDois(self):
        mao = [
            Carta(1, '1', 'Copas', 'Teste'),
            Carta(2, '2', 'Copas', 'Teste'),
            Carta(3, '3', 'Copas', 'Teste'),
            Carta(48, '9', 'Espadas', 'Teste'),
            Carta(36, '10', 'Ouro', 'Teste'),
            Carta(4, '4', 'Copas', 'Teste'),
            Carta(14, '1', 'Paus', 'Teste'),
            Carta(43, '4', 'Espadas', 'Teste'),
            Carta(24, '11', 'Paus', 'Teste')
        ]

        lixo = [Carta(27, '1', 'Ouro', 'Teste')]

        oponente = Oponente(mao)

        oponente.compra([], lixo, cartaVazia)

        self.assertEqual(len(oponente.jogos), 2)
        self.assertEqual(oponente.jogos[0][0].valor, '1')
        self.assertEqual(oponente.jogos[0][1].valor, '1')
        self.assertEqual(oponente.jogos[0][2].valor, '1')

        self.assertEqual(oponente.jogos[1][0].valor, '2')
        self.assertEqual(oponente.jogos[1][1].valor, '3')
        self.assertEqual(oponente.jogos[1][2].valor, '4')


if __name__ == '__main__':
    unittest.main()