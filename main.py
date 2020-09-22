import numpy as np
import random as rand
import math
import json
from datetime import date, time, datetime
import os


import modules.sparse_matrix_generator as smgen
import modules.sell_c_sigma as scs
import modules.matrix_visulizer as mvis
import modules.unit_pattern as up
import modules.calculations as scscalc
from time import time

def main():
    # for i in range(12):
    size = 12.0
    sigmaSize = 6.0
    units=2
    print("\nTest\n")
    m = smgen.create(int(size), int(size))
    # Nummerate matrix
    i = 1
    for irow, row in enumerate(m):
        for icol, col in enumerate(row):
            if col != 0:
                m[irow][icol] = i
                i +=1
    mvis.matprint(m,13,11,None,None,None,True) # Mark Diagonal = true
    # print(m)
    r = 0
    base = 0
    tikz = "\\definecolor{myblue}{rgb}{0, 0.624, 0.89}\n\\definecolor{mypurple}{rgb}{0.576, 0.376, 0.216}\n\\definecolor{mygreen}{rgb}{0.35,0.788,0.333}\n\\definecolor{myred}{rgb}{0.976,0.698,0.2}\n\\definecolor{highlight}{rgb}{0.89, 0.024, 0.075}\n\\begin{tikzpicture}[every node/.style={minimum size=0.95cm-\\pgflinewidth, outer sep=0pt}]\n\t\\draw[step=1cm,color=black] ("+str(base)+",0) grid ("+str(base+size)+","+str(size)+");\n\t\\foreach \\y\\x\\i in {%\n\t\t"
    for row in m:
        c = 0
        v = False
        for col in row:
            if col != 0:
                tikz += str(r)+ "/ " + str(c)+"/"+str(int(col-1))+", "
                v = True
            c+=1
        r+=1
        if v:
            tikz += "\n\t\t"
    tikz = tikz[:-5]+"%"
    tikz += "\n\t}{\n\t\t\\node[fill=black] at (\\x+"+str(base+0.5)+",-\\y+"+str(size-0.5)+") {};\n\t\\node[color=white] at (\\x+"+str(base+0.5)+",-\\y+"+str(size-0.5)+") {$a_{\\i}$};\n\t}\n\n\n"
    base += size +1
    sell1 = scs.Sell_c_sigma(sigmaSize/2, sigmaSize)
    sell1.construct(m)
    # sell1.prepare_units(4, up.uniform)
    print(sell1.m_final)
    maxrow = 0
    for isigma, sigma in enumerate(sell1.m_final):
        for ichunk, chunk in enumerate(sigma):
            maxcol=0
            for icol, col in enumerate(chunk[0]):
                if col != 0:
                    maxcol+=1
            if maxrow < maxcol:
                maxrow = maxcol
            tikz += "\t\\draw[step=1cm,color=black] ("+str(base)+","+str(size-(isigma*sigmaSize+ichunk*sigmaSize/2))+") grid ("+str(base+maxcol)+","+str(size-sigmaSize/2-(isigma*sigmaSize+ichunk*sigmaSize/2))+");\n"
    tikz += "\t\\foreach \\y\\x\\i in {%\n\t\t"
    for isigma, sigma in enumerate(sell1.m_final):
        for ichunk, chunk in enumerate(sigma):
            for irow, row in enumerate(chunk):
                v = False
                for icol, col in enumerate(row):
                    if col != 0:
                        tikz += (str(isigma*sigmaSize+ichunk*sigmaSize/2+irow)+ "/"  +str(icol)+ "/"+str(int(col-1)))
                        # print(icol, (len(row)-1))
                        # if isigma != (len(sell1.m_final)-1) and ichunk != (len(sigma)-1) and irow != (len(chunk)-1) and icol != (len(row)-1):
                        tikz +=  ", "
                        v = True
                if v:
                    tikz += "\n\t\t"
    tikz = tikz[:-5]+"%"
    tikz += "\n\t}{\n\t\t\\node[fill=black] at (\\x+"+str(base+0.5)+",-\\y+"+str(size-0.5)+") {};\n\t\\node[color=white] at (\\x+"+str(base+0.5)+",-\\y+"+str(size-0.5)+") {$a_{\\i}$};\n\t}\n\n\n"
    base += maxrow+1
    for isigma, sigma in enumerate(sell1.m_final):
        for ichunk, chunk in enumerate(sigma):
            maxcol=0
            for icol, col in enumerate(chunk[0]):
                if col != 0:
                    maxcol+=1
            tikz += "\t\\draw[step=1cm,color=black] ("+str(base)+","+str(size-(isigma*sigmaSize+ichunk*sigmaSize/2))+") grid ("+str(base+maxcol)+","+str(size-sigmaSize/2-(isigma*sigmaSize+ichunk*sigmaSize/2))+");\n"
    tikz += "\t\\foreach \\y\\x\\c\\i in {%\n\t\t"
    tmp = "\n\t\\foreach \\y\\x\\c\\i in {%\n\t\t"
    kcol = 0
    chunkcolor = 0
    # mem=["","","",""]
    # mem[0] = []
    # mem[1] = []
    # mem[2] = []
    # mem[3] = []
    for isigma, sigma in enumerate(sell1.m_final):
        for ichunk, chunk in enumerate(sigma):
            for irow, row in enumerate(chunk):
                v = False
                kcol = chunkcolor
                for icol, col in enumerate(row):
                    # print(isigma,ichunk,irow,icol,f,k)
                    # if len(mem[kcol]) < len(row):
                    #     mem[kcol].add("")
                    if col != 0:
                        if kcol == 0:
                            color = "myred"
                        if kcol == 1:
                            color = "mygreen"
                        if kcol == 2:
                            color = "myblue"
                        if kcol == 3:
                            color = "mypurple"
                        # mem[kcol][icol+irow*] += str(int(col-1))+"/"+color+", "
                        tikz += (str(isigma*sigmaSize+ichunk*sigmaSize/2+irow)+ "/"  +str(icol)+ "/"+color+"/"+str(int(col-1)))
                        # print(icol, (len(row)-1))
                        # if isigma != (len(sell1.m_final)-1) and ichunk != (len(sigma)-1) and irow != (len(chunk)-1) and icol != (len(row)-1):
                        tikz +=  ", "
                        v = True
                    else:
                        if kcol == 0:
                            color = "myred"
                        if kcol == 1:
                            color = "mygreen"
                        if kcol == 2:
                            color = "myblue"
                        if kcol == 3:
                            color = "mypurple"
                        # mem[kcol][icol] += str(0)+"/"+color+", "
                        tmp += (str(isigma*sigmaSize+ichunk*sigmaSize/2+irow)+ "/"  +str(icol)+ "/"+color+"/")
                        # print(icol, (len(row)-1))
                        # if isigma != (len(sell1.m_final)-1) and ichunk != (len(sigma)-1) and irow != (len(chunk)-1) and icol != (len(row)-1):
                        tmp +=  ", "
                    # if irow == len(chunk)-1:
                    #         mem[kcol] = mem[kcol][:-2] +";,\n\t\t"
                    kcol = (kcol + 1) % 4

                if v:
                    tikz += "\n\t\t"
            chunkcolor = kcol

    # print(mem)
    tikz = tikz[:-3] + "%"
    tmp = tmp[:-3] + "%"
    print(size)
    tikz += "\n\t}{\n\t\t\\node[fill=\\c] at (\\x+"+str(base+0.5)+",-\\y+"+str(size-0.5)+") {};\n\t\\node[color=black] at (\\x+"+str(base+0.5)+",-\\y+"+str(size-0.5)+") {$a_{\\i}$};\n\t}"
    tikz += tmp+"\n\t}{\n\t\t\\node[fill=\\c] at (\\x+"+str(base+0.5)+",-\\y+"+str(size-0.5)+") {};\n\t}"
    tikz += "\n\\end{tikzpicture}"
    f = open("tikz.txt", "w")
    f.write(tikz)
    f.close()
    # print("\n#################\n")
    # sell1.prepare_units(4, up.uniform, "scope")
    # sell1.print(0,0)
    # print("\n#################\n")
    # sell1.prepare_units(4, up.uniform, "chunk")
    # sell1.print(13,11)
    # print("\n#################\n")
    # sell1.prepare_units(4, up.balanced)
    # sell1.print(13,11)
    # print("\n#################\n")
    # sell1.global_to_sell(6,6)
