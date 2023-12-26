"""
This file includes the functions used by grading_assist.py
"""

import os
import subprocess
import time
from threading import Timer

# For spliting Canvas files to differnt folders.
def organize_downloaded_canvas_files(canvas_file_dir, output_dir, dict_student_obj, \
                                     list_student_name, c_file_name):

    # Iterate the downloaded Canvas files
    list_canvas_file_name=os.listdir(canvas_file_dir)
    for single_name in list_canvas_file_name:
        # Note: split_canvas_file_name[0] is a student name in (Last, First, M),
        # split_canvas_file_name[1] will be 'LATE' if there is a late submission
        # split_canvas_file_name[-1] is a file name
        split_canvas_file_name=single_name.split('_')

        # Find out which student submitted the file, then create a dir for the file
        for single_student_obj in dict_student_obj.values():
            if split_canvas_file_name[0]==single_student_obj.canvas_name:

                # Record the number of submission
                single_student_obj.num_submission+=1

                # Check if the student's c file name is correct 
                # (Case 1: If a student has only one submission, and the c file name is incorrect) 
                if single_student_obj.num_submission==1 and split_canvas_file_name[-1]!=c_file_name:
                    single_student_obj.bool_incorrect_c_file_name=True
                # (Case 2: If a student has multiple submissions, and at least one of the c file name is correct)
                if single_student_obj.num_submission>1 and split_canvas_file_name[-1]==c_file_name:
                    single_student_obj.bool_incorrect_c_file_name=False

                # 
                output_dir_single_student = output_dir+single_student_obj.actual_name+'/'
                # If the dir does not exist, create the dir and move the file to that dir
                if os.path.exists(output_dir_single_student) == False:
                    os.makedirs(output_dir_single_student)
                    os.rename(canvas_file_dir+single_name, output_dir_single_student+c_file_name)
                else: # If the dir exists, it indicates the student submitted multiple files
                    c_file_name_split=c_file_name.split('.')
                    output_file_name=output_dir_single_student+c_file_name_split[0]+'_'+\
                        str(single_student_obj.num_submission)+'.c'
                    os.rename(canvas_file_dir+single_name, output_file_name)
                
                # Check late submission
                if split_canvas_file_name[1]=='LATE':
                    single_student_obj.bool_late_submissionmission=True

    # Generate a report
    output_csv_name=output_dir+'report_submission.csv'
    output_csv=open(output_csv_name, 'w')
    output_csv.write('Name,Wrong_c_file_name,Num_submission,Late_submissionmission\n')
    for single_student_name in list_student_name:
        output_csv.write('{},{},{},{}\n'.format(single_student_name, \
                    int(dict_student_obj[single_student_name].bool_incorrect_c_file_name), \
                    dict_student_obj[single_student_name].num_submission, \
                    int(dict_student_obj[single_student_name].bool_late_submissionmission)))
    output_csv.close()

    return

# Generate moss command
def generate_moss_command(output_dir, dict_student_obj, list_student_name, moss_file_name, \
                          c_file_name, boilerplate_dir, prev_student_submission_dir):

    # File for saving the moss command
    moss_file_txt=open(output_dir+moss_file_name, 'w')
    moss_file_txt.write('perl moss_script.pl -l c -d -b ' + boilerplate_dir + ' ')
    for single_name in list_student_name:
        if dict_student_obj[single_name].num_submission>0:
            c_file_dir=output_dir+dict_student_obj[single_name].actual_name+'/'+c_file_name
            # Check if a student have submitted a c file
            if os.path.exists(c_file_dir):
                moss_file_txt.write(dict_student_obj[single_name].actual_name+'/' + c_file_name + ' ')
            else:
                print('Error from generate_moss_command()! c file does not exist.')

    # If there are previous students' submissions, add the submissions at the end
    # The file MUST be origanized in this format: /<prev_student_submission_dir>/<student_name>/<c_file_name>.c
    if os.path.exists(prev_student_submission_dir):
        list_prev_student_dir = os.listdir(prev_student_submission_dir)
        for single_name in list_prev_student_dir:
            # Check if the c file exists 
            if os.path.exists(prev_student_submission_dir + single_name + '/' + c_file_name):
                dir_split=prev_student_submission_dir.split('/')
                moss_file_txt.write(dir_split[-2] + '/' + single_name+'/' + c_file_name  + ' ')
            else:
                print('Error from generate_moss_command()! Previous students c file does not exist.')

    moss_file_txt.close()

    # Sanity check
    if not os.path.exists(output_dir+'moss_script.pl'):
        print('Error from generate_moss_command()! Fail to find moss_script.pl at ')
        print(output_dir)
    elif not os.path.exists(output_dir+boilerplate_dir):
        print('Error from generate_moss_command()! Fail to find the boilerplate code at ')
        print(output_dir+boilerplate_dir)
    else:
        print('moss_command.txt has been generated.')
        print('Ready to check plagiarism.')

    return


