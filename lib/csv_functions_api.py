'''
my module csv_functions.py
include import csv_functions in you code
call the functions in your code like csv_functions.write_string()
'''

''' write string to a csv text file '''
def write_string(string_to_write, action):
    
    f = open("temp_log.txt", action)
    f.write(string_to_write)
    #print("csv string " + string_to_write)
    f.close()

''' write lines to a csv text file '''
''' for some reason this causes an error '''
def write_lines(lines_to_write, action):

    f = open("temp_log.txt", action)
    f.writelines(lines_to_write)
    #print("csv lines " + lines_to_write)
    f.close()