def matrixmult (m1, m2):
    # zerocompu = 0
    # nonzerocomp=0

    r=[]
    m=[]
    for i, iv in enumerate(m1):
    # for i in range(len(m1)):
        for j in range(len(m2[0])):
            sums=0
            for k, kv in enumerate((m2)):
                sums=sums+(m1[i][k]*m2[k][j])
                # if m1[i][k] == 0 or m2[k][j] == 0:
                #     zerocompu += 1
                # else:
                #     nonzerocomp += 1
            r.append(sums)
        m.append(r)
        r=[]
    # print(zerocompu)
    # print(nonzerocomp)
    return m

def quickbenchmark():
    size = 512
    sigmaSize = 64
    reps_mat = 3
    reps = 2
    results_all= {"manual": [], "numpy":[], "scs": [], "speedup": []}
    print("Repetions: "+str(reps_mat)+" x "+str(reps))
    print("Matrix: "+str(size)+"x"+str(size))
    print("Sell-"+str(int(sigmaSize/2))+"-"+str(sigmaSize))
    for rep_over in range (0, reps_mat):
        print()
        m1 = smgen.create(int(size), int(size))
        m2 = smgen.create(int(size), int(size))
        allend = 0
        allend_numpy = 0
        allend_scs=0
        for i in range(0, reps):
            start = time()
            matrixmult(m1,m2)
            end = time()
            allend += end - start
            print("Done Manual "+str(1+i)+"/"+str(reps)+": "+str(end - start))

        for i in range(0, reps):
            start = time()
            np.matmul(m1,m2)
            end = time()
            allend_numpy += end - start
            print("Done Numpy "+str(1+i)+"/"+str(reps)+": "+str(end - start))


        start = time()
        sell1 = scs.Sell_c_sigma(sigmaSize/2, sigmaSize)
        sell1.construct(m1)
        end = time()

        # tikz2, sell1RowPtrs = mvis.print_tikz_scs(sell1, "", True, False)
        # f = open("tikz-scs-bench.txt", "w")
        # f.write(mvis.print_tikz_image(tikz2))
        # f.close()
        print("Prep1: "+ str((end - start)))

        start = time()
        m2 = m2.transpose()
        sell2 = scs.Sell_c_sigma(sigmaSize/2, sigmaSize)
        sell2.construct(m2)
        end = time()
        print("Prep2: "+ str((end - start)))


        # tikz = mvis.print_tikz_matrix(m1,"\\times", True, True, True)
        # tikz += mvis.print_tikz_matrix(m2,"=", False, True, True)
        # tikz2a, sell1RowPtrs = mvis.print_tikz_scs(sell1, "\\times", False)
        # tikz2b, sell2RowPtrs = mvis.print_tikz_scs(sell2, "=", False)
        # tikz +=tikz2a
        # tikz +=tikz2b
        # f = open("tikz-scs-bench.pgf", "w")
        # f.write(mvis.print_tikz_image(tikz))
        # f.close()

        for i in range(0, reps):
            start = time()
            scscalc.matrix_times_matrix(sell1,sell2,True)
            end = time()
            allend_scs += end - start
            print("Done SCS "+str(1+i)+"/"+str(reps)+": "+str(end - start))

        print("\tRESULTS ("+str(rep_over)+")")
        print("\tManual: "+ str((allend) / reps))
        print("\tnumpy: "+ str((allend_numpy) / reps))
        print("\tSCS: "+ str((allend_scs) / reps))
        results_all["manual"].append(allend)
        results_all["scs"].append(allend_scs)
        results_all["numpy"].append(allend_numpy)
        results_all["speedup"].append(allend/allend_scs)

    print("\n\n\tResults Manual:")
    for rep_over in range (0, reps_mat):
        print("\t\t"+str(rep_over)+": "+str(results_all["manual"][rep_over]))
    print("\tResults Numpy:")
    for rep_over in range (0, reps_mat):
        print("\t\t"+str(rep_over)+": "+str(results_all["numpy"][rep_over]))
    print("\tResults SCS:")
    for rep_over in range (0, reps_mat):
        print("\t\t"+str(rep_over)+": "+str(results_all["scs"][rep_over]))
    print("\n\tBest Speedup: "+str(max(results_all["speedup"])))
    print("\tWorst Speedup: "+str(min(results_all["speedup"])))

