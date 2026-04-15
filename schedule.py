from utils import *


class Schedule:
    def __init__(self, name):
        self.name = name
        self.durations = None
        self.categories = None
        self.websites = None
    
    def create(name, durations, categories=[], websites=[]):
        if os.path.exists(join_path(SCHEDULE_DIR_PATH, name)):
            return ALREADY_EXSISTS
        write_file = open(join_path(SCHEDULE_DIR_PATH, name), 'w')

        schedule = {
            'name': name,
            'durations': durations,
            'categories': categories,
            'websites': websites
        }
        write_file.write(json.dumps(schedule, indent=4))
        return Schedule(name)

    def destroy(self):
        os.remove(join_path(SCHEDULE_DIR_PATH, self.name))
        return SUCCESS

    def load(self):
        self._get()
        return SUCCESS


    def _get(self):
        read_file = open(join_path(SCHEDULE_DIR_PATH, self.name), 'r')
        file_data = json.load(read_file)
        self.websites = file_data.get('websites')
        self.categories = file_data.get('categories')
        self.durations = file_data.get('durations')
        

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
        read_file = open(join_path(SCHEDULE_DIR_PATH, self.name), 'r')
        file_data = json.load(read_file)
        file_data.get('categories').append(category_name)
        if self.categories == None:
            self.load()
        self.categories.append(category_name)
        write_file = open(join_path(SCHEDULE_DIR_PATH, self.name), 'w')
        json.dump(file_data, write_file, indent=4)
        return SUCCESS
    
    def add_website_to_schedule(self, website_name):
        read_file = open(join_path(SCHEDULE_DIR_PATH, self.name), 'r')
        file_data = json.load(read_file)
        file_data.get('websites').append(website_name)
        if self.categories == None:
            self.load()
        self.categories.append(website_name)
        write_file = open(join_path(SCHEDULE_DIR_PATH, self.name), 'w')
        json.dump(file_data, write_file, indent=4)
        return SUCCESS
    
    def delete_category_from_schedule(self, category_name):
        read_file = open(join_path(SCHEDULE_DIR_PATH, self.name), 'r')
        file_data = json.load(read_file)
        file_data.get('categories').remove(category_name)
        if self.categories == None:
            self.load()
        self.categories.remove(category_name)
        write_file = open(join_path(SCHEDULE_DIR_PATH, self.name), 'w')
        json.dump(file_data, write_file, indent=4)
        return SUCCESS
    
    def delete_website_from_schedule(self, website_name):
        read_file = open(join_path(SCHEDULE_DIR_PATH, self.name), 'r')
        file_data = json.load(read_file)
        file_data.get('websites').remove(website_name)
        if self.websites == None:
            self.load()
        self.websites.remove(website_name)
        write_file = open(join_path(SCHEDULE_DIR_PATH, self.name), 'w')
        json.dump(file_data, write_file, indent=4)
        return SUCCESS

    def edit(self, durations, new_name):
        if os.path.exists(join_path(SCHEDULE_DIR_PATH, new_name)):
            return ALREADY_EXSISTS
        read_file = open(join_path(SCHEDULE_DIR_PATH, self.name), 'r')
        file_data = json.load(read_file)
        file_data['durations'] = durations
        file_data['name'] = new_name
        write_file = open(join_path(SCHEDULE_DIR_PATH, new_name), 'w')
        json.dump(file_data, write_file, indent=4)
        write_file.close()
        self.name = new_name
        os.remove(join_path(SCHEDULE_DIR_PATH, self.name))
        return SUCCESS

    def get_schedules_for_category(category):
        schedules = []
        for schedule in os.listdir(SCHEDULE_DIR_PATH):
            read_file = json.load(open(join_path(SCHEDULE_DIR_PATH, schedule), 'r'))
            if category in read_file.get('categories'):
                schedules.append(schedule)
        return schedules
    
    def get_schedules_for_website(website):
        schedules = []
        for schedule in os.listdir(SCHEDULE_DIR_PATH):
            read_file = json.load(open(join_path(SCHEDULE_DIR_PATH, schedule), 'r'))
            if website in read_file.get('websites'):
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
