from copy import copy
from random import random
from time import time
import random_small_stuff.travelling_salesman_genetic as tsg

cities = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
distances = [[0, 36, 45, 58, 48, 44, 96, 18, 88, 67, 28, 13, 2, 70, 1, 78, 34, 80, 76, 1, 91, 52, 23, 54, 98],
             [36, 0, 33, 62, 38, 76, 5, 32, 31, 22, 88, 97, 19, 69, 27, 16, 69, 45, 82, 22, 76, 66, 27, 16, 7],
             [45, 33, 0, 27, 49, 55, 75, 16, 14, 69, 93, 52, 58, 81, 88, 99, 84, 27, 95, 12, 78, 18, 93, 51, 4],
             [58, 62, 27, 0, 73, 51, 38, 53, 75, 7, 23, 5, 16, 33, 65, 23, 69, 27, 46, 8, 99, 90, 28, 27, 11],
             [48, 38, 49, 73, 0, 71, 45, 46, 24, 66, 38, 93, 61, 92, 3, 75, 93, 36, 38, 17, 89, 42, 65, 33, 22],
             [44, 76, 55, 51, 71, 0, 97, 27, 28, 38, 10, 89, 22, 90, 83, 84, 26, 36, 38, 77, 14, 77, 65, 83, 64],
             [96, 5, 75, 38, 45, 97, 0, 27, 25, 93, 96, 66, 29, 72, 77, 23, 13, 23, 56, 75, 13, 61, 67, 22, 92],
             [18, 32, 16, 53, 46, 27, 27, 0, 87, 36, 16, 57, 88, 10, 42, 92, 73, 36, 54, 98, 70, 81, 64, 62, 82],
             [88, 31, 14, 75, 24, 28, 25, 87, 0, 56, 49, 21, 23, 12, 75, 6, 63, 73, 40, 81, 48, 24, 44, 35, 15],
             [67, 22, 69, 7, 66, 38, 93, 36, 56, 0, 51, 72, 48, 20, 76, 18, 20, 51, 57, 54, 93, 37, 96, 19, 13],
             [28, 88, 93, 23, 38, 10, 96, 16, 49, 51, 0, 60, 15, 64, 97, 37, 86, 48, 13, 46, 49, 16, 35, 34, 56],
             [13, 97, 52, 5, 93, 89, 66, 57, 21, 72, 60, 0, 10, 3, 96, 77, 86, 34, 19, 99, 33, 14, 93, 78, 87],
             [2, 19, 58, 16, 61, 22, 29, 88, 23, 48, 15, 10, 0, 2, 86, 33, 85, 37, 7, 81, 79, 97, 18, 75, 47],
             [70, 69, 81, 33, 92, 90, 72, 10, 12, 20, 64, 3, 2, 0, 1, 1, 13, 47, 95, 5, 96, 24, 37, 69, 63],
             [1, 27, 88, 65, 3, 83, 77, 42, 75, 76, 97, 96, 86, 1, 0, 32, 96, 10, 52, 25, 68, 41, 16, 60, 35],
             [78, 16, 99, 23, 75, 84, 23, 92, 6, 18, 37, 77, 33, 1, 32, 0, 23, 41, 83, 90, 2, 94, 13, 91, 85],
             [34, 69, 84, 69, 93, 26, 13, 73, 63, 20, 86, 86, 85, 13, 96, 23, 0, 97, 85, 31, 20, 73, 12, 2, 64],
             [80, 45, 27, 27, 36, 36, 23, 36, 73, 51, 48, 34, 37, 47, 10, 41, 97, 0, 3, 81, 65, 19, 19, 71, 13],
             [76, 82, 95, 46, 38, 38, 56, 54, 40, 57, 13, 19, 7, 95, 52, 83, 85, 3, 0, 56, 88, 78, 1, 37, 95],
             [1, 22, 12, 8, 17, 77, 75, 98, 81, 54, 46, 99, 81, 5, 25, 90, 31, 81, 56, 0, 23, 79, 68, 36, 30],
             [91, 76, 78, 99, 89, 14, 13, 70, 48, 93, 49, 33, 79, 96, 68, 2, 20, 65, 88, 23, 0, 9, 20, 39, 71],
             [52, 66, 18, 90, 42, 77, 61, 81, 24, 37, 16, 14, 97, 24, 41, 94, 73, 19, 78, 79, 9, 0, 49, 84, 85],
             [23, 27, 93, 28, 65, 65, 67, 64, 44, 96, 35, 93, 18, 37, 16, 13, 12, 19, 1, 68, 20, 49, 0, 73, 5],
             [54, 16, 51, 27, 33, 83, 22, 62, 35, 19, 34, 78, 75, 69, 60, 91, 2, 71, 37, 36, 39, 84, 73, 0, 9],
             [98, 7, 4, 11, 22, 64, 92, 82, 15, 13, 56, 87, 47, 63, 35, 85, 64, 13, 95, 30, 71, 85, 5, 9, 0]]

final_path = None


class Path:
    def __init__(self, index, path, dist):
        self.path = path
        self.curr_dist = dist
        self.index = index
        self.children = []
        global final_path
        if final_path is None or self.curr_dist < final_path.curr_dist:
            for i in range(len(cities)):
                if cities[i] not in self.path:
                    self.travel(i, cities[i])
                elif len(self.path) == len(cities):
                    new_path = self.travel(0, self.path[0])
                    if final_path is None or final_path.curr_dist > new_path.curr_dist:
                        final_path = new_path

    def travel(self, index, city):
        new_path = copy(self.path)
        new_path.append(city)
        new_dist = calcular_distancia(new_path)
        child_path = Path(index, new_path, new_dist)
        self.children.append(child_path)
        return child_path

    def __str__(self):
        return 'Melhor caminho: ' + str(self.path) + '. Distância: ' + str(self.curr_dist)


def main():
    global distances
    if len(distances) == 0:
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
        for d in distances:
            print(d)

    tsg_caminho = tsg.main(distances, cities)
    calcular_distancia(tsg_caminho)

    print('\n\n### Árvore ###')
    print('Calculating. Please wait...')
    t = time()

    Path(0, ['a'], 0)

    print(str(final_path))
    print('\nFinished in: ' + str(time() - t)[:7] + ' seconds.')
    calcular_distancia(final_path.path)


def calcular_distancia(caminho):
    distancia = 0
    for i in range(len(caminho)-1):
        distancia += distances[cities.index(caminho[i])][cities.index(caminho[i+1])]
    # print(str(caminho) + '. ' + str(distancia))
    return distancia


if __name__ == '__main__':
    main()
