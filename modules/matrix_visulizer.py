import numpy as np
import random as rand
import math
from termcolor import colored


def printmatrix(m):
    x, y = m.shape
    if x != 0 and y != 0:
        print_indexinates_x(x)
        printline(y)
        for ix in range(x):
            t = "#  "
            for iy in range(y):
                if m[ix][iy] != 0:
                    t += str(m[ix][iy])
                else:
                    t += "   "
                if iy != y - 1:
                    t += "  "
            print(t + "  #")
        printline(y)
    else:
        print("Error! Dimensions are " + str(m.shape))


def printline(y):
    str = "##"
    for iy in range(y):
        str += "#####"
    str += "##"
    print(str)


def print_indexinates_x(x):
    t = "   "
    for i in range(x):
        t += " " + str(i)
        if (x < 10):
            t += " "
        t += "  "
    print(t)


def matprint(mat, highlight_x=-1, highlight_y=-1, sellcsigma=None, isigma=None, ichunk=None, markDiagonal=False, fmt="g"):
    col_maxes = [max([len(("{:" + fmt + "}").format(x))
                      for x in col]) for col in mat.T]
    row, col = np.diag_indices(mat.shape[0])
    for idy, y in enumerate(mat):
        if sellcsigma is not None and isigma is not None and ichunk is not None:
            tmp, original_row_index = sellcsigma.sell_index_to_global_index(isigma, ichunk, idy, -1)
            # original_row_index=0
            c = sellcsigma.print_unit(isigma, ichunk, idy, True)
            print(colored("{:02d}".format(
                isigma) + " | " + "{:02d}".format(ichunk) + " | " + "{:02d}".format(idy) + " | ", c) + colored("{:02d}".format(
                    original_row_index), "green"), end=" ")
        else:
            print(colored("{:02d}".format(idy), "green"), end=" ")
        for idx, x in enumerate(y):
            c = "white"
            if x == 0:
                c = "magenta"
            # print(idx,i, row[idx], col[i])
            if idy == row[idy] and idx == col[idy] and markDiagonal:
                c = "red"
            if idx == highlight_x and idy == highlight_y:
                c = 'green'
            print(
                colored(("{:" + str(col_maxes[idx]) + fmt + "}").format(x), c), end="  ")
        print("")


def print_sellcsigma_matrix(sell_c_sigma, highlight_x=-1, highlight_y=-1):
    print("\nPrinting SELL-" + str(sell_c_sigma.sell_c) + "-" +
          str(sell_c_sigma.sell_sigma), end=" ")

    if highlight_x > -1 and highlight_y > -1:
        scope_index, chunk_offset, row_index, sell_x = sell_c_sigma.global_index_to_sell_index(
            highlight_x, highlight_y)
        print("with highlighted point: (x= " +
              str(highlight_x) + ", y= " + str(highlight_y) + ")", end=" ")
        print("Scope: " + str(scope_index) + " Chunk: " + str(chunk_offset) +
              " Row: " + str(row_index) + " x:" + str(sell_x), end="\n")
    else:
        print("\n", end="")
    # print("\nprint_sellcsigma_matrix")
    # print("scope_index: "+str(scope_index))
    # print("chunk_offset: "+str(chunk_offset))
    # print("row_index: "+str(row_index))
    # print("sell_x: "+str(sell_x))
    # print(sell_c_sigma.global_index_to_sell_value(highlight_x, highlight_y))
    print(colored("U  | S  | C  | R  | ", "cyan") +
          colored("OR", "green"), end="\n")
    # sell_c_sigma.sell_index_to_global_index(scope_index,chunk_offset,row_index,sell_x)
    for isigma, sigma in enumerate(sell_c_sigma.m_final):
        for ichunk, chunk in enumerate(sigma):
            if highlight_x > -1 and highlight_y > -1:
                if isigma == scope_index and ichunk == chunk_offset:
                    kx = sell_x
                    ky = row_index
                else:
                    kx = -1
                    ky = -1
                matprint(np.array(chunk), kx, ky, sell_c_sigma, isigma, ichunk)
            else:
                matprint(np.array(chunk), -1, -1, sell_c_sigma, isigma, ichunk)

            # for irow, row in enumerate(chunk):
            #     print(row)

