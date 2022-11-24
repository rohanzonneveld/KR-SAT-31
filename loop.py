from SAT import *
import time
import pandas as pd

# read database of sudokus into file
with open('SAT resources/top2365.sdk.txt','r') as f:
    sudokus = f.readlines()

# create empty csv file to store data
# df = pd.DataFrame({'n_sudoku': [None], 'calls': [None], 'backtracks': [None], 'algorithm': [None]})
# df.to_csv('data.csv', index=False)

start = time.time()

for n_sudoku, sudoku in enumerate(sudokus):
    # create a file with the sudoku rules
    shutil.copy('SAT resources/sudoku-rules-9x9.txt','sudoku.txt')

    # convert givens to DIMACS
    cells = [*sudoku.replace("\n","")]
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

    SAT_Solver("-S2", 'sudoku.txt', p=0.2, n_sudoku=n_sudoku, save_results=True)

end = time.time()
print(f"Execution of all {len(sudokus)} sudokus took {end-start} seconds")