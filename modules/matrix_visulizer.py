import numpy as np
import random as rand
import math
from termcolor import colored


def printmatrix(m):
    x, y = m.shape
    if x != 0 and y != 0:
        print_indexinates_x(x)
        printline(y)
        for ix in range(x):
            t = "#  "
            for iy in range(y):
                if m[ix][iy] != 0:
                    t += str(m[ix][iy])
                else:
                    t += "   "
                if iy != y - 1:
                    t += "  "
            print(t + "  #")
        printline(y)
    else:
        print("Error! Dimensions are " + str(m.shape))


def printline(y):
    str = "##"
    for iy in range(y):
        str += "#####"
    str += "##"
    print(str)


def print_indexinates_x(x):
    t = "   "
    for i in range(x):
        t += " " + str(i)
        if (x < 10):
            t += " "
        t += "  "
    print(t)


def matprint(mat, highlight_x=-1, highlight_y=-1, sellcsigma=None, isigma=None, ichunk=None, markDiagonal=False, fmt="g"):
    col_maxes = [max([len(("{:" + fmt + "}").format(x))
                      for x in col]) for col in mat.T]
    row, col = np.diag_indices(mat.shape[0])
    for idy, y in enumerate(mat):
        if sellcsigma is not None and isigma is not None and ichunk is not None:
            c = sellcsigma.print_unit(isigma, ichunk, idy)
            print(colored("{:02d}".format(
                isigma) + " | " + "{:02d}".format(ichunk) + " | " + "{:02d}".format(idy), c), end=" ")
        else:
            print(colored("{:02d}".format(idy), "green"), end=" ")
        for idx, x in enumerate(y):
            c = "white"
            if x == 0:
                c = "magenta"
            # print(idx,i, row[idx], col[i])
            if idy == row[idy] and idx == col[idy] and markDiagonal:
                c = "red"
            if idx == highlight_x and idy == highlight_y:
                c = 'green'
            print(
                colored(("{:" + str(col_maxes[idx]) + fmt + "}").format(x), c), end="  ")
        print("")


def print_sellcsigma_matrix(sell_c_sigma, highlight_x=-1, highlight_y=-1):
    print("\nPrinting SELL-" + str(sell_c_sigma.sell_c) +
          "-" + str(sell_c_sigma.sell_sigma))

    print(colored("U  | S  | C  | R", "cyan"), end="\n")
    scope_index, chunk_offset, row_index, sell_x = sell_c_sigma.global_index_to_sell_index(
        highlight_x, highlight_y)
    # print("\nprint_sellcsigma_matrix")
    # print("scope_index: "+str(scope_index))
    # print("chunk_offset: "+str(chunk_offset))
    # print("row_index: "+str(row_index))
    # print("sell_x: "+str(sell_x))
    # print(sell_c_sigma.global_index_to_sell_value(highlight_x, highlight_y))
    for isigma, sigma in enumerate(sell_c_sigma.m_padded):
        for ichunk, chunk in enumerate(sigma):
            if isigma == scope_index and ichunk == chunk_offset:
                kx = sell_x
                ky = row_index
            else:
                kx = -1
                ky = -1
            matprint(np.array(chunk), kx, ky, sell_c_sigma, isigma, ichunk)
            # for irow, row in enumerate(chunk):
            #     print(row)
