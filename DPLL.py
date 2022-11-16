import sys
import math
from collections import Counter
import copy
import numpy as np
import time

def print_sudoku(solution):
    digits = [x for x in solution if x>0]
    sudoku = np.zeros((9,9))

    for digit in digits:
        string = str(digit)
        row = int(string[0])
        column = int(string[1])
        value = int(string[2])
        sudoku[row-1,column-1] = value
    
    print()
    print("Solution:")
    print()
    print(sudoku)
    print()



def simplify(clauses):

    removed_literals = []
    unit_clauses = [True]
    while len(unit_clauses) >= 1:
        
        # find all unit clauses
        unit_clauses = []
        for clause in clauses:
            if len(clause) == 1:
                unit_clauses.append(clause[0])
    
        # remove clauses containing unit clauses and shorten clauses containing -P
        if len(unit_clauses) != 0:
            for unit in unit_clauses:
                true_idx = []
                for i, clause in enumerate(clauses):
                    if unit in clause:
                        true_idx.append(i)
                    if -unit in clause:
                        clauses[i].pop(clause.index(-unit))
                for index in sorted(true_idx, reverse=True):
                    clauses.pop(index)
        # add all unit clauses to removed literals
        removed_literals.extend(unit_clauses)  
    
    return clauses, list(set(removed_literals))

def SAT_Solver():
    clauses = []

    # read rules file
    with open(sys.argv[1],'r') as f:
        lines = f.read().splitlines()

    # get information on data
    _, _, n_var, n_clauses = lines[0].split(' ')
    lines.pop(0)

    # convert to clauses
    for line in lines:
        var_ids = line.split(' ')
        clauses.append([int(x) for x in var_ids if x != '0'])
    
    # convert given digits to clauses
    cells = [*sys.argv[2]]
    size = math.sqrt(len(cells))
    for i, cell in enumerate(cells):
        if cell.isdigit()==True:
            row = math.ceil((i+1)/size)
            column = i%size+1
            digit = int(cell)
            literal = row*100 + column*10 + digit
            clauses.append([int(literal)])


    # Tautology rule
    for i, clause in enumerate(clauses):
        for literal in clause:
            for j in range(len(clause)):
                if clause[j] == -literal:
                    clauses.pop(i)    

    clauses, solution = simplify(clauses)

    if len(clauses) == 0:
        return 'sat', [x for x in solution if x > 0]

    if DPLL(clauses, solution=solution) == True: return 'sat'
    else: return 'unsat'


def DPLL(clauses, P=None, solution=[]):
    # print(clauses)
    # print()
    # print()
    # print(len(clauses))

    copy_clauses = copy.deepcopy(clauses)

    if P != None:
        copy_clauses.append([P])
    
    new_clauses, unit_clauses = simplify(copy_clauses)
    new_solution = solution.copy()
    new_solution += unit_clauses

    # check for contradiction
    for literal in new_solution:
        if -literal in new_solution: 
            return False

    # no clauses
    if len(new_clauses) == 0:
        print_sudoku(new_solution)
        return True

    # empty clause
    for clause in new_clauses:
        if len(clause)==0: 
            return False 
    
    # split (DLCS)
    
    # concatenate all literals
    all_literals=[]
    for clause in new_clauses:
        all_literals+=clause

    # sort by DLCS
    scores = Counter(all_literals)
    CP_CN = max(sorted(scores), key=lambda symbol: scores[symbol] + scores[-symbol])

    # split JW
    new_clauses = sorted(new_clauses, key = lambda c: len(c))
    picked_literal = new_clauses[0][0]

    if DPLL(new_clauses, P = picked_literal, solution = new_solution) == True: # proceed down the tree
        return True
    elif DPLL(clauses, P = -picked_literal, solution = solution) == True: # flip literal and proceed along other side of tree
        return True
    else: return False # branch up
       
if __name__ == '__main__':
    start = time.time()
    print(SAT_Solver()) 
    end = time.time()
    print(f"execution of sudoku solver took {end-start} seconds")