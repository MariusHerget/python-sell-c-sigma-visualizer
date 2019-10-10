import numpy as np
import random as rand
import math


import modules.sparse_matrix_generator as smgen
import modules.sell_c_sigma as scs
import modules.matrix_visulizer as mvis


def main():
    i = 6
    # for i in range(12):
    m = smgen.diag_prob(30, 30)
    mvis.matprint(m,13,11,None,None,None,True) # Mark Diagonal = true
    sell1 = scs.Sell_c_sigma(3, 6)
    sell1.construct(m)
    sell1.print(13,11)
    print("\n#################\n")
    # sell1.global_to_sell(6,6)

if __name__ == "__main__":
    main()
