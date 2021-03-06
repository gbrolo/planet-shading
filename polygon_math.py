from collections import namedtuple
import numpy as np
import math

VERTEX_2 = namedtuple('Point2', ['x', 'y'])
VERTEX_3 = namedtuple('Point3', ['x', 'y', 'z'])
OUTSIDE_P = -1, -1, -1

def sum(v1, v2):
    return VERTEX_3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def sub(v1, v2):
    return VERTEX_3(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

def scalar_mult(v1, k):
    return VERTEX_3(v1.x * k, v1.y * k, v1.z *k)

def dot_product(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

def cross_product(v1, v2):
    return VERTEX_3(v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x,)

def vector_length(v1):
    return (v1.x**2 + v1.y**2 + v1.z**2)**0.5

def vector_normal(v1):
    length = vector_length(v1)

    if not length:
        return VERTEX_3(0, 0, 0)
    else:
        return VERTEX_3(v1.x/length, v1.y/length, v1.z/length)

def bounding_box(*vertices):
    x_coords = [ v.x for v in vertices ]
    y_coords = [ v.y for v in vertices ]
    x_coords.sort()
    y_coords.sort()

    return VERTEX_2(x_coords[0], y_coords[0]), VERTEX_2(x_coords[-1], y_coords[-1])

def transform(v, t=(0,0,0), s=(1,1,1)):
        return VERTEX_3(round((v[0] + t[0]) * s[0]), round((v[1] + t[1]) * s[1]), round((v[2] + t[2]) * s[2]))

def matrix_transform(v, view_port, projection, view, model):
    augmented_v_matrix = [ [v.x], [v.y], [v.z], [1] ]
    transformed_v_matrix = matrix_mult(matrix_mult(matrix_mult(matrix_mult(view_port, projection), view), model), augmented_v_matrix)    
    # transformed_v_matrix = transformed_v_matrix[0]
    transformed_v_matrix = [
        round(transformed_v_matrix[0][0] / transformed_v_matrix[3][0]),
        round(transformed_v_matrix[1][0] / transformed_v_matrix[3][0]),
        round(transformed_v_matrix[2][0] / transformed_v_matrix[3][0])
    ]
    # print(VERTEX_3(*transformed_v_matrix))
    return VERTEX_3(*transformed_v_matrix)

def matrix_mult(A, B):
    result = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]    

    for i in range(len(A)):        
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]

    return result

def barycentric(vector_A, vector_B, vector_C, P):
    b = cross_product(
        VERTEX_3(vector_C.x - vector_A.x, vector_B.x - vector_A.x, vector_A.x - P.x), 
        VERTEX_3(vector_C.y - vector_A.y, vector_B.y - vector_A.y, vector_A.y - P.y)
    )

    if abs(b[2]) < 1:
        return OUTSIDE_P
    else:
        return (1 - (b[0] + b[1]) / b[2], b[1] / b[2], b[0] / b[2])

def getBaryCoords(vector_A, vector_B, vector_C, min_bounding_box, max_bounding_box):
    transform = np.linalg.inv(
        [
            [vector_A.x, vector_B.x, vector_C.x],
            [vector_A.y, vector_B.y, vector_C.y],
            [         1,          1,          1]
        ]
    )

    bounding_box_grid = np.mgrid[
        min_bounding_box.x:max_bounding_box.x,
        min_bounding_box.y:max_bounding_box.y
    ].reshape(2, -1)
    bounding_box_grid = np.vstack((bounding_box_grid, numpy.ones((1, bounding_box_grid.shape[1]))))
    
    return np.transpose(np.dot(transform, bounding_box_grid))
