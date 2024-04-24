class Vertex:
    def __init__(self, pos_x: int, pos_y: int, *connected_to: int):
        self.x = pos_x
        self.y = pos_y
        self.connected_to = {vertex for vertex in connected_to}
        self.colour = (255, 255, 255)

    def __repr__(self):
        return [(self.x, self.y), self.connected_to]

    def connect(self, other):
        if isinstance(other, int):
            self.connected_to.add(other)
        else:
            raise TypeError

    def disconnect(self, other):
        if isinstance(other, int):
            self.connected_to.remove(other)
        else:
            raise TypeError

    def position(self):
        return self.x, self.y