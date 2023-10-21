from utils import *
from display import _ListBox, _Label, _Button, _Entry, TimePicker
from tkinter import *
from tkinter.messagebox import *
from constant import *
from core import Core
from schedule import Schedule
from category import Category
from datetime import datetime
import threading


root = Tk()
root.title('website blocker')
root.iconbitmap('favicon.ico')
def disable_event():
    Core._end()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", disable_event)

category_settings = LabelFrame(root, text='category settings', padx=10, pady=10)
category_settings.grid(column=0, row=0, padx=10, pady=10)

schedule_settings = LabelFrame(root, text='schedule settings', padx=10, pady=10)
schedule_settings.grid(column=1, row=0, padx=10, pady=10)

active = LabelFrame(root, text='active', padx=10, pady=10)
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

website_frame_label  = _Label(category_settings, 'websites', 4, 0, [ 10, 0, 0, 0], 2)
website_frame_label.create()

# --------------------------------------------------------------------------------------------------------------
website_frame = _ListBox(category_settings, [], SINGLE, 17, 30, 4, 1, [10, 10, 5, 10], 2, 2, on_website_click)
website_frame.create()

schedule_frame_label  = _Label(category_settings, 'schedules', 4, 4, [0, 0, 0, 0], 2)
schedule_frame_label.create()

# --------------------------------------------------------------------------------------------------------------
schedule_frame = _ListBox(category_settings, [], SINGLE, 5, 30, 4, 5, [0, 10, 5, 0], 2, 3)
schedule_frame.create()


def on_category_select(self):
    def load_part_websites(value):
        new_label = value + ' websites'
        website_frame_label.update_value(new_label)
        category = Category(value)
        websites = category._load_part_websites()
        if len(websites)!=0:
            websites.append(LOAD_ALL)
        website_frame._update_link(value)
        website_frame.value = None
        website_frame.update_value(websites)
    
    def load_schedules(value):
        new_label = value + ' schedules'
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

category_frame_label  = _Label(category_settings, 'categories', 0, 0, [ 10, 0, 0, 0], 3)
category_frame_label.create()

def add_website_button_on_click(self):  
    def _():
        if category_frame.value:
            new_window = Toplevel()
            new_window.title('adding')
            new_window_label = _Label(new_window, 'website name: ',0, 0, [10, 0, 0, 0], 1)
            new_window_entry = _Entry(new_window, 1, 0, [10, 0, 0, 10], 1, 2)
            
            def cancel(self):
                new_window.destroy()

            def save(self):
                if new_window_entry.get_value() != '':
                    category = Category(category_frame.value)
                    output = category.add_website_to_category(new_window_entry.get_value())
                    if output == SUCCESS:
                        websites = category._load_all_websites()
                        website_frame.update_value(websites)
                    elif output==ALREADY_EXSISTS:
                        showinfo('adding website', 'website already exists')
                else:
                    showinfo('adding website', 'a name is requiered')
            

            def save_add(self):
                    save(self)
                    new_window_entry.clear_value()
                
            def save_and_exit(self):
                save(self)
                cancel(self)

            new_window_button_save_and_exit = _Button(new_window, 'save and exit', 0, 1, 2, 15, [10, 5, 10, 5], save_and_exit)
            new_window_button_save_and_add = _Button(new_window, 'save and add', 1, 1, 2, 15, [10, 5, 10, 5], save_add)
            new_window_button_canel = _Button(new_window, 'cancel', 2, 1, 2, 15, [10, 5, 10, 5], cancel)
            new_window_label.create()
            new_window_entry.create()
            new_window_button_save_and_exit.create()
            new_window_button_save_and_add.create()
            new_window_button_canel.create()
        else:
            showinfo('add website', 'no category selected')
    thread = threading.Thread(target=_)
    thread.start()
        


add_website_button = _Button(category_settings, 'add', 4, 3, 1, 1, [10, 5, 10, 5], add_website_button_on_click)
add_website_button.create()

