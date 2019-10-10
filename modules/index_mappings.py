import copy
import numpy
# Logical View to offset


def zero_offset(row):
    compressedrow = []
    offsets = []
    off = 0
    for (i, x) in enumerate(row):
        if (x == 0):
            off += 1
        else:
            compressedrow.append(x)
            offsets.append(off)
            off = 0
    # print("original   " + str(row) + " // " + str(row[row != 0]))
    # print("compressed " + str(compressedrow) +
    #       " // offsets " + str(offsets) + "\n")
    return compressedrow, offsets

# Offset to Scope (Row Mapping)


def scope_mapping(sigma_scope_rows):
    debugrows = copy.deepcopy(sigma_scope_rows)
    mapping = {}
    sigma_scope_lengths = list(map(lambda x: len(x), sigma_scope_rows))
    # print(sigma_scope_lengths)
    sigma_scope_sorted = []

    for i in range(len(sigma_scope_rows)):
        longest_index = numpy.where(sigma_scope_lengths == numpy.amax(
            numpy.array(sigma_scope_lengths)))[0][0]
        # print(i,longest_index,sigma_scope_lengths[longest_index])
        sigma_scope_lengths[longest_index] = -1
        sigma_scope_sorted.append(sigma_scope_rows[longest_index])
        mapping[longest_index] = i
    return sigma_scope_sorted, mapping

def map_units_to_sellcsigma(sell_c_sigma):
    print("test")
