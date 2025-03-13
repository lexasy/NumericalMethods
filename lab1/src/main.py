import sys
import copy

from tools.matrix import Matrix
from tools.matrix import edit_for_reverse

def reverse(matrix: Matrix, is_right_parts):
    # calculating reversed matrix
    matrix_for_reverse, indices_matrix = edit_for_reverse(copy.deepcopy(matrix), is_right_parts)
    # straight running
    for i in range(matrix_for_reverse.rows - 1):
        if matrix_for_reverse.data[i][i] == 0:
            for j in range(matrix_for_reverse.rows):
                if matrix_for_reverse.data[j][i] != 0:
                    matrix_for_reverse.data[i], matrix_for_reverse.data[j] = matrix_for_reverse.data[j], matrix_for_reverse.data[i]
                    indices_matrix.data[i], indices_matrix.data[j] = indices_matrix.data[j], indices_matrix.data[i]
                    break
        ratios = []
        for j in range(i + 1, matrix_for_reverse.rows):
            ratios.append(-(matrix_for_reverse.data[j][i] / matrix_for_reverse.data[i][i]))
        for j in range(i + 1, matrix_for_reverse.rows):
            for k in range(i, matrix_for_reverse.columns):
                matrix_for_reverse.data[j][k] += matrix_for_reverse.data[i][k] * ratios[j - i - 1]

    #reverse running
    variables = [[0 for i in range(indices_matrix.rows)] for j in range(indices_matrix.rows)]
    for i in range(indices_matrix.rows, 0, -1):
        for j in range(matrix_for_reverse.rows, 0, -1):
            right_part = matrix_for_reverse.data[j - 1][matrix_for_reverse.columns - i]
            for k in range(j, matrix_for_reverse.rows):
                right_part -= variables[i - 1][k] * matrix_for_reverse.data[j - 1][k]
            variables[i - 1][j - 1] = right_part / matrix_for_reverse.data[j - 1][j - 1]

    result_data = [[0 for i in range(indices_matrix.rows)] for j in range(indices_matrix.rows)]
    for i in range(indices_matrix.rows):
        for j in range(indices_matrix.columns):
            result_data[indices_matrix.data[i][j][0] - 1][indices_matrix.data[i][j][1] - 1] = variables[i][j]
    return Matrix(result_data)


""" Gaussian method """
def task1():
    matrix = Matrix.read()
    orig_matrix = copy.deepcopy(matrix)
    print("==========================task1==========================")

    # solving equation
    # straight running
    p = 0 # parameter of swaps for calculating determinant    
    for i in range(matrix.rows - 1):
        if matrix.data[i][i] == 0:
            for j in range(matrix.rows):
                if matrix.data[j][i] != 0:
                    matrix.data[i], matrix.data[j] = matrix.data[j], matrix.data[i]
                    p += 1
                    break
        ratios = []
        for j in range(i + 1, matrix.rows):
            ratios.append(-(matrix.data[j][i] / matrix.data[i][i]))
        for j in range(i + 1, matrix.rows):
            for k in range(i, matrix.columns):
                matrix.data[j][k] += matrix.data[i][k] * ratios[j - i - 1]
    
    #reverse running
    variables = [0 for _ in range(matrix.columns - 1)]
    for i in range(matrix.rows, 0, -1):
        right_part = matrix.data[i - 1][matrix.columns - 1]
        for j in range(i, matrix.rows):
            right_part -= variables[j] * matrix.data[i - 1][j]
        variables[i - 1] = right_part / matrix.data[i - 1][i - 1]
    for i in range(len(variables)):
        print(f"x{i + 1} = {variables[i]:.2f}")
    
    # calculating determinant
    det = (-1) ** p
    for i in range(matrix.rows):
        det *= matrix.data[i][i]
    print(f"Determinant of matrix is {det:.2f}")

    result = reverse(orig_matrix, True)
    
    print("Reversed matrix is\n", result)
    print("==========================task1==========================")

""" The run-through method """
def task2():
    equations_quantity = int(input("Please, type quantity of equations in system: "))
    data = []
    for i in range(equations_quantity):
        row = list(map(int, input(f"Type ratios before variables in {i + 1} equation: ").split()))
        data.append(row)
    right_parts = list(map(int, input("Type right parts of equations: ").split()))
    
    print("==========================task2==========================")
    ps = []
    qs = []
    # straight running
    for i in range(equations_quantity):
        if i == 0:
            ps.append((-data[i][-1]) / data[i][0])
            qs.append(right_parts[i] / data[i][0])
        elif i == equations_quantity - 1:
            ps.append(0)
            qs.append((right_parts[i] - data[i][0] * qs[i - 1]) / (data[i][1] + data[i][0] * ps[i - 1]))
        else:
            ps.append(-data[i][2] / (data[i][1] + data[i][0] * ps[i - 1]))
            qs.append((right_parts[i] - data[i][0] * qs[i - 1]) / (data[i][1] + data[i][0] * ps[i - 1]))

    # reverse running
    variables = [0 for _ in range(equations_quantity + 1)]
    for i in range(equations_quantity, 0, -1):
        variables[i - 1] = ps[i - 1] * variables[i] + qs[i - 1]
    
    for i in range(equations_quantity):
        print(f"x{i + 1} = {variables[i]:.2f}")
    print("==========================task2==========================")

