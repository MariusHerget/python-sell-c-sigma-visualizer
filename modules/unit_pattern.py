import numpy as np
from termcolor import colored

def uniform(nunits, sell_c_sigma, group="all"):
    print("Balanced pattern for " + str(nunits) + " units (" + str(group) + ").")

    unitmapping = {}
    if group == "all":
        i = 0
    for scope_index, scope in enumerate(sell_c_sigma.m_final):
        unitmapping[scope_index] = {}
        if group == "scope":
            i = 0
        for chunk_offset, chunk in enumerate(scope):
            unitmapping[scope_index][chunk_offset] = {}
            if group == "chunk":
                i = 0
            for row_index, row in enumerate(chunk):
                unitmapping[scope_index][chunk_offset][row_index] = i % nunits
                i += 1
                # pattern(nunits, scope_index, chunk_offset, row_index)
    return unitmapping


def balanced(nunits, sell_c_sigma):
    print("Balanced pattern for " + str(nunits) + " units.\n" +
          colored("U: Unit | R: Number of rows | E: Number of elements", "yellow"))
    unitmapping = {}

    sell_c_sigma.mark_first_unit = False

    count_units = np.zeros(nunits, dtype=int)
    count_units_rows = np.zeros(nunits, dtype=int)
    tmp_m = []
    for scope_index, scope in enumerate(sell_c_sigma.m_final):
        unitmapping[scope_index] = {}
        for chunk_offset, chunk in enumerate(scope):
            unitmapping[scope_index][chunk_offset] = {}
            for row_index, row in enumerate(chunk):
                tmp_m.append(row)
    # print(tmp_m)
    npa = np.array(tmp_m)
    tmpsorted_index = np.argsort([len(i) for i in npa])
    tmpsorted = npa[tmpsorted_index[::-1]]
    for irow, row in enumerate(tmpsorted):
        smallest_unit = np.argmin(count_units)
        count_units[smallest_unit] += len(row)
        count_units_rows[smallest_unit] += 1
        scope_index, chunk_offset, row_index, sell_x = sell_c_sigma.global_index_to_sell_index(
            0, np.where(tmpsorted_index == irow)[0][0])
        unitmapping[scope_index][chunk_offset][row_index] = smallest_unit

    print("U  | R  | E  ")
    for icount, count in enumerate(count_units_rows):
        print("{:02d}".format(icount), end=" | ")
        print("{:02d}".format(count), end=" | ")
        print("{:02d}".format(count_units[icount]), end="\n")

    return unitmapping