# Compile student's code
def compile_files(output_dir, dict_student_obj, list_student_name, c_file_name):
    exe_name=c_file_name.split('.')[0]
    compile_txt_name='log_compile.txt'
    
    #
    for single_student_name in list_student_name:
        c_file_dir=output_dir+dict_student_obj[single_student_name].actual_name\
            +'/'+c_file_name
        exe_dir=output_dir+dict_student_obj[single_student_name].actual_name\
            +'/'+exe_name
        compile_txt_dir=output_dir+dict_student_obj[single_student_name].actual_name\
            +'/'+compile_txt_name
        
        # Check if a student has submissions
        if os.path.exists(c_file_dir):

            # Compile students' code
            with open(compile_txt_dir, 'w') as compile_txt:
                subprocess.call(['gcc', '-Wall', '-g', c_file_dir, '-o', exe_dir], stderr=compile_txt)

            # Check if there is any warnings or error when compiling the code
            # If there are warning or errors, set compile_dicuction to -3
            if os.stat(compile_txt_dir).st_size!=0:
                dict_student_obj[single_student_name].compiled_deduction=-3
        # If no submission, set compile_diduction to -100
        else:
            dict_student_obj[single_student_name].compiled_deduction=-100

    # Generate a report
    output_csv_name=output_dir+'report_compile.csv'
    output_csv=open(output_csv_name, 'w')
    output_csv.write('Name,Compile_deduction\n')
    for single_student_name in list_student_name:
        output_csv.write('{},{}\n'.format(single_student_name, \
                    int(dict_student_obj[single_student_name].compiled_deduction)))
    output_csv.close()

    return


# Test student's code
# Note: MAX_RUN_TIME: The max running time for a student's code (unit: second)
def test_code(test_input_dir, test_file_name, output_dir, dict_student_obj, \
              list_student_name, c_file_name, extra_input_dir, MAX_RUN_TIME=5):
    exe_name=c_file_name.split('.')[0]
    test_file_dir=test_input_dir+test_file_name
    split_test_file_name=test_file_name.split('.')
    output_txt_name=split_test_file_name[0].split('_')[-1]+'_log.txt'

    # Generate reports
    output_csv_name=output_dir+'report_test_'+split_test_file_name[0].split('_')[-1]+'.csv'
    output_csv=open(output_csv_name, 'w')
    output_csv.write('Name,Have_exe,proc_klled,Run_finished\n')

    # 
    for single_student_name in list_student_name:
        student_dir=output_dir+dict_student_obj[single_student_name].actual_name+'/'
        exe_file_dir=output_dir+dict_student_obj[single_student_name].actual_name\
            +'/'+exe_name
        output_txt_dir=output_dir+dict_student_obj[single_student_name].actual_name\
            +'/'+output_txt_name

        # Check if a student has an executable
        if os.path.exists(exe_file_dir):

            # Program start time
            start_time=time.time()

            # (Version 4) Use time-out and avoid bash cammand
            # The code is from: 
            # https://stackoverflow.com/questions/1191374/using-module-subprocess-with-timeout
            with open(test_file_dir) as input_f, open(output_txt_dir, 'w') as output_f:
                if extra_input_dir=='':
                    proc = subprocess.Popen([exe_file_dir], stdin=input_f, stdout=output_f, stderr=subprocess.PIPE)
                else:
                    proc = subprocess.Popen([exe_file_dir, extra_input_dir], stdin=input_f, stdout=output_f, stderr=subprocess.PIPE)
                timer = Timer(MAX_RUN_TIME, proc.kill)
                try:
                    timer.start()
                    stderr = proc.communicate()
                finally:
                    timer.cancel()

            # Program end time
            end_time=time.time()

            # Record info to the report
            if (end_time-start_time)>=MAX_RUN_TIME:
                print('-----------------------')
                print(f'*** {single_student_name} ***: Program is killed')
                print('-----------------------')
                output_csv.write('{},{},{},{}\n'.format(single_student_name, 'Yes', 'Yes',0)) 
            else:
                print(f'{single_student_name}: Finished')
                output_csv.write('{},{},{},{}\n'.format(single_student_name, 'Yes', 'No', 1)) 
        # Record info to the report if no exe file
        else:
            print('-----------------------')
            print(f'*** {single_student_name} ***: No exe')
            print('-----------------------')
            output_csv.write('{},{},{},{}\n'.format(single_student_name, 'No', -1, 0))

    output_csv.close()
    return


