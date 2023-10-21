from datetime import datetime
from time import sleep
from tkinter import *
from tkinter.messagebox import showinfo
import threading
import json
import os
import shutil
import re

# constant -FILE

SCHEDULE_DIR_PATH = "data\schedule"
CATEGORY_DIR_PATH = "data\category"
ORIGINAL_HOST_FILE_PATH = "data\original"
STATUS_FILE_PATH = "data\__status__"
HOST_FILE_PATH = "c:\Windows\System32\Drivers\etc\hosts"
INIT_FILE = "__init__"
LOCALHOST_1 = "127.0.0.1"
LOCALHOST_2 = "0.0.0.0"

ALREADY_EXSISTS = "ALREADY_EXSISTS"
SUCCESS = "SUCCESS"
DOES_NOT_EXSIST = "DOES_NOT_EXSIST"
CHANGE = "CHANGE"
STOPED = "STOPED"
BLOCKING = "BLOCKING"
DISABLED = "DISABLED"
STARTING = "START"
ENDING = "END"
LOAD_ALL = "load all"

SCHEDULE_TIME_FORMAT = "%H:%M:%S"
IP_ADDRESS_REGULAR_EXPRESSION = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"

# utlis -FILE

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

# schedule -FILE

class Schedule:
    def __init__(self, name):
        self.name = name
        self.durations = None
        self.categories = None
        self.websites = None
    
    def create(name, durations, categories=[], websites=[]):
        if os.path.exists(join_path(SCHEDULE_DIR_PATH, name)):
            return ALREADY_EXSISTS
        write_file = open(join_path(SCHEDULE_DIR_PATH, name), "w")

        schedule = {
            "name": name,
            "durations": durations,
            "categories": categories,
            "websites": websites
        }
        write_file.write(json.dumps(schedule, indent=4))
        write_file.close()
        return Schedule(name)

    def destroy(self):
        os.remove(join_path(SCHEDULE_DIR_PATH, self.name))
        return SUCCESS

    def load(self):
        self._get()
        return SUCCESS


    def _get(self):
        read_file = open(join_path(SCHEDULE_DIR_PATH, self.name), "r")
        file_data = json.load(read_file)
        self.websites = file_data.get("websites")
        self.categories = file_data.get("categories")
        self.durations = file_data.get("durations")
        

    def is_active(self):
        current = datetime.now().time()
        if self.durations == None:
            self.load()
        schedule = self.durations
        for duration in schedule:
            start_time = datetime.strptime(duration[0], SCHEDULE_TIME_FORMAT).time()
            end_time = datetime.strptime(duration[1], SCHEDULE_TIME_FORMAT).time()
            if end_time > current > start_time:
                return True

    def add_category_to_schedule(self, category_name):
        read_file = open(join_path(SCHEDULE_DIR_PATH, self.name), "r")
        file_data = json.load(read_file)
        file_data.get("categories").append(category_name)
        if self.categories == None:
            self.load()
        self.categories.append(category_name)
        write_file = open(join_path(SCHEDULE_DIR_PATH, self.name), "w")
        json.dump(file_data, write_file, indent=4)
        return SUCCESS
    
    def add_website_to_schedule(self, website_name):
        read_file = open(join_path(SCHEDULE_DIR_PATH, self.name), "r")
        file_data = json.load(read_file)
        file_data.get("websites").append(website_name)
        if self.categories == None:
            self.load()
        self.categories.append(website_name)
        write_file = open(join_path(SCHEDULE_DIR_PATH, self.name), "w")
        json.dump(file_data, write_file, indent=4)
        return SUCCESS
    
    def delete_category_from_schedule(self, category_name):
        read_file = open(join_path(SCHEDULE_DIR_PATH, self.name), "r")
        file_data = json.load(read_file)
        file_data.get("categories").remove(category_name)
        if self.categories == None:
            self.load()
        self.categories.remove(category_name)
        write_file = open(join_path(SCHEDULE_DIR_PATH, self.name), "w")
        json.dump(file_data, write_file, indent=4)
        return SUCCESS
    
    def delete_website_from_schedule(self, website_name):
        read_file = open(join_path(SCHEDULE_DIR_PATH, self.name), "r")
        file_data = json.load(read_file)
        file_data.get("websites").remove(website_name)
        if self.websites == None:
            self.load()
        self.websites.remove(website_name)
        write_file = open(join_path(SCHEDULE_DIR_PATH, self.name), "w")
        json.dump(file_data, write_file, indent=4)
        return SUCCESS

    def edit(self, durations, new_name):
        if os.path.exists(join_path(SCHEDULE_DIR_PATH, new_name)):
            return ALREADY_EXSISTS
        read_file = open(join_path(SCHEDULE_DIR_PATH, self.name), "r")
        file_data = json.load(read_file)
        file_data["durations"] = durations
        file_data["name"] = new_name
        write_file = open(join_path(SCHEDULE_DIR_PATH, new_name), "w")
        json.dump(file_data, write_file, indent=4)
        write_file.close()
        self.name = new_name
        os.remove(join_path(SCHEDULE_DIR_PATH, self.name))
        return SUCCESS

    def get_schedules_for_category(category):
        schedules = []
        for schedule in os.listdir(SCHEDULE_DIR_PATH):
            read_file = json.load(open(join_path(SCHEDULE_DIR_PATH, schedule), "r"))
            if category in read_file.get("categories"):
                schedules.append(schedule)
        return schedules
    
    def get_schedules_for_website(website):
        schedules = []
        for schedule in os.listdir(SCHEDULE_DIR_PATH):
            read_file = json.load(open(join_path(SCHEDULE_DIR_PATH, schedule), "r"))
            if website in read_file.get("websites"):
                schedules.append(schedule)
        return schedules

    def is_category_active(category):
        return any(Schedule(schedule).is_active() for schedule in Schedule.get_schedules_for_category())
    
    def is_website_active(category):
        return any(Schedule(schedule).is_active() for schedule in Schedule.get_schedules_for_website())
    
    def update_category_name_in_schedule(category, new_name):
        for schedule in Schedule.get_schedules_for_category(category):
            schedule_object = Schedule(schedule)
            schedule_object.delete_category_from_schedule(category)
            schedule_object.add_category_to_schedule(new_name)
        return SUCCESS

    def get_all():
        return os.listdir(SCHEDULE_DIR_PATH)


