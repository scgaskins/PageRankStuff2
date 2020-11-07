from Vector import Vector
from decimal import *


class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix  # should be a list of vectors
        self.num_rows = matrix[0].size
        self.num_columns = len(matrix)

    def duplicate_matrix(self):
        duplicate = []
        for i in range(self.num_columns):
            duplicate.append(self[i].duplicate_vector())
        return Matrix(duplicate)

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
        elif type(other) == Vector and self.num_columns == 1:
            return self + Matrix([other])
        raise TypeError

    def __sub__(self, other):
        if type(other) == Matrix:
            return self + (-1 * other)
        else:
            raise TypeError

    def __mul__(self, other):
        if type(other) == int or type(other) == float or type(other) == Decimal:
            return self.multiply_scalars(other)
        elif type(other) == Vector:
            return self.multiply_with_vector(other)
        elif type(other) == Matrix:
            return self.multiply_matrices(other)
        else:
            raise TypeError

    def __rmul__(self, other):
        if type(other) == int or type(other) == float or type(other) == Decimal:
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
            total_of_entries = Decimal(sum(vector.entries))
            new_vector = []
            for i in range(vector.size):
                new_vector.append(vector[i] / total_of_entries)
            new_matrix.append(Vector(new_vector))
        return Matrix(new_matrix)

    # Functions for finding the determinant

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

    # Row replacement functions

    def replace_row(self, row_index, new_row):
        if len(new_row) == self.num_columns:
            for i in range(self.num_columns):
                self[i][row_index] = new_row[i]
        else:
            raise Exception('new_row must have same number of entries as old row')

    def swap_rows(self, row1_index, row2_index):
        row1 = self.get_row(row1_index)
        row2 = self.get_row(row2_index)
        self.replace_row(row1_index, row2)
        self.replace_row(row2_index, row1)

    def get_multiple_of_row(self, row_index, multiplier):
        multiple_of_row = self.get_row(row_index)
        for i in range(len(multiple_of_row)):
            multiple_of_row[i] = multiple_of_row[i] * Decimal(multiplier)
        return multiple_of_row

    def add_multiple_of_other_row_to_row(self, row_index, other_row_index, multiplier):
        multiple_of_other_row = self.get_multiple_of_row(other_row_index, multiplier)
        row = self.get_row(row_index)
        for i in range(len(row)):
            row[i] = multiple_of_other_row[i] + row[i]
        self.replace_row(row_index, row)

    def multiply_row(self, row_index, multiplier):
        for i in range(self.num_columns):
            self[i][row_index] *= multiplier

    def find_first_non_zero_in_row(self, row_index):
        row = self.get_row(row_index)
        for i in range(len(row)):
            if row[i] != 0:
                return i
        return self.num_rows

    def is_in_echelon_form(self):
        prev_pivot_index = self.find_first_non_zero_in_row(0)
        for i in range(1, self.num_rows):
            current_pivot_index = self.find_first_non_zero_in_row(i)
            if prev_pivot_index >= current_pivot_index:
                if prev_pivot_index != current_pivot_index == self.num_rows:
                    return False
            prev_pivot_index = current_pivot_index
        return True

    def find_pivot_position_for_row(self, row_index):
        pivot_position = self.find_first_non_zero_in_row(row_index)
        i = row_index
        while i < self.num_rows:
            first_nonzero_pos = self.find_first_non_zero_in_row(i)
            if first_nonzero_pos < pivot_position:
                pivot_position = first_nonzero_pos
                self.swap_rows(row_index, i)
                i = row_index
            else:
                i += 1
        return pivot_position

    def set_pivot_value_to_one(self, pivot_row_index, pivot_index):
        pivot_value = self[pivot_index][pivot_row_index]
        if pivot_value != 1:
            multiplier = 1/pivot_value
            self.multiply_row(pivot_row_index, multiplier)

    def reduce_all_below_pivot(self, pivot_row_index, pivot_index):
        pivot_value = self[pivot_index][pivot_row_index]
        for i in range(pivot_row_index + 1, self.num_rows):
            value_below_pivot = self[pivot_index][i]
            if value_below_pivot != 0:
                multiplier = (-1 * value_below_pivot) / pivot_value
                self.add_multiple_of_other_row_to_row(i, pivot_row_index, multiplier)

    def reduce_all_above_pivot(self, pivot_row_index, pivot_index):
        pivot_value = self[pivot_index][pivot_row_index]
        for i in range(pivot_row_index - 1, -1, -1):
            value_above_pivot = self[pivot_index][i]
            if value_above_pivot != 0:
                multiplier = (-1 * value_above_pivot) / pivot_value
                self.add_multiple_of_other_row_to_row(i, pivot_row_index, multiplier)

    def put_in_echelon_form(self):
        for i in range(self.num_rows):
            pivot_pos = self.find_pivot_position_for_row(i)
            if pivot_pos < self.num_columns:
                self.set_pivot_value_to_one(i, pivot_pos)
                self.reduce_all_below_pivot(i, pivot_pos)

    def put_in_reduced_echelon_form(self):
        for i in range(self.num_rows - 1, -1, -1):
            pivot_pos = self.find_pivot_position_for_row(i)
            if pivot_pos < self.num_columns:
                self.reduce_all_above_pivot(i, pivot_pos)

    def row_reduce(self):
        new_matrix = self.duplicate_matrix()
        new_matrix.put_in_echelon_form()
        new_matrix.put_in_reduced_echelon_form()
        return new_matrix


if __name__ == '__main__':
    def test():
        v1 = Vector([4, 1, 3, 8])
        v2 = Vector([0, 7, 0, -4])
        v3 = Vector([0, 3, 0, 2])
        v4 = Vector([5, -5, 0, 7])
        m = Matrix([v1, v2, v3, v4])
        print(m)
        print(m.get_determinant())

    test()
