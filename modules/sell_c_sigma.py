import modules.sell_c_sigma_functions as sell
import modules.matrix_visulizer as mvis
from termcolor import colored
import traceback
import sys


class Sell_c_sigma:
    def __init__(self, sell_c, sell_sigma):
        self.sell_c = sell_c
        self.sell_sigma = sell_sigma
        self.mark_first_unit = True
        self.unitmapping = None
        # print("Create Sell-" + str(sell_c) + "-" + str(sell_sigma))

    def construct(self, m):
        self.original_matrix = m
        self.m_sigma, self.sigma_scope_offsets, self.sigma_scope_rows_mapping, self.sigma_scope_columnIndex = sell.sort_rows_in_scope(
            m, self.sell_sigma)
        self.m_final = sell.pad_chunk_with_zeros(self.m_sigma, self.sell_c)
        return self.m_final

    def print(self, x, y):
        mvis.print_sellcsigma_matrix(self, x, y)

    def global_index_to_sell_value(self, x, y):
        scope_index, chunk_offset, row_index, sell_x = self.global_index_to_sell_index(
            x, y)
        if scope_index is None or chunk_offset is None or row_index is None or sell_x is None:
            return 0
        value = self.m_final[scope_index][chunk_offset][row_index][sell_x]
        # print(x, y)
        # print("scope_index: " + str(scope_index) + " // " +
        #       str(y - self.sell_sigma * scope_index))
        # print("Index: " + str(row_index))
        # print("row_offsets: " + str(row_offsets))
        # print("row_within_sell: " + str(row_within_sell))
        # print("row_reconstructed: " + str(row_reconstructed))
        # print("value: " + str(value))
        # print("original: " + str(self.original_matrix[x][y]))
        return value

    def global_index_to_sell_index(self, x, y):
        # y=y-1
        scope_index = int(y / self.sell_sigma)
        # print(y, self.sell_sigma,scope_index,
        #       len(self.sigma_scope_rows_mapping))
        # print(str(len(self.sigma_scope_rows_mapping)) + ": scope_index("+str(scope_index)+") -> y(" + str(y) + ") - self.sell_sigma(" + str(self.sell_sigma) + ") * scope_index(" + str(scope_index) + ")", y - self.sell_sigma * scope_index)
        # if int(scope_index) >= int(len(self.sigma_scope_rows_mapping)):
        #     print("Error scope index", y, self.sell_sigma,
        #           scope_index, len(self.sigma_scope_rows_mapping))

        try:
            row_index = self.sigma_scope_rows_mapping[scope_index][y -
                                                                   self.sell_sigma * scope_index]
        except Exception as e:
            try:
                print("###############################")
                print(str(e))
                traceback.print_exc()
                print("Error (y, self.sell_sigma, scope_index)",
                      y, self.sell_sigma, scope_index)
                print("Error (y -self.sell_sigma * scope_index)",
                      (y - (self.sell_sigma * scope_index)))
                print("Error len(self.sigma_scope_rows_mapping[scope_index])", len(
                    self.sigma_scope_rows_mapping[scope_index]))
                print("###############################")
            except Exception as e:
                print("###############################")
                print(str(e))
                traceback.print_exc()
                print("Error (y, self.sell_sigma)", y, self.sell_sigma)
                print("Error (scope_index)", scope_index)
                print("Error len(self.sigma_scope_rows_mapping)",
                      len(self.sigma_scope_rows_mapping))
                print("Error self.sigma_scope_rows_mapping",
                      self.sigma_scope_rows_mapping)
                print("###############################")
            # exiing with a non zero value is better for returning from an error
            sys.exit(1)

        row_offsets = self.sigma_scope_offsets[scope_index][y -
                                                            self.sell_sigma * scope_index]
        row_within_sell = self.m_sigma[scope_index][row_index]
        # print("row_offsets:     " + str(row_offsets))
        # print("row_within_sell: " + str(row_within_sell))
        sell_x = self.reconstruct_sell_x(row_within_sell, row_offsets, x)
        # print("original:        " + str(self.original_matrix[x]))
        # print("sell_y:          " + str(sell_y))
        # print()
        # if sell_y is not None:
        # print("                (" + str(row_within_sell[sell_x]) + ")")
        chunk_offset = int(row_index / self.sell_c)
        # print("\nself.sigma_scope_rows_mapping[]: " +
        #       str(self.sigma_scope_rows_mapping[scope_index]))
        # print("chunk_offset: " + str(chunk_offset) + "=" + str(row_index) +
        #       "/" + str(self.sell_c) + " = " + str(row_index / self.sell_c))
        return scope_index, chunk_offset, row_index % self.sell_c, sell_x

    def sell_index_to_global_index(self, isigma, ichunk, irow, ix=-1):
        irow += ichunk * self.sell_c
        # print(isigma, ichunk, irow)
        # print(self.sigma_scope_rows_mapping[isigma])
        for or_index, sell_index in self.sigma_scope_rows_mapping[isigma].items():
            if sell_index == irow:
                original_row = or_index
        original_y = isigma * self.sell_sigma + original_row
        original_x = -1
        if ix != -1:
            offsets = 0
            for i in range(0, ix):
                offsets += self.sigma_scope_offsets[isigma][original_row][i]
            original_x = ix + offsets
        return original_x, original_y

    def reconstruct_row(self, row_within_sell, row_within_sell_offsets):
        reconstructed_row = []
        for idrow, row in enumerate(row_within_sell):
            for i in range(row_within_sell_offsets[idrow]):
                reconstructed_row.append(0)
            reconstructed_row.append(row)
        return reconstructed_row

    def reconstruct_sell_x(self, row_within_sell, row_within_sell_offsets, x):
        # print("\n y:"+str(y))
        sell_x = 0
        # print("\nrow_within_sell_offsets" + str(row_within_sell_offsets))
        for idrow, row in enumerate(row_within_sell):
            # print("idrow: " + str(idrow) + " // " + "sell_x: " + str(sell_x) + " // " + "x: " + str(x) +
            #       " // " + "row_within_sell_offsets[idrow]: " + str(row_within_sell_offsets[idrow]) + " // " +
            #       "sellx after: " + str(sell_x + row_within_sell_offsets[idrow]))
            sell_x += row_within_sell_offsets[idrow]
            if sell_x == x:
                return idrow
            sell_x += 1
        return None

    def prepare_units(self, nunits, pattern, *args):
        self.unitmapping = pattern(nunits, self, *args)

    def print_unit(self, isigma, ichunk, irow, mark_first=False):
        c = "cyan"
        if self.unitmapping is not None:
            if self.unitmapping[isigma][ichunk][irow] == 0 and mark_first and self.mark_first_unit:
                c = "green"
            print(colored("{:02d}".format(
                self.unitmapping[isigma][ichunk][irow]) + " |", c), end=" ")
        else:
            print(colored("## |", c), end=" ")
        return c
