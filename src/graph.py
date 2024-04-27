from src.vertex import Vertex
from itertools import product
from src.colours import colours_generator


class Graph:
    def __init__(self):
        self.count = 0
        self.vertices = []
        self.not_included = []

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
        colours = list(colours_generator())
        for vertex in self.vertices:
            vertex.colour = (255, 255, 255)
        vertices_queue = [max(self.vertices, key=lambda x: len(x.connected_to)), ]

        for i in range(self.count):
            if len(vertices_queue) != 0:
                vertex = vertices_queue.pop(0)
            else:
                vertex = max([vertex for vertex in self.vertices if vertex.colour == (255, 255, 255)],
                             key=lambda x: len(x.connected_to))

            colour_idx = 0
            colours_to_skip = set()
            for connected in vertex.connected_to:
                if self.vertices[connected].colour != (255, 255, 255):
                    if self.vertices[connected].colour == colours[colour_idx]:
                        colour_idx += 1
                        while colours[colour_idx] in colours_to_skip:
                            colour_idx += 1
                    else:
                        colours_to_skip.add(self.vertices[connected].colour)
                else:
                    for (idx, queued) in enumerate(vertices_queue):
                        if len(self.vertices[connected].connected_to) > len(queued.connected_to):
                            vertices_queue.insert(idx, self.vertices[connected])
                            break
                    else:
                        vertices_queue.append(self.vertices[connected])
                    self.vertices[connected].colour = (255, 255, 254)

            vertex.colour = colours[colour_idx]