def delete_website_button_on_click(self):
    def _():
        if website_frame.value and category_frame.value:
            category = Category(category_frame.value)
            category.delete_website_from_category(website_frame.value)
            websites = category._load_all_websites()
            website_frame.update_value(websites)
            showinfo('delete website', 'website deleted')
        else:
            showinfo('delete website', 'no website selected')
    thread = threading.Thread(target=_)
    thread.start()

delete_website_button = _Button(category_settings, 'delete', 5, 3, 1, 1, [10, 5, 10, 5], delete_website_button_on_click)
delete_website_button.create()


category_frame = _ListBox(category_settings, categories, SINGLE, 28, 30, 0, 1, [5, 10, 5, 10], 3 , 6, on_category_select)
category_frame.create()


def add_category_button_on_click(self):
    def _():
        new_window = Toplevel()
        new_window.title('adding')
        new_window_label = _Label(new_window, 'category name: ',0, 0, [10, 0, 0, 0], 1)
        new_window_entry = _Entry(new_window, 1, 0, [10, 0, 0, 10], 1, 2)
        
        def cancel(self):
            new_window.destroy()

        def save(self):
            if new_window_entry.get_value() != '':
                output = Category.create(new_window_entry.get_value(), 100)
                if output==ALREADY_EXSISTS:
                    showinfo('adding category', 'category already exists')
                else:
                    categories = Category.get_all()
                    category_frame.update_value(categories)
            else:
                    showinfo('adding category', 'a name is requiered')
        
        def save_add(self):
                save(self)
                new_window_entry.clear_value()
            
        def save_and_exit(self):
            save(self)
            cancel(self)

        new_window_button_save_and_exit = _Button(new_window, 'save and exit', 0, 1, 2, 15, [10, 5, 10, 5], save_and_exit)
        new_window_button_save_and_add = _Button(new_window, 'save and add', 1, 1, 2, 15, [10, 5, 10, 5], save_add)
        new_window_button_canel = _Button(new_window, 'cancel', 2, 1, 2, 15, [10, 5, 10, 5], cancel)
        new_window_label.create()
        new_window_entry.create()
        new_window_button_save_and_exit.create()
        new_window_button_save_and_add.create()
        new_window_button_canel.create()
    thread = threading.Thread(target=_)
    thread.start()

add_category_button = _Button(category_settings, 'add', 0, 8, 2, 1, [10, 5, 10, 5], add_category_button_on_click)
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

            showinfo('delete category', 'category deleted')
        else:
            showinfo('delete category', 'no category selected')
    thread = threading.Thread(target=_)
    thread.start()

delete_category_button = _Button(category_settings, 'delete', 1, 8, 2, 1, [10, 5, 10, 5], delete_category_button_on_click)
delete_category_button.create()
 
def rename_category_button_on_click(self): 
    def _():
        if category_frame.value:
            new_window = Toplevel()
            new_window.title('rename')
            new_window_label = _Label(new_window, 'category name: ',0, 0, [10, 0, 0, 0], 1)
            new_window_entry = _Entry(new_window, 1, 0, [10, 0, 0, 10], 1, 2, category_frame.value)
            
            def cancel(self):
                new_window.destroy()

            def save(self):
                if new_window_entry.get_value() != '':
                    category = Category(category_frame.value)
                    output = category.rename(new_window_entry.get_value())
                    if output == SUCCESS:
                        categories = Category.get_all()
                        category_frame.update_value(categories)
                    elif output==ALREADY_EXSISTS:
                        showinfo('rename category', 'category already exists')
                else:
                    showinfo('rename category', 'a name is requiered')
            
                
            def save_and_exit(self):
                save(self)
                cancel(self)

            new_window_button_save_and_exit = _Button(new_window, 'save', 0, 1, 2, 15, [10, 5, 10, 5], save_and_exit)
            new_window_button_canel = _Button(new_window, 'cancel', 2, 1, 2, 15, [10, 5, 10, 5], cancel)
            new_window_label.create()
            new_window_entry.create()
            new_window_button_save_and_exit.create()
            new_window_button_canel.create()
        else:
            showinfo('add website', 'no category selected')
    thread = threading.Thread(target=_)
    thread.start()


