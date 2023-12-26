# -*- coding: utf-8 -*-
"""
This file includes the 4 boolean variables for controling the auto grader program
"""

import pandas as pd
import os
import subprocess
import shlex
import signal
import time
from threading import Timer
from utils_assist import organize_downloaded_canvas_files, compile_files, generate_moss_command, test_code
from pp1 import pp1_auto_grader

class student_class:
    actual_name=''
    canvas_name=''
    num_submission=0
    bool_late_submissionmission=False
    bool_incorrect_c_file_name=False
    compiled_deduction=0


if __name__=='__main__':
    BOOL_ORGANIZE_CANVAS_FILES=False
    BOOL_COMPILE_FILES=False
    BOOL_TEST=False
    BOOL_GRADE=True
    student_name_csv_dir='/users/jianxig/ece2220/extra/student_names.csv'
    canvas_file_dir='/users/jianxig/ece2220/pp1/canvas_files/' # Dir for unzipped students' answers
    output_dir='/users/jianxig/ece2220/pp1/student_answers/' 
    test_input_dir='/users/jianxig/ece2220/pp1/test_input/' # Dir for test input
    prev_student_submission_dir = output_dir+'prev_student_submissions/'
    boilerplate_dir='base/lab1.c'
    test_file_name='test_input'
    extra_input_dir=''#Note: It is only for pp4, as pp4 requires two input files
    c_file_name='lab1.c'
    moss_file_name='moss_command.txt'

    # Get student actual names
    df_student_name=pd.read_csv(student_name_csv_dir, sep='\s*,\s*', header=[0], engine='python')
    list_student_name=df_student_name['Name'].tolist()# This method does not work occasionally
    #list_student_name=df_student_name.iloc[:,0].tolist()# 'Name' is the first column in csv file

    # Create a dictionary of student objects
    dict_student_obj={}
    for single_name in list_student_name:
        dict_student_obj[single_name]=student_class()

        # Get student names listed in the downloaded Canvas files
        # First, M, Last -> Last, First, M
        split_single_name=single_name.split(' ')
        str_First_Middle=''.join(split_single_name[0:-1])
        single_name_modified=split_single_name[-1]+str_First_Middle
        single_name_lower=single_name_modified.lower()# Make all letters lowercase
        dict_student_obj[single_name].actual_name='_'.join(split_single_name)
        dict_student_obj[single_name].canvas_name=single_name_lower

    # For spliting Canvas files to differnt folders. Also, it generates the moss command
    if BOOL_ORGANIZE_CANVAS_FILES:
        organize_downloaded_canvas_files(canvas_file_dir, output_dir, dict_student_obj, \
                                         list_student_name, c_file_name)
        generate_moss_command(output_dir, dict_student_obj, list_student_name, \
                              moss_file_name, c_file_name, boilerplate_dir, \
                              prev_student_submission_dir)

    # For compiling students' programs
    if BOOL_COMPILE_FILES:
        compile_files(output_dir, dict_student_obj, list_student_name, c_file_name)

    # For test students' programs
    if BOOL_TEST:
        test_code(test_input_dir, test_file_name, output_dir, dict_student_obj, list_student_name, \
                  c_file_name, extra_input_dir)

    # For grading students' programs
    if BOOL_GRADE:
        pp1_auto_grader(list_student_name, dict_student_obj, test_file_name, output_dir)
