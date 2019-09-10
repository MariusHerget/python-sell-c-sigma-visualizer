import numpy as np
import math
import modules.matrix_visulizer as mvis

def construct(m, sell_c, sell_sigma):
    m_sigma = sort_rows_in_scope(m, sell_sigma)
    m_padded = pad_chunk_with_zeros(m_sigma, sell_c)
    return m_padded

def delete_zeors_in_row(row):
    return row[row != 0]


def sort_rows_in_scope(m, sell_sigma):
    sigma_scope = []
    # print(sigma_scope)
    sigma_scope_index = -1
    for idrow, row in enumerate(m):
        if (idrow % sell_sigma) == 0:
            sigma_scope_index +=1
            sigma_scope.append([])
        row_nonzero = delete_zeors_in_row(row)
        # print("row_nonzero "+str(idrow)+": "+str(row_nonzero))
        sigma_scope[sigma_scope_index].append(row_nonzero)
    # print("\n-----------")
    for ix, x in enumerate(sigma_scope):
        sigma_scope[ix] = sorted(x, key=len, reverse=True)
        # for iy, y in enumerate(sigma_scope[ix]):
        #     print(y)
        #
        # print("-----------")

    return sigma_scope

def pad_chunk_with_zeros(m, sell_c):
    # print("\n\n")
    sigma_scope_chunks = []
    for isc, sigma_scope in enumerate(m):
        sigma_cunk_index = -1
        sigma_chunks = []
        sigma_scope_chunks.append([])
        for ichunk, chunk in enumerate(sigma_scope):
            if (ichunk % sell_c) == 0:
                sigma_cunk_index +=1
                sigma_chunks.append([])
                chunk_pad_length = len(chunk)
            # print(str(ichunk)+" "+str(chunk_pad_length)+"-"+str(len(chunk))+"="+str(chunk_pad_length-len(chunk)))
            chunk = np.pad(chunk, [0, chunk_pad_length-len(chunk)], 'constant', constant_values=0)
            # print(str(chunk))
            sigma_chunks[sigma_cunk_index].append(chunk)
        sigma_scope_chunks[isc] = sigma_chunks
    print ("")
    return sigma_scope_chunks
