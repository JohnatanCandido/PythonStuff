import math


def padronizar(equacao, index):
    if equacao[index - 1] in('-', '+') or index == 0:
        equacao = equacao[:index] + '1' + equacao[index:]
        return equacao


def bhaskara(equacao):
    try:
        a = 1
        while True:
            i = equacao.find('-', a)
            a = i + 2
            if i == -1:
                break

            equacao = (equacao[:i] + '+' + equacao[i:])

        index = equacao.find('x^2')
        equacao = padronizar(equacao, index)
        index = equacao.find('x', index+2)
        equacao = padronizar(equacao, index)
        print(equacao)
        equacao = equacao.split('+')
        a = int(equacao[0].split('x^2')[0])
        b = int(equacao[1].split('x')[0])
        c = int(equacao[2])

        delta = b * b - 4 * a * c
        if delta >= 0:
            x1 = (-b + (math.sqrt(delta))) / (2 * a)
            x2 = (-b - (math.sqrt(delta))) / (2 * a)
            print(f'Delta = {delta:.2f}\nx1 = {x1:.2f}\nx2 = {x2:.2f}')
        else:
            print('Delta negativo: %f' % delta)

    except IndexError:
        print('Equação inválida!')
        bhaskara(input('Digite a equação no modelo: \"ax^2+bx+c\" '))
    except ValueError:
        print('Equação inválida!')
        bhaskara(input('Digite a equação no modelo: \"ax^2+bx+c\" '))


print('Para sair digite 0')
while True:
    formula = input('Digite a equação: ')
    if formula == '0':
        break
    bhaskara(formula)
