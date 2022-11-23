"""
SAT solver for sudoku
Make sure that the .txt files are in the folder sudokus
This is version 1.3
Created by Lars Woudstra and Victor Retamal
"""
import pandas as pd
#from typing_extensions import final
from pysat import *
import sys
import os
import math
from itertools import chain
import random
import copy
from sys import argv
from util import *
from heuristics import *
import time
import argparse

stats = {
    "backs": 0,
    "time": 0,
}


def SAT(rules):
    """
    Returns true when rules is empty, which means that the problem has been
    solved
    """
    if len(rules) == 0:
        return True

    # check if clause is empty
    for clause in rules:
        if len(clause) == 0:
            return False

    return None


def solve(rules, solution, heuristic):
    """
    Solves the rest of the SAT problem until SAT returns True or False. Returning
    True means that there are no rules left to simplify and thus that the problem
    is satisfied. Returning false means that there is no solution to this problem
    """
    global stats
    # check if the problem is satisfied
    if SAT(rules) != None:
        return SAT(rules), solution

    # create a list of all literals that are left in the rules
    unique_literals = list(set(chain.from_iterable(rules)))
    copy_rules = copy.deepcopy(rules)

    # implement heuristics
    if heuristic == "1":
        picked_literal = random.choice(unique_literals)
    if heuristic == "2":
        picked_literal = mrv(solution, unique_literals)
    if heuristic == "3":
        picked_literal = JW(rules)

    new_rules = simplify(copy_rules, picked_literal)
    new_solution = solution.copy()
    new_solution.append(picked_literal)

    # filter out unit clauses again
    new_rules, removed_literals = remove_unit_clauses(new_rules)
    new_solution.extend(removed_literals)

    # check if it worked. If so, continue on this branch
    result = solve(new_rules, new_solution, heuristic)
    if result[0]:
        return result

    # print("backbranch")
    stats["backs"] = stats["backs"] + 1
    picked_literal = -picked_literal
    new_rules = simplify(rules, picked_literal)
    new_solution = solution.copy()
    new_solution.append(picked_literal)

    # filter out unit clauses again
    new_rules, removed_literals = remove_unit_clauses(new_rules)
    new_solution.extend(removed_literals)

    # add picked literal to the solution
    return solve(new_rules, new_solution, heuristic)


def dpll2(rules, heuristic):
    """
    Remove unit clauses and start solving the problem. Returns True when problem
    is satisfied and its solution. Returns false and a counter example when problem
    can not be satisfied
    """

    # check if the problem is satisfied
    if SAT(rules) != None:
        return SAT(rules)

    # remove unit clauses
    rules, removed_clauses = remove_unit_clauses(rules)

    return solve(rules, removed_clauses, heuristic)


def run_sat(args):
    """
    Reads input arguments and sets up the right rules for the SAT problem
    """
    try:
        file_path = str(args["f"])
    except:
        print("Sudoku file not found, running default")
        file_path = "sudokus/1000 sudokus.txt"
    heuristic = str(args["S"])
    try:
        sudoku_nr = int(args["n"])
    except:
        sudoku_nr = 1
    # stores each sudoku example in a list
    with open(file_path) as f:
        sudoku_list = f.readlines()

    # get the CNF of the current sudoku example (sudoku_setup_CNF)
    sudoku_setup_CNF, sudoku_setup_DIMACS, sudoku_size = line2CNF(
        sudoku_list[sudoku_nr]
    )

    # create rules and add setup rules as unit clauses
    try:
        four = int(args["t"])
        rules = read_DIMACS(os.path.join("sudokus/sudoku-rules-4x4.txt"))

    except:
        rules = read_DIMACS(os.path.join("sudokus/sudoku-rules-9x9.txt"))
    rules.extend(sudoku_setup_CNF)

    # start the dpll2 algorithm
    final_results = dpll2(rules, heuristic)
    return final_results


def main():
    # Create an argument parser to parse the arguments
    print(
        "Introduce 9x9 sudoku. Format SAT.py -S<Heuristic> -f<file> -n<sudoku number if needed>"
    )
    print("For 4x4 Format SAT.py -SHeuristic -ffile -nsudoku number if needed -t4")
    ap = argparse.ArgumentParser()
    ap.add_argument("-S", required=True, help="S1:DPLL, S2:MRV, S3:JW-OS")
    ap.add_argument("-f", required=False, help="Input file.")
    ap.add_argument("-n", required=False, help="Sudoku number in file")
    ap.add_argument("-t", required=False, help="4x4 sudoku activated")
    args = vars(ap.parse_args())

    final_results = run_sat(args)
    file_name = str(args["f"])
    to_DIMAC(final_results[1], file_name)


if __name__ == "__main__":

    main()