def doNothing(m):
    return ""

def standardGrid(m):
    x, y = m.shape
    return tikz_grid(x,y)

# def print_tikz_matrix(m, add="", print_edefs=False, print_indexinates_x=False, print_indexinates_y=False):
def print_tikz_matrix(m, add="", print_edefs=False, print_indexinates_x=False, print_indexinates_y=False, printSCSindex=None):
    ret = print_tikz_matrix_intern(m, add, print_edefs, print_indexinates_x, print_indexinates_y, standardGrid, printSCSindex)
    # ret = addLine(ret, tikz_grid(x,y),1)
    return ret

def print_edefs_ret(b, y, ret=""):
    if b:
        ret = addLine(ret, "\\edef\\basex{0}", 1)
        ret = addLine(ret, "\\edef\\basey{"+str(y)+"}", 1)
    return ret

def print_tikz_matrix_intern(m, add="", print_edefs=False, print_indexinates_x=False, print_indexinates_y=False, printGrids=doNothing, printSCSindex=None):
    x, y = m.shape
    ret = ""
    ret = print_edefs_ret(print_edefs, y, ret)
    if x != 0 and y != 0:
        if print_indexinates_y:
            if printSCSindex == None:
                ret += tikz_index_y(m)
            else:
                ret += tikz_index_scs_y(printSCSindex[0])
        ret = addLine(ret, tikz_foreach[0], 1)
        for ix in range(x):
            ret += ts(2)
            for iy in range(y):
                ret += foreach_element(m, ix, iy)
            ret = addLine(ret, "")
        ret = addLine(ret, tikz_foreach[1],1)
        ret = addLine(ret, tikz_foreach[3]+str(y-0.5)+tikz_foreach[4],2)
        ret = addLine(ret, tikz_foreach[5],1)
        ret = addLine(ret, printGrids(m), 1)
        if print_indexinates_x:
            if printSCSindex == None:
                ret += tikz_index_x(m)
            else:
                ret += tikz_index_scs_x(printSCSindex[1])
        ret = addBaseX(ret, x)
        if add != "":
            ret = addBaseX(ret, 1)
            ret = addLine(ret, "\\node[color=black] at (\\basex,"+str(y/2)+") {{\Huge${"+str(add)+"}$}};",1)
            ret = addBaseX(ret, 1)
        return ret
    else:
        print("Error! Dimensions are " + str(m.shape))
        return ""

def addLine(string, stradd, tsn=0):
    t = ts(tsn)
    # print("addLine: "+t+stradd+"%\n")
    if stradd == "":
        return string
    return string+t+stradd+"%\n"

tikz_foreach= [
    "\\foreach \\y\\x\\i in {%",
    "}{",
    "\\node[fill=black] at ( \\x+0.5+\\basex,-\\y+\\basey) {};",
	"\\node[color=black] at (\\x+\\basex+0.5,-\\y+",
    ") {{${\\i}$}};",
	"}"
]

def foreach_element(m, ix, iy, ts=0):
    if m[ix][iy] != 0:
        return str(ix)+"/"+str(iy)+"/"+str(int(m[ix][iy]))+", "
    else:
        return str(ix)+"/"+str(iy)+"/, "

def tikz_grid(sizex,sizey, kx=0):
    return "\\draw[step=1cm,color=black] (\\basex,"+str(kx)+") grid (\\basex+"+str(sizex)+","+str(sizey)+");"

