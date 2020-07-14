import numpy as np
from time import time

def matrix_times_matrix(m1, m2,reorder=False):
    # print(m1.original_matrix)
    # print(len(m1.original_matrix[0]))
    #
    m_result = np.zeros((int(len(m1.original_matrix)), int(len(m1.original_matrix))))
    # print(m1.sigma_scope_rows_mapping)
    # computations = 0
    # comparisions = 0
    loriginal_column2 = []
    for isigma2, sigma2 in enumerate(m2.m_final):
        loriginal_column2.append([])
        for ichunk2, chunk2 in enumerate(sigma2):
            loriginal_column2[isigma2].append([])
            for irow2, row2 in enumerate(chunk2):
                loriginal_column2[isigma2][ichunk2].append({"original_row2": -1, "cols": []})
                # for iv, value in enumerate(row2):
                loriginal_column2[isigma2][ichunk2][irow2]["original_row2"], loriginal_column2[isigma2][ichunk2][irow2]["cols"] = get_Original_rowcol(m2, isigma2, ichunk2, irow2, -1, reorder)
    # print(loriginal_column2)
    # allend=0
    # allend1=0
    for isigma, sigma in enumerate(m1.m_final):
        for ichunk, chunk in enumerate(sigma):
            for irow, row in enumerate(chunk):
                original_row, original_column = get_Original_rowcol(m1, isigma, ichunk, irow, -1, reorder)
                for isigma2, sigma2 in enumerate(m2.m_final):
                    for ichunk2, chunk2 in enumerate(sigma2):
                        for irow2, row2 in enumerate(chunk2):
                            found = 0
                            original_row2 = loriginal_column2[isigma2][ichunk2][irow2]["original_row2"]
                            for iv, value in enumerate(row):
                                if value != 0:
                                    # original_row2, loriginal_column2 = get_Original_rowcol(m2, isigma2, ichunk2, irow2, -1, reorder)
                                    # start1 = time()
                                    for iv2, value2 in enumerate(row2):
                                        # print("("+str(found)+") array len "+str(len(row2[found:]))+" = "+str(row2[found:]))
                                        if value2 != 0:
                                            # start = time()
                                            original_column2 = loriginal_column2[isigma2][ichunk2][irow2]["cols"][iv2]
                                            # comparisions += 1
                                            if original_column[iv] == original_column2:
                                                # print("Found matching: "+str(value)+" * "+str(value2))
                                                # print(str(original_row)+" ("+str(irow)+") // "+str(original_row2)+" "+str(value)+" * "+str(value2))
                                                m_result[original_row][original_row2] += value*value2
                                                # print("found at ("+str(original_column)+"/"+str(original_column2)+") "+str(iv2))
                                                found += iv2+1
                                                # computations+=1
                                                continue
                                            if original_column[iv] > original_column2:
                                                continue
                                            # print (str(original_column)+"/"+str(original_column2))
                                            # print (str(original_column)+"/"+str(original_column2))
                #             print("new row")
                                    #         end =time()
                                    #         allend +=end -start
                                    # end1 =time()
                                    # allend1 +=end1 -start1
                # end =time()
    # print("\tInner Loop: "+ str((allend1)))
    # print("\tSeond: "+ str((allend)))
    # print("computations: "+str(computations))
    # print("comparisions: "+str(comparisions))
    return m_result

def get_Original_rowcol(m, isigma, ichunk, irow, iv, reorder=False):
    # print(isigma, ichunk, irow, iv)
    for or_index, sell_index in m.sigma_scope_rows_mapping[isigma].items():
        if sell_index == irow + ichunk*len(m.m_final[isigma][ichunk]):
            original_row = or_index
    # print(m.m_final[isigma][ichunk][irow], m.sigma_scope_columnIndex[isigma][original_row])
    # print(m.__dict__)
    retrow = int(irow+m.sell_sigma*isigma+m.sell_c*ichunk)
    if reorder:
        retrow = original_row+m.sell_sigma*isigma
    # print(irow, original_row+m.sell_sigma*isigma)
    if iv == -1:
        return retrow, m.sigma_scope_columnIndex[isigma][original_row]
    return retrow, m.sigma_scope_columnIndex[isigma][original_row][iv]
