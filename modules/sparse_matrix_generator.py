import numpy as np
import random as rand
import math
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt


def create(x, y):
    nonzero = x * y - calc_sparsity(x * y)
    m_origin = np.zeros((y, x))
    print("Generate matrix (" + str(y) + " rows with each " + str(x) + " elements"
          ") with " + str(nonzero) + " values.")
    return fill_matrix_with_random(m_origin, nonzero)


def calc_sparsity(n):
    sparsity_treshhold = 0.20
    return (1.0 - sparsity_treshhold) * n


def diag_prob(or_x, or_y):
    m_origin = np.zeros((or_y, or_x))
    nonzero = math.ceil(or_x * or_y - calc_sparsity(or_x * or_y))
    print("Generate multivariate normal matrix (" + str(or_y) + " rows with each " + str(or_x) + " elements"
          + ") with " + str(nonzero) + " values.")
    mean = [math.ceil(or_y / 2) - 1, math.ceil(or_x / 2)]
    # diagonal covariance, points lie on x or y-axis
    cov = [[or_y / 2, 0], [0, or_x]]
    x, y = np.random.multivariate_normal(mean, cov, nonzero).T
    for ix in range(len(y)):
        # rotate point 45° to left to be in diagonal
        x[ix], y[ix] = rotate_point(
            x[ix], y[ix], -45, math.ceil(or_x / 2) - 1, math.ceil(or_y / 2))
        valx = math.ceil(x[ix])
        valy = math.ceil(y[ix])
        if or_x > valx >= 0 and or_y > valy >= 0 and m_origin[valy][valx] == 0:
            m_origin[valy][valx] = rand_num()
            nonzero -= 1
    m_origin, usedNonZero = fill_matrix_diagonal_with_random(m_origin, 0.75)
    nonzero += usedNonZero
    # print("nonzero left: " + str(nonzero))
    return fill_matrix_with_random(m_origin, nonzero / 3)


def fill_matrix_with_random(m_origin, nonzero):
    x, y = m_origin.shape
    while nonzero > 0:
        xr = rand.randrange(x)
        yr = rand.randrange(y)
        if (m_origin[xr][yr] == 0.0):
            m_origin[xr][yr] = rand_num()
            nonzero -= 1
    return m_origin


def fill_matrix_diagonal_with_random(m_origin, probaility):
    row, col = np.diag_indices(m_origin.shape[0])
    x, y = m_origin.shape
    filler = []
    n = 0
    for i in range(len(row)):
        if rand.random() > (1 - probaility):
            if i < x and i < y:
                m_origin[i][i] = rand_num()
                n += 1
    return m_origin, n


def rotate_point(in_x, in_y, angle, rot_x, rot_y):
    r00 = math.cos(angle)
    r01 = -1 * math.sin(angle)
    r10 = math.sin(angle)
    r11 = r00
    # xout =  r00 * xin   +  r01 * yin   + x     - r00*x     - r01*y
    out_x = r00 * in_x + r01 * in_y + rot_x - r00 * rot_x - r01 * rot_y
    # yout  = r10 * xin   +  r11 * yin   + y     - r10*x     - r11*y
    out_y = r10 * in_x + r11 * in_y + rot_y - r10 * rot_x - r11 * rot_y
    return out_x, out_y


def rand_num():
    return rand.randrange(100)
