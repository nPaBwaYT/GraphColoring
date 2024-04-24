from src.vertex import Vertex
from itertools import product
from src.colours import colours_generator


class Graph:
    def __init__(self):
        self.count = 0
        self.vertices = []

    def add(self, pos_x: int, pos_y: int, *connected_to: int):
        self.vertices.append(Vertex(pos_x, pos_y))
        for num in connected_to:
            self.connect(self.count, num - 1)
        self.count += 1

    def delete(self, index: int):
        connected = self.vertices[index - 1].connected_to
        for con in connected:
            self.vertices[con].disconnect(index - 1)

        for vertex in self.vertices:
            vertex.connected_to = set(
                map(lambda x: x - 1 if (x >= index) else x, vertex.connected_to))

        self.vertices.pop(index - 1)
        self.count -= 1

    def clear(self):
        self.vertices.clear()
        self.count = 0

    def connect(self, first_index: int, second_index: int):
        self.vertices[first_index - 1].connect(second_index - 1)
        self.vertices[second_index - 1].connect(first_index - 1)

    def disconnect(self, first_index: int, second_index: int):
        self.vertices[first_index - 1].disconnect(second_index - 1)
        self.vertices[second_index - 1].disconnect(first_index - 1)

    def reset(self):
        for vertex in self.vertices:
            vertex.colour = (255, 255, 255)

    def colour(self):
        found = []
        already_marked = [0 for i in range(self.count)]

        for values in product((1, 0), repeat=self.count):

            if self.is_subset(values, already_marked):
                continue

            f = 1
            for st in range(self.count):
                if not values[st]:
                    continue
                k = 1
                for fi in self.vertices[st].connected_to:
                    k = k and not values[fi]
                    if not k:
                        break
                f = f and k
                if not f:
                    break

            if f:
                s_sets = found
                for s_set in s_sets:
                    if self.is_subset(s_set, values):
                        found.remove(s_set)

                found.append(values)
                for (idx, val) in enumerate(values):
                    already_marked[idx] = already_marked[idx] or val

        colours = list(colours_generator())
        for (s_set, colour) in zip(found, colours):
            for (idx, val) in enumerate(s_set):
                if val:
                    self.vertices[idx].colour = colour

    @staticmethod
    def is_subset(first, second):
        for (l, r) in zip(first, second):
            if (l == 1) and (r == 0):
                return False
        return True
