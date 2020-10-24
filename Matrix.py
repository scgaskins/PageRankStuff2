from Vector import Vector


class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix  # should be a list of vectors
        self.num_rows = matrix[0].size
        self.num_columns = len(matrix)

    def __getitem__(self, item):
        return self.matrix[item]

    def __repr__(self):
        matrix_string = ''
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                matrix_string += str(self[j][i])
                matrix_string += ' '
            matrix_string += '\n'
        return matrix_string

    def same_size(self, other):
        if type(other) == Matrix:
            return self.num_rows == other.num_rows and self.num_columns == other.num_columns
        else:
            raise TypeError

    def get_row(self, row_index):
        row = []
        for i in range(self.num_columns):
            row.append(self[i][row_index])
        return row

    def __add__(self, other):
        if type(other) == Matrix:
            if self.same_size(other):
                new_matrix = []
                for i in range(self.num_columns):
                    new_matrix.append(self[i] + other[i])
                return Matrix(new_matrix)
            else:
                raise Exception('matrices must be the same size to be added')
        raise TypeError

    def __sub__(self, other):
        if type(other) == Matrix:
            return self + (-1 * other)
        else:
            raise TypeError

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            return self.multiply_scalars(other)
        elif type(other) == Vector:
            return self.multiply_with_vector(other)
        elif type(other) == Matrix:
            return self.multiply_matrices(other)
        else:
            raise TypeError

    def __rmul__(self, other):
        if type(other) == int or type(other) == float:
            return self.multiply_scalars(other)

    def multiply_scalars(self, scalar):
        new_matrix = []
        for i in range(self.num_columns):
            new_matrix.append(self[i] * scalar)
        return Matrix(new_matrix)

    def multiply_with_vector(self, other):
        if other.size == self.num_columns:
            products = []
            for i in range(self.num_rows):
                products.append(0)
                for j in range(self.num_columns):
                    products[i] += (self[j][i] * other[j])
            return Vector(products)
        else:
            raise Exception('Can only multiply with vectors of size == num columns')

    def multiply_matrices(self, other):
        if self.num_columns == other.num_rows:
            new_matrix = []
            for i in range(other.num_columns):
                new_matrix.append(self * other[i])
            return Matrix(new_matrix)
        else:
            raise Exception("columns on left must equal rows on right")

    def get_stochastic_matrix(self):
        new_matrix = []
        for vector in self.matrix:
            total_of_entries = sum(vector.entries)
            new_vector = []
            for i in range(vector.size):
                new_vector.append(vector[i] / total_of_entries)
            new_matrix.append(Vector(new_vector))
        return Matrix(new_matrix)

    def find_matrix_without_row_column(self, row, column):
        new_matrix = []
        for i in range(self.num_columns):
            if i != column:
                new_vector = []
                for j in range(self.num_rows):
                    if j != row:
                        new_vector.append(self[i][j])
                new_matrix.append(Vector(new_vector))
        return Matrix(new_matrix)

    def find_row_with_most_zeros(self):
        most_zeros = 0
        best_row = 0
        for i in range(self.num_rows):
            rowi = self.get_row(i)
            zeros = 0
            for entry in rowi:
                if entry == 0:
                    zeros += 1
            if zeros >= most_zeros:
                most_zeros = zeros
                best_row = i
        return best_row, most_zeros

    def find_column_with_most_zeros(self):
        most_zeros = 0
        best_col = 0
        for i in range(self.num_columns):
            zeros = 0
            for j in range(self[i].size):
                if self[i][j] == 0:
                    zeros += 1
            if zeros >= most_zeros:
                best_col = i
                most_zeros = zeros
        return best_col, most_zeros

    def get_minor(self, row, column):
        return self.find_matrix_without_row_column(row, column).get_determinant()

    def get_cofactor(self, row, column):
        return ((-1) ** (row + column)) * self.get_minor(row, column)

    def get_sum_of_cofactors_in_row(self, row):
        total = 0
        r = self.get_row(row)
        for i in range(len(r)):
            if r[i] != 0:
                total += r[i] * self.get_cofactor(row, i)
        return total

    def get_sum_of_cofactors_in_col(self, col):
        total = 0
        column = self[col]
        for i in range(column.size):
            if column[i] != 0:
                total += column[i] * self.get_cofactor(i, col)
        return total

    def get_determinant(self):
        if self.num_rows == 2 and self.num_columns == 2:
            return (self[0][0] * self[1][1]) - (self[0][1] * self[1][0])
        row_with_most_zeros, zeros_in_row = self.find_row_with_most_zeros()
        col_with_most_zeros, zeros_in_col = self.find_column_with_most_zeros()
        if zeros_in_col >= zeros_in_row:
            return self.get_sum_of_cofactors_in_col(col_with_most_zeros)
        return self.get_sum_of_cofactors_in_row(row_with_most_zeros)


if __name__ == '__main__':
    def test():
        v1 = Vector([2, 1])
        v2 = Vector([3, -5])
        m = Matrix([v1, v2])
        print(m)
        u1 = Vector([4, 1])
        u2 = Vector([3, -2])
        u3 = Vector([6, 3])
        m2 = Matrix([u1, u2, u3])
        print(m)
        print(m - m2)

    test()
