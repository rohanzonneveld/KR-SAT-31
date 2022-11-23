from DPLL import *
import os

with open('SAT resources/top91.sdk.txt','r') as f:
    lines = f.readlines()

os.chdir(os.get_exec_path)

for line in lines:
    os.system("/Users/rohanzonneveld/Documents/Artificial\ Intelligence/Knowledge\ Representation/KR-SAT-31/DPLL.py")
            # "SAT resources/sudoku-rules-9x9.txt"
            # str(line))
