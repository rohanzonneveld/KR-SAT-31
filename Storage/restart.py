import sys
import math
from collections import Counter
import copy

def remove_unit_clauses(clauses):
    
    # find all unit clauses
    
    unit_clauses = []
    for clause in clauses:
        if len(clause)==1:
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
    
    return clauses, unit_clauses

def is_satisfiable(clauses):    
    # no clauses
    if len(clauses) == 0:
        return True
    
    # empty clause
    for clause in clauses:
        if len(clause)==0: 
            return False 
    return None


def solve(clauses, solution):

    if is_satisfiable(clauses) != None:
        return is_satisfiable(clauses), solution

    # pick a literal (DLCS)
    all_literals=[]
    for clause in clauses:
        all_literals+=clause

    print(all_literals)
    # sort by DLCS
    scores = Counter(all_literals)
    CP_CN = max(sorted(scores), key=lambda symbol: scores[symbol] + scores[-symbol])

    clauses.append([CP_CN])
    new_clauses = remove_unit_clauses(clauses)
    new_solution = copy.deepcopy(solution)
    new_solution.append(CP_CN)


    result = solve(new_clauses, new_solution)
    if result[0]:
        return result

    # backbranch
    clauses.append([-CP_CN])
    new_clauses = remove_unit_clauses(clauses)
    new_solution = copy.deepcopy(solution)
    new_solution.append(-CP_CN)

    new_clauses, removed_literals = remove_unit_clauses(new_clauses)
    new_solution.extend(removed_literals)

    return solve(new_clauses, new_solution)

def DPLL(clauses):
    
    if is_satisfiable(clauses) != None:
        return is_satisfiable(clauses)
    
    clauses, unit_clauses = remove_unit_clauses(clauses)


    return solve(clauses, unit_clauses)    
    
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
    
    if DPLL(clauses) == True: return 'sat'
    else: return 'unsat'



   
if __name__ == '__main__':
    print(SAT_Solver()) 
    # TODO access true literals
    # TODO unsat? 