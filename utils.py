from constant import *
import re

def get_original_data():
    return open(ORIGINAL_HOST_FILE_PATH, "r").read()

def join_path(*kw):
    return "\\".join([str(i) for i in kw])

def pad(variable, length, to_last = False):
    variable = str(variable)
    if length > len(variable):
        return variable
    return (length-len(variable)) * int(to_last) * "0" + variable + (length-len(variable)) * int(not to_last) * "0"

def write_init_file(name, length):
    with open(join_path(CATEGORY_DIR_PATH, name, INIT_FILE), "w") as file:
        file.write(length)
    return SUCCESS
 
def get_init_file(name):
    return int(open(join_path(CATEGORY_DIR_PATH, name, INIT_FILE)).read())

def get_unique_elements(array, _array):
    return [i for i in array if i not in _array]


def join_if_not_ip_address(array, value):
    pattern = re.compile(IP_ADDRESS_REGULAR_EXPRESSION)
    joint_array = "\n" + LOCALHOST_2 + ' '
    joint_array += 'www.' if pattern.match(array[0]) else ''
    for element in array:
        if not pattern.match(element):
            joint_array += 'www.'
        joint_array += element + value
    return joint_array