def vectormult(m,v):
    result = np.zeros(v.shape)
    for irow, row in enumerate(m):
        for ivalue, value in enumerate(row):
            result[irow] += value * v[ivalue]
    return result

def mult_benchmark_vector():
    sizes = [2**x for x in range(16,9+10)]
    print(sizes)
    results = {}
    excel = "Size,Manual,Numpy,SCS,Best Speedup,Worst Speedup\n"
    f = open("mult_benchmark_vector.csv2", "w")
    f.write(excel)
    f.close()
    excelresults=["Manual,","Numpy,","SCS,","Best Speedup,","Worst Speedup,"]
    for s in sizes:
        excel = str(s)+","
        results[s] = quickbenchmark_vector(size = s, p=False)
        excel += str(np.average(results[s]["manual"]))+","
        excel += str(np.average(results[s]["numpy"]))+","
        excel += str(np.average(results[s]["scs"]))+","
        excel += str(max(results[s]["speedup"]))+","
        excel += str(min(results[s]["speedup"]))+"\n"
        f = open("mult_benchmark_vector2.csv", "a")
        f.write(excel)
        f.close()

    # excel= excel[:-1]+"\n"
    # excel+= excelresults[0][:-1]+"\n"
    # excel+= excelresults[1][:-1]+"\n"
    # excel+= excelresults[2][:-1]+"\n"
    # excel+= excelresults[3][:-1]+"\n"
    # excel+= excelresults[4][:-1]

    f = open("mult_benchmark_vector2.json", "w")
    f.write(str(results))
    f.close()
    print(results)

