import numpy as np
import random as rand
import math
import json
from datetime import date, time, datetime


import modules.sparse_matrix_generator as smgen
import modules.sell_c_sigma as scs
import modules.matrix_visulizer as mvis
import modules.unit_pattern as up


def main():
    i = 6
    # for i in range(12):
    m = smgen.diag_prob(30, 30)
    mvis.matprint(m,13,11,None,None,None,True) # Mark Diagonal = true
    sell1 = scs.Sell_c_sigma(3, 6)
    sell1.construct(m)
    sell1.prepare_units(4, up.uniform)
    sell1.print(13,11)
    print("\n#################\n")
    sell1.prepare_units(4, up.uniform, "scope")
    sell1.print(13,11)
    print("\n#################\n")
    sell1.prepare_units(4, up.uniform, "chunk")
    sell1.print(13,11)
    print("\n#################\n")
    sell1.prepare_units(4, up.balanced)
    sell1.print(13,11)
    print("\n#################\n")
    # sell1.global_to_sell(6,6)

def index_example():
    x = 25
    y = 30
    m = np.zeros((y, x))
    for i in range(0,x):
        m[i][i] = i
    for i in range(x,y):
        m[i][5] = i
    m[0][0] = 0.1
    m[17][0] = 0.1
    m[17][1] = 0.1
    sell1 = scs.Sell_c_sigma(6,12)
    sell1.construct(m)
    # sell1.prepare_units(1, up.balanced)
    mvis.matprint(m,17,17,None,None,None,True) # Mark Diagonal = true
    sell1.print(17,17)
    print("\n")

def random_for_properties():
    ms = {}
    min = 25
    max = 36
    amount_of_matrices = 20
    for i in range(amount_of_matrices):
        ms[i] = {}
        ms[i]['x'] = rand.randrange(min, max, 1)
        ms[i]['y'] = rand.randrange(min, max, 1)
        m = smgen.diag_prob(ms[i]['x'], ms[i]['y'])
        ms[i]['highlight'] = {}
        while True:
            ms[i]['highlight']['x'] = rand.randrange(0, ms[i]['x']-1, 1)
            ms[i]['highlight']['y'] = rand.randrange(0, ms[i]['y']-1, 1)
            if m[ms[i]['highlight']['y']][ms[i]['highlight']['x']] != 0:
                break
        ms[i]['matrix'] = m.tolist()
        mvis.matprint(m,ms[i]['highlight']['x'],ms[i]['highlight']['y'],None,None,None,True) # Mark Diagonal = true
        c = rand.randrange(3, max/4, 3)
        ms[i]['sellcsigma'] = {}
        ms[i]['sellcsigma']['c'] = 6
        ms[i]['sellcsigma']['sigma'] = ms[i]['sellcsigma']['c']*2
        ms[i]['sellcsigma']['units'] = rand.randrange(2, 8, 2)
        ms[i]['sellcsigma']['pattern'] = "balanced"
        # print("###############################################")
        # print(ms[i]['sellcsigma'])
        sell1 = scs.Sell_c_sigma(ms[i]['sellcsigma']['c'], ms[i]['sellcsigma']['sigma'])
        sell1.construct(m)
        sell1.prepare_units(ms[i]['sellcsigma']['units'], up.balanced)
        sell1.print(ms[i]['highlight']['x'],ms[i]['highlight']['y'])
        print("\n")
    timestamp = str(datetime.fromtimestamp(datetime.timestamp(datetime.now()))).replace(" ","_").replace(":","-")
    print(timestamp)
    with open('tmp/matrix-examples-'+timestamp+'.json', 'w') as outfile:
        json.dump(ms, outfile)

if __name__ == "__main__":
    # main()
    random_for_properties()
