import pygame
import random
from Pife.jogador import Jogador
from Pife.oponente import Oponente
from Pife import tela_utils

pygame.init()

jogadores = []
baralho = []
lixo = []
em_jogo = True
rodada = 0
vitorias = 0
derrotas = 0

COMPRAR = 'Compre uma carta'
DESCARTAR = 'Descarte uma carta'
DESCARTE_INVALIDO = 'Você não pode descartar a carta que acabou de comprar do lixo!'
ESPERAR = 'Espere seu oponente'
GANHOU = 'Você ganhou!'
PERDEU = 'Você perdeu...'

COMPROU_DO_BOLO = 'Comprou do bolo'
COMPROU_DO_LIXO = 'Comprou do lixo'

pygame.display.set_caption('Pife 2.1')
clock = pygame.time.Clock()


class Carta:
    def __init__(self, id_carta, valor, naipe, url):
        self.id_carta = id_carta
        self.valor = valor
        self.naipe = naipe
        self.url = url

    def __str__(self):
        return self.valor + ' - ' + self.naipe


cartaVazia = Carta(99, 'Carta', 'Vazia', 'img_cartas//fundo_carta.png')
joker_vermelho = Carta(999, 'joker', 'Vermelho', 'Não tem kkkk')
joker_preto = Carta(999, 'joker', 'Preto', 'Não tem kkkk')


def eventos_handler():
    global em_jogo

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if em_jogo:
                global vitorias
                if event.dict.get('button') == 2:
                    checa_fim_de_jogo()
                x = event.dict.get('pos')[0]
                y = event.dict.get('pos')[1]

                if 580 < y < 676:
                    move_ou_descarta(event)
                elif 300 < y < 396:
                    if 480 < x < 551:
                        jogadores[0].compra(baralho, False, cartaVazia)
                        tela_utils.msg_player = DESCARTAR
                    elif 800 < x < 871 and len(lixo) > 0:
                        jogadores[0].compra(lixo, True, cartaVazia)
                        tela_utils.msg_player = DESCARTAR
            elif event.dict.get('button') == 1:
                novo_jogo()
                break
        if checa_input_teclado(event):
            break


def checa_fim_de_jogo():
    global em_jogo, vitorias
    if jogadores[0].checar_mao():
        em_jogo = False
        tela_utils.msg_player = GANHOU
        vitorias += 1
        printa_jogos_oponente()


def checa_input_teclado(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                novo_jogo()
                return True
            if event.key == pygame.K_m:
                jogadores[1].mostra_jogo = not jogadores[1].mostra_jogo
                return True
            if event.key == pygame.K_g:
                checa_fim_de_jogo()
                return True
        return False


def move_ou_descarta(event):
    global em_jogo, derrotas
    if event.dict.get('button') == 1:
        jogadores[0].seleciona_carta(event.dict.get('pos')[0])
    elif event.dict.get('button') == 3:
        try:
            descarte = jogadores[0].descartar(event.dict.get('pos')[0], cartaVazia)
        except ValueError:
            tela_utils.msg_player = DESCARTE_INVALIDO
            descarte = None
        jogadores[0].carta_selecionada = None
        if descarte is not None:
            lixo.append(descarte)
            tela_utils.msg_player = ESPERAR

            retorno_oponente = jogadores[1].jogar(baralho, lixo, cartaVazia)
            if retorno_oponente[1]:
                em_jogo = False
                tela_utils.msg_player = PERDEU
                derrotas += 1
                printa_jogos_oponente()
            else:
                tela_utils.msg_player = COMPRAR
            if retorno_oponente[2]:
                tela_utils.msg_oponente = COMPROU_DO_LIXO
            else:
                tela_utils.msg_oponente = COMPROU_DO_BOLO
            lixo.append(retorno_oponente[0])


def printa_jogos_oponente(i=1):
    o = jogadores[i]
    print('### JOGOS ###')
    for j in o.jogos:
        for c in j:
            print(c.__str__())
        print('----------------')
    print('### PARES ###')
    for p in o.pares:
        for c in p:
            print(c.__str__())
        print('----------------')


def game_loop():
    tela_utils.display = pygame.display.set_mode((1366, 768), pygame.RESIZABLE)
    novo_jogo()
    while True:
        tela_utils.printa_tela(rodada, vitorias, derrotas, lixo)
        if not em_jogo:
            jogadores[1].mostra_jogo = True
        for j in jogadores:
            j.printa_mao(tela_utils.display)
        pygame.display.update()
        clock.tick(30)
        eventos_handler()
        if len(baralho) == 0:
            refil_baralho()


def refil_baralho():
    global baralho
    baralho = [c for c in lixo]
    lixo.clear()


def novo_jogo(testes=False):
    global em_jogo, rodada
    if not testes:
        for _ in range(20):
            print('.')
    rodada += 1
    em_jogo = True
    tela_utils.init(cartaVazia, COMPRAR)
    init_baralho()
    lixo.clear()
    jogadores.clear()

    mao_1 = []
    mao_2 = []
    for _ in range(9):
        carta = baralho[random.randrange(len(baralho))]
        mao_1.append(carta)
        baralho.remove(carta)
        carta = baralho[random.randrange(len(baralho))]
        mao_2.append(carta)
        baralho.remove(carta)

    mao_1.append(cartaVazia)  # carta extra
    mao_2.append(cartaVazia)  # carta extra
    if testes:
        jogadores.append(Oponente(mao_1))
    else:
        jogadores.append(Jogador(mao_1))
    jogadores.append(Oponente(mao_2))


def init_baralho():
    baralho.clear()
    naipes = ['copas', 'paus', 'ouro', 'espadas']
    for i in range(4):
        for j in range(13):
            url = 'img_cartas//' + str(j+1) + '_' + naipes[i] + '.png'
            baralho.append(Carta((j+(13*i+1)), str(j+1), naipes[i], url))


def oponente_vs_oponente(jogos):
    wins = [0, 0]
    for jogo in range(jogos):
        novo_jogo(True)
        while True:
            for i in range(2):
                descarte, ganhou, comp_lixo = jogadores[i].jogar(baralho, lixo, cartaVazia)
                lixo.append(descarte)
                if ganhou:
                    wins[i] += 1
                    break
                if len(baralho) == 0:
                    refil_baralho()
            else:
                continue
            break
        if jogo % 100 == 0:
            print('[' + str(wins[0]) + ',' + str(wins[1]) + '] #' + ' Diferença: ' + str((wins[0] - wins[1])))
    if wins[0] > wins[1]:
        print('Jogador 1')
    elif wins[1] > wins[0]:
        print('Jogador 2')
    else:
        print('Empate')


if __name__ == '__main__':
    game_loop()
    # oponente_vs_oponente(1000)


pygame.quit()
quit()