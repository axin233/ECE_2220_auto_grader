"""
Project 1 is for a cybersecurity protection system to find the threat level and count the likely incursion.
"""

import os

def pp1_auto_grader(list_student_name, dict_student_obj, test_file_name, output_dir):

    # Get the file name of test output
    split_test_file_name=test_file_name.split('.')
    student_output_name=split_test_file_name[0].split('_')[-1]+'_log.txt'
    # The file saving the comparison result
    output_csv_name=split_test_file_name[0].split('_')[-1]+'_compare.csv'

    # Correct answers
    list_target_answers=['Threat detected with level 5 and appears 3 times',
                      'Threat detected with level 10 and appears 3 times',
                      'No threat detected',
                      'Threat detected with level 5 and appears 4 times',
                      'No threat detected']

    # Compare the student's output with the correct output
    for single_student_name in list_student_name:
        student_output_dir=output_dir+dict_student_obj[single_student_name].actual_name+'/'+student_output_name
        output_csv_dir=output_dir+dict_student_obj[single_student_name].actual_name+'/'+output_csv_name

        # If the student does not have an output file, go to the next student
        if os.path.exists(student_output_dir)==False:
            print('-----------------------------')
            print('No output.txt. Student: ', single_student_name)
            print('-----------------------------')
            continue

        # Open the student's output file
        idx=0
        with open(student_output_dir, 'r') as fp, open(output_csv_dir, 'w') as out_p:
            out_p.write('Student_answers,Target_answers,Correctness\n')

            for line_number, line in enumerate(fp):

                # Remove the newline character
                line=line[:-1]

                # Check if key words appears in the current line
                if ('Threat detected' in line) or ('No threat detected' in line):

                    # Compare and then save results
                    if line == list_target_answers[idx]:
                        out_p.write(f'{line},{list_target_answers[idx]},1\n')
                    else:
                        out_p.write(f'{line},{list_target_answers[idx]},0\n')

                    # Update parameters
                    idx+=1

    return

# class student_class:
#     actual_name=''
#     canvas_name=''
#     num_submission=0
#     bool_late_submissionmission=False
#     bool_incorrect_c_file_name=False
#     compiled_deduction=0
    

# if __name__=='__main__':
#     test_file_name='test_input'
#     output_dir='/users/jianxig/ece2220/pp1/student_answers/'
#     list_student_name=['Chris Ashley', 'Aarav Sujit Rekhi', 'David T Bootle', 'Adam Brooks Whitestone'] 
#     dict_student_obj={}

#     for single_student_name in list_student_name:
#         dict_student_obj[single_student_name]=student_class()
#         split_single_name=single_student_name.split(' ')
#         dict_student_obj[single_student_name].actual_name='_'.join(split_single_name)

#     #
#     pp2_auto_grader(list_student_name, dict_student_obj, test_file_name, output_dir)