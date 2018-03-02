import pygame


display = None
carta_vazia = None
msg_player = ''
msg_oponente = ''


def init(init_carta_vazia, msg):
    global carta_vazia, display, msg_player
    carta_vazia = init_carta_vazia
    msg_player = msg


def printar_texto(tam_fonte, mensagem, cor, coords):
    large_text = pygame.font.Font('freesansbold.ttf', tam_fonte)
    txt_surf, text_rect = _text_objects(mensagem, large_text, cor)
    text_rect.center = coords
    display.blit(txt_surf, text_rect)


def _text_objects(text, font, cor):
    text_surface = font.render(text, True, cor)
    return text_surface, text_surface.get_rect()


def printa_tela(rodada, vitorias, derrotas, lixo):
    display.fill((0, 155, 0))
    printa_centro_tela(lixo)
    printa_mensagens()
    printa_placar(rodada, vitorias, derrotas)


def printa_centro_tela(lixo):
    # lixo
    if len(lixo) > 0:
        carta_lixo = pygame.image.load(lixo[-1].url)
        display.blit(carta_lixo, (800, 300))
        printar_texto(15, 'Lixo', (0, 0, 255), (835, 415))

    # bolo
    imagem_bolo = pygame.image.load(carta_vazia.url)
    display.blit(imagem_bolo, (480, 300))
    printar_texto(15, 'Bolo', (0, 0, 255), (515, 415))


def printa_mensagens():
    printar_texto(30, msg_oponente, (255, 0, 0), (675, 200))
    printar_texto(30, msg_player, (255, 0, 0), (675, 500))


def printa_placar(rodada, vitorias, derrotas):
    printar_texto(15, 'Rodada: ' + str(rodada), (0, 0, 255), (45, 630))
    printar_texto(15, 'Vitórias: ' + str(vitorias), (0, 0, 255), (45, 660))
    printar_texto(15, 'Derrotas: ' + str(derrotas), (0, 0, 255), (47, 690))


if __name__ == '__main__':
    pass