def quickbenchmark_vector(size = 512, p=True):
    sigmaSize = 64 * (size/512)
    reps_mat = 1
    reps = 1
    reps_numpy = 1
    results_all= {"manual": [], "numpy":[], "scs": [], "speedup": []}
    if p or True:
        print("Repetions: "+str(reps_mat)+" x "+str(reps))
        print("Matrix: "+str(size)+"x"+str(size))
        print("Sell-"+str(int(sigmaSize/2))+"-"+str(sigmaSize))
    for rep_over in range (0, reps_mat):
        if p:
            print()
        m1 = smgen.create(int(size), int(size))
        v1 = np.random.randint(100, size=size)
        allend = 0
        allend_numpy = 0
        allend_scs=0
        for i in range(0, reps):
            start = time()
            vectormult(m1,v1)
            end = time()
            allend += end - start
            if p:
                print("Done Manual "+str(1+i)+"/"+str(reps)+": "+str(end - start))

        for i in range(0, reps_numpy ):
            start = time()
            m1.dot(v1)
            end = time()
            allend_numpy += end - start
            if p:
                print("Done Numpy "+str(1+i)+"/"+str(reps)+": "+str(end - start))

        #
        start = time()
        sell1 = scs.Sell_c_sigma(sigmaSize/2, sigmaSize)
        sell1.construct(m1)
        end = time()
        if p:
            print("Prep1: "+ str((end - start)))
        #

        #
        # # tikz = mvis.print_tikz_matrix(m1,"\\times", True, True, True)
        # # tikz += mvis.print_tikz_matrix(m2,"=", False, True, True)
        # # tikz2a, sell1RowPtrs = mvis.print_tikz_scs(sell1, "\\times", False)
        # # tikz2b, sell2RowPtrs = mvis.print_tikz_scs(sell2, "=", False)
        # # tikz +=tikz2a
        # # tikz +=tikz2b
        # # f = open("tikz-scs-bench.pgf", "w")
        # # f.write(mvis.print_tikz_image(tikz))
        # # f.close()
        #
        for i in range(0, reps):
            start = time()
            scscalc.matrix_times_vector(sell1,v1,True)
            end = time()
            allend_scs += end - start
            if p:
                print("Done SCS "+str(1+i)+"/"+str(reps)+": "+str(end - start))

        if p:
            print("\tRESULTS ("+str(rep_over)+")")
            print("\tManual: "+ str((allend) / reps))
            print("\tnumpy: "+ str((allend_numpy) / reps_numpy))
            print("\tSCS: "+ str((allend_scs) / reps))
        results_all["manual"].append(allend)
        results_all["scs"].append(allend_scs)
        results_all["numpy"].append(allend_numpy)
        results_all["speedup"].append(allend/allend_scs)

    if p:
        print("\n\n\tResults Manual:")
        for rep_over in range (0, reps_mat):
            print("\t\t"+str(rep_over)+": "+str(results_all["manual"][rep_over]))
        print("\tResults Numpy:")
        for rep_over in range (0, reps_mat):
            print("\t\t"+str(rep_over)+": "+str(results_all["numpy"][rep_over]))
        print("\tResults SCS:")
        for rep_over in range (0, reps_mat):
            print("\t\t"+str(rep_over)+": "+str(results_all["scs"][rep_over]))
        print("\n\tBest Speedup: "+str(max(results_all["speedup"])))
        print("\tWorst Speedup: "+str(min(results_all["speedup"])))
    return results_all

