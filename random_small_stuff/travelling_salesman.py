from copy import copy
from random import random
from time import time

cities = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
distances = []
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
                    self.travel(i, cities[i], distances[self.index][i])
                elif len(self.path) == len(cities):
                    new_path = self.travel(0, self.path[0], self.curr_dist)
                    if final_path is None or final_path.curr_dist > new_path.curr_dist:
                        final_path = new_path

    def travel(self, index, city, distance):
        new_path = copy(self.path)
        new_path.append(city)
        new_dist = copy(self.curr_dist)
        new_dist += distance
        child_path = Path(index, new_path, new_dist)
        self.children.append(child_path)
        return child_path

    def __str__(self):
        return str(self.path) + ' - ' + str(self.curr_dist)


def main():
    global distances
    print('Calculating. Please wait...')
    t = time()

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

    Path(0, ['a'], 0)

    print(str(final_path))
    print('\nFinished in: ' + str(time() - t)[:7] + ' seconds.')


if __name__ == '__main__':
    main()
