import pygame
import random
from Pife.jogador import Jogador
from Pife.oponente import Oponente

pygame.init()

jogadores = []
baralho = []
lixo = []
em_jogo = True
mensagem = ''
mensagemOponente = ''

COMPRAR = 'Compre uma carta'
DESCARTAR = 'Descarte uma carta'
DESCARTE_INVALIDO = 'Você não pode descartar a carta que acabou de comprar do lixo!'
ESPERAR = 'Espere seu oponente'
GANHOU = 'Você ganhou!'
PERDEU = 'Você perdeu...'

COMPROU_DO_BOLO = 'Comprou do bolo'
COMPROU_DO_LIXO = 'Comprou do lixo'

gameDisplay = pygame.display.set_mode((1366, 768), pygame.RESIZABLE)
pygame.display.set_caption('Pife 2.0')
clock = pygame.time.Clock()


class Carta:
    def __init__(self, id_carta, valor, naipe, url):
        self.id_carta = id_carta
        self.valor = valor
        self.naipe = naipe
        self.url = url

cartaVazia = Carta(99, 99, '-', 'img_cartas//fundo_carta.png')
joker_vermelho = Carta(999, 'joker', 'Vermelho', 'Não tem kkkk')
joker_preto = Carta(999, 'joker', 'Preto', 'Não tem kkkk')


def printa_centro_tela():
    # lixo
    if len(lixo) > 0:
        carta_lixo = pygame.image.load(lixo[-1].url)
        gameDisplay.blit(carta_lixo, (800, 300))

    # bolo
    imagem_bolo = pygame.image.load(cartaVazia.url)
    gameDisplay.blit(imagem_bolo, (480, 300))

    printa_mensagem()

    # pygame.draw.rect(gameDisplay, (0, 200, 0), [615, 320, 120, 60])
    # OBS: isso seria um botão para reinciar o jogo mas pressionar espaço já faz isso.
    # Talvez outra hora eu faça...


def printa_mensagem():
    # Mensagem oponente
    large_text = pygame.font.Font('freesansbold.ttf', 30)
    txt_surf, text_rect = text_objects(mensagemOponente, large_text, (255, 0, 0))
    text_rect.center = (675, 200)
    gameDisplay.blit(txt_surf, text_rect)

    # Mensagem jogador
    large_text = pygame.font.Font('freesansbold.ttf', 30)
    txt_surf, text_rect = text_objects(mensagem, large_text, (255, 0, 0))
    text_rect.center = (675, 500)
    gameDisplay.blit(txt_surf, text_rect)

    printa_descricao_lixo_e_bolo()


def printa_descricao_lixo_e_bolo():
    large_text = pygame.font.Font('freesansbold.ttf', 15)
    txt_surf, text_rect = text_objects('Bolo', large_text, (0, 0, 255))
    text_rect.center = (515, 415)
    gameDisplay.blit(txt_surf, text_rect)

    large_text = pygame.font.Font('freesansbold.ttf', 15)
    txt_surf, text_rect = text_objects('Lixo', large_text, (0, 0, 255))
    text_rect.center = (835, 415)
    gameDisplay.blit(txt_surf, text_rect)


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def eventos_handler():
    global em_jogo

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if em_jogo:
                global mensagem
                if event.dict.get('button') == 2:
                    if jogadores[0].checar_mao():
                        em_jogo = False
                        mensagem = GANHOU
                        printa_jogos_oponente()
                x = event.dict.get('pos')[0]
                y = event.dict.get('pos')[1]

                if 580 < y < 676:
                    move_ou_descarta(event)
                elif 300 < y < 396:
                    if 480 < x < 551:
                        jogadores[0].compra_bolo(baralho, cartaVazia)
                        mensagem = DESCARTAR
                    elif 800 < x < 871 and len(lixo) > 0:
                        jogadores[0].compra_lixo(lixo, cartaVazia)
                        mensagem = DESCARTAR
            elif event.dict.get('button') == 1:
                novo_jogo()
                break
        if checa_input_teclado(event):
            break


def checa_input_teclado(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                novo_jogo()
                return True
            if event.key == pygame.K_m:
                jogadores[1].mostra_jogo = not jogadores[1].mostra_jogo
                return True
        return False


def move_ou_descarta(event):
    global em_jogo, mensagem
    if event.dict.get('button') == 1:
        jogadores[0].seleciona_carta(event.dict.get('pos')[0])
    elif event.dict.get('button') == 3:
        try:
            descarte = jogadores[0].descartar(event.dict.get('pos')[0], cartaVazia)
        except ValueError:
            mensagem = DESCARTE_INVALIDO
            descarte = None
        jogadores[0].carta_selecionada = None
        if descarte is not None:
            lixo.append(descarte)
            mensagem = ESPERAR

            retorno_oponente = jogadores[1].jogar(baralho, lixo, cartaVazia)
            if retorno_oponente[1]:
                em_jogo = False
                mensagem = PERDEU
                printa_jogos_oponente()
            else:
                mensagem = COMPRAR
            global mensagemOponente
            if retorno_oponente[2]:
                mensagemOponente = COMPROU_DO_LIXO
            else:
                mensagemOponente = COMPROU_DO_BOLO
            lixo.append(retorno_oponente[0])


def printa_jogos_oponente():
    o = jogadores[1]
    print('### JOGOS ###')
    for j in o.jogos:
        for c in j:
            print(c.valor + ' - ' + c.naipe)
        print('----------------')
    print('### PARES ###')
    for p in o.pares:
        for c in p:
            print(c.valor + ' - ' + c.naipe)
        print('----------------')


def game_loop():
    global baralho
    novo_jogo()
    while True:
        gameDisplay.fill((0, 155, 0))
        printa_centro_tela()
        if not em_jogo:
            jogadores[1].mostra_jogo = True
        for j in jogadores:
            j.printa_mao(gameDisplay)
        pygame.display.update()
        clock.tick(30)
        eventos_handler()
        if len(baralho) == 0:
            refil_baralho()


def refil_baralho():
    global baralho
    baralho = [c for c in lixo]
    baralho.remove(cartaVazia)
    lixo.clear()


def novo_jogo():
    global em_jogo, mensagem, mensagemOponente
    print('---------------------')
    print('##### NOVO JOGO #####')
    print('---------------------')
    em_jogo = True
    mensagem = COMPRAR
    mensagemOponente = ''
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
    jogadores.append(Jogador(mao_1))
    jogadores.append(Oponente(mao_2))


def init_baralho():
    baralho.clear()
    naipes = ['copas', 'paus', 'ouro', 'espadas']
    for i in range(4):
        for j in range(13):
            url = 'img_cartas//' + str(j+1) + '_' + naipes[i] + '.png'
            baralho.append(Carta((j+(13*i+1)), str(j+1), naipes[i], url))

if __name__ == '__main__':
    game_loop()


pygame.quit()
quit()