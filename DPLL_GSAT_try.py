import sys
import math
from collections import Counter
import random
def isSatisfied(clause, literals):
        for value in clause:
            if value in literals:
                return True
            else:
                return False
    # Checks if the current assignment satisfies all clauses
def isComplete(clauses, assignment):
        for clause in clauses:
            if not isSatisfied(clause, assignment):
                return False
        return True
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
    
    if DPLL(clauses, digit) == True: return 'sat'
    else: return 'unsat'
    
def DPLL(clauses, P, trues=[]):
    # add P to true literals
    if P not in trues: trues.append(P)

    # sort clauses on length
    clauses = sorted(clauses, key = lambda l: len(l))
    print(clauses)
    print()
    
    # remove clauses containing literal P and shorten clauses containing -P
    true_idx = []
    for i, clause in enumerate(clauses):
        if P in clause:
            true_idx.append(i)
        if -P in clause:
            clauses[i].pop(clause.index(-P))
    for index in sorted(true_idx, reverse=True):
        clauses.pop(index)   

    # no clauses
    if len(clauses) == 0:
        return True

    # empty clause
    for clause in clauses:
        if len(clause)==0: 
            del trues[-1]
            return False 

    # choose P in clauses
    
    # either:

    # unit clause
    if len(clauses[0]) == 1:
        DPLL(clauses, clauses[0][0], trues)
        
    # or:

    # split (DLCS) TODO implement GSAT
    
    # concatenate all literals
    all_literals=[]
    for clause in clauses:
        all_literals+=clause

    # sort by DLCS
    scores = Counter(all_literals)
    CP_CN = max(sorted(scores), key=lambda symbol: scores[symbol] + scores[-symbol])

    if DPLL(clauses, CP_CN, trues) == True: 
        print([x for x in trues if x>0])
        return True 
    else: DPLL(clauses, -CP_CN, trues) 
def GSAT(clauses,max_tries,max_flips,literals):
    for counter in range (max_tries):
        for i, clause in enumerate(clauses):
            for x in clause:
                if x in literals:
                    #nothing
                    True
                else:
                    rand = random.random()
                    if rand<0.5:
                        literals.append(x)
                    else:
                        literals.append(-x)
        flip_index_list=[]
        frequencies=[]
        for index, z in enumerate(literals):
            for y, clause in enumerate(clauses):
                for lits in clause:
                    if z==lits:
                        frequencies[index]+=1
        for counter2 in range (max_flips):
            if isComplete(clauses,literals):
                return True
            else:
                #change the variable which is the most frequent
                literals[frequencies.index(max(frequencies))]*=-1
                flip_index_list.append(frequencies.index(max(frequencies)))
                frequencies[frequencies.index(max(frequencies))]=0
                #question: when we make a flip and cannot find the solution, should we reverse  
                #this flip and then have another flip or go on by having another flip without reversing the old flip?
    return False

if __name__ == '__main__':
    print(SAT_Solver()) 
    # TODO access true literals
    # TODO unsat? 