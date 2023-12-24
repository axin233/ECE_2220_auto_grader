# ECE_2220_auto_grader
Being tired of checking students' C programs? This Python program will save your lives! The Python program supports
1. Automatically organize students' solutions downloaded from Canvas.
2. Automatically generate [MOSS](https://theory.stanford.edu/~aiken/moss/) command for checking plagiarism.
3. Automatically compile students' code.
4. Automatically test students' code.
5. (For Project 2,3 and 4) Automatically compare the students' output with the correct output.

Step 1, 3, 4, and 5 generate a CSV report that has the same arrangement. By combining the CSV files into a single spreadsheet, students' final scores are calculated via Excel formula. :hugs:

## Prerequisite
1. A MOSS account. (Here is a great [MOSS tutorial](https://www.youtube.com/watch?v=VT_7Rps0Wdk)!)
2. A CSV file with students' full names. (Please refer to *student_names.csv* in this repository)
3. A virtual environment for running the auto grader program. (I recommend creating a [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) virtual environment and then activate it in VScode. A tutorial is available [here](https://stackoverflow.com/questions/43351596/activating-anaconda-environment-in-vscode))
