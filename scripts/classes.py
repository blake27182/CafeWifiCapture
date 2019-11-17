from math import sqrt
from numpy import max, min


class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def manhattan_to(self, a_vertex):
        return abs(self.x - a_vertex.x) + abs(self.y - a_vertex.y)

    def pythagorean_to(self, a_vertex):
        return sqrt(
            (self.x - a_vertex.x)**2
            + (self.y - a_vertex.y)**2
        )

    def inside(self, a_word_poly):
        xss = [
            self.x - a_word_poly.vertices[0].x,
            self.x - a_word_poly.vertices[1].x,
            self.x - a_word_poly.vertices[2].x,
            self.x - a_word_poly.vertices[3].x
        ]
        x_within = min(xss) < 0 < max(xss)
        yss = [
            self.y - a_word_poly.vertices[0].y,
            self.y - a_word_poly.vertices[1].y,
            self.y - a_word_poly.vertices[2].y,
            self.y - a_word_poly.vertices[3].y
        ]
        y_within = max(yss) > 0 > min(yss)
        return x_within and y_within


class WordPoly:
    def __init__(self, *args, **kwargs):
        self.confidence = None      # float
        self.word = None            # string
        self.center = None          # Vertex
        self.vertices = []          # list of Vertex
        if 'vertices' in kwargs:
            self.vertices = kwargs['vertices']
        else:
            self.vertices = [*args]
        if 'center' in kwargs:
            self.center = kwargs['center']
        else:
            self.center = self.get_center()
        if 'confidence' in kwargs:
            self.confidence = kwargs['confidence']
        if 'word' in kwargs:
            self.word = kwargs['word']

    def get_center(self):
        x = 0
        y = 0
        if self.vertices:
            for i, vertex in enumerate(self.vertices):
                x += vertex.x
                y += vertex.y
            x /= i
            y /= i
            return Vertex(x, y)

    def manhattan_to_center(self, a_word_poly):
        return self.center.manhattan_to(a_word_poly.center)

    def pythagorean_to_center(self, a_word_poly):
        return self.center.pythagorean_to(a_word_poly.center)

    def print(self):
        temp_x = int(self.center.x * 1000000) / 1000000
        temp_y = int(self.center.y * 1000000) / 1000000
        temp_conf = int(self.confidence * 100000) / 100000
        print(f'{self.word:10} '
              f'{temp_conf:<8} '
              f'x: {temp_x:<12} '
              f'y: {temp_y:<15}')
