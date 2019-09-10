import numpy as np
import random as rand
import math

import modules.sparse_matrix_generator as smgen
import modules.matrix_visulizer as mvis
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
    mvis.printmatrix(smgen.create(16,16))


if __name__ == "__main__":
    main()
