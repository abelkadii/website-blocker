from utils import *


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
        scrollbar = Scrollbar(self.root, orient='vertical', command=self.listbox.yview)
        self.listbox['yscrollcommand'] = scrollbar.set
        self.listbox.grid(column=self.position_x, row=self.position_y, sticky='nwes', pady=(self.pad[0], self.pad[2]), padx=(self.pad[3], 0), columnspan=self.xspan, rowspan=self.yspan)
        scrollbar.grid(column=self.position_x+self.xspan, row=self.position_y, sticky='ns', padx=(0, self.pad[1]), pady=(self.pad[0], self.pad[2]), rowspan=self.yspan)
        self.listbox.bind('<<ListboxSelect>>', lambda event: self.onClick(self))
    
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
        self.label.grid(column=self.position_x, row=self.position_y, sticky='nwes', pady=(self.pad[0], self.pad[2]), padx=(self.pad[1], self.pad[3]), columnspan=self.xspan)
    
    def destroy(self):
        self.label.destroy()
    
    def update_value(self, value):
        self.value = value
        self.label.configure(text=value)

class _Button:
    def __init__(self, root, text, position_x, position_y, height, width, pad, onClick):
        self.root = root
        self.text = text
        self.position_x = position_x
        self.position_y = position_y
        self.height = height
        self.width = width
        self.pad = pad
        self.bind_component = []
        self.onClick = onClick

    def create(self):
        self.button = Button(self.root, text=self.text, command=lambda: self.onClick(self), height=self.height, width=self.width)
        self.button.grid(column=self.position_x, row=self.position_y, sticky='nwes', pady=(self.pad[0], self.pad[2]), padx=(self.pad[1], self.pad[3]))
    
    def destroy(self):
        self.button.destroy()
    
    def update_text(self, text):
        self.text = text
        self.button.configure(text=text)

    


class _Entry:
    def __init__(self, root, position_x, position_y, pad, border_width, xspan, default=''):
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
        self.entry.grid(column=self.position_x, row=self.position_y, sticky='nwes', pady=(self.pad[0], self.pad[2]), padx=(self.pad[1], self.pad[3]), columnspan=self.xspan)
    
    def destroy(self):
        self.entry.destroy()
    
    def get_value(self):
        return self.entry.get()
    
    def clear_value(self):
        return self.entry.delete(0, END)


class TimePicker:
    def __init__(self, frame, row, _default='00:00:00', default_='23:59:59'):
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

        self._hourstr= StringVar(self.frame, self._default.split(':')[0])
        self._minutestr= StringVar(self.frame, self._default.split(':')[1])
        self._secondstr= StringVar(self.frame, self._default.split(':')[2])
        
        self.hourstr_= StringVar(self.frame, self.default_.split(':')[0])
        self.minutestr_= StringVar(self.frame, self.default_.split(':')[1])
        self.secondstr_= StringVar(self.frame, self.default_.split(':')[2])

        self._hour = Spinbox(self.frame,from_=0,to=23,wrap=True,textvariable=self._hourstr,width=2,state='readonly')
        self._minute = Spinbox(self.frame,from_=0,to=59,wrap=True,textvariable=self._minutestr,width=2,state='readonly')
        self._second = Spinbox(self.frame,from_=0,to=59,wrap=True,textvariable=self._secondstr,width=2,state='readonly')
        self.label_ = Label(self.frame, text='to: ')
        
        self.hour_ = Spinbox(self.frame,from_=0,to=23,wrap=True,textvariable=self.hourstr_,width=2,state='readonly')
        self.minute_ = Spinbox(self.frame,from_=0,to=59,wrap=True,textvariable=self.minutestr_,width=2,state='readonly')
        self.second_ = Spinbox(self.frame,from_=0,to=59,wrap=True,textvariable=self.secondstr_,width=2,state='readonly')
        self._label = Label(self.frame, text='from: ')

        self.destroy_button = Button(self.frame, text='-', command=destroy_button)


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

            return '{}:{}:{}'.format(_hour, _minute, _second), '{}:{}:{}'.format(hour_, minute_, second_)
        return None, None 
