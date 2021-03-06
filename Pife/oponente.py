import random
import Pife.validador as validador
from Pife.jogador_base import JogadorBase


class Oponente(JogadorBase):
    def __init__(self, cartas):
        JogadorBase.__init__(self, cartas, False, 30)
        self.jogos = []
        self.pares = []

    def cria_jogo(self, c1, c2, c3):
        if not self.is_cartas_usadas([c1, c2, c3]):
            self.jogos.append([c1, c2, c3])

    def cria_par(self, c1, c2):
        if c1 not in self.cartas_usadas() and c2 not in self.cartas_usadas():
            self.pares.append([c1, c2])

    def printa_mao(self, display):
        self.organiza_cartas()
        JogadorBase.printa_mao(self, display)

    def organiza_cartas(self):
        cartas_soltas = [c for c in self.cartas if c not in self.cartas_usadas()+self.cartas_em_pares()]
        self.cartas.clear()
        for j in self.jogos:
            j.sort(key=lambda c: c.id_carta)
            self.cartas += j
        pares = []
        for p in self.pares:
            p.sort(key=lambda c: c.id_carta)
            pares += p
        self.cartas += [c for c in set(pares)] + cartas_soltas

    def descarta(self, carta_vazia):
        descarte = self.escolhe_carta_para_descartar()

        self.pares = [p for p in self.pares if descarte not in p]
        return self.descartar(descarte, carta_vazia)

    def escolhe_carta_para_descartar(self):
        cartas_validas = [c for c in self.cartas if c not in self.cartas_usadas()+self.cartas_em_pares()]
        if len(cartas_validas) == 0:
            for p in self.pares:
                p.sort(key=lambda c: c.id_carta)
                if p[0] != self.carta_lixo and p[1] != self.carta_lixo:
                    if (p[0].id_carta + 2) == p[1].id_carta:
                        pares_1 = len([p for p in self.pares if p[0] in p])
                        pares_2 = len([p for p in self.pares if p[1] in p])
                        if pares_1 == pares_2 == 1:
                            return p[0]
            else:
                cartas_validas = [c for c in self.cartas if c not in self.cartas_usadas() and c != self.carta_lixo]

        return cartas_validas[random.randrange(len(cartas_validas))]

    def compra(self, baralho, lixo, carta_vazia):
        if len(lixo) > 0 and self.valida_lixo(lixo[-1]):
            JogadorBase.compra(self, lixo, True, carta_vazia)
            return True
        else:
            JogadorBase.compra(self, baralho, False, carta_vazia)
            self.cria_jogos()
            return False

    def valida_lixo(self, carta):
        mao_hipotetica = self.cartas + [carta]
        mao_hipotetica.sort(key=lambda c: c.id_carta)
        self.validar_cartas(mao_hipotetica)
        return carta in self.cartas_usadas()+self.cartas_em_pares() and not self.trancado(mao_hipotetica, carta)

    def trancado(self, cartas, carta_lixo):
        for p in self.pares:
            if carta_lixo in p:
                p.sort(key=lambda c: c.id_carta)
                if p[0].id_carta+1 == p[1].id_carta:
                    return not self.has_cartas_soltas(cartas)

    def cria_jogos(self):
        self.cartas.sort(key=lambda c: c.id_carta)
        self.validar_cartas(self.cartas)

    def validar_cartas(self, cartas):
        self.limpar_jogos_e_pares()
        self.valida_e_cria_jogos(cartas)
        self.valida_e_cria_pares(cartas)

    def limpar_jogos_e_pares(self):
        self.jogos.clear()
        self.pares.clear()

    def valida_e_cria_jogos(self, cartas):
        # Verifica se possui sequência
        for c1 in cartas:
            c2 = self.busca_carta_por_id(c1.id_carta + 1, cartas)
            c3 = self.busca_carta_por_id(c1.id_carta + 2, cartas)
            if c2 is not None and c3 is not None:
                if validador.validar_sequencia([c1, c2, c3]):
                    self.cria_jogo(c1, c2, c3)
            if c1.valor == '12':
                c2 = self.busca_carta_por_id(c1.id_carta + 1, cartas)
                c3 = self.busca_carta_por_id(c1.id_carta - 11, cartas)
                if c2 is not None and c3 is not None:
                    if validador.validar_sequencia([c1, c2, c3]):
                        self.cria_jogo(c1, c2, c3)

        self.tenta_transformar_um_jogo_em_dois(cartas)
        # Verifica se possui trinca
        for i in range(1, 14):
            trinca = self.buscar_cartas_por_valor(str(i), cartas)
            if len(trinca) > 2:
                self.cria_jogo(trinca[0], trinca[1], trinca[2])

    def tenta_transformar_um_jogo_em_dois(self, cartas):
        for i in range(len(self.jogos)):
            jogo = self.jogos[i]
            trinca = self.buscar_cartas_por_valor(str(jogo[0].valor), cartas, False)
            nova_carta = self.busca_carta_por_id((jogo[2].id_carta+1), cartas)

            if len(trinca) == 3 and nova_carta is not None:
                self.jogos.remove(jogo)
                self.cria_jogo(trinca[0], trinca[1], trinca[2])
                self.cria_jogo(jogo[1], jogo[2], nova_carta)

    def valida_e_cria_pares(self, cartas):
        for c1 in cartas:  # Sequência
            c2 = self.busca_carta_por_id(c1.id_carta + 1)
            if c2 is None:
                c2 = self.busca_carta_por_id(c1.id_carta + 2)
            if c2 is not None and c2 not in self.cartas_usadas():
                if validador.par_sequencia([c1, c2]):
                    self.cria_par(c1, c2)
        for i in range(1, 14):  # Trinca
            par = self.buscar_cartas_por_valor(str(i), cartas)
            if len(par) == 2:
                self.cria_par(par[0], par[1])

    def jogar(self, baralho, lixo, carta_vazia):
        comprou_do_lixo = self.compra(baralho, lixo, carta_vazia)
        descarte = self.descarta(carta_vazia)
        self.organiza_cartas()
        return descarte, self.checar_mao(), comprou_do_lixo

    def busca_carta_por_id(self, id_carta, cartas=None):
        if cartas is None:
            carta = [c for c in self.cartas if c.id_carta == id_carta and c not in self.cartas_usadas()]
        else:
            carta = [c for c in cartas if c.id_carta == id_carta and c not in self.cartas_usadas()]
        if len(carta) == 0:
            return None
        return carta[0]

    def buscar_cartas_por_valor(self, valor, cartas=None, sem_uso=True):
        if sem_uso:
            if cartas is None:
                return [c for c in self.cartas if c.valor == valor and c not in self.cartas_usadas()]
            else:
                return [c for c in cartas if c.valor == valor and c not in self.cartas_usadas()]
        else:
            if cartas is None:
                return [c for c in self.cartas if c.valor == valor]
            else:
                return [c for c in cartas if c.valor == valor]

    def cartas_usadas(self):
        c = []
        for j in self.jogos:
            c += j
        return c

    def cartas_em_pares(self):
        c = []
        for p in self.pares:
            c += p
        return c

    def is_cartas_usadas(self, cartas):
        for c in cartas:
            if c in self.cartas_usadas():
                return True
        return False

    def checar_mao(self):
        if len(self.jogos) == 3:
            return JogadorBase.checar_mao(self)
        return False

    def has_cartas_soltas(self, cartas):
        for c in cartas:
            for p in self.pares:
                if c in p:
                    break
            else:
                return True
        return False


if __name__ == '__main__':
    pass