""" Iterations methods """
def task3():
    matrix = Matrix.read()
    epsilon = float(input("Please, type the presision of calculatings: "))

    print("==========================task3==========================")
    # elementary iterations
    alphas = [[0 for i in range(matrix.rows)] for j in range(matrix.rows)]
    bethas = [[0] for _ in range(matrix.rows)]

    for i in range(matrix.rows):
        if matrix.data[i][i] == 0:
            for j in range(matrix.rows):
                if matrix.data[j][i] != 0:
                    matrix.data[i], matrix.data[j] = matrix.data[j], matrix.data[i]
                    break
    
    for i in range(matrix.rows):
        bethas[i][0] = matrix.data[i][-1] / matrix.data[i][i]
        for j in range(matrix.rows):
            alphas[i][j] = 0 if i == j else -matrix.data[i][j] / matrix.data[i][i]
    
    alphas_matrix, bethas_matrix = Matrix(alphas), Matrix(bethas)

    if alphas_matrix.regularization() < 1:    
        x_prev = bethas_matrix
        x_curr = bethas_matrix.add(alphas_matrix.multiply(bethas_matrix))

        iters_count = 1

        while (alphas_matrix.regularization() / (1 - alphas_matrix.regularization())) * x_curr.subtraction(x_prev).regularization() > epsilon: # error estimation
            iters_count += 1
            x_prev = x_curr
            x_curr = bethas_matrix.add(alphas_matrix.multiply(x_prev))

        print("Elementary iterations:")
        for i in range(x_curr.rows):
            print(f"x{i + 1} = {x_curr.data[i][0]:.5f}")
        print(f"{iters_count} iterations")

    # Zeidel method
    alphas = [[0 for i in range(matrix.rows)] for j in range(matrix.rows)]
    bethas = [[0] for _ in range(matrix.rows)]

    for i in range(matrix.rows):
        if matrix.data[i][i] == 0:
            for j in range(matrix.rows):
                if matrix.data[j][i] != 0:
                    matrix.data[i], matrix.data[j] = matrix.data[j], matrix.data[i]
                    break
    
    for i in range(matrix.rows):
        bethas[i][0] = matrix.data[i][-1] / matrix.data[i][i]
        for j in range(matrix.rows):
            alphas[i][j] = 0 if i == j else -matrix.data[i][j] / matrix.data[i][i]
    
    alphas_matrix, bethas_matrix = Matrix(alphas), Matrix(bethas)
    lower, upper = alphas_matrix.decomposition()
    elementary_matrix = Matrix.elementary(alphas_matrix.rows)

    x_prev = bethas_matrix
    x_curr = reverse(elementary_matrix.subtraction(lower), False).multiply(upper).multiply(x_prev).add(reverse(elementary_matrix.subtraction(lower), False).multiply(bethas_matrix))

    iters_count = 1

    while (upper.regularization() / (1 - alphas_matrix.regularization())) * x_curr.subtraction(x_prev).regularization() > epsilon: # error estimation
        iters_count += 1
        x_prev = x_curr
        x_curr = reverse(elementary_matrix.subtraction(lower), False).multiply(upper).multiply(x_prev).add(reverse(elementary_matrix.subtraction(lower), False).multiply(bethas_matrix))

    print("Zeidel method:")
    for i in range(x_curr.rows):
        print(f"x{i + 1} = {x_curr.data[i][0]:.5f}")
    print(f"{iters_count} iterations")

    print("==========================task3==========================")


""" Start of program """
def main():
    if len(sys.argv) != 2:
        print("You need to type the number of task!")
        sys.exit(1)
    
    # try:
    if int(sys.argv[1]) == 1:
        task1()
    elif int(sys.argv[1]) == 2:
        task2()
    elif int(sys.argv[1]) == 3:
        task3()
    else:
        print("Type numbers from range [1, 2, 3]!")
    # except:
    #     print("Type numbers!")
    #     sys.exit(1)

if __name__ == "__main__":
    main()
