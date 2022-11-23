import sys
import random
import copy
import operator
from itertools import chain
from pysat import *
import os
import math
from sys import argv


def to_DIMAC(cnf, name_file="sudoku_solved.txt"):
    name_file = name_file.split(".")[0] + ".out.txt"
    with open(name_file, "w") as f:
        f.write("c Solution for sudoku \n")
        f.write(" p cnf 729 729 \n")
        for lit in cnf:
            lit = str(lit)
            if "-" in lit:
                f.write(f"{lit[0]}{lit[1]}{lit[2]}{lit[3]}0 \n")
            else:
                f.write(f"{lit[0]}{lit[1]}{lit[2]}0 \n")
        f.close()
        print("The output is ready in your sudoku directory")


def read_DIMACS(path):
    """
    Takes a DIMACS input file and returns a list of clauses
    """
    return CNF(from_file=path).clauses


def line2DIMACS(sudoku):
    """
    Takes one line of a sudoku file and converts it to a DIMACS line
    for variables that are true for this sudoku
    """
    input_mapping = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "A": 10,
        "B": 11,
        "C": 12,
        "D": 13,
        "E": 14,
        "F": 15,
        "G": 16,
    }

    inverse_input_mapping = {v: k for k, v in input_mapping.items()}

    input_len = len(sudoku)
    sudoku_size = int(math.pow(input_len, 0.5))
    clause_list = []
    for row in range(sudoku_size):
        for column in range(sudoku_size):
            current_line_index = column + sudoku_size * row
            cell_value = sudoku[current_line_index]
            if cell_value != ".":
                clause_list.append(
                    f"{inverse_input_mapping[row+1]}{inverse_input_mapping[column+1]}{cell_value} 0"
                )
    return clause_list, sudoku_size


def line2CNF(line):
    """
    Converts the line out of the line2DIMACS function and returns it as a list
    of clauses of which variables are true in this sudoku
    """
    cnf_list, sudoku_size = line2DIMACS(line)
    return CNF(from_string="\n".join(cnf_list)).clauses, cnf_list, sudoku_size


def simplify(rules, literal):
    """
    Simplifies the rules list of clauses by removing the true clauses and
    remove negations of true values out of a clause of a given value
    """
    for rule_clause in list(rules):
        # remove clause when true variable is in that clause
        if literal in rule_clause:
            rules.remove(rule_clause)

        # remove negative value from the clause when present
        neg_literal = 0 - literal
        if neg_literal in rule_clause:
            rule_clause.remove(neg_literal)

    return rules


def find_pure_literals(sigma):
    pure_lits = []
    merged = set(chain.from_iterable(sigma))

    for lit in merged:
        if -lit not in merged:
            pure_lits.append(lit)

    return pure_lits


def is_tautology(clause):
    neg_clause = {literal * -1 for literal in clause}
    diff = clause - neg_clause
    tautology = clause - diff

    if tautology:
        return tautology
    else:
        return None


def remove_negative(rules):
    no_neg = []
    for lit in rules[1]:
        if lit > 0:
            no_neg.append(lit)
    return no_neg


def remove_unit_clauses(rules):
    """
    Removes unit clauses from given list of rules
    """
    # get all unit clauses
    unit_clauses = []
    for clause in rules:
        if len(clause) == 1:
            literal = clause[0]
            unit_clauses.append(literal)

    # make sure unit literals occur only once
    unit_clauses = list(set(unit_clauses))

    # simplify rules based on all unit clauses
    if len(unit_clauses) != 0:
        for literal in unit_clauses:
            rules = simplify(rules, literal)

    return rules, unit_clauses


def pretty_print_sudoku(solution, size):

    # Init board
    board = [["." for x in range(size)] for y in range(size)]

    for literal in solution:
        # We need a true literal as well as one that is positive
        number = str(literal - 110)

        # Prepend a zero so that we have 3 character string

        diff = 3 - len(number)
        number = "0" * diff + number
        row = int(number[0])
        col = int(number[1])
        val = int(number[2])

        board[row][col] = val

    builder = ""
    for row in board:
        builder += str(row) + "\n"

    print(builder)
