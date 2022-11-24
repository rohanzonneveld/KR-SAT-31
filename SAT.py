import sys
import math
from collections import Counter
import copy
import numpy as np
import time
from heuristics import *
import random
import shutil
import pandas as pd

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
    
        # remove clauses containing unit clauses P and shorten clauses containing -P
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


def DPLL(clauses, P=None, solution=[], version='-S2', p=0, n_backtracks=0, n_sudoku=0, save_results=False, calls=0):
    # update total calls to the function
    calls+=1

    copy_clauses = copy.deepcopy(clauses)
    copy_solution = copy.deepcopy(solution)

    if P != None:
        copy_clauses.append([P])
    
    new_clauses, unit_clauses = simplify(copy_clauses)
    new_solution = copy_solution
    new_solution += unit_clauses

    # check for contradiction
    for literal in new_solution:
        if -literal in new_solution: 
            return False

    # no clauses
    if len(new_clauses) == 0:
        print_sudoku(new_solution)
        # write to results to file
        if save_results == True:
            df = pd.DataFrame({'n_sudoku': [n_sudoku], 'calls': [calls], 'algorithm': [version]})
            df.to_csv('data.csv', mode='a', index=False, header=False)
        return True

    # empty clause
    for clause in new_clauses:
        if len(clause)==0: 
            return False
    
    # split
    if version == "-S1" : # basic DPLL algorithm: random choice
        all_literals=[]
        for clause in new_clauses:
            all_literals+=clause
        all_literals = list(set(all_literals)) # get all unique literals
    
        picked_literal = random.choice(all_literals)

        if DPLL(new_clauses, P = picked_literal, solution = new_solution, version=version, p=p, n_backtracks=n_backtracks, n_sudoku=n_sudoku, save_results=save_results, calls=calls) == True: # proceed down the tree
            return True
        elif DPLL(clauses, P = -picked_literal, solution = solution, version=version, p=p, n_backtracks=n_backtracks, n_sudoku=n_sudoku, save_results=save_results, calls=calls) == True: # flip literal and proceed along other side of tree
            return True
        else: return False # branch up

    # change version with probability p
    if random.uniform(0, 1) < p:
        version = "-S3" if version=="-S2" else "-S2"

    if version == "-S2": # number strategy 
        possibles = number_strategy(new_solution)

        for option in possibles:    # test all options
            if DPLL(new_clauses, option, new_solution, version=version, p=p, n_backtracks=n_backtracks, n_sudoku=n_sudoku, save_results=save_results, calls=calls) == True:
                return True     # if satisfactory return True
            else:
                n_backtracks += 1
                continue    # if not satisfactory: test next option
        else: return False    # if all options are unsatisfactory: branch up
   
    if version == "-S3": # TODO cell strategy
        possibles = cell_strategy(new_solution)

        for option in possibles:
            if DPLL(new_clauses, option, new_solution, version=version, p=p, n_backtracks=n_backtracks, n_sudoku=n_sudoku, save_results=save_results, calls=calls) == True:
                return True     # if satisfactory return True
            else:
                n_backtracks += 1
                continue    # if not satisfactory: test next option
        else: return False    # if all options are unsatisfactory: branch up             

    else:
        print('Invalid version format, try: "-Sn" ')

def SAT_Solver(version, sudoku, p=0, n_sudoku=0, save_results=False):
    clauses = []

    # read rules file
    with open(sudoku,'r') as f:
        lines = f.read().splitlines()
    lines.pop(0)


    # convert to clauses
    for line in lines:
        var_ids = line.split(' ')
        clauses.append([int(x) for x in var_ids if x != '0'])
    
    # Tautology rule
    for i, clause in enumerate(clauses):
        for literal in clause:
            for j in range(len(clause)):
                if clause[j] == -literal:
                    clauses.pop(i)

    clauses, solution = simplify(clauses)

    if len(clauses) == 0:
        print_sudoku(solution)
        # write to results file
        if save_results == True:
            df = pd.DataFrame({'n_sudoku': [n_sudoku], 'calls': [0], 'algorithm': [version]})
            df.to_csv('data.csv', mode='a', index=False, header=False)
        return 'sat'

    if DPLL(clauses, solution=solution, version=version, p=p, n_sudoku=n_sudoku, save_results=save_results) == True: return 'sat'
    else: return 'unsat'
    

if __name__ == '__main__':
    start = time.time()

    # use command line arguments as input
    try:
        version = sys.argv[1]
        sudoku = sys.argv[2]
    except:
        # create a file with the sudoku rules
        shutil.copy('SAT resources/sudoku-rules-9x9.txt','sudoku.txt')
        
        # convert givens to DIMACS
        input = '...5.1....9....8...6.......4.1..........7..9........3.8.....1.5...2..4.....36....'
        cells = [*input]
        givens = []
        size = math.sqrt(len(cells))
        for i, cell in enumerate(cells):
            if cell.isdigit()==True:
                row = math.ceil((i+1)/size)
                column = i%size+1
                digit = int(cell)
                givens.append(row*100 + column*10 + digit)    
        
        # write the givens to the sudoku file in DIMACS format
        with open('sudoku.txt', 'a') as f: 
            for given in givens:
                f.write(str(int(given)) + ' 0\n')

        version = "-S1"
        sudoku = 'sudoku.txt'


    print(SAT_Solver(version, sudoku, p=0, save_results=False)) 
    end = time.time()
    print(f"execution of sudoku solver took {end-start} seconds")
