from utils import *

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