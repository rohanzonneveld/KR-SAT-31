import sys
import math
from collections import Counter

def SAT_Solver():
    clauses = []
    digits = []
    deleted_clauses = []

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
            digits.append(int(literal))
    
    clauses = sorted(clauses, key = lambda l: len(l))
    # start DPLL

    # Tautology rule
    for i, clause in enumerate(clauses):
        for literal in clause:
            for j in range(len(clause)):
                if clause[j] == -literal:
                    clauses.pop(i)
    while True:
        # no clauses
        if len(clauses) == 0:
            return 'sat', digits

        # empty clause
        for clause in clauses:
            if len(clause)==0:
                return 'unsat' 

        # unit clause
        while True:
            if len(clauses[0]) == 1:
                literal = clauses[0][0]
                if literal not in digits:
                    digits.append(literal)
                true_idx = []
                for i, clause in enumerate(clauses):
                    if literal in clause:
                        true_idx.append(i)
                for index in sorted(true_idx, reverse=True):
                    deleted_clauses.append(clauses.pop(index))
            else:
                break

        # split (DLCS)
        # TODO implement split GSAT
      
        # concatenate all literals
        all_clauses=[]
        for clause in clauses:
            all_clauses+=clause

        # sort by DLCS
        scores = Counter(all_clauses)
        CP_CN = sorted(sorted(scores), key=lambda symbol: scores[symbol] + scores[-symbol])

        # set next truth value to literal 
        v = 0 # TODO adjust
        literal = CP_CN[v]
        if scores[abs(literal)] >= scores[-abs(literal)]:
            clauses.append([abs(literal)])
        else:
            clauses.append([-abs(literal)])

        # sort clauses again
        clauses = sorted(clauses, key = lambda l: len(l))

        # finished?
        if len(digits)==size**2:
            return digits
        
        
        
if __name__ == '__main__':
    print(SAT_Solver())