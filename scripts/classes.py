from math import sqrt
from numpy import max, min


class Match:
    def __init__(self, **kwargs):
        self.from_poly = None       # WordPoly
        self.to_poly = None         # WordPoly
        self.word_from = None       # str
        self.word_to = None         # str
        self.similarity = None      # float
        if 'from_poly' in kwargs:
            self.from_poly = kwargs['from_poly']
            self.word_from = self.from_poly.word
        elif 'word_from' in kwargs:
            self.word_from = kwargs['word_from']
        if 'to_poly' in kwargs:
            self.to_poly = kwargs['to_poly']
            self.word_to = self.to_poly.word
        elif 'word_to' in kwargs:
            self.word_to = kwargs['word_to']
        if 'similarity' in kwargs:
            self.similarity = kwargs['similarity']

    def __str__(self):
        output = (
            '`M` {'
            f'{self.word_from:<10} , '
            f'{self.word_to:<10} '
            f'{self.similarity}'
            '}'
        )
        return output

    def __repr__(self):
        output = (
            '`M` {'
            f'{self.word_from:<10} , '
            f'{self.word_to:<10} '
            f'{self.similarity}'
            '}'
        )
        return output


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

    def __str__(self):
        temp_x = int(self.x * 10000) / 10000
        temp_y = int(self.y * 10000) / 10000
        return (
            f'`V` x: {temp_x:<10}'
            f'y: {temp_y:<10}'
        )

    def __eq__(self, other):
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        return True

    def __ne__(self, other):
        if self.x != other.x:
            return True
        if self.y != other.x:
            return True
        return False


class WordPoly:
    def __init__(self, *args, **kwargs):
        self.confidence = None      # float
        self.word = None            # string
        self.center = None          # Vertex
        self.para_idx = None        # int
        self.block_idx = None       # int
        self.vertices = []          # list of Vertex
        if 'block_idx' in kwargs:
            self.block_idx = kwargs['block_idx']
        if 'para_idx' in kwargs:
            self.para_idx = kwargs['para_idx']
        if 'vertices' in kwargs:
            self.vertices = kwargs['vertices']
        else:
            self.vertices = [*args]
        if 'center' in kwargs:
            self.center = kwargs['center']
        else:
            self.get_center()
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
            x /= i+1
            y /= i+1
            self.center = Vertex(x, y)
            return self.center

    def get_height(self):
        return abs(self.vertices[0].y - self.vertices[2].y)

    def get_width(self):
        return abs(self.vertices[0].x - self.vertices[2].x)

    def manhattan_to(self, a_word_poly):
        return self.center.manhattan_to(a_word_poly.center)

    def pythagorean_to(self, a_word_poly):
        return self.center.pythagorean_to(a_word_poly.center)

    def __str__(self):
        temp_conf = int(self.confidence * 100000) / 100000
        output = (
            '`WP` {'
            f'{self.word:13} '
            f'{temp_conf:<8} '
        )
        if self.block_idx is not None:
            output += f'b: {self.block_idx:<3} '
        if self.para_idx is not None:
            output += f'p: {self.para_idx:<3} '
        output += '}'
        return output

    def __repr__(self):
        temp_conf = int(self.confidence * 100000) / 100000
        output = (
            '`WP` {'
            f'{self.word:13} '
            f'{temp_conf:<8} '
        )
        if self.block_idx is not None:
            output += f'b: {self.block_idx:<3} '
        if self.para_idx is not None:
            output += f'p: {self.para_idx:<3} '
        output += '}'
        return output

    def __eq__(self, other):
        if len(self.vertices) != len(other.vertices):
            return False
        for v1, v2 in zip(self.vertices, other.vertices):
            if v1 != v2:
                return False
        if self.word != other.word:
            return False
        # not comparing block and para idx since if they have the same vertices,
        # and the idx info was not provided, they should be seen as equal
        return True

    def __len__(self):
        return len(self.word)


class Constraint:
    def __init__(self, *args):
        self.constraints = [*args]     # list of constraint function pointers

    def satisfies(self, obj):
        for constraint in self.constraints:
            if not constraint(obj):
                return False
        return True

    def add_constraint(self, con):
        self.constraints.append(con)


if __name__ == '__main__':
    vert1 = Vertex(1.9484390840042,2)
    poly1 = WordPoly(
        word='hello',
        vertices=[Vertex(1.9484390840042,2),
                  Vertex(2.9484390840042,2),
                  Vertex(2.9484390840042,1),
                  Vertex(1.9484390840042,1)],
        confidence=.938394543,
        para_idx=2,
        block_idx=0
    )
    poly2 = WordPoly(
        word='there',
    )
    thing = Match(
        from_poly=poly1,
        to_poly=poly2,
        similarity=.89
    )
    print(poly1)

