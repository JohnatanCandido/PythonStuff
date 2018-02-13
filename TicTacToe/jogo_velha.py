import os
import oponente as op
os.system('cls')


class Board(object):
    def __init__(self):
        self.cells = [" " for _ in range(10)]

    def display(self):
        print("\n %s | %s | %s" % (self.cells[0], self.cells[1], self.cells[2]))
        print('-----------')
        print(" %s | %s | %s" % (self.cells[3], self.cells[4], self.cells[5]))
        print('-----------')
        print(" %s | %s | %s" % (self.cells[6], self.cells[7], self.cells[8]))

    def update_cell(self, cell, player):
        if self.cells[cell] == " ":
            self.cells[cell] = player
            refresh_screen()
        else:
            if player == "O":
                for i in range(9):
                    if self.cells[i] == " ":
                        self.cells[i] = "O"
                        break
            else:
                do_play(player, True)

    def is_tie(self):
        used_cells = 0
        for cell in self.cells:
            if cell != " ":
                used_cells += 1

        if used_cells == 9:
            return True
        return False

    def is_winner(self, player):
        if self.cells[0] == self.cells[1] == self.cells[2] == player:  # top row
            return True
        elif self.cells[3] == self.cells[4] == self.cells[5] == player:  # middle row
            return True
        elif self.cells[6] == self.cells[7] == self.cells[8] == player:  # bottom row
            return True
        elif self.cells[0] == self.cells[3] == self.cells[6] == player:  # left collumn
            return True
        elif self.cells[1] == self.cells[4] == self.cells[7] == player:  # middle collumn
            return True
        elif self.cells[2] == self.cells[5] == self.cells[8] == player:  # right collumn
            return True
        elif self.cells[0] == self.cells[4] == self.cells[8] == player:  # diagonal 1
            return True
        elif self.cells[2] == self.cells[4] == self.cells[6] == player:  # diagonal 2
            return True
        return False


board = Board()
in_game = True


def refresh_screen():
    os.system('cls')
    board.display()


def do_play(player, wrong=False):
    refresh_screen()
    if wrong:
        print('\n### ERRO ### \nEsta posição já foi marcada! \nEscolha outra. ')
    choice = int(input('\n%s) Escolha a posição: 1 - 9: ' % player))
    board.update_cell((choice-1), player)
    fim_de_jogo(player)


def fim_de_jogo(player):
    global in_game
    if board.is_winner(player):
        print(player, " ganhou!")
        in_game = False
    elif board.is_tie():
        print('Empate!')
        in_game = False

# op_choice = op.escolhe(board, 3, -1)
# board.update_cell(op_choice, "X")
# fim_de_jogo("X")
while True:
    if in_game:
        do_play("X")
    if in_game:
        n = 0
        for cell in board.cells:
            if cell == " ":
                n += 1
        op_choice = op.escolhe(board, n, 1)
        board.update_cell(op_choice, "O")
        fim_de_jogo("O")
    # if in_game:
    #     op_choice = op.escolhe(board, 3, -1)
    #     board.update_cell(op_choice, "X")
    #     fim_de_jogo("X")

    if not in_game:
        novo_jogo = input('Deseja jogar novamente? s/n: ')
        if novo_jogo == 's':
            board = Board()
            in_game = True
        else:
            break
