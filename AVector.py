from fractions import *


class AVector:
    def __init__(self, entries):
        self.entries = list(map(Fraction, entries))
        self.size = len(entries)

    def duplicate_vector(self):
        duplicate = []
        for i in range(self.size):
            duplicate.append(self[i])
        return AVector(duplicate)

    def __repr__(self):
        s = ''
        for i in range(self.size):
            s += str(self[i])
            s += '\n'
        return s

    def __getitem__(self, item):
        return self.entries[item]

    # Any entries are converted to decimals before
    # being put in
    def __setitem__(self, key, value):
        self.entries[key] = Fraction(value)

    def __add__(self, other):
        if self.size == other.size:
            new_vector = []
            for i in range(self.size):
                new_vector.append(self[i] + other[i])
            return AVector(new_vector)
        raise Exception("Can't add vectors of different sizes")

    def __sub__(self, other):
        if type(other) == AVector:
            return self + (-1 * other)
        raise TypeError

    def __mul__(self, other):
        if type(other) == int or type(other) == float or type(other) == Fraction:
            return other * self
        raise TypeError("Can only multiply vectors by scalars")

    def __rmul__(self, other):
        if type(other) == int or type(other) == float or type(other) == Fraction:
            new_vector = []
            for i in range(self.size):
                new_vector.append(self[i] * Fraction(other))
            return AVector(new_vector)
        else:
            raise TypeError("Can only multiply vectors by scalars")

    def dot_product(self, other):
        if type(other) == AVector:
            if other.size == self.size:
                product = 0
                for i in range(self.size):
                    product += self[i] * other[i]
                return product
            raise Exception("vectors must be the same size for dot products")
        raise TypeError("Can only dot vectors with vectors")


if __name__ == '__main__':
    def test():
        v1 = AVector([1, 1, 0])
        v2 = v1.duplicate_vector()
        print(v1)
        print(v2)
        print(v1 == v2)

    test()
