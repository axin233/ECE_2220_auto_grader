"""
Project 2 is to encode a 3 letter Ascii string using Hamming(29.24)
    		as well as decode and correct the error of hex input following 
  			Hamminh(29,24).
"""

import os

def pp2_auto_grader(list_student_name, dict_student_obj, test_file_name, output_dir):

    # Get the file name of test output
    split_test_file_name=test_file_name.split('.')
    student_output_name=split_test_file_name[0].split('_')[-1]+'_log.txt'
    # The file saving the comparison result
    output_csv_name=split_test_file_name[0].split('_')[-1]+'_compare.csv'

    # Correct answers
    list_target_bits=['00110', '00000', '00111', '10011', \
                      '10101', '00000', '10111', '00011', \
                      '00000', '00000', '00101', '00001', \
                      '11111', '00000', '11010', '00110', \
                      '00000', '00000', '10000', '01000', '11111']
    list_target_word=['0x0E8A549C', '0x745543 (CUt)', '0x745543 (CUt)', '0x745543 (CUt)', \
                      '0x09088619', '0x484062 (b@H)', '0x484062 (b@H)', '0x484062 (b@H)', \
                      '0x08080404', '0x404041 (A@@)', '0x404041 (A@@)', '0x404041 (A@@)', \
                      '0x0FA7F7EB', '0x7D3F7C (|?})', '0x7D3F7C (|?})', '0x7D3F7C (|?})', \
                      '0x0BEF6560', '0x5F7E5C (\~_)', '0x5F7E5C (\~_)', '0x5F7E5C (\~_)', '0x5F725C (\\r_)']

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
        str_student_parity_bit, str_student_err_bit='', ''
        idx=0
        with open(student_output_dir, 'r') as fp, open(output_csv_dir, 'w') as out_p:
            out_p.write('Student_bits,Target_bits,Correctness,Student_word,Target_word,Correctness\n')

            for line_number, line in enumerate(fp):
                # After checking all outputs, break the loop
                if idx>=len(list_target_bits):
                    print('Finished. Student: ', single_student_name)
                    break

                # Ignore the top 5 lines
                if line_number>5:
                    #
                    split_line=line.split(':')

                    # Find out the parity bit
                    if 'P' in split_line[0]:
                        str_student_parity_bit+=split_line[-1].strip()
                    # Find out the error location bit
                    if 'E' in split_line[0]:
                        str_student_err_bit+=split_line[-1].strip()
                    # When meeting 'Codeword' or 'Information Word', clear the two strings
                    if ('Codeword' in split_line[0]) or ('Information Word' in split_line[0]):
                        str_student_final_answer=split_line[-1].strip()

                        # Compare and then save results 
                        # (bits)
                        if str_student_parity_bit !='':
                            if str_student_parity_bit==list_target_bits[idx]:
                                out_p.write(f'\'{str_student_parity_bit},\'{list_target_bits[idx]},1,')
                            else:
                                out_p.write(f'\'{str_student_parity_bit},\'{list_target_bits[idx]},0,')
                        else:
                            if str_student_err_bit==list_target_bits[idx]:
                                out_p.write(f'\'{str_student_err_bit},\'{list_target_bits[idx]},1,')
                            else:
                                out_p.write(f'\'{str_student_err_bit},\'{list_target_bits[idx]},0,')
                        # (Words)
                        if str_student_final_answer==list_target_word[idx]:
                            out_p.write(f'{str_student_final_answer},{list_target_word[idx]},1\n')
                        else:
                            out_p.write(f'{str_student_final_answer},{list_target_word[idx]},0\n')

                        # Clear content
                        str_student_parity_bit, str_student_err_bit='', ''
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
#     test_file_name='test_input.txt'
#     output_dir='/users/jianxig/ece2220/pp2/student_answers/'
#     list_student_name=['Chris Ashley', 'David T Bootle', 'Adam Brooks Whitestone'] 
#     dict_student_obj={}

#     for single_student_name in list_student_name:
#         dict_student_obj[single_student_name]=student_class()
#         split_single_name=single_student_name.split(' ')
#         dict_student_obj[single_student_name].actual_name='_'.join(split_single_name)

#     #
#     pp2_auto_grader(list_student_name, dict_student_obj, test_file_name, output_dir)