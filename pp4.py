"""
Project 4 is to design A simple packet sniffer that can handle packets with non-printable
characters. The sniffer can find any byte, string, or web address 
in any packet.
"""

import os
import subprocess
import time
from threading import Timer

# Note: For pp4, students' answers are checked by Meld, which supports comparing two files side by side.

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


# class student_class:
#     actual_name=''
#     canvas_name=''
#     num_submission=0
#     bool_late_submissionmission=False
#     bool_incorrect_c_file_name=False
#     compiled_deduction=0
    

# if __name__=='__main__':
#     test_file_name='mp4testcommands'
#     output_dir='/users/jianxig/ece2220/pp4/student_answers/'
#     test_input_dir='/users/jianxig/ece2220/pp4/test_input/'
#     extra_input_dir=test_input_dir+'mp4testinput'
#     c_file_name='lab4.c'
#     list_student_name=['David T Bootle', 'Adam Brooks Whitestone'] #'Chris Ashley',
#     dict_student_obj={}

#     for single_student_name in list_student_name:
#         dict_student_obj[single_student_name]=student_class()
#         split_single_name=single_student_name.split(' ')
#         dict_student_obj[single_student_name].actual_name='_'.join(split_single_name)

#     #
#     test_code(test_input_dir, test_file_name, output_dir, dict_student_obj, \
#               list_student_name, c_file_name, extra_input_dir)