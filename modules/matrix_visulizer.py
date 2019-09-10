import numpy as np
import random as rand
import math

def printmatrix(m):
    x,y = m.shape
    if x != 0 and y !=0:
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
