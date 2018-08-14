limiar = 0.5
resultados_and = {'1,1': 1,
                  '1,0': 0,
                  '0,1': 0,
                  '0,0': 0}

resultados_or = {'1,1': 1,
                 '1,0': 1,
                 '0,1': 1,
                 '0,0': 0}

resultados_xor = {'1,1': 0,
                  '1,0': 1,
                  '0,1': 1,
                  '0,0': 0}

pesos_and = [0, 0]
pesos_or = [0, 0]
pesos_xor = [
    [0, 0],
    [0, 0],
    [0, 0]
]


def main():
    while True:
        tipo = input('Tipo: ')
        if tipo == '':
            break
        if tipo == 'a':
            operador_and()
        elif tipo == 'o':
            operador_or()
        elif tipo == 'x':
            operador_xor()


def operador_and():
    while True:
        try:
            expressao = input('> ')
            if expressao == '':
                break
            rede = [int(i) for i in expressao.split(',')]
            result = 0
            for i in range(0, len(rede)):
                result += rede[i] * pesos_and[i]
            saida = 0 if result <= limiar else 1
            if saida != resultados_and[expressao]:
                print('Errou')
                for i in range(0, len(rede)):
                    pesos_and[i] += 0.5 * rede[i] * (resultados_and[expressao] - saida)
                    print('    - Peso ' + str(i) + ': ' + str(pesos_and[i]))
            else:
                print('Acertou')
        except:
            print('Entrada inválida')


def operador_or():
    while True:
        try:
            expressao = input('> ')
            if expressao == '':
                break
            rede = [int(i) for i in expressao.split(',')]
            result = 0
            for i in range(0, len(rede)):
                result += rede[i] * pesos_and[i]
            saida = 0 if result <= limiar else 1
            if saida != resultados_or[expressao]:
                print('Errou')
                for i in range(0, len(rede)):
                    pesos_or[i] += 0.5 * rede[i] * (resultados_or[expressao] - saida)
                    print('    - Peso ' + str(i) + ': ' + str(pesos_or[i]))
            else:
                print('Acertou')
        except:
            print('Entrada inválida')


def operador_xor():
    while True:
        try:
            expressao = input('> ')
            if expressao == '':
                break
            rede = [int(i) for i in expressao.split(',')]
            result = 0
            for i in range(0, len(rede)):
                result += rede[i] * pesos_and[i]
            saida = 0 if result <= limiar else 1
            if saida != resultados_or[expressao]:
                print('Errou')
                for i in range(0, len(rede)):
                    pesos_and[i] += 0.5 * rede[i] * (resultados_xor[expressao] - saida)
                    print('    - Peso ' + str(i) + ': ' + str(pesos_and[i]))
            else:
                print('Acertou')
        except:
            print('Entrada inválida')


if __name__ == '__main__':
    main()