def matrix_A(size = 8):
    m = np.zeros((size,size))
    m[0][2]=1
    m[0][4]=2
    m[0][7]=3
    m[1][0]=4
    m[1][2]=5
    m[1][4]=6
    m[1][6]=7
    m[2][1]=8
    m[2][5]=9
    m[3][3]=10
    m[4][6]=11
    m[5][2]=12
    m[5][6]=13
    m[5][7]=14
    m[6][1]=15
    m[6][5]=16
    m[6][6]=17
    m[7][6]=18
    m[7][7]=19
    return m

def exampleMMM():
    size = 8
    sigmaSize = 4
    m1=matrix_A(size)

    m2 = np.zeros((size,size))
    m2[0][0]=1
    m2[0][1]=2
    m2[0][6]=3
    m2[1][1]=4
    m2[1][2]=5
    m2[2][5]=6
    m2[2][6]=7
    m2[3][0]=8
    m2[3][1]=9
    m2[3][6]=10
    m2[4][0]=11
    m2[4][3]=12
    m2[4][4]=13
    m2[4][7]=14
    m2[5][2]=15
    m2[5][5]=16
    m2[5][6]=17
    m2[6][3]=18
    m2[6][6]=19
    m2[7][0]=20
    m2[7][6]=21
    m2[7][7]=22

    print(matrixmult(m1,m2))
    m2 = m2.transpose()
    result = np.zeros((8,8))

    # Normal multiplcation
    # iterate through rows of



    sell1 = scs.Sell_c_sigma(sigmaSize/2, sigmaSize)
    sell1.construct(m1)
    print(sell1.m_final)
    sell1.print(0,0)

    sell2 = scs.Sell_c_sigma(sigmaSize/2, sigmaSize)
    # sell2 = scs.Sell_c_sigma(8, 8)
    sell2.construct(m2)
    print(sell1.m_final)
    sell2.print(0,0)
    result = scscalc.matrix_times_matrix(sell1,sell2,True)
    mvis.matprint(result,-1,-1,None,None,None,True)
    tikz = mvis.print_tikz_matrix(m1,"\\times", True, True, True)
    tikz += mvis.print_tikz_matrix(m2,"=", False, True, True)
    tikz += mvis.print_tikz_matrix(result, "", False, True, True)
    result = scscalc.matrix_times_matrix(sell1,sell2,True)
    tikz2, sell1RowPtrs = mvis.print_tikz_scs(sell1, "\\times", True)
    tikz2a, sell2RowPtrs = mvis.print_tikz_scs(sell2, "=", False)
    tikz2 +=tikz2a
    tikz2 += mvis.print_tikz_matrix(result, "", False, True, True, [sell1RowPtrs, sell2RowPtrs])
    f = open("tikz-matrix.txt", "w")
    f.write(mvis.print_tikz_image(tikz))
    f.close()
    f = open("tikz-scs.txt", "w")
    f.write(mvis.print_tikz_image(tikz2))
    f.close()

