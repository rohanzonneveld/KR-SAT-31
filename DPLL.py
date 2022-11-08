import sys
import math

def SAT_Solver():
    clauses = []
    digits = []

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
            return 'sat'

        # empty clause
        for clause in clauses:
            if len(clause)==0:
                return 'unsat' 

        # unit clause
        if len(clauses[0]) == 1:
            literal = clauses[0][0]
            if literal not in digits:
                digits.append(literal)
            true_idx = []
            for i, clause in enumerate(clauses):
                if literal in clause:
                    true_idx.append(i)
            for index in sorted(true_idx, reverse=True):
                del clauses[index]

        # split
        # TODO implement split

        # sort clauses again
        clauses = sorted(clauses, key = lambda l: len(l))

        # finished?
        if len(digits)==size**2:
            return digits
        
        break
        
if __name__ == '__main__':
    print(SAT_Solver())