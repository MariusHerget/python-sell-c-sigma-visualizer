import numpy as np
import random as rand
import math

def create(x,y):
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






def calc_sparsity(n):
    sparsity_treshhold = 0.49
    return (1.0 -sparsity_treshhold)*n