rename_category_button = _Button(category_settings, 'rename', 2, 8, 2, 1, [10, 5, 10, 5], rename_category_button_on_click)
rename_category_button.create()

def add_schedule_button_on_click(self):
    def _():
        if category_frame.value:
            new_window = Toplevel()
            schedules = get_unique_elements(Schedule.get_all(), schedule_frame.values)
            schedule__frame = _ListBox(new_window, schedules, MULTIPLE, 18, 25, 1, 0, [10, 10, 5, 10], 1, 1)
            schedule_frame_label  = _Label(new_window, 'choose schedules: ',0 , 0, [ 10, 10, 10, 0], 1)  
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
                    showinfo('add schedule', 'no schedule selected')
            
            def save_and_exit(self):
                save(self)
                cancel(self)

            new_window_button_save_and_exit = _Button(new_window, 'save', 0, 1, 2, 15, [10, 5, 10, 5], save_and_exit)
            new_window_button_canel = _Button(new_window, 'cancel', 1, 1, 2, 15, [10, 5, 10, 5], cancel)
            new_window_button_save_and_exit.create()
            new_window_button_canel.create()
            schedule__frame.create()
            schedule_frame_label.create()
    thread = threading.Thread(target=_)
    thread.start()



add_schedule_button = _Button(category_settings, 'add', 4, 8, 1, 2, [10, 5, 10, 5], add_schedule_button_on_click)
add_schedule_button.create()

def delete_schedule_button_on_click(self):
    def _():
        if schedule_frame.value:
            schedule = Schedule(schedule_frame.value)
            schedule.delete_category_from_schedule(category_frame.value)
            schedules = Schedule.get_schedules_for_category(category_frame.value)
            schedule_frame.update_value(schedules)
            showinfo('delete schedule', 'schedule deleted')
        else:
            showinfo('delete schedule', 'no schedule selected')
    thread = threading.Thread(target=_)
    thread.start()

delete_schedule_button = _Button(category_settings, 'delete', 5, 8, 1, 2, [ 10, 5, 10, 5], delete_schedule_button_on_click)
delete_schedule_button.create()


# schedule settings


_website_frame_label  = _Label(schedule_settings, 'websites', 4, 0, [ 10, 0, 0, 0], 2)
_website_frame_label.create()

# --------------------------------------------------------------------------------------------------------------
_website_frame = _ListBox(schedule_settings, [], SINGLE, 16, 30, 4, 1, [10, 10, 5, 10], 2, 2)
_website_frame.create()

_categorie_frame_label  = _Label(schedule_settings, 'categories', 4, 4, [0, 0, 0, 0], 2)
_categorie_frame_label.create()

# --------------------------------------------------------------------------------------------------------------
_categorie_frame = _ListBox(schedule_settings, [], SINGLE, 7, 30, 4, 5, [10, 10, 5, 0], 2, 4)
_categorie_frame.create()

durations_frame = _ListBox(schedule_settings, [], SINGLE, 4, 30, 0, 8, [5, 10, 5, 10], 3 , 2)
durations_frame.create()

def _on_schedule_select(self):
    def load_websites(value):
        new_label = ' websites linked to ' + value
        _website_frame_label.update_value(new_label)
        schedule = Schedule(value)
        schedule.load()
        websites = schedule.websites
        _website_frame._update_link(value)
        _website_frame.value = None
        _website_frame.update_value(websites)
    
    def _load_categories(value):
        new_label = ' categories linked to ' + value
        _categorie_frame_label.update_value(new_label)
        schedule = Schedule(value)
        schedule.load()
        categories = schedule.categories
        _categorie_frame._update_link(value)
        _categorie_frame.value = None
        _categorie_frame.update_value(categories)
    
    def _load_durations(value):
        new_label = 'durations linked to ' + value
        durations_frame_label.update_value(new_label)
        schedule = Schedule(value)
        schedule.load()
        categories = ['from {} to {}'.format(duration[0], duration[1]) for duration in schedule.durations]
        durations_frame._update_link(value)
        durations_frame.value = None
        durations_frame.update_value(categories)

    website_thread = threading.Thread(target=lambda: load_websites(self.value))
    schedule_thread = threading.Thread(target=lambda: _load_categories(self.value))
    duraitons_thread = threading.Thread(target=lambda: _load_durations(self.value))
    website_thread.start()
    duraitons_thread.start()
    schedule_thread.start()

