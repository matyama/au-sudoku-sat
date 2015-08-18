Sudoku SAT Solver
=================
General sudoku solver that uses SAT formulation and MiniSat solver. 
Lab project for Automatic Reasoning (A4M33AU) course.

Execution:
----------
- $ python3 sudoku.py -i [input_file] -n [size]
- e.g. $ python3 sudoku.py -i sudoku.in -n 9
- both input file and size are optional parameters
- if the input file is not specified, the sudoku is unconstrained
- if the size is not specified, default size of 9 is assumed

Input file format:
------------------
- specifies constraints on the sudoku, i.e. default cell values
- line record format: [row] [column] [value]
- see *sudoku.in* as an example

Requirements:
-------------
- python3
- [MiniSat](http://minisat.se)