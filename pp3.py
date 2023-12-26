"""
The propose of Project 3 is:
Upon the user entering two strings with all values mapped to
a finite field array, with an operation symbol separating the two,
the output will be calculated from the finite field values then
converted back to a string. The input does not need to be to the leftmost
of the terminal either, but this function only supports one command
per line.
"""

import os

def pp3_auto_grader(list_student_name, dict_student_obj, test_file_name, output_dir):

    # Get the file name of test output
    split_test_file_name=test_file_name.split('.')
    student_output_name=split_test_file_name[0].split('_')[-1]+'_log.txt'
    # The file saving the comparison result
    output_csv_name=split_test_file_name[0].split('_')[-1]+'_compare.csv'

    # Correct answers
    list_target_word=['\'abc\' + \'bbc\' => \'bce\'',\
                      '\'tuvwx\' + \'CBAzy\' => \'aaaaa\'',\
                      '\'orange\' + \'white\' => \'KyiGkE\'',\
                      '\'abcqH\' * \'AUydkzAB\' => \'aUbbbZab\'',\
                      '\'yyyyyyyyyyyy\' * \'abcdefghijkl\' => \'aybzcAdBeCfD\'',\
                      '\'abcqHU\' / \'Aabdk\' => \'aacviu\'',\
                      '\'bbbbb\' / \'ABCDU\' => \'MhQnU\'',\
                      '\'yyyyyy\' ^ \'abcdef\' => \'bymgdz\'',\
                      '\'bird\' / \'tiger\' => \'fbQKR\'',\
                      '\'emu\' ^ \'zebra\' => \'qjuRA\'']

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
        num_correct_answers=0
        with open(student_output_dir, 'r') as fp, open(output_csv_dir, 'w') as out_p:
            out_p.write('Student_answers,Target_answers,Correctness\n')

            for line_number, line in enumerate(fp):
                # After checking all outputs, break the loop
                if idx>=len(list_target_word):
                    print('Finished. Student: ', single_student_name)
                    break

                # Ignore the top 6 lines
                if line_number>6:
                    
                    # Ignore the line with #. It denotes the line is the comment
                    if ('#' not in line) and ('=>' in line):

                        # Compare and then save results
                        student_single_answer=line[2:-1]# Ignore the leading '> ' and the tailing '\n'
                        if student_single_answer==list_target_word[idx]:
                            out_p.write(f'{student_single_answer},{list_target_word[idx]},1\n')
                            num_correct_answers+=1
                        else:
                            out_p.write(f'{student_single_answer},{list_target_word[idx]},0\n')

                        # Update parameters
                        idx+=1

            # write the number of correct answers
            out_p.write(f'Number of correct answer: {num_correct_answers}\n')

    return

# class student_class:
#     actual_name=''
#     canvas_name=''
#     num_submission=0
#     bool_late_submissionmission=False
#     bool_incorrect_c_file_name=False
#     compiled_deduction=0
    

# if __name__=='__main__':
#     test_file_name='test_input.txt'
#     output_dir='/users/jianxig/ece2220/pp3/student_answers/'
#     list_student_name=['David T Bootle', 'Shana Lynn Batchelor', 'Adam Brooks Whitestone'] 
#     dict_student_obj={}

#     for single_student_name in list_student_name:
#         dict_student_obj[single_student_name]=student_class()
#         split_single_name=single_student_name.split(' ')
#         dict_student_obj[single_student_name].actual_name='_'.join(split_single_name)

#     #
#     pp3_auto_grader(list_student_name, dict_student_obj, test_file_name, output_dir)