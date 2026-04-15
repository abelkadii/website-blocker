from utils import *

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
            data = get_original_data() + '\n' + LOCAL_HOST + ' '
            data += f'\n{LOCAL_HOST} '.join(configure_data)
            file = open(HOST_FILE_PATH, 'w')
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
        file = open(STATUS_FILE_PATH, 'w')
        file.write(BLOCKING)
        file.close()
        return SUCCESS
        
    def _end():
        file = open(STATUS_FILE_PATH, 'w')
        file.write(DISABLED)
        file.close()
        return SUCCESS

    def _status():
        file = open(STATUS_FILE_PATH, 'r')
        status = file.read()
        file.close()
        return status