def tikz_index_scs_x(r):
    print(r)
    ret = ""
    for iir, ir in enumerate(r):
        ret = addLine(ret, "\\node[color=lightgray] at (\\basex+0.5+"+str(iir)+","+str(len(r)+0.5)+") {{${"+str(ir)+"}$}};",1)
    return ret

def tikz_index_x(m):
    x, y = m.shape
    ret = ""
    for ix in range(x):
        ret = addLine(ret, "\\node[color=lightgray] at (\\basex+0.5+"+str(ix)+","+str(y+0.5)+") {{${"+str(ix)+"}$}};",1)
    return ret

def tikz_index_scs_y(r):
    ret = ""
    for iir, ir in enumerate(r):
        ret = addLine(ret, "\\node[color=lightgray] at (\\basex+0.5,-"+str(iir)+"+"+str(len(r)-0.5)+") {{${"+str(ir)+"}$}};",1)
    ret = addBaseX(ret, 1)
    # print(ret)
    return ret

def tikz_index_y(m):
    x, y = m.shape
    ret = ""
    for iy in range(y):
        ret = addLine(ret, "\\node[color=lightgray] at (\\basex+0.5,-"+str(iy)+"+"+str(y-0.5)+") {{${"+str(iy)+"}$}};",1)
    ret = addBaseX(ret, 1)
    # print(ret)
    return ret

def addBaseX(string,basex):
    r = addLine(string, "\\pgfmathparse{\\basex+"+str(basex)+"}", 1)
    return addLine(r, "\\xdef\\basex{\\pgfmathresult}", 1)

def ts(t=0):
    tss = ""
    for i in range(t):
        tss+="\t"
    return tss

def print_tikz_image(string):
    ret = ""
    ret = addLine(ret, "\\definecolor{mygreen}{rgb}{0.35,0.788,0.333}")
    ret = addLine(ret, "\\definecolor{myred}{rgb}{0.976,0.698,0.2}")
    ret = addLine(ret, "\\definecolor{highlight}{rgb}{0.89, 0.024, 0.075}")
    ret = addLine(ret, "\\definecolor{myblue}{rgb}{0, 0.624, 0.89}")
    ret = addLine(ret, "\\definecolor{mypurple}{rgb}{0.576, 0.376, 0.216}")
    ret = addLine(ret, "\\usetikzlibrary{backgrounds}")
    ret = addLine(ret, "\\begin{tikzpicture}[every node/.style={minimum size=0.95cm-\\pgflinewidth, outer sep=0pt}, scale=1]")
    ret += string
    ret = addLine(ret, "\\end{tikzpicture}")
    return ret

