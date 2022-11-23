import sys
import math
from collections import Counter
import random
import pdb
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
    
    if GSAT(clauses, 500,500,[])[0] == True:
        #print(GSAT(clauses, 100,100,[])[1]) 
        return 'sat'
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
        literals=[] #this list includes the true variables
        processed_literals=[] #to understand which values we assign a true or false
        for clause in (clauses):
            for x in clause:
                if abs(x) not in processed_literals: #check if a variable is assigned with true or false before
                    processed_literals.append(abs(x)) 
                    rand = random.random()
                    if rand<0.5:
                        literals.append(abs(x))
                    else:
                        literals.append((-1)*abs(x)) #assigning false means negating in our solution

        for counter2 in range (max_flips):
            if isComplete(clauses,literals):#function which checks sat or unsat for the all case, look at top to see the func
                print([lit for lit in literals if lit>0])               
                return True,[lit for lit in literals if lit>0]
            else:
                frequencies=[0]*len(literals) #creating a frequency list, important to flip the most frequent one at each flip in terms of unsatisfied clauses
                for index, z in enumerate(literals):
                    for y, clause in enumerate(clauses): 
                        if isSatisfied(clause,literals)==False:
                            for lits in clause:
                                if z==lits or ((-1)*z)==lits:
                                    frequencies[index]+=1 
                rand2=random.random()
                if rand2<0.7:
                    literals[frequencies.index(max(frequencies))]*=-1  #change the variable which is the most frequent
                else:
                    new_rand=random.randint(0,63)
                    literals[new_rand]*=-1
    return False, [liter for liter in literals if liter>0]
if __name__ == '__main__':
    print(SAT_Solver()) 
    # TODO access true literals
    # TODO unsat?
    # 
def H_Number_Based(sudoku_sentence,total_row_or_col_num,digit): # for a specific digit, it checks if there is any cell that we can put directly that digit on to that cell!
    row=0
    empty_cells=[]
    already_eliminated=[]
    for i in range(sudoku_sentence): #sentence we write at command prompt to define sudoku
        if i%total_row_or_col_num==0:
            row+=1
        column=((i-(row-1)*total_row_or_col_num))
        if i==".":
            empty_cells.append(str(row)+str(column))
    candidate_cells=[] 
    for cell in empty_cells:
        if cell not in already_eliminated:
            is_candidate=True
            shuffle=[]#it will include the row and column info of the cell
            shuffle.append(cell[0])
            shuffle.append(cell[1])
            counter=0
            for unit in shuffle:
                counter+=1
                if counter==1:
                    for x in range(total_row_or_col_num):
                        compare=sudoku_sentence[x+((unit-1)*total_row_or_col_num)]#picking the other cells in the same row
                else:
                    for y in range(total_row_or_col_num):
                        compare=sudoku_sentence[y*total_row_or_col_num+unit-1]#picking the other cells in the same column
                if digit == compare:
                    is_candidate=False
                    already_eliminated.append(cell)
                    break
        if is_candidate:
            candidate_cells.add(cell)
    if len(candidate_cells)==1:
        sudoku_sentence[(candidate_cells[0]-1)*total_row_or_col_num+candidate_cells[1]]=digit
    return sudoku_sentence
    #This heuristic should run for many times because lets say there is 2 cell in one row or column both got the chance to have 2 and 5.
    #Probably in next scans for different row and columns this dilemma will be solved and if we scan the same row or column next time,
    #heuristic will have clear idea which number will be assigned to which cell rather then the previous scan.
    
