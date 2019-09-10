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
    x=6
    y=6
    mvis.matprint(smgen.create(16,16))
    print()
    mvis.matprint(smgen.diag_prob(16,16))
    # smgen.diag_prob(10,10)


if __name__ == "__main__":
    main()