def print_tikz_scs(m, add="", print_edefs=False, print_Colors=False):
    ret = ""
    tmp = ""
    x, y = m.original_matrix.shape
    sigmaSize = m.sell_sigma
    additional_height=0
    if y% (sigmaSize/2) !=0:
        additional_height = sigmaSize/2 - y % (sigmaSize/2)
    # print("height: "+str(additional_height))
    maxrow = getMaxRow(m)
    ret = print_edefs_ret(print_edefs, y, ret)
    ret = addLine(ret, "\\edef\\startbasex{\\basex}", 1)
    ret = addLine(ret, "\\foreach \\y\\x\\c\\i in {", 1)
    tmp = addLine(tmp, "\\foreach \\y\\x\\c\\i in {", 1)
    kcol = 0
    chunkcolor = 0
    for isigma, sigma in enumerate(m.m_final):
        for ichunk, chunk in enumerate(sigma):
            for irow, row in enumerate(chunk):
                v = False
                kcol = chunkcolor
                for icol, col in enumerate(row):
                    if col != 0:
                        if kcol == 0:
                            color = "myred"
                        if kcol == 1:
                            color = "mygreen"
                        if kcol == 2:
                            color = "myblue"
                        if kcol == 3:
                            color = "mypurple"
                        if not print_Colors:
                            color = "black"
                        ret = addLine(ret, (str(isigma*sigmaSize+ichunk*sigmaSize/2+irow)+ "/"  +str(icol)+ "/"+color+"/"+str(int(col))+ ", "), 2)
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
                        if not print_Colors:
                            color = "black"
                        tmp = addLine(tmp, (str(isigma*sigmaSize+ichunk*sigmaSize/2+irow)+ "/"  +str(icol)+ "/"+color+"/"+ ", "), 2)
                    kcol = (kcol + 1) % 4
            if sigmaSize/2 - irow >= 0:
                for i in range(int(sigmaSize/2-irow)):
                    ret = addLine(ret, (str(isigma*sigmaSize+ichunk*sigmaSize/2+i)+ "//black/, "), 2)
                # if v:
                    # ret += "\t\t"
            chunkcolor = kcol

    # print(mem)
    ret = ret[:-4] + "%\n"
    tmp = tmp[:-4] + "%\n"
    # print(size)
    ret = addLine(ret, "}{",1)
    if print_Colors:
        ret = addLine(ret, "\\node[fill=\\c] at (\\x+"+str(0.5)+",-\\y+"+str(y-0.5)+") {};", 2)
    ret = addLine(ret, "\\node[color=black] at (\\x+\\basex+0.5,-\\y+"+str(y-0.5)+") {${\\i}$};",2)
    ret = addLine(ret, "}", 1)
    if print_Colors:
        ret = addLine(ret, tmp, 1)
        ret = addLine(ret, "}{",1)
        ret = addLine(ret, "\\node[fill=\\c] at (\\x+\\basex+0.5,-\\y+"+str(y-0.5)+") {};",2)
        ret = addLine(ret, "}",1)

    for isigma, sigma in enumerate(m.m_final):
        for ichunk, chunk in enumerate(sigma):
            maxcol=0
            for icol, col in enumerate(chunk[0]):
                if col != 0:
                    maxcol+=1
            ret = addLine(ret, tikz_grid(maxcol, (y-sigmaSize/2-(isigma*sigmaSize+ichunk*sigmaSize/2)), (y-(isigma*sigmaSize+ichunk*sigmaSize/2))),1)

    ret = addLine(ret, "\\node[draw=none, align=center] at (\\basex+.75,-0.6-"+str(additional_height)+") {Values};",1)
    ret = addBaseX(ret, maxrow+1)

    # colum_index
    ret = addLine(ret, "\\foreach \\y\\x\\i in {", 1)
    rowptrs = []
    for isigma, sigma in enumerate(m.m_final):
        for ichunk, chunk in enumerate(sigma):
            for irow, row in enumerate(chunk):
                rowptr, columnIndexes = get_Original_rowcol(m, isigma, ichunk, irow)
                rowptrs.append(rowptr)
                for icolindex, colindex in enumerate(columnIndexes):
                    ret = addLine(ret, (str(isigma*sigmaSize+ichunk*sigmaSize/2+irow)+ "/"  +str(icolindex)+ "/"+str(int(colindex))+ ", "), 2)
    ret = ret[:-4] + "%\n"
    tmp = tmp[:-4] + "%\n"
    ret = addLine(ret, "}{",1)
    ret = addLine(ret, "\\node[color=black] at (\\x+\\basex+0.5,-\\y+"+str(y-0.5)+") {${\\i}$};",2)
    ret = addLine(ret, "}", 1)

    for isigma, sigma in enumerate(m.m_final):
        for ichunk, chunk in enumerate(sigma):
            maxcol=0
            for icol, col in enumerate(chunk[0]):
                if col != 0:
                    maxcol+=1
            ret = addLine(ret, tikz_grid(maxcol, (y-sigmaSize/2-(isigma*sigmaSize+ichunk*sigmaSize/2)), (y-(isigma*sigmaSize+ichunk*sigmaSize/2))),1)

    ret = addLine(ret, "\\node[draw=none, align=center] at (\\basex+1.5,-0.6-"+str(additional_height)+") {Column Indicies};",1)
    ret = addBaseX(ret, maxrow+1)


    # ROW PTRs
    ret = addLine(ret, "\\foreach \\y\\i in {", 1)
    for irowptr, rowptr in enumerate(rowptrs):
        ret = addLine(ret, str(irowptr)+"/"+str(rowptr)+", ", 1)
    for i in range(int(additional_height)):
        ret = addLine(ret, str(i+y)+"/, ", 1)
    ret = ret[:-4] + "%\n"
    # print(size)
    ret = addLine(ret, "}{",1)
    ret = addLine(ret, "\\node[color=black] at (\\basex+0.5,-\\y+"+str(y-0.5)+") {${\\i}$};",2)
    ret = addLine(ret, "}", 1)
    ret = addLine(ret, tikz_grid(1, y), 1)
    if additional_height != 0:
        ret = addLine(ret, tikz_grid(1, additional_height*-1), 1)

    ret = addLine(ret, "\\node[draw=none, align=center] at (\\basex+0.5,-0.6-"+str(additional_height)+") {Original \\\\ row index};",1)

    ret = addBaseX(ret, 1)

    # Beschriftungen


    # Border startbasex
    ret = addLine(ret, "\draw[dashed] (\\startbasex-0.5, -1.5-"+str(additional_height)+") -- (\\basex+0.5,-1.5-"+str(additional_height)+") -- ((\\basex+.5,"+str(y)+"+0.5) -- (\\startbasex-0.5, "+str(y)+"+0.5) -- (\\startbasex-0.5, -1.5-"+str(additional_height)+");", 1)

    if add != "":
        ret = addBaseX(ret, 1)
        ret = addLine(ret, "\\node[color=black] at (\\basex,"+str(y/2)+") {{\Huge${"+str(add)+"}$}};",1)
        ret = addBaseX(ret, 1)
    # print(m.__dict__)
    return ret, rowptrs

