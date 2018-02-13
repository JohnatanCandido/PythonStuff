import copy

class Node(object):
    def __init__(self, depth, board, player, max_layer, choice):
        self.choice = choice
        self.depth = depth
        self.board = copy.deepcopy(board)
        self.player = player
        self.max_layer = max_layer
        # Valor de empate por padrão
        self.value = 0
        self.children = []
        if depth == max_layer:
            self.i_win()
            if self.value == 0:
                self.i_lose()
                if self.value == 0:
                    self.do_play()
        else:
            # Tenta uma jogada
            self.do_play()
        if depth > 0 and self.value == 0:
            self.CreateChildren()

    def CreateChildren(self):
        for i in range(9):
            choice = i
            if choice > 8:
                choice -= 9
            if self.board.cells[choice] == " ":
                self.children.append(Node(self.depth-1, self.board, -self.player, self.max_layer, choice))

    def do_play(self):
        decisiva = False
        if self.player == 1:
            play = "O"
        else:
            play = "X"
            if self.depth+1 == self.max_layer:
                for i in range(9):
                    board = copy.deepcopy(self.board)
                    if board.cells[i] == " ":
                        board.cells[i] = "O"
                        if board.is_winner("O"):
                            self.board.cells[i] = play
                            self.choice = i
                            decisiva = True
        if not decisiva:
            self.board.cells[self.choice] = play
        if self.board.is_winner(play):  # Se ganha: 2 pontos, se perde: -1 ponto
            if play == 'X':
                self.value = -self.depth
            else:
                self.value = 2*self.depth
        elif self.board.is_tie():  # Se empata: 1 ponto
            self.value = self.depth

    def i_lose(self):
        for i in range(9):
            board = copy.deepcopy(self.board)
            if board.cells[i] == " ":
                board.cells[i] = "X"
                if board.is_winner("X"):  # Se o oponente vencer com essa jogada: 9999 pontos
                    self.value = 9999
                    self.choice = i
                    break

    def i_win(self):
        for i in range(9):
            board = copy.deepcopy(self.board)
            if board.cells[i] == " ":
                board.cells[i] = "O"
                if board.is_winner("O"):  # Se ganha com essa jogada: 99999 pontos
                    self.value = 99999
                    self.choice = i
                    break


def MinMax(node, depth):
    if depth == 0 or node.value > 99995:
        return node.value

    val = 0
    for child in node.children:
        if child.value == 99999:
            return child.value
        val += MinMax(child, depth-1)

    node.value += val
    return node.value


def escolhe(board, depth, player):
    nodes = []
    for i in range(9):
        if board.cells[i] == " ":
            nodes.append(Node(depth, board, player, depth, i))
    best_choice = nodes[0]
    choice = nodes[0].choice
    for node in nodes:
        node.val = MinMax(node, depth)
        if node.value == 99999:
            return node.choice
        elif node.value == 9999:
            return node.choice
        elif node.value > best_choice.value:
            best_choice = node
            choice = node.choice
    return choice