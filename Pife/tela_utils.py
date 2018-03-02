import pygame


def printar_texto(display, tam_fonte, mensagem, cor, coords):
    large_text = pygame.font.Font('freesansbold.ttf', tam_fonte)
    txt_surf, text_rect = _text_objects(mensagem, large_text, cor)
    text_rect.center = coords
    display.blit(txt_surf, text_rect)


def _text_objects(text, font, cor):
    text_surface = font.render(text, True, cor)
    return text_surface, text_surface.get_rect()