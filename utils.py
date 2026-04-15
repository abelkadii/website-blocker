from random import randint
from datetime import datetime
from tkinter import *
import threading
from utils import *
from time import sleep
import json
import os
import shutil
from constant import *
from tkinter.messagebox import showinfo
from schedule import Schedule
from category import Category
from website import Website
from core import Core

def get_original_data():
    return open(ORIGINAL_HOST_FILE_PATH, 'r').read()

def join_path(*kw):
    return '\\'.join([str(i) for i in kw])

def pad(variable, length, to_last = False):
    variable = str(variable)
    if length > len(variable):
        return variable
    return (length-len(variable)) * int(to_last) * '0' + variable + (length-len(variable)) * int(not to_last) * '0'

def write_init_file(name, length):
    open(join_path(CATEGORY_DIR_PATH, name, INIT_FILE), 'w').write(length)
    return SUCCESS
 
def get_init_file(name):
    return int(open(join_path(CATEGORY_DIR_PATH, name, INIT_FILE)).read())

def get_unique_elements(array, _array):
    return [i for i in array if i not in _array]