import numpy as np
import random as rand
import math
# SELL-4-σspMVM  kernelwith four-way unrolling
# for(i = 0; i < N/4; ++i){
#     for(j = 0; j < cl[i]; ++j) {
#         y[i*4+0]  += val[cs[i]+j*4+0] *
#                     x[col[cs[i]+j*4+0]];
#         y[i*4+1]  += val[cs[i]+j*4+1] *
#                     x[col[cs[i]+j*4+1]];
#         y[i*4+2]  += val[cs[i]+j*4+2] *
#                     x[col[cs[i]+j*4+2]];
#         y[i*4+3]  += val[cs[i]+j*4+3] *
#                     x[col[cs[i]+j*4+3]];
#     }
# }

def main():
    print("Which size should the matrix have?")
    # print("x")
    # x = int(input())
    # print("y")
    # y = int(input())
    x=6
    y=6
    # for ix in range(x):
    #     for iy in range(y):
    #         print()
    printmatrix(create_random_sparse_matrix(16,16))

def create_random_sparse_matrix(x,y):
    nonzero = x*y-calc_sparsity(x*y)
    m_origin = np.zeros((x,y))
    print("Generate matrix "+str((x,y))+" with "+str(nonzero)+" values.")
    while nonzero > 0:
        xr = rand.randrange(x)
        yr = rand.randrange(y)
        if (m_origin[xr][yr] == 0.0):
            m_origin[xr][yr] = rand.randrange(10)+rand.randrange(10)/10
            nonzero-=1
    return m_origin


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



def calc_sparsity(n):
    sparsity_treshhold = 0.49
    return (1.0 -sparsity_treshhold)*n

if __name__ == "__main__":
    main()