def getMaxRow(m):
    maxrow=0
    for isigma, sigma in enumerate(m.m_final):
        for ichunk, chunk in enumerate(sigma):
            maxcol=0
            for icol, col in enumerate(chunk[0]):
                if col != 0:
                    maxcol+=1
            if maxrow < maxcol:
                maxrow = maxcol
    return maxrow

def get_Original_rowcol(m, isigma, ichunk, irow):
    for or_index, sell_index in m.sigma_scope_rows_mapping[isigma].items():
        if sell_index == irow + ichunk*m.sell_c:
            original_row = or_index
    retrow = original_row+m.sell_sigma*isigma
    return retrow, m.sigma_scope_columnIndex[isigma][original_row]

def print_tikz_vector(v, add="", print_edefs=False, row_ptr=None):
    y = len(v)
    ret = ""
    ret = print_edefs_ret(print_edefs, y, ret)
    print("print_edefs "+str(print_edefs)+ret)
    if row_ptr != None:
        print("row_ptr "+str(row_ptr))
        ret += tikz_index_scs_y(row_ptr)
    ret = addLine(ret, tikz_grid(1, y) ,1)
    ret = addLine(ret, "\\foreach \\y\\i in {", 1)
    for iv, val in enumerate(v):
        ret = addLine(ret, (str(iv)+ "/"+ str(int(val))+ ", "), 2)
    ret = addLine(ret, "}{",1)
    ret = addLine(ret, "\\node[color=black] at (\\basex+0.5,-\\y+"+str(y-0.5)+") {${\\i}$};",2)
    ret = addLine(ret, "}", 1)
    ret = addBaseX(ret, 1)
    if add != "":
        ret = addBaseX(ret, 1)
        ret = addLine(ret, "\\node[color=black] at (\\basex,"+str(y/2)+") {{\Huge${"+str(add)+"}$}};",1)
        ret = addBaseX(ret, 1)
    return ret
