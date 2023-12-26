# ECE_2220_auto_grader
Being tired of checking students' C programs? This Python program will save your lives! The Python program supports
1. Automatically organize students' solutions downloaded from Canvas.
2. Automatically generate [MOSS](https://theory.stanford.edu/~aiken/moss/) command for checking plagiarism.
3. Automatically compile students' code.
4. Automatically test students' code.
5. (For Project 1, 2, 3, and 4) Automatically compare students' output with the correct output.

Step 1, 3, and 4 generate a CSV report that has the same arrangement. By combining the CSV files into a single spreadsheet and checking the results of Step 5, students' final scores can then be calculated via Excel formula. :hugs:

## Prerequisite
1. An Apollo account for using the university's Linux workstation. (Please send an Apollo account request to `coes-unixadm@clemson.edu`)
2. A MOSS account. (Here is a great [MOSS tutorial](https://www.youtube.com/watch?v=VT_7Rps0Wdk)!)
3. A CSV file with students' full names. (Please refer to *student_names.csv* in this repository)
4. A virtual environment for running the auto grader program. (I recommend creating a [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) virtual environment and then activating it in VSCode. A tutorial is available [here](https://stackoverflow.com/questions/43351596/activating-anaconda-environment-in-vscode))

## How does it work
Here is an example of using the auto grader program to grade ECE-2220 Project 1.
- Download students' answers from Canvas, and then unzip the file in the directory `canvas_files`.
- Create a directory called `student_answers`.
- (For plagiarism check) In `student_answers`, save the boilerplate file as `/base/lab1.c`
- (For plagiarism check) In `student_answers`, save previous student submissions as `/prev_student_submissions/<student_name>/lab1.c`
- (For plagiarism check) In `student_answers`, create a file called `moss_script.pl` to save the MOSS email content. (Refer to 1:43-4:40 in the [MOSS tutorial](https://www.youtube.com/watch?v=VT_7Rps0Wdk))

Now, it is time to use the auto grader program. Line 21-24 in `grading_assist.py` has 4 boolean variables. This flowchart demonstrates how to use those boolean variables.

<!--
![flowchart](https://github.com/axin233/ECE_2220_auto_grader/assets/59490151/7ccad1a6-cf6a-4825-a9b7-ac6d93b86d4e)
-->

<p align="center">
  <img width="1080" height="340" src="https://github.com/axin233/ECE_2220_auto_grader/assets/59490151/e73f8f9e-28c6-45e6-b175-beb80e5bee03">
</p>

> Fig. 1. Instructions for using the auto grader program.

For the output files
- *moss_command.txt* contains the instructions for plagiarism check. To check plagiarism, first navigate to `student_answers` directory via the terminal, and then paste the instructions to the terminal. After hitting `Enter`, a URL will returned. The plagiarism report can be accessed by pasting the URL to a web browser. (Refer to 7:35-13:08 in the [MOSS tutorial](https://www.youtube.com/watch?v=VT_7Rps0Wdk))
- *report_submission.csv* shows if a student has submissions in Column `Num_submission` and if it is submitted late in Column `Late_submissionmission`.
- *log_compile.txt* contains warnings and errors when compiling each student's code.
- *report_compile.csv* shows the results of compiling students' code. In Column `Compile_deduction`, 0, -3, and -100 denote 'no warnings or errors', 'has warnings', and 'has errors', respectively.
- *input_log.txt* contains the results of testing a student's code with *test_input*.
- *report_test_input.csv* has a column `Run_finished` to show if a student's code can process *test_input*.
- *input_compare.csv* shows students' answers in Column `Student_answers`, and shows the correct answers in Column `Target_answers`. **(Since students might have their own output format, the auto grader program might fail to detect their answers. It is recommended to manually check the student's *input_log.txt* if he/she fails to get full credits.)**

## Known problems
- Project 5 (i.e., Shell I/O) cannot be processed by the auto grader program, as each student has two submitted files. Also, the students' executable files need to be re-started after running a single test example.
- Project 6 (i.e., Parent and child process) requires manually testing students' programs, as the instantaneous program output determines the next program input.
- When comparing students' answers with the correct answers, the comparison results (i.e., `input_compare.csv` in Fig. 1) are in each student's directory. Thus, it is still required to check the comparison results per student.
- If there are other problems, please feel free to email me at jianxig@g.clemson.edu :sunglasses:
