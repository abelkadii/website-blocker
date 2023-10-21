from utils import *
from constant import *
from schedule import *
import os

import shutil


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
        data[index] = website_name + '[frozen]'
        if self.websites: self.websites[index] = website_name + '[frozen]'
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
            if file_name != '__init__':
                data += open(join_path(CATEGORY_DIR_PATH, self.name, file_name), 'r').read().split()
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
            write_file = open(join_path(path, padded_name), 'w')
            start = self.length*i
            end = self.length*(i+1) if self.length*(i+1) < _len-1 else _len -1
            write_file.write('\n'.join(websites[start:end]))
        return SUCCESS
    
    def _load_part_websites(self):
        if len(os.listdir(join_path(CATEGORY_DIR_PATH, self.name)))>1:
            length = len(str(len(os.listdir(join_path(CATEGORY_DIR_PATH, self.name)))))
            data = open(join_path(CATEGORY_DIR_PATH, self.name, pad(self.part, length)), 'r').read().split('\n')
            self.websites = self.websites if self.loaded else self.websites + data
            self.part += 1
        return self.websites