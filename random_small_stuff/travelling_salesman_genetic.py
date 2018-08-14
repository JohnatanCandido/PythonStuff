from time import time
from random import random

cities = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
distances = []
geracoes = []


class Caminho:
    def __init__(self, caminho):
        self.caminho = caminho
        self.fitness = 9999

    def __str__(self):
        return 'Melhor caminho: ' + str(self.caminho) + '. Distância: ' + str(self.fitness)


def main(dists, new_cities):
    global distances, cities
    cities = new_cities
    print('\n\n### Genético ###')
    print('Calculating. Please wait...')
    t = time()

    if dists is None:
        distances = [[0 for _ in cities] for _ in cities]
        for i in range(len(cities)):
            for j in range(i + 1, len(cities)):
                if i == j:
                    distances.append(0)
                else:
                    d = 0
                    while d == 0:
                        d = int(random() * 100)
                    distances[i][j] = d
                    distances[j][i] = d
    else:
        distances = dists

    r = gerar('a', 500, 100)
    print('\nFinished in: ' + str(time() - t)[:7] + ' seconds.')
    return r.caminho


def gerar(cidade_inicial, tamanho_geracao, quantidade_geracoes):
    populacao = []
    for i in range(tamanho_geracao):
        path = [cidade_inicial]
        while True:
            cidade = cities[int(random() * len(cities))]
            if cidade not in path:
                path.append(cidade)
            elif len(path) == len(cities):
                path.append(cidade_inicial)
                break
        populacao.append(Caminho(path))
    geracoes.append(populacao)

    nova_populacao = populacao
    for i in range(quantidade_geracoes):
        if i > 10:  # i > int(len(nova_populacao)/10):
            if checar_fitness():
                print('>>>>>> break na geração: ' + str(i))
                break
        for c in nova_populacao:
            c.fitness = 0
            for j in range(len(c.caminho)-1):
                c.fitness += distances[cities.index(c.caminho[j])][cities.index(c.caminho[j + 1])]
        nova_populacao.sort(key=lambda x: x.fitness)
        nova_populacao = cruzar(nova_populacao)
        geracoes.append(nova_populacao)

    melhores = []
    for p in geracoes:
        p.sort(key=lambda x: x.fitness)
        melhores.append(p[0])
    melhores.sort(key=lambda x: x.fitness)
    print(str(melhores[0]))
    if len(set(melhores[0].caminho)) != len(cities):
        print('####### Cidades faltando! Desconsiderar! #######')
    return melhores[0]


def cruzar(populacao):
    nova_populacao = populacao[:int(len(populacao) / 4)] + populacao[int(len(populacao) / 4*3):]
    print(len(populacao))
    print(len(nova_populacao))
    for i in range(0, len(nova_populacao), 2):
        filho_1 = []
        filho_2 = []
        a = True
        for j in range(len(nova_populacao[i].caminho)):
            if a:
                filho_1.append(nova_populacao[i].caminho[j])
                filho_2.append(nova_populacao[i+1].caminho[j])
            else:
                filho_1.append(nova_populacao[i + 1].caminho[j])
                filho_2.append(nova_populacao[i].caminho[j])
            if j + 1 % 3 == 0:
                a = not a
        if 50 < random() * 5000 < 60:
            mutar(filho_1)
            mutar(filho_2)
        nova_populacao.append(Caminho(filho_1))
        nova_populacao.append(Caminho(filho_2))
    return nova_populacao


def checar_fitness():
    somas = []
    for i in range(len(geracoes)-1, len(geracoes)-10, -1):
        soma = 0
        for c in geracoes[i]:
            soma += c.fitness
        if soma not in somas:
            somas.append(soma)
    if len(somas) < 5:
        return True
    return False


def mutar(caminho):
    while True:
        c1 = int(random()*len(caminho))
        c2 = int(random()*len(caminho))
        if caminho[c1] != 'a' and caminho[c2] != 'a':
            print('> Mutou!')
            aux = caminho[c1]
            caminho[c1] = caminho[c2]
            caminho[c2] = aux
            break


if __name__ == '__main__':
    main(None, cities)
