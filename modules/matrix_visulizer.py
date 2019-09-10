import numpy as np
import random as rand
import math
from termcolor import colored

def printmatrix(m):
    x,y = m.shape
    if x != 0 and y !=0:
        print_coordinates_x(x)
        printline(y)
        for ix in range(x):
            t = "#  "
            for iy in range(y):
                if m[ix][iy] != 0:
                    t += str(m[ix][iy])
                else:
                    t+= "   "
                if iy != y-1:
                    t+="  "
            print(t+"  #")
        printline(y)
    else:
        print("Error! Dimensions are "+str(m.shape))

def printline(y):
    str="##"
    for iy in range(y):
        str+="#####"
    str+="##"
    print(str)

def print_coordinates_x(x):
    t = "   "
    for i in range(x):
        t+=" "+str(i)
        if (x<10):
            t+=" "
        t+="  "
    print(t)

def matprint(mat, fmt="g"):
    col_maxes = [max([len(("{:"+fmt+"}").format(x)) for x in col]) for col in mat.T]
    row,col = np.diag_indices(mat.shape[0])
    for idx, x in enumerate(mat):
        for i, y in enumerate(x):
            c = "white"
            if y == 0:
                c = "magenta"
            # print(idx,i, row[idx], col[i])
            if idx == row[idx] and i == col[idx]:
                c= "red"
            print(colored(("{:"+str(col_maxes[i])+fmt+"}").format(y), c), end="  ")
        print(" ")
