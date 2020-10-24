class Vector:
    def __init__(self, entries):
        self.entries = entries
        self.size = len(entries)

    def duplicate_vector(self):
        duplicate = []
        for i in range(self.size):
            duplicate.append(self[i])
        return Vector(duplicate)

    def __repr__(self):
        s = ''
        for i in range(self.size):
            s += str(self[i])
            s += '\n'
        return s

    def __getitem__(self, item):
        return self.entries[item]

    def __setitem__(self, key, value):
        self.entries[key] = value

    def __add__(self, other):
        if self.size == other.size:
            new_vector = []
            for i in range(self.size):
                new_vector.append(self[i] + other[i])
            return Vector(new_vector)

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            return other * self

    def __rmul__(self, other):
        if type(other) == int or type(other) == float:
            new_vector = []
            for i in range(self.size):
                new_vector.append(self[i] * other)
            return Vector(new_vector)
        else:
            raise TypeError


if __name__ == '__main__':
    def test():
        v1 = Vector([1, 1, 0])
        v2 = Vector([0, 1, 0])
        print(v1)
        v1[0] = 2
        print(v1)

    test()
