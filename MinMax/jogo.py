from sys import maxsize


class Node(object):
    def __init__(self, i_depth, i_playerNum, i_sticksRemaining, i_value=0):
        self.i_depth = i_depth
        self.i_playerNum = i_playerNum
        self.i_sticksRemaining = i_sticksRemaining
        self.i_value = i_value
        self.children = []
        self.CreateChildren()

    def CreateChildren(self):
        if self.i_depth >= 0:
            for i in range(1, 3):
                v = self.i_sticksRemaining - i
                self.children.append(Node(self.i_depth - 1,
                                          -self.i_playerNum,
                                          v,
                                          self.RealVal(v)))

    def RealVal(self, value):
        if value == 0:
            return maxsize * self.i_playerNum
        elif value < 0:
            return maxsize * -self.i_playerNum
        return 0

# ----------------------------------------------------------------------------------------------------------------------


def MinMax(node, i_depth, i_playerNum):
    if (i_depth == 0) or (abs(node.i_value) == maxsize):
        return node.i_value

    i_bestValue = maxsize * -i_playerNum

    for child in node.children:
        i_val = MinMax(child, i_depth - 1, -i_playerNum)
        menor = maxsize * i_playerNum - i_val
        maior = maxsize * i_playerNum - i_bestValue
        if abs(menor) < abs(maior):
            i_bestValue = i_val

    return i_bestValue

# ----------------------------------------------------------------------------------------------------------------------

def WinCheck(i_sticks, i_playerNum):
    if i_sticks <= 0:
        print('*'*30)
        if i_playerNum > 0:
            if i_sticks == 0:
                print('\t You Win!!!')
            else:
                print('\t Too Many! You Lose...')
        else:
            if i_sticks == 0:
                print('\t Comp Wins... Better Luck next time.')
            else:
                print('\t Comp error!')
        print('*'*30)
        return 0
    return 1


if __name__ == '__main__':
    i_stickTotal = 11
    i_depth = 8
    i_curPlayer = 1
    print('''INSTRUCTIONS: Be the player to pick up the last stick
    \t\t\t You can only pick 1 or 2 sticks at at time.''')

    while i_stickTotal > 0:
        print('\n%d sticks remain. How many would you like to pick up?' %i_stickTotal)
        i_choice = input('\n 1 or 2: ')
        i_stickTotal -= int(float(i_choice))

        if WinCheck(i_stickTotal, i_curPlayer):
            i_curPlayer *= -1
            node = Node(i_depth, i_curPlayer, i_stickTotal)
            bestChoice = -100
            i_bestValue = -i_curPlayer * maxsize

            for i in range(len(node.children)):
                n_child = node.children[i]
                i_val = MinMax(n_child, i_depth, i_curPlayer)
                if abs(i_curPlayer * maxsize - i_val) <= abs(i_curPlayer * maxsize - i_bestValue):
                    i_bestValue = i_val
                    bestChoice = i

            bestChoice += 1
            print("Comp chooses: " + str(bestChoice) + '\t Based on value: ' + str(i_bestValue))

            i_stickTotal -= bestChoice
            WinCheck(i_stickTotal, i_curPlayer)
            i_curPlayer *= -1