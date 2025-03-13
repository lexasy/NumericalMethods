class Matrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.columns = len(data[0])

    def __str__(self):
        result = ""
        for row in self.data:
            for el in row:
                result += f"{el:.4f} "
            result += "\n"
        return result
    
    def add(self, other):
        result = []
        for i in range(self.rows):
            result_row = [self.data[i][j] + other.data[i][j] for j in range(self.columns)]
            result.append(result_row)
        return Matrix(result)
    
    def subtraction(self, other):
        result = []
        for i in range(self.rows):
            result_row = [self.data[i][j] - other.data[i][j] for j in range(self.columns)]
            result.append(result_row)
        return Matrix(result)
    
    def multiply(self, other):
        result = []
        for i in range(self.rows):
            result_row = []
            for j in range(other.columns):
                element = sum(self.data[i][k] * other.data[k][j] for k in range(self.columns))
                result_row.append(element)
            result.append(result_row)
        return Matrix(result)
    
    def regularization(self):
        max_row_sum = 0
        for i in range(self.rows):
            row_sum = sum(abs(self.data[i][j]) for j in range(self.columns))
            max_row_sum = max(max_row_sum, row_sum)
        return max_row_sum
    
    def decomposition(self):
        new_data_upper = [[0 for i in range(self.rows)] for j in range(self.rows)]
        new_data_lower = [[0 for i in range(self.rows)] for j in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.rows):
                if j < i:
                    new_data_lower[i][j] = self.data[i][j]
                else:
                    new_data_upper[i][j] = self.data[i][j]
        return Matrix(new_data_lower), Matrix(new_data_upper)
    
    @classmethod
    def read(cls):
        rows = int(input("Please, type quantity of equations in system: "))
        data = []
        for i in range(rows):
            row = list(map(int, input(f"Type ratios before variables in {i + 1} equation: ").split()))
            right_part = int(input("Type the right part of equation: "))
            row.append(right_part)
            data.append(row)
        return cls(data)
    
    @classmethod
    def elementary(cls, rows_quantity):
        new_data = [[0 for i in range(rows_quantity)] for j in range(rows_quantity)]
        for i in range(rows_quantity):
            new_data[i][i] = 1
        return cls(new_data)

    
def delete_right_parts(matrix: Matrix):
    for i in range(matrix.rows):
        matrix.data[i].pop(matrix.columns - 1)

def extend_matrix(matrix: Matrix):
    indices_data = [[] for _ in range(matrix.rows)]
    for i in range(matrix.rows):
        for j in range(matrix.rows):
            matrix.data[i].append(0 if i != j else 1)
        for j in range(matrix.rows):
            indices_data[i].append((j + 1, matrix.rows - i))
    return Matrix(indices_data) 
    
def edit_for_reverse(matrix: Matrix, is_right_parts):
    if is_right_parts:
        delete_right_parts(matrix)
    indices_matrix = extend_matrix(matrix)
    return Matrix(matrix.data), indices_matrix