_schedule_frame_label  = _Label(schedule_settings, 'schedules', 0, 0, [ 10, 0, 0, 0], 3)
_schedule_frame_label.create()

durations_frame_label  = _Label(schedule_settings, 'durations', 0, 7, [ 10, 0, 0, 0], 3)
durations_frame_label.create()


def _add_website_button_on_click(self):  
    def _():
        if _schedule_frame.value:
            new_window = Toplevel()
            new_window.title('adding')
            new_window_label = _Label(new_window, 'website name: ',0, 0, [10, 0, 0, 0], 1)
            new_window_entry = _Entry(new_window, 1, 0, [10, 0, 0, 10], 1, 2)
            
            def cancel(self):
                new_window.destroy()

            def save(self):
                if new_window_entry.get_value() != '':
                    schedule = Schedule(_schedule_frame.value)
                    output = schedule.add_website_to_schedule(new_window_entry.get_value())
                    if output == SUCCESS:
                        schedule.load()
                        websites = schedule.websites
                        _website_frame.update_value(websites)
                    elif output==ALREADY_EXSISTS:
                        showinfo('adding website', 'website already exists')
                else:
                    showinfo('adding website', 'a name is requiered')
            

            def save_add(self):
                    save(self)
                    new_window_entry.clear_value()
                
            def save_and_exit(self):
                save(self)
                cancel(self)

            new_window_button_save_and_exit = _Button(new_window, 'save and exit', 0, 1, 2, 15, [10, 5, 10, 5], save_and_exit)
            new_window_button_save_and_add = _Button(new_window, 'save and add', 1, 1, 2, 15, [10, 5, 10, 5], save_add)
            new_window_button_canel = _Button(new_window, 'cancel', 2, 1, 2, 15, [10, 5, 10, 5], cancel)
            new_window_label.create()
            new_window_entry.create()
            new_window_button_save_and_exit.create()
            new_window_button_save_and_add.create()
            new_window_button_canel.create()
        else:
            showinfo('add website', 'no schedule selected')
    thread = threading.Thread(target=_)
    thread.start()
        


add_website_button = _Button(schedule_settings, 'add', 4, 3, 1, 1, [10, 5, 10, 5], _add_website_button_on_click)
add_website_button.create()

def _delete_website_button_on_click(self):
    def _():
        if _website_frame.value and _schedule_frame.value:
            schedule = Schedule(_schedule_frame.value)
            schedule.delete_website_from_schedule(_website_frame.value)
            schedule.load()
            websites = schedule.websites
            _website_frame.update_value(websites)
            showinfo('delete website', 'website deleted')
        else:
            showinfo('delete website', 'no website selected')
    thread = threading.Thread(target=_)
    thread.start()

delete_website_button = _Button(schedule_settings, 'delete', 5, 3, 1, 1, [10, 5, 10, 5], _delete_website_button_on_click)
delete_website_button.create()

_schedule_frame = _ListBox(schedule_settings, schedules, SINGLE, 20, 30, 0, 1, [5, 10, 10, 10], 3 , 4, _on_schedule_select)
_schedule_frame.create()





