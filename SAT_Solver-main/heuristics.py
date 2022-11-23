import sys
import random
import copy
import operator
from itertools import chain


def JW(sigma):

    jw_counts = {}

    for clause in sigma:
        for literal in clause:
            if literal in jw_counts:
                jw_counts[literal] += 2 ** -len(clause)
            else:
                jw_counts[literal] = 2 ** -len(clause)

    # max_lit = max(jw_counts, key=jw_counts.get)
    max_lit = min(jw_counts, key=jw_counts.get)

    return max_lit


def mrv(removed_literals, unique_variables):

    """
    Returns the literal with the highest score based upon Minimum Remaining
    Values (MRV), on which the dpll2 should branch on next
    """
    to_choose_dict_2 = {}
    row_dict = {i: 0 for i in range(1, 10)}
    column_dict = {i: 0 for i in range(1, 10)}

    for removed_literal in removed_literals:
        row = abs(removed_literal) // 10**2 % 10
        column = abs(removed_literal) // 10 % 10
        # print(f"Row {row}, and column {column}")
        row_dict[row] = row_dict[row] + 1
        column_dict[column] = column_dict[column] + 1

    for unique_variable in unique_variables:
        var_row = abs(unique_variable) // 10**2 % 10
        var_column = abs(unique_variable) // 10 % 10
        to_choose_dict_2[unique_variable] = row_dict[var_row] + column_dict[var_column]
    max(to_choose_dict_2, key=to_choose_dict_2.get)

    return max(to_choose_dict_2, key=to_choose_dict_2.get)