# # (Deprecated) Test student's code
# # Note: MAX_RUN_TIME: The max running time for a student's code (unit: second)
# def test_code(test_input_dir, test_file_name, output_dir, dict_student_obj, \
#               list_student_name, c_file_name, MAX_RUN_TIME=5):
#     exe_name=c_file_name.split('.')[0]
#     test_file_dir=test_input_dir+test_file_name
#     split_test_file_name=test_file_name.split('.')
#     output_txt_name=split_test_file_name[0].split('_')[-1]+'_log.txt'

#     # Generate reports
#     output_csv_name=output_dir+'report_test_'+split_test_file_name[0].split('_')[-1]+'.csv'
#     output_csv=open(output_csv_name, 'w')
#     output_csv.write('Name,Have_exe,proc_klled,Run_finished\n')

#     # 
#     for single_student_name in list_student_name:
#         student_dir=output_dir+dict_student_obj[single_student_name].actual_name+'/'
#         exe_file_dir=output_dir+dict_student_obj[single_student_name].actual_name\
#             +'/'+exe_name
#         output_txt_dir=output_dir+dict_student_obj[single_student_name].actual_name\
#             +'/'+output_txt_name

#         # Check if a student has an executable
#         if os.path.exists(exe_file_dir):

#             # Program start time
#             start_time=time.time()

#             # (Version 4) Use time-out and avoid bash cammand
#             # The code is from: 
#             # https://stackoverflow.com/questions/1191374/using-module-subprocess-with-timeout
#             with open(test_file_dir) as input_f, open(output_txt_dir, 'w') as output_f:
#                 proc = subprocess.Popen([exe_file_dir], stdin=input_f, stdout=output_f, stderr=subprocess.PIPE)
#                 timer = Timer(MAX_RUN_TIME, proc.kill)
#                 try:
#                     timer.start()
#                     stderr = proc.communicate()
#                 finally:
#                     timer.cancel()

#             # Program end time
#             end_time=time.time()

#             # Record info to the report
#             if (end_time-start_time)>=MAX_RUN_TIME:
#                 print('-----------------------')
#                 print(f'*** {single_student_name} ***: Program is killed')
#                 print('-----------------------')
#                 output_csv.write('{},{},{},{}\n'.format(single_student_name, 'Yes', 'Yes',0)) 
#             else:
#                 print(f'{single_student_name}: Finished')
#                 output_csv.write('{},{},{},{}\n'.format(single_student_name, 'Yes', 'No', 1)) 
#         # Record info to the report if no exe file
#         else:
#             print('-----------------------')
#             print(f'*** {single_student_name} ***: No exe')
#             print('-----------------------')
#             output_csv.write('{},{},{},{}\n'.format(single_student_name, 'No', -1, 0))

#     output_csv.close()
#     return
