from collections import Counter
import math
 
def number_strategy(solution):
    # mimics human behavior by producing a list of possible places to place a digit in the most restricted column/row

    # returns False if digit already in unit
    # returns list of possible cells where digit can be placed in unit
    
    # select most restricted not filled row or column as unit
    filled_rows = [str(x)[0] for x in solution if x>0]
    filled_cols = [str(x)[1] for x in solution if x>0]

    for i in range(1,10):
        row = list(Counter(filled_rows).most_common(i)[-1])
        col = list(Counter(filled_cols).most_common(i)[-1])
        a= row[1] == 9
        b= col[1] == 9
        if a ^ b:
            row[1] = 0 if row[1]==9 else row[1]
            col[1] = 0 if col[1]==9 else col[1]
            break
        elif row[1] == 9 & col[1]==9:
            continue
        else:
            break

    if row[1] > col[1]:
        idx = [i for i, x in enumerate(solution) if str(math.trunc(x / 100)) == row[0]]
        unit = [solution[i] for i in idx if solution[i]>0]
        choice = 1
    elif col[1] > row[1]:
        idx = [i for i, x in enumerate(solution) if str(math.trunc((x%100)/10)) == col[0]]
        unit = [solution[i] for i in idx if solution[i]>0]
        choice = 2
    else:
        idx = [i for i, x in enumerate(solution) if str(math.trunc(x / 100)) == row[0]]
        unit = [solution[i] for i in idx if solution[i]>0]   
        choice = 1 

    # create ordered list of most placed digits in current solution
    digits = [elem%10 for elem in solution if elem>0]
    order = Counter(digits).most_common(9)
    if len(order) != 9: # not all digits present in current sudoku, so add them to posibilities
        for number in range(1,10):
            for elem in order:
                if number != elem[0]:
                    pass
                else:
                    break
            else:
                order.append((number,0))

    # create list of placed digits in unit
    placed = [elem%10 for elem in unit]

    # get the most frequent digit not in unit
    for digit in order:
        if digit[0] in placed: # if digit already in row/column: test next digit
            continue
        else:
            digit = digit[0]
            break 
            
    # identify filled cells in unit
    filled = [math.trunc(elem/10) for elem in unit]

    # return possible cells for digit
    output = []
    if choice == 1:
        row = int(row[0])*100
        column=10
        for _ in range(9):
            cell = (row+column)/10
            if cell not in filled:
                output.append(row+column+digit)
            column+=10
    else:
        row = 100
        column = int(col[0])*10
        for _ in range(9):
            cell = (row+column)/10
            if cell not in filled:
                output.append(row+column+digit)
            row+=100

    return output


def cell_strategy(solution):
    # find all empty cells
    all_cells=[]
    for r in range(1,10):
        for c in range(1,10):
            all_cells.append(10*r + c)

    filled = [math.trunc(elem/10) for elem in solution if elem>0]

    # find first empty cell
    for cell in all_cells:
        if cell not in filled:
            empty = cell
            break

    # find possibilities for first empty cell
    restricts = []
    for i, x in enumerate(solution):
        if math.ceil(x/10) == -empty:
            restricts.append(-solution[i]%10)
    
    possibles = []
    for i in range(1,10):
        if i not in restricts:
            possibles.append(empty*10+i)

    return possibles            


if __name__ == '__main__':
    solution = [111, 126, 158,
                237, 289, 292, 248,
                -131, -136, -138]
    print(cell_strategy(solution))