def denseMatrixMulti():
    size = 3
    m1 = np.random.randint(1,5,size=(size,size))
    m2 = np.random.randint(1,5,size=(size,size))
    result = np.matmul(m1,m2)
    tikz = mvis.print_tikz_matrix(result, "=", True, True, True)
    tikz += mvis.print_tikz_matrix(m1,"\\times", False, True, True)
    tikz += mvis.print_tikz_matrix(m2,"", False, True, True)
    f = open("tikz-dense.pgf", "w")
    f.write(mvis.print_tikz_image(tikz))
    f.close()

def slicing():
    # Dense
    size = 5
    m1 = np.random.randint(1,9,size=(size,size))
    m2 = m1[0:4,0:5]
    m3 = m1[0:5,0:4]

    tikz = mvis.print_tikz_matrix(m1, "\\rightarrow", True, True, True)
    tikz += mvis.print_tikz_matrix(m2,"or", False, True, True)
    tikz += mvis.print_tikz_matrix(m3,"", False, True, True)
    f = open("tikz-slicing-dense.pgf", "w")
    f.write(mvis.print_tikz_image(tikz))
    f.close()

    # Sparse SCS
    size = 9
    sigmaSize = 6
    m1 = smgen.create(int(size), int(size))
    sell1 = scs.Sell_c_sigma(sigmaSize/2, sigmaSize)
    sell1.construct(m1)

    tikzb, sell1RowPtrs = mvis.print_tikz_scs(sell1, "\\rightarrow", True)
    tikz21, sell1RowPtrs = mvis.print_tikz_scs(sell1,"", False)
    # tikzb += tikz2
    tikzb += tikz21
    f = open("tikz-slicing-scs.pgf", "w")
    f.write(mvis.print_tikz_image(tikzb))
    f.close()

def vectorMatrixMulti():
    size=8
    sigmaSize = 4
    v = np.array([(size-x) for x in range(size)])
    m1 = matrix_A(size)
    result = m1.dot(v)
    tikz = mvis.print_tikz_vector(result, "=", True)
    tikz += mvis.print_tikz_matrix(m1, "\\times", False)
    tikz += mvis.print_tikz_vector(v, "", False)
    f = open("tikz-vectormatrix-sparse.pgf", "w")
    f.write(mvis.print_tikz_image(tikz))
    f.close()

    sell1 = scs.Sell_c_sigma(sigmaSize/2, sigmaSize)
    sell1.construct(m1)
    print(sell1.m_final)
    sell1.print(0,0)

    result = scscalc.matrix_times_vector(sell1,v,False)
    tikz2, sell1RowPtrs = mvis.print_tikz_scs(sell1, "\\times", False)
    tikz = mvis.print_tikz_vector(result, "=", True, sell1RowPtrs)
    tikz += tikz2
    tikz += mvis.print_tikz_vector(v, "", False)
    f = open("tikz-vectormatrix-sparse.pgf", "w")
    f.write(mvis.print_tikz_image(tikz))
    f.close()

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
    amount_of_matrices = 1
    timestamp = str(datetime.fromtimestamp(datetime.timestamp(datetime.now()))).replace(" ","_").replace(":","-")
    # get global count
    glob = 0
    for r, d, f in os.walk("./tmp"):
        # print("DO",f)
        for file in f:
            if '.json' in file:
                glob +=1
    filename = 'tmp/'+str(glob)+'-matrix-examples-'+timestamp+'.json'

    for i in range(amount_of_matrices):
        # Some Output for better working
        print("\n#############################################")
        print("This is matrix "+str(i)+" of "+filename+"\n")
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

    with open(filename, 'w') as outfile:
        json.dump(ms, outfile)
        preint("\begin{tikzpicture}[every node/.style={minimum size=0.45cm-\pgflinewidth, outer sep=0pt}, scale=0.5]")

if __name__ == "__main__":
    # main()
    # exampleMMM()
    # quickbenchmark()
    # quickbenchmark_vector()
    # mult_benchmark_vector()
    # denseMatrixMulti()
    # vectorMatrixMulti()
    slicing()