# category -FILE

class Category:
    def __init__(self, name):
        self.name = name
        self.schedules = self._get_schedules()
        self.websites = []
        self.length = None
        self.part = 1
        self.loaded = False
    
    def create(name, length, schedules=[], websites=[]):
        path = join_path(CATEGORY_DIR_PATH, name)
        if os.path.exists(path):
            return ALREADY_EXSISTS
        os.mkdir(path)
        for schedule in schedules:
            shedule_object = Schedule(schedule)
            shedule_object.add_category_to_schedule(name)
        category = Category(name)
        category.length = length
        category._write_websites(websites)
        write_init_file(name, str(length))
        return category

    def destroy(self):
        schedules = Schedule.get_schedules_for_category(self.name)
        for schedule in schedules:
            Schedule(schedule).delete_category_from_schedule(self.name)
        shutil.rmtree(join_path(CATEGORY_DIR_PATH, self.name), ignore_errors=True)
        return SUCCESS

    def rename(self, new_name):
        if os.path.exists(join_path(CATEGORY_DIR_PATH, new_name)):
            return ALREADY_EXSISTS
        os.rename(join_path(CATEGORY_DIR_PATH, self.name), join_path(CATEGORY_DIR_PATH, new_name))
        self.name = new_name
        Schedule.update_category_name_in_schedule(self.name, new_name)
        self.name = new_name
        return SUCCESS

    def is_active(self):
        return Schedule.is_category_active(self.name)

    def add_category_to_schedule(self, schedule_name):
        return Schedule(schedule_name).add_category_to_schedule(self.name)
        
    
    def add_website_to_category(self, website_name):
        data = self.websites if self.loaded else self._load_all_websites()
        if website_name in data:
            return ALREADY_EXSISTS
        data.append(website_name)
        if self.websites: self.websites.append(website_name)
        self._write_websites()
        return SUCCESS
    
    def delete_website_from_category(self, website_name):
        data = self.websites if self.loaded else self._load_all_websites()
        if website_name not in data:
            return DOES_NOT_EXSIST
        # data.remove(website_name)
        if self.websites: self.websites.remove(website_name)
        self._write_websites()
        return self.websites
    
    def freeze_website_from_category(self, website_name):
        data = self.websites if self.loaded else self._load_all_websites()
        if website_name not in data:
            return DOES_NOT_EXSIST
        index = data.index(website_name)
        data[index] = website_name + "[frozen]"
        if self.websites: self.websites[index] = website_name + "[frozen]"
        self._write_websites()
        return SUCCESS
    
    def unfreeze_website_from_category(self, website_name):
        data = self.websites if self.loaded else self._load_all_websites()
        if website_name not in data:
            return DOES_NOT_EXSIST
        index = data.index(website_name)
        data[index] = website_name[:-8]
        if self.websites: self.websites[index] = website_name[:-8]
        self._write_websites()
        return SUCCESS

    def _get_schedules(self):
        return Schedule.get_schedules_for_category(self.name)
    
    def _load_all_websites(self):
        data = []
        for file_name in os.listdir(join_path(CATEGORY_DIR_PATH, self.name)):
            if file_name != "__init__":
                data += open(join_path(CATEGORY_DIR_PATH, self.name, file_name), "r").read().split()
        self.websites = data
        self.length = get_init_file(self.name)
        self.loaded = True
        return data

    def get_all():
        return os.listdir(CATEGORY_DIR_PATH)

    def _write_websites(self, websites=None):
        websites = websites or self.websites
        path = join_path(CATEGORY_DIR_PATH, self.name)
        for i in range(((_len := len(websites))//self.length)+1):
            padded_name = pad(i+1, len(str(len(websites)//self.length))+1)
            write_file = open(join_path(path, padded_name), "w")
            start = self.length*i
            end = self.length*(i+1) if self.length*(i+1) < _len-1 else _len -1
            write_file.write("\n".join(websites[start:end]))
            write_file.close()
        return SUCCESS
    
    def _load_part_websites(self):
        if len(os.listdir(join_path(CATEGORY_DIR_PATH, self.name)))>1:
            length = len(str(len(os.listdir(join_path(CATEGORY_DIR_PATH, self.name)))))
            data = open(join_path(CATEGORY_DIR_PATH, self.name, pad(self.part, length)), "r").read().split("\n")
            self.websites = self.websites if self.loaded else self.websites + data
            self.part += 1
        return self.websites


# website -FILE

class Website:
    def __init__(self, url):
        self.url = url
        self.schedules = self._get_schedules()
    
    def create(name, schedules=[]):
        for schedule in schedules:
            shedule_object = Schedule(schedule)
            shedule_object.add_website_to_schedule(name)
        return Website(name)

    def destroy(self):
        for schedule in self.schedules:    
            shedule_object = Schedule(schedule)
            shedule_object.delete_website_from_schedule(self.url)
        return SUCCESS

    def is_active(self):
        return Schedule.is_website_active(self.name)

    def add_website_to_schedule(self, schedule_name):
        return Schedule(schedule_name).add_website_to_schedule(self.name)
    
    def delete_website_from_schedule(self, schedule_name):
        return Schedule(schedule_name).delete_website_from_schedule(self.name)

    def _get_schedules(self):
        return Schedule.get_schedules_for_website(self.name)


# display -FILE

class _ListBox:
    def __init__(self, root, values, mode, height, width, position_x, position_y, pad, xspan, yspan, onClick=lambda self: None, default=None, link=None):
        self.root = root
        self.values = values
        self.mode = mode
        self.height = height
        self.width = width
        self.position_x = position_x
        self.position_y = position_y
        self.pad = pad
        self.xspan = xspan
        self.yspan = yspan
        self.value = default
        self.link = link
        self.bind_component = []

        def _onclick(e):
            try:
                if self.mode==SINGLE:
                    value = self.listbox.get(self.listbox.curselection()[0])
                    self.value = value
                elif self.mode==MULTIPLE:
                    value = [self.listbox.get(i) for i in self.listbox.curselection()]
                    self.value = value
            except:
                pass
            onClick(self)
        
        self.onClick = _onclick
    
    def create(self):
        categories_var = StringVar(value=tuple(self.values))
        self.listbox = Listbox(self.root, listvariable=categories_var, height=self.height, selectmode=self.mode, width=self.width)
        scrollbar = Scrollbar(self.root, orient="vertical", command=self.listbox.yview)
        self.listbox["yscrollcommand"] = scrollbar.set
        self.listbox.grid(column=self.position_x, row=self.position_y, sticky="nwes", pady=(self.pad[0], self.pad[2]), padx=(self.pad[3], 0), columnspan=self.xspan, rowspan=self.yspan)
        scrollbar.grid(column=self.position_x+self.xspan, row=self.position_y, sticky="ns", padx=(0, self.pad[1]), pady=(self.pad[0], self.pad[2]), rowspan=self.yspan)
        self.listbox.bind("<<ListboxSelect>>", lambda event: self.onClick(self))
    
    def destroy(self):
        self.listbox.destroy()
    
    def update_value(self, value):
        self.values = value
        categories_var = StringVar(value=tuple(self.values))
        self.listbox.configure(listvariable=categories_var)
    
    def _update_link(self, link):
        self.link = link
        return SUCCESS

    def _bind(self, display_component):
        length = len(self.bind_component)
        self.bind_component.append(display_component)
        return length

class _Label:
    def __init__(self, root, value, position_x, position_y, pad, xspan):
        self.root = root
        self.value = value
        self.position_x = position_x
        self.position_y = position_y
        self.pad = pad
        self.xspan = xspan
        self.bind_component = []

    def create(self):
        self.label = Label(self.root, text=self.value)
        self.label.grid(column=self.position_x, row=self.position_y, sticky="nwes", pady=(self.pad[0], self.pad[2]), padx=(self.pad[1], self.pad[3]), columnspan=self.xspan)
    
    def destroy(self):
        self.label.destroy()
    
    def update_value(self, value):
        self.value = value
        self.label.configure(text=value)

class _Button:
    def __init__(self, root, text, position_x, position_y, height, width, pad, onClick, xspan=1):
        self.root = root
        self.text = text
        self.position_x = position_x
        self.position_y = position_y
        self.height = height
        self.width = width
        self.pad = pad
        self.xspan = xspan
        self.bind_component = []
        self.onClick = onClick

    def create(self):
        self.button = Button(self.root, text=self.text, command=lambda: self.onClick(self), height=self.height, width=self.width)
        self.button.grid(column=self.position_x, row=self.position_y, sticky="nwes", pady=(self.pad[0], self.pad[2]), padx=(self.pad[1], self.pad[3]), columnspan=self.xspan)
    
    def destroy(self):
        self.button.destroy()
    
    def update_text(self, text):
        self.text = text
        self.button.configure(text=text)

    


class _Entry:
    def __init__(self, root, position_x, position_y, pad, border_width, xspan, default=""):
        self.root = root
        self.position_x = position_x
        self.position_y = position_y
        self.pad = pad
        self.border_width = border_width
        self.xspan = xspan
        self.default = default
        self.bind_component = []

    def create(self):
        self.entry = Entry(self.root, borderwidth=self.border_width)
        self.entry.insert(0, self.default)
        self.entry.grid(column=self.position_x, row=self.position_y, sticky="nwes", pady=(self.pad[0], self.pad[2]), padx=(self.pad[1], self.pad[3]), columnspan=self.xspan)
    
    def destroy(self):
        self.entry.destroy()
    
    def get_value(self):
        return self.entry.get()
    
    def clear_value(self):
        return self.entry.delete(0, END)


class TimePicker:
    def __init__(self, frame, row, _default="00:00:00", default_="23:59:59"):
        self.frame = frame
        self.row = row
        self.is_destroyed = False
        self._default = _default
        self.default_ = default_
        
    def create(self):

        def destroy_button():
            self._label.destroy()
            self._hour.destroy()
            self._minute.destroy()
            self._second.destroy()
            self.label_.destroy()
            self.hour_.destroy()
            self.minute_.destroy()
            self.second_.destroy()
            self.destroy_button.destroy()
            self.is_destroyed = True

        self._hourstr= StringVar(self.frame, self._default.split(":")[0])
        self._minutestr= StringVar(self.frame, self._default.split(":")[1])
        self._secondstr= StringVar(self.frame, self._default.split(":")[2])
        
        self.hourstr_= StringVar(self.frame, self.default_.split(":")[0])
        self.minutestr_= StringVar(self.frame, self.default_.split(":")[1])
        self.secondstr_= StringVar(self.frame, self.default_.split(":")[2])

        self._hour = Spinbox(self.frame,from_=0,to=23,wrap=True,textvariable=self._hourstr,width=2,state="readonly")
        self._minute = Spinbox(self.frame,from_=0,to=59,wrap=True,textvariable=self._minutestr,width=2,state="readonly")
        self._second = Spinbox(self.frame,from_=0,to=59,wrap=True,textvariable=self._secondstr,width=2,state="readonly")
        self.label_ = Label(self.frame, text="to: ")
        
        self.hour_ = Spinbox(self.frame,from_=0,to=23,wrap=True,textvariable=self.hourstr_,width=2,state="readonly")
        self.minute_ = Spinbox(self.frame,from_=0,to=59,wrap=True,textvariable=self.minutestr_,width=2,state="readonly")
        self.second_ = Spinbox(self.frame,from_=0,to=59,wrap=True,textvariable=self.secondstr_,width=2,state="readonly")
        self._label = Label(self.frame, text="from: ")

        self.destroy_button = Button(self.frame, text="-", command=destroy_button)


        self._label.grid(column=0, row=self.row, padx=5, pady=5)
        self._hour.grid(column=1, row=self.row, padx=5, pady=5)
        self._minute.grid(column=2, row=self.row, padx=5, pady=5)
        self._second.grid(column=3, row=self.row, padx=5, pady=5)
        
        self.label_.grid(column=4, row=self.row, padx=5, pady=5)
        self.hour_.grid(column=5, row=self.row, padx=5, pady=5)
        self.minute_.grid(column=6, row=self.row, padx=5, pady=5)
        self.second_.grid(column=7, row=self.row, padx=5, pady=5)
        self.destroy_button.grid(column=8, row=self.row, padx=15, pady=5)

    def get_value(self):
        if ~self.is_destroyed:
            _hour = self._hour.get()
            _minute = self._minute.get()
            _second = self._second.get()

            hour_ = self.hour_.get()
            minute_ = self.minute_.get()
            second_ = self.second_.get()

            return "{}:{}:{}".format(_hour, _minute, _second), "{}:{}:{}".format(hour_, minute_, second_)
        return None, None 


# core -FILE

class Core:
    def _configure(categories, websites):
        def _():
            a = datetime.now()
            configure_data = []
            configure_data += websites
            for category in categories:
                category_object = Category(category)
                configure_data += category_object._load_all_websites()
            a = datetime.now()
            data = get_original_data() + f"\n{LOCALHOST_1} " if len(configure_data)>0 else ""
            data += f"\n{LOCALHOST_1} ".join(configure_data)
            data += join_if_not_ip_address(configure_data, f"\n{LOCALHOST_2} ") if len(configure_data)>0 else ""
            file = open(HOST_FILE_PATH, "w")
            file.write(data)
            file.close()
            return SUCCESS
        threading.Thread(target=_).start()
    def _active():
        schedules = Schedule.get_all()
        categories = []
        websites = []
        active_schedules = []
        for schedule in schedules:
            schedule_object = Schedule(schedule)
            if schedule_object.is_active():
                active_schedules.append(schedule)
                categories += schedule_object.categories
                websites += schedule_object.websites
        return categories, websites, active_schedules

    def _listen(sleep_duration, on_change):
        categories, websites, schedules = Core._active()
        on_change(categories, websites, schedules)
        Core._configure(categories, websites)
        while True:
            if Core._status() == DISABLED:
                on_change([], [], [])
                Core._configure([], [])
                break
            active_categories, active_websites, active_schedules = Core._active()
            if active_categories != categories or active_websites != websites:
                Core._configure(active_categories, active_websites)
            if active_categories != categories or active_websites != websites or active_schedules != schedules:
                on_change(active_categories, active_websites, active_schedules)
            categories, websites, schedules = active_categories, active_websites, active_schedules
            sleep(sleep_duration)
        
    def _start():
        file = open(STATUS_FILE_PATH, "w")
        file.write(BLOCKING)
        file.close()
        return SUCCESS
        
    def _end():
        file = open(STATUS_FILE_PATH, "w")
        file.write(DISABLED)
        file.close()
        return SUCCESS

    def _status():
        file = open(STATUS_FILE_PATH, "r")
        status = file.read()
        file.close()
        return status

root = Tk()
root.title("website blocker")
root.iconbitmap("favicon.ico")
def disable_event():
    Core._end()
    root.destroy()


# main -FILE

root.protocol("WM_DELETE_WINDOW", disable_event)

category_settings = LabelFrame(root, text="category settings", padx=10, pady=10)
category_settings.grid(column=0, row=0, padx=10, pady=10)

schedule_settings = LabelFrame(root, text="schedule settings", padx=10, pady=10)
schedule_settings.grid(column=1, row=0, padx=10, pady=10)

active = LabelFrame(root, text="active", padx=10, pady=10)
active.grid(column=2, row=0, padx=10, pady=10)

schedules = Schedule.get_all()
categories = Category.get_all()

def on_website_click(self):
    if self.value == LOAD_ALL:
        def load():
            category = Category(self.link)
            websites = category._load_all_websites()
            self.update_value(websites)
        thread = threading.Thread(target=load)
        thread.start()

website_frame_label  = _Label(category_settings, "websites", 4, 0, [ 10, 0, 0, 0], 2)
website_frame_label.create()

# --------------------------------------------------------------------------------------------------------------
website_frame = _ListBox(category_settings, [], SINGLE, 17, 30, 4, 1, [10, 10, 5, 10], 2, 2, on_website_click)
website_frame.create()

schedule_frame_label  = _Label(category_settings, "schedules", 4, 4, [0, 0, 0, 0], 2)
schedule_frame_label.create()

# --------------------------------------------------------------------------------------------------------------
schedule_frame = _ListBox(category_settings, [], SINGLE, 5, 30, 4, 5, [0, 10, 5, 0], 2, 3)
schedule_frame.create()


def on_category_select(self):
    def load_part_websites(value):
        new_label = value + " websites"
        website_frame_label.update_value(new_label)
        category = Category(value)
        websites = category._load_part_websites()
        if len(websites)!=0:
            websites.append(LOAD_ALL)
        website_frame._update_link(value)
        website_frame.value = None
        website_frame.update_value(websites)
    
    def load_schedules(value):
        new_label = value + " schedules"
        schedule_frame_label.update_value(new_label)
        category = Category(value)
        schedules = category.schedules
        schedule_frame._update_link(value)
        schedule_frame.value = None
        schedule_frame.update_value(schedules)

    website_thread = threading.Thread(target=lambda: load_part_websites(self.value))
    schedule_thread = threading.Thread(target=lambda: load_schedules(self.value))
    website_thread.start()
    schedule_thread.start()

category_frame_label  = _Label(category_settings, "categories", 0, 0, [ 10, 0, 0, 0], 3)
category_frame_label.create()

def add_website_button_on_click(self):  
    def _():
        if category_frame.value:
            new_window = Toplevel()
            new_window.title("adding")
            new_window_label = _Label(new_window, "website name: ",0, 0, [10, 0, 0, 0], 1)
            new_window_entry = _Entry(new_window, 1, 0, [10, 0, 0, 10], 1, 2)
            
            def cancel(self):
                new_window.destroy()

            def save(self):
                if new_window_entry.get_value() != "":
                    category = Category(category_frame.value)
                    output = category.add_website_to_category(new_window_entry.get_value())
                    if output == SUCCESS:
                        websites = category._load_all_websites()
                        website_frame.update_value(websites)
                    elif output==ALREADY_EXSISTS:
                        showinfo("adding website", "website already exists")
                else:
                    showinfo("adding website", "a name is requiered")
            

            def save_add(self):
                    save(self)
                    new_window_entry.clear_value()
                
            def save_and_exit(self):
                save(self)
                cancel(self)

            new_window_button_save_and_exit = _Button(new_window, "save and exit", 0, 1, 2, 15, [10, 5, 10, 5], save_and_exit)
            new_window_button_save_and_add = _Button(new_window, "save and add", 1, 1, 2, 15, [10, 5, 10, 5], save_add)
            new_window_button_canel = _Button(new_window, "cancel", 2, 1, 2, 15, [10, 5, 10, 5], cancel)
            new_window_label.create()
            new_window_entry.create()
            new_window_button_save_and_exit.create()
            new_window_button_save_and_add.create()
            new_window_button_canel.create()
        else:
            showinfo("add website", "no category selected")
    thread = threading.Thread(target=_)
    thread.start()
        


add_website_button = _Button(category_settings, "add", 4, 3, 1, 1, [10, 5, 10, 5], add_website_button_on_click)
add_website_button.create()

def delete_website_button_on_click(self):
    def _():
        if website_frame.value and category_frame.value:
            category = Category(category_frame.value)
            category.delete_website_from_category(website_frame.value)
            websites = category._load_all_websites()
            website_frame.update_value(websites)
            showinfo("delete website", "website deleted")
        else:
            showinfo("delete website", "no website selected")
    thread = threading.Thread(target=_)
    thread.start()

delete_website_button = _Button(category_settings, "delete", 5, 3, 1, 1, [10, 5, 10, 5], delete_website_button_on_click)
delete_website_button.create()


category_frame = _ListBox(category_settings, categories, SINGLE, 28, 30, 0, 1, [5, 10, 5, 10], 3 , 6, on_category_select)
category_frame.create()


def add_category_button_on_click(self):
    def _():
        new_window = Toplevel()
        new_window.title("adding")
        new_window_label = _Label(new_window, "category name: ",0, 0, [10, 0, 0, 0], 1)
        new_window_entry = _Entry(new_window, 1, 0, [10, 0, 0, 10], 1, 2)
        
        def cancel(self):
            new_window.destroy()

        def save(self):
            if new_window_entry.get_value() != "":
                output = Category.create(new_window_entry.get_value(), 100)
                if output==ALREADY_EXSISTS:
                    showinfo("adding category", "category already exists")
                else:
                    categories = Category.get_all()
                    category_frame.update_value(categories)
            else:
                    showinfo("adding category", "a name is requiered")
        
        def save_add(self):
                save(self)
                new_window_entry.clear_value()
            
        def save_and_exit(self):
            save(self)
            cancel(self)

        new_window_button_save_and_exit = _Button(new_window, "save and exit", 0, 1, 2, 15, [10, 5, 10, 5], save_and_exit)
        new_window_button_save_and_add = _Button(new_window, "save and add", 1, 1, 2, 15, [10, 5, 10, 5], save_add)
        new_window_button_canel = _Button(new_window, "cancel", 2, 1, 2, 15, [10, 5, 10, 5], cancel)
        new_window_label.create()
        new_window_entry.create()
        new_window_button_save_and_exit.create()
        new_window_button_save_and_add.create()
        new_window_button_canel.create()
    thread = threading.Thread(target=_)
    thread.start()

add_category_button = _Button(category_settings, "add", 0, 8, 2, 1, [10, 5, 10, 5], add_category_button_on_click)
add_category_button.create()
 
def delete_category_button_on_click(self):
    def _():
        if category_frame.value:
            category = Category(category_frame.value)
            category.destroy()
            categories = Category.get_all()
            category_frame.update_value(categories)
            website_frame.update_value([])
            schedule_frame.update_value([])

            showinfo("delete category", "category deleted")
        else:
            showinfo("delete category", "no category selected")
    thread = threading.Thread(target=_)
    thread.start()

delete_category_button = _Button(category_settings, "delete", 1, 8, 2, 1, [10, 5, 10, 5], delete_category_button_on_click)
delete_category_button.create()
 
def rename_category_button_on_click(self): 
    def _():
        if category_frame.value:
            new_window = Toplevel()
            new_window.title("rename")
            new_window_label = _Label(new_window, "category name: ",0, 0, [10, 0, 0, 0], 1)
            new_window_entry = _Entry(new_window, 1, 0, [10, 0, 0, 10], 1, 2, category_frame.value)
            
            def cancel(self):
                new_window.destroy()

            def save(self):
                if new_window_entry.get_value() != "":
                    category = Category(category_frame.value)
                    output = category.rename(new_window_entry.get_value())
                    if output == SUCCESS:
                        categories = Category.get_all()
                        category_frame.update_value(categories)
                    elif output==ALREADY_EXSISTS:
                        showinfo("rename category", "category already exists")
                else:
                    showinfo("rename category", "a name is requiered")
            
                
            def save_and_exit(self):
                save(self)
                cancel(self)

            new_window_button_save_and_exit = _Button(new_window, "save", 0, 1, 2, 15, [10, 5, 10, 5], save_and_exit)
            new_window_button_canel = _Button(new_window, "cancel", 2, 1, 2, 15, [10, 5, 10, 5], cancel)
            new_window_label.create()
            new_window_entry.create()
            new_window_button_save_and_exit.create()
            new_window_button_canel.create()
        else:
            showinfo("add website", "no category selected")
    thread = threading.Thread(target=_)
    thread.start()


rename_category_button = _Button(category_settings, "rename", 2, 8, 2, 1, [10, 5, 10, 5], rename_category_button_on_click)
rename_category_button.create()

def add_schedule_button_on_click(self):
    def _():
        if category_frame.value:
            new_window = Toplevel()
            schedules = get_unique_elements(Schedule.get_all(), schedule_frame.values)
            schedule__frame = _ListBox(new_window, schedules, MULTIPLE, 18, 25, 1, 0, [10, 10, 5, 10], 1, 1)
            schedule_frame_label  = _Label(new_window, "choose schedules: ",0 , 0, [ 10, 10, 10, 0], 1)  
            def cancel(self):
                    new_window.destroy()

            def save(self):
                if len(schedule__frame.value)!=0:
                    for i in schedule__frame.value:
                        schedule = Schedule(i)
                        schedule.add_category_to_schedule(category_frame.value)
                    categories = Category.get_all()
                    category_frame.update_value(categories)
                    category_schedules = Schedule.get_schedules_for_category(category_frame.value)
                    schedule_frame.update_value(category_schedules)
                else:
                    showinfo("add schedule", "no schedule selected")
            
            def save_and_exit(self):
                save(self)
                cancel(self)

            new_window_button_save_and_exit = _Button(new_window, "save", 0, 1, 2, 15, [10, 5, 10, 5], save_and_exit)
            new_window_button_canel = _Button(new_window, "cancel", 1, 1, 2, 15, [10, 5, 10, 5], cancel)
            new_window_button_save_and_exit.create()
            new_window_button_canel.create()
            schedule__frame.create()
            schedule_frame_label.create()
    thread = threading.Thread(target=_)
    thread.start()



add_schedule_button = _Button(category_settings, "add", 4, 8, 1, 2, [10, 5, 10, 5], add_schedule_button_on_click)
add_schedule_button.create()

def delete_schedule_button_on_click(self):
    def _():
        if schedule_frame.value:
            schedule = Schedule(schedule_frame.value)
            schedule.delete_category_from_schedule(category_frame.value)
            schedules = Schedule.get_schedules_for_category(category_frame.value)
            schedule_frame.update_value(schedules)
            showinfo("delete schedule", "schedule deleted")
        else:
            showinfo("delete schedule", "no schedule selected")
    thread = threading.Thread(target=_)
    thread.start()

delete_schedule_button = _Button(category_settings, "delete", 5, 8, 1, 2, [ 10, 5, 10, 5], delete_schedule_button_on_click)
delete_schedule_button.create()


# schedule settings


_website_frame_label  = _Label(schedule_settings, "websites", 4, 0, [ 10, 0, 0, 0], 2)
_website_frame_label.create()

# --------------------------------------------------------------------------------------------------------------
_website_frame = _ListBox(schedule_settings, [], SINGLE, 16, 30, 4, 1, [10, 10, 5, 10], 2, 2)
_website_frame.create()

_categorie_frame_label  = _Label(schedule_settings, "categories", 4, 4, [0, 0, 0, 0], 2)
_categorie_frame_label.create()

# --------------------------------------------------------------------------------------------------------------
_categorie_frame = _ListBox(schedule_settings, [], SINGLE, 7, 30, 4, 5, [10, 10, 5, 0], 2, 4)
_categorie_frame.create()

durations_frame = _ListBox(schedule_settings, [], SINGLE, 4, 30, 0, 8, [5, 10, 5, 10], 3 , 2)
durations_frame.create()

def _on_schedule_select(self):
    def load_websites(value):
        new_label = " websites linked to " + value
        _website_frame_label.update_value(new_label)
        schedule = Schedule(value)
        schedule.load()
        websites = schedule.websites
        _website_frame._update_link(value)
        _website_frame.value = None
        _website_frame.update_value(websites)
    
    def _load_categories(value):
        new_label = " categories linked to " + value
        _categorie_frame_label.update_value(new_label)
        schedule = Schedule(value)
        schedule.load()
        categories = schedule.categories
        _categorie_frame._update_link(value)
        _categorie_frame.value = None
        _categorie_frame.update_value(categories)
    
    def _load_durations(value):
        new_label = "durations linked to " + value
        durations_frame_label.update_value(new_label)
        schedule = Schedule(value)
        schedule.load()
        categories = ["from {} to {}".format(duration[0], duration[1]) for duration in schedule.durations]
        durations_frame._update_link(value)
        durations_frame.value = None
        durations_frame.update_value(categories)

    website_thread = threading.Thread(target=lambda: load_websites(self.value))
    schedule_thread = threading.Thread(target=lambda: _load_categories(self.value))
    duraitons_thread = threading.Thread(target=lambda: _load_durations(self.value))
    website_thread.start()
    duraitons_thread.start()
    schedule_thread.start()

_schedule_frame_label  = _Label(schedule_settings, "schedules", 0, 0, [ 10, 0, 0, 0], 3)
_schedule_frame_label.create()

durations_frame_label  = _Label(schedule_settings, "durations", 0, 7, [ 10, 0, 0, 0], 3)
durations_frame_label.create()


def _add_website_button_on_click(self):  
    def _():
        if _schedule_frame.value:
            new_window = Toplevel()
            new_window.title("adding")
            new_window_label = _Label(new_window, "website name: ",0, 0, [10, 0, 0, 0], 1)
            new_window_entry = _Entry(new_window, 1, 0, [10, 0, 0, 10], 1, 2)
            
            def cancel(self):
                new_window.destroy()

            def save(self):
                if new_window_entry.get_value() != "":
                    schedule = Schedule(_schedule_frame.value)
                    output = schedule.add_website_to_schedule(new_window_entry.get_value())
                    if output == SUCCESS:
                        schedule.load()
                        websites = schedule.websites
                        _website_frame.update_value(websites)
                    elif output==ALREADY_EXSISTS:
                        showinfo("adding website", "website already exists")
                else:
                    showinfo("adding website", "a name is requiered")
            

            def save_add(self):
                    save(self)
                    new_window_entry.clear_value()
                
            def save_and_exit(self):
                save(self)
                cancel(self)

            new_window_button_save_and_exit = _Button(new_window, "save and exit", 0, 1, 2, 15, [10, 5, 10, 5], save_and_exit)
            new_window_button_save_and_add = _Button(new_window, "save and add", 1, 1, 2, 15, [10, 5, 10, 5], save_add)
            new_window_button_canel = _Button(new_window, "cancel", 2, 1, 2, 15, [10, 5, 10, 5], cancel)
            new_window_label.create()
            new_window_entry.create()
            new_window_button_save_and_exit.create()
            new_window_button_save_and_add.create()
            new_window_button_canel.create()
        else:
            showinfo("add website", "no schedule selected")
    thread = threading.Thread(target=_)
    thread.start()

add_website_button = _Button(schedule_settings, "add", 4, 3, 1, 1, [10, 5, 10, 5], _add_website_button_on_click)
add_website_button.create()

def _delete_website_button_on_click(self):
    def _():
        if _website_frame.value and _schedule_frame.value:
            schedule = Schedule(_schedule_frame.value)
            schedule.delete_website_from_schedule(_website_frame.value)
            schedule.load()
            websites = schedule.websites
            _website_frame.update_value(websites)
            showinfo("delete website", "website deleted")
        else:
            showinfo("delete website", "no website selected")
    thread = threading.Thread(target=_)
    thread.start()

delete_website_button = _Button(schedule_settings, "delete", 5, 3, 1, 1, [10, 5, 10, 5], _delete_website_button_on_click)
delete_website_button.create()

_schedule_frame = _ListBox(schedule_settings, schedules, SINGLE, 20, 30, 0, 1, [5, 10, 10, 10], 3 , 4, _on_schedule_select)
_schedule_frame.create()





def _add_schedule_button_on_click(self):
    def _():
        new_window = Toplevel()
        new_window.title("adding")
        new_window_label = _Label(new_window, "schedule name: ",0, 0, [10, 0, 0, 0], 1)
        new_window_entry = _Entry(new_window, 1, 0, [10, 0, 0, 10], 1, 2)
        new_window_time_picker_frame = Frame(new_window)
        new_window_time_picker_frame.grid(column=0, row=1, columnspan=3)
        new_window_time_pickers = [TimePicker(new_window_time_picker_frame, 0)]
        new_window_time_pickers[0].create()
        
        def cancel(self):
            new_window.destroy()

        def save(self):
            if new_window_entry.get_value() != "":
                durations = []
                for time_picker in new_window_time_pickers:
                    _start_time, _end_time = time_picker.get_value()
                    if _start_time and _end_time:
                        start_time = datetime.strptime(_start_time, SCHEDULE_TIME_FORMAT)
                        end_time = datetime.strptime(_end_time, SCHEDULE_TIME_FORMAT)
                        if start_time < end_time:
                            durations.append([_start_time, _end_time])

                output = Schedule.create(new_window_entry.get_value(), durations)
                if output==ALREADY_EXSISTS:
                    showinfo("adding schedule", "schedule already exists")
                else:
                    schedules = Schedule.get_all()
                    _schedule_frame.update_value(schedules)
            else:
                    showinfo("adding schedule", "a name is requiered")
        
        def save_add(self):
                save(self)
                new_window_entry.clear_value()
            
        def save_and_exit(self):
            save(self)
            cancel(self)

        new_window_button_save_and_exit = _Button(new_window, "save and exit", 0, 3, 2, 15, [10, 5, 10, 5], save_and_exit)
        new_window_button_save_and_add = _Button(new_window, "save and add", 1, 3, 2, 15, [10, 5, 10, 5], save_add)
        new_window_button_canel = _Button(new_window, "cancel", 2, 3, 2, 15, [10, 5, 10, 5], cancel)
        new_window_button_save_and_exit.create()
        new_window_button_save_and_add.create()
        new_window_button_canel.create()


        def add_new_time_picker(self):
            row = len(new_window_time_pickers)
            time_picker = TimePicker(new_window_time_picker_frame, row)
            time_picker.create()
            new_window_time_pickers.append(time_picker)
            
        
        new_window_button_add_time_picker = _Button(new_window, "+", 1, 2, 2, 15, [10, 5, 10, 5], add_new_time_picker)
        new_window_button_add_time_picker.create()
        new_window_label.create()
        new_window_entry.create()
    thread = threading.Thread(target=_)
    thread.start()

add_category_button = _Button(schedule_settings, "add", 0, 6, 1, 1, [5, 5, 5, 5], _add_schedule_button_on_click)
add_category_button.create()
 
def _delete_schedule_button_on_click(self):
    def _():
        if _schedule_frame.value:
            schedule = Schedule(_schedule_frame.value)
            schedule.destroy()
            schedules = Schedule.get_all()
            _schedule_frame.update_value(schedules)
            _website_frame.update_value([])
            _categorie_frame.update_value([])
            durations_frame.update_value([])

            showinfo("delete schedule", "schedule deleted")
        else:
            showinfo("delete schedule", "no schedule selected")
    thread = threading.Thread(target=_)
    thread.start()

delete_category_button = _Button(schedule_settings, "delete", 1, 6, 1, 1, [5, 5, 5, 5], _delete_schedule_button_on_click)
delete_category_button.create()
 
def edit_category_button_on_click(self): 
    def _():
        if _schedule_frame.value:
            schedule = Schedule(_schedule_frame.value)
            schedule.load()
            new_window = Toplevel()
            new_window.title("adding")
            new_window_label = _Label(new_window, "schedule name: ",0, 0, [10, 0, 0, 0], 1)
            new_window_entry = _Entry(new_window, 1, 0, [10, 0, 0, 10], 1, 2, schedule.name)
            new_window_time_picker_frame = Frame(new_window)
            new_window_time_picker_frame.grid(column=0, row=1, columnspan=3)
            new_window_time_pickers = [TimePicker(new_window_time_picker_frame, 0, i[0], i[1]) for i in schedule.durations]
            [i.create() for i in new_window_time_pickers]
            
            def cancel(self):
                new_window.destroy()

            def save(self):
                if new_window_entry.get_value() != "":
                    durations = []
                    for time_picker in new_window_time_pickers:
                        _start_time, _end_time = time_picker.get_value()
                        if _start_time and _end_time:
                            start_time = datetime.strptime(_start_time, SCHEDULE_TIME_FORMAT)
                            end_time = datetime.strptime(_end_time, SCHEDULE_TIME_FORMAT)
                            if start_time < end_time:
                                durations.append([_start_time, _end_time])

                    schedule.edit(durations, new_window_entry.get_value())
                    schedules = Schedule.get_all()
                    _schedule_frame.update_value(schedules)
                else:
                        showinfo("adding schedule", "a name is requiered")
            
            def save_add(self):
                    save(self)
                    new_window_entry.clear_value()
                
            def save_and_exit(self):
                save(self)
                cancel(self)

            new_window_button_save_and_exit = _Button(new_window, "save and exit", 0, 3, 2, 15, [10, 5, 10, 5], save_and_exit)
            new_window_button_save_and_add = _Button(new_window, "save and add", 1, 3, 2, 15, [10, 5, 10, 5], save_add)
            new_window_button_canel = _Button(new_window, "cancel", 2, 3, 2, 15, [10, 5, 10, 5], cancel)
            new_window_button_save_and_exit.create()
            new_window_button_save_and_add.create()
            new_window_button_canel.create()


            def add_new_time_picker(self):
                row = len(new_window_time_pickers)
                time_picker = TimePicker(new_window_time_picker_frame, row)
                time_picker.create()
                new_window_time_pickers.append(time_picker)
                
            
            new_window_button_add_time_picker = _Button(new_window, "+", 1, 2, 2, 15, [10, 5, 10, 5], add_new_time_picker)
            new_window_button_add_time_picker.create()
            new_window_label.create()
            new_window_entry.create()
    thread = threading.Thread(target=_)
    thread.start()

rename_category_button = _Button(schedule_settings, "edit", 2, 6, 1, 1, [5, 5, 5, 5], edit_category_button_on_click)
rename_category_button.create()

def _add_category_button_on_click(self):
    def _():
        if _schedule_frame.value:
            new_window = Toplevel()
            categories = get_unique_elements(Category.get_all(), _categorie_frame.values)
            category__frame = _ListBox(new_window, categories, MULTIPLE, 18, 25, 1, 0, [10, 10, 5, 10], 1, 1)
            _categorie_frame_label  = _Label(new_window, "choose categories: ",0 , 0, [ 10, 10, 10, 0], 1)  
            def cancel(self):
                    new_window.destroy()

            def save(self):
                if len(category__frame.value)!=0:
                    for i in category__frame.value:
                        category = Category(i)
                        category.add_category_to_schedule(_schedule_frame.value)

                    schedule = Schedule(_schedule_frame.value)
                    schedule.load()
                    categories = schedule.categories
                    _categorie_frame.update_value(categories)
                else:
                    showinfo("add schedule", "no schedule selected")
            
            def save_and_exit(self):
                save(self)
                cancel(self)

            new_window_button_save_and_exit = _Button(new_window, "save", 0, 1, 2, 15, [10, 5, 10, 5], save_and_exit)
            new_window_button_canel = _Button(new_window, "cancel", 1, 1, 2, 15, [10, 5, 10, 5], cancel)
            new_window_button_save_and_exit.create()
            new_window_button_canel.create()
            category__frame.create()
            _categorie_frame_label.create()
    thread = threading.Thread(target=_)
    thread.start()



add_schedule_button = _Button(schedule_settings, "add", 4, 9, 1, 2, [10, 5, 10, 5], _add_category_button_on_click)
add_schedule_button.create()

def _delete_category_button_on_click(self):
    def _():
        if _categorie_frame.value:
            schedule = Schedule(_schedule_frame.value)
            schedule.delete_category_from_schedule(_categorie_frame.value)
            schedule.load()
            schedules = schedule.categories
            _categorie_frame.update_value(schedules)
            showinfo("delete category", "category deleted")
        else:
            showinfo("delete category", "no category selected")
    thread = threading.Thread(target=_)
    thread.start()

delete_schedule_button = _Button(schedule_settings, "delete", 5, 9, 1, 2, [ 10, 5, 10, 5], _delete_category_button_on_click)
delete_schedule_button.create()




# def main():



current_active_categories = _ListBox(active, [], SINGLE, 5, 30, 0, 1, [10, 10, 10, 10], 1, 1)
current_active_schedules = _ListBox(active, [], SINGLE, 5, 30, 0, 3, [10, 10, 10, 10], 1, 1)
current_active_websites = _ListBox(active, [], SINGLE, 5, 30, 0, 5, [10, 10, 10, 10], 1, 1)

current_active_categories_label = _Label(active, "active ategories: ", 0, 0, [10, 10, 10, 30], 2)
current_active_schedules_label = _Label(active, "active schedules: ", 0, 2, [10, 10, 10, 10], 2)
current_active_websites_label = _Label(active, "active websites: ", 0, 4, [10, 10, 10, 10], 2)

current_active_categories_label.create()
current_active_schedules_label.create()
current_active_websites_label.create()

current_active_categories.create()
current_active_schedules.create()
current_active_websites.create()


def block(self):
    if self.text == "block":
        Core._start()
        def on_change(categories, websites, schedules):
            def _():
                current_active_categories.update_value(categories)
                current_active_schedules.update_value(schedules)
                current_active_websites.update_value(websites)
            thread = threading.Thread(target=_)
            thread.start()
            
        thread = threading.Thread(target=lambda: Core._listen(1, on_change))
        thread.start()
        self.update_text("stop")
        
    elif self.text == "stop":
        Core._end()
        self.update_text("block")



def exit(self):
    disable_event()

delete_schedule_button = _Button(active, "block", 0, 7, 2, 1, [ 10, 5, 10, 5], block, xspan=2)
delete_schedule_button.create()

delete_schedule_button = _Button(active, "exit", 0, 8, 2, 1, [ 10, 5, 5, 5], exit, xspan=2)
delete_schedule_button.create()

root.mainloop()