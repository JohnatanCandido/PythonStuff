def validar(cartas):
    cartas.sort(key=lambda c: c.id_carta)
    c1 = cartas[0]
    c2 = cartas[1]
    c3 = cartas[2]

    return sequencia(c1, c2, c3) or trinca(c1, c2, c3)


def validar_sequencia(cartas):
    cartas.sort(key=lambda c: c.id_carta)
    c1 = cartas[0]
    c2 = cartas[1]
    c3 = cartas[2]

    return sequencia(c1, c2, c3)


def validar_trinca(cartas):
    cartas.sort(key=lambda c: c.id_carta)
    c1 = cartas[0]
    c2 = cartas[1]
    c3 = cartas[2]

    return trinca(c1, c2, c3)


def sequencia(c1, c2, c3):
    if c1.naipe == c2.naipe and (c1.naipe == c3.naipe or c3.valor == 'joker'):
        if (c1.id_carta + 1) == c2.id_carta:
            if (c2.id_carta + 1) == c3.id_carta or c3.valor == 'joker':
                return True
        if c1.valor == '1' and (c2.valor == '12' or c2.valor == '13'):
            if c3.valor == '13' or c3.valor == 'joker':
                return True
    return False


def trinca(c1, c2, c3):
    if c1.valor == c2.valor == c3.valor:
        if c1.naipe != c2.naipe != c3.naipe:
            return True
    if c1.valor == c2.valor and c3.valor == 'joker':
        if c1.naipe != c2.naipe:
            return True
    return False


def par_trinca(c1, c2):
    return c1.valor == c2.valor and c1.naipe != c2.naipe


def par_sequencia(par):
    par.sort(key=lambda c: c.id_carta)
    c1 = par[0]
    c2 = par[1]
    if c1.naipe == c2.naipe:
        if (c1.id_carta + 1) == c2.id_carta or (c1.id_carta + 2) == c2.id_carta:
            return True
    return False


if __name__ == '__main__':
    pass