def _add_schedule_button_on_click(self):
    def _():
        new_window = Toplevel()
        new_window.title('adding')
        new_window_label = _Label(new_window, 'schedule name: ',0, 0, [10, 0, 0, 0], 1)
        new_window_entry = _Entry(new_window, 1, 0, [10, 0, 0, 10], 1, 2)
        new_window_time_picker_frame = Frame(new_window)
        new_window_time_picker_frame.grid(column=0, row=1, columnspan=3)
        new_window_time_pickers = [TimePicker(new_window_time_picker_frame, 0)]
        new_window_time_pickers[0].create()
        
        def cancel(self):
            new_window.destroy()

        def save(self):
            if new_window_entry.get_value() != '':
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
                    showinfo('adding schedule', 'schedule already exists')
                else:
                    schedules = Schedule.get_all()
                    _schedule_frame.update_value(schedules)
            else:
                    showinfo('adding schedule', 'a name is requiered')
        
        def save_add(self):
                save(self)
                new_window_entry.clear_value()
            
        def save_and_exit(self):
            save(self)
            cancel(self)

        new_window_button_save_and_exit = _Button(new_window, 'save and exit', 0, 3, 2, 15, [10, 5, 10, 5], save_and_exit)
        new_window_button_save_and_add = _Button(new_window, 'save and add', 1, 3, 2, 15, [10, 5, 10, 5], save_add)
        new_window_button_canel = _Button(new_window, 'cancel', 2, 3, 2, 15, [10, 5, 10, 5], cancel)
        new_window_button_save_and_exit.create()
        new_window_button_save_and_add.create()
        new_window_button_canel.create()


        def add_new_time_picker(self):
            row = len(new_window_time_pickers)
            time_picker = TimePicker(new_window_time_picker_frame, row)
            time_picker.create()
            new_window_time_pickers.append(time_picker)
            
        
        new_window_button_add_time_picker = _Button(new_window, '+', 1, 2, 2, 15, [10, 5, 10, 5], add_new_time_picker)
        new_window_button_add_time_picker.create()
        new_window_label.create()
        new_window_entry.create()
    thread = threading.Thread(target=_)
    thread.start()

add_category_button = _Button(schedule_settings, 'add', 0, 6, 1, 1, [5, 5, 5, 5], _add_schedule_button_on_click)
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

            showinfo('delete schedule', 'schedule deleted')
        else:
            showinfo('delete schedule', 'no schedule selected')
    thread = threading.Thread(target=_)
    thread.start()

delete_category_button = _Button(schedule_settings, 'delete', 1, 6, 1, 1, [5, 5, 5, 5], _delete_schedule_button_on_click)
delete_category_button.create()
 
def edit_category_button_on_click(self): 
    def _():
        if _schedule_frame.value:
            schedule = Schedule(_schedule_frame.value)
            schedule.load()
            new_window = Toplevel()
            new_window.title('adding')
            new_window_label = _Label(new_window, 'schedule name: ',0, 0, [10, 0, 0, 0], 1)
            new_window_entry = _Entry(new_window, 1, 0, [10, 0, 0, 10], 1, 2, schedule.name)
            new_window_time_picker_frame = Frame(new_window)
            new_window_time_picker_frame.grid(column=0, row=1, columnspan=3)
            new_window_time_pickers = [TimePicker(new_window_time_picker_frame, 0, i[0], i[1]) for i in schedule.durations]
            [i.create() for i in new_window_time_pickers]
            
            def cancel(self):
                new_window.destroy()

            def save(self):
                if new_window_entry.get_value() != '':
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
                        showinfo('adding schedule', 'a name is requiered')
            
            def save_add(self):
                    save(self)
                    new_window_entry.clear_value()
                
            def save_and_exit(self):
                save(self)
                cancel(self)

            new_window_button_save_and_exit = _Button(new_window, 'save and exit', 0, 3, 2, 15, [10, 5, 10, 5], save_and_exit)
            new_window_button_save_and_add = _Button(new_window, 'save and add', 1, 3, 2, 15, [10, 5, 10, 5], save_add)
            new_window_button_canel = _Button(new_window, 'cancel', 2, 3, 2, 15, [10, 5, 10, 5], cancel)
            new_window_button_save_and_exit.create()
            new_window_button_save_and_add.create()
            new_window_button_canel.create()


            def add_new_time_picker(self):
                row = len(new_window_time_pickers)
                time_picker = TimePicker(new_window_time_picker_frame, row)
                time_picker.create()
                new_window_time_pickers.append(time_picker)
                
            
            new_window_button_add_time_picker = _Button(new_window, '+', 1, 2, 2, 15, [10, 5, 10, 5], add_new_time_picker)
            new_window_button_add_time_picker.create()
            new_window_label.create()
            new_window_entry.create()
    thread = threading.Thread(target=_)
    thread.start()

rename_category_button = _Button(schedule_settings, 'edit', 2, 6, 1, 1, [5, 5, 5, 5], edit_category_button_on_click)
rename_category_button.create()

def _add_category_button_on_click(self):
    def _():
        if _schedule_frame.value:
            new_window = Toplevel()
            categories = get_unique_elements(Category.get_all(), _categorie_frame.values)
            category__frame = _ListBox(new_window, categories, MULTIPLE, 18, 25, 1, 0, [10, 10, 5, 10], 1, 1)
            _categorie_frame_label  = _Label(new_window, 'choose categories: ',0 , 0, [ 10, 10, 10, 0], 1)  
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
                    showinfo('add schedule', 'no schedule selected')
            
            def save_and_exit(self):
                save(self)
                cancel(self)

            new_window_button_save_and_exit = _Button(new_window, 'save', 0, 1, 2, 15, [10, 5, 10, 5], save_and_exit)
            new_window_button_canel = _Button(new_window, 'cancel', 1, 1, 2, 15, [10, 5, 10, 5], cancel)
            new_window_button_save_and_exit.create()
            new_window_button_canel.create()
            category__frame.create()
            _categorie_frame_label.create()
    thread = threading.Thread(target=_)
    thread.start()



add_schedule_button = _Button(schedule_settings, 'add', 4, 9, 1, 2, [10, 5, 10, 5], _add_category_button_on_click)
add_schedule_button.create()

def _delete_category_button_on_click(self):
    def _():
        if _categorie_frame.value:
            schedule = Schedule(_schedule_frame.value)
            schedule.delete_category_from_schedule(_categorie_frame.value)
            schedule.load()
            schedules = schedule.categories
            _categorie_frame.update_value(schedules)
            showinfo('delete category', 'category deleted')
        else:
            showinfo('delete category', 'no category selected')
    thread = threading.Thread(target=_)
    thread.start()

delete_schedule_button = _Button(schedule_settings, 'delete', 5, 9, 1, 2, [ 10, 5, 10, 5], _delete_category_button_on_click)
delete_schedule_button.create()




# def main():



current_active_categories = _ListBox(active, [], SINGLE, 5, 30, 0, 1, [10, 10, 10, 10], 1, 1)
current_active_schedules = _ListBox(active, [], SINGLE, 5, 30, 0, 3, [10, 10, 10, 10], 1, 1)
current_active_websites = _ListBox(active, [], SINGLE, 5, 30, 0, 5, [10, 10, 10, 10], 1, 1)

current_active_categories_label = _Label(active, 'active ategories: ', 0, 0, [10, 10, 10, 30], 2)
current_active_schedules_label = _Label(active, 'active schedules: ', 0, 2, [10, 10, 10, 10], 2)
current_active_websites_label = _Label(active, 'active websites: ', 0, 4, [10, 10, 10, 10], 2)

current_active_categories_label.create()
current_active_schedules_label.create()
current_active_websites_label.create()

current_active_categories.create()
current_active_schedules.create()
current_active_websites.create()


def block(self):
    if self.text == 'block':
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
        self.update_text('stop')
        
    elif self.text == 'stop':
        Core._end()
        self.update_text('block')



def exit(self):
    disable_event()

delete_schedule_button = _Button(active, 'block', 0, 7, 2, 1, [ 10, 5, 10, 5], block, xspan=2)
delete_schedule_button.create()

delete_schedule_button = _Button(active, 'exit', 0, 8, 2, 1, [ 10, 5, 5, 5], exit, xspan=2)
delete_schedule_button.create()

root.mainloop()