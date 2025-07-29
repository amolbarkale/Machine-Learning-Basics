v1 = [1, 2, 3]

v2 = [4, 5, 6]

def are_orthogonal(v1, v2):
    return dot_product(v1, v2) == 0

def dot_product(v1, v2):
    return [x * y for x, y in zip(v1, v2)]

def add_vectors(v1, v2):
    return [x + y for x, y in zip(v1, v2)]

# Matrix Multiplication using Nested Loops

def multiply_matrices(A, B):
    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(B[0])):
            val = 0
            for k in range(len(B)):
                val += A[i][k] * B[k][j]
            row.append(val)
        result.append(row)
    return result

# Test matrices
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]

# Output
print("Matrix Multiplication Result:")
for row in multiply_matrices(A, B):
    print(row)

