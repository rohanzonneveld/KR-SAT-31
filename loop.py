from SAT import *

with open('SAT resources/top91.sdk.txt','r') as f:
    sudokus = f.readlines()

for sudoku in sudokus:
    print(SAT_Solver('SAT resources/sudoku-rules-9x9.txt', sudoku.replace("\n",""), "S0"))