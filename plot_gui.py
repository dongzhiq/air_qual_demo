from tkinter import *
import tkinter.messagebox as messagebox
from tkinter.ttk import *
from get_data import *

top_window = Tk()
top_window.title('Get Chinese city AQIs')
top_window.geometry('265x230')


def clicked_request_btn():
    global result
    result = CityAQI(request.widgets['cn_ent'].get())
    if result.error_description != 'Successful':
        messagebox.showinfo('Error', result.error_description)
    update_record()


def update_record():
    global result

    latest.disp_records = result.latest_rec
    latest.update_all_displbl(result.latest_rec)

    recent.disp_records = result.recent_rec
    recent.config_combo_list('date_combo')
    recent.select_combo_record('date_combo')

    details.disp_records = result.detailed_latest_rec
    details.config_combo_list('site_combo')
    details.select_combo_record('site_combo')


result = CityAQI('')


class ContentFrame(Frame):

    def __init__(self, master, **grid_para):
        # use grid_para to position self in master
        # use disp_record to tell which records this frame should display
        Frame.__init__(self, master)
        self.grid(**grid_para)
        self.widgets = {}
        self.disp_records = None

    def add_widget(self, wid_name_type, grid_para, spec_para):
        # widget name, widget type (Label or Combobox); wid_name_type is a list of tuples
        # grid parameters, specified parameters; grid_para and spec_para are lists of dicts
        # self.widgets is a dictionary with items like wid_name: wid_obj
        for (w_name, w_type), grid, spec in zip(wid_name_type, grid_para, spec_para):
            if w_type in {'Label', 'StaticLabel', 'DispLabel'}:
                if w_type == 'DispLabel':
                    disp_attr_key = spec['disp']
                    del spec['disp']
                self.widgets[w_name] = Label(self, **spec)
                if w_type == 'DispLabel':
                    self.widgets[w_name].disp_attr_key = disp_attr_key
            elif w_type == 'Entry':
                self.widgets[w_name] = Entry(self, **spec)
            elif w_type == 'Button':
                self.widgets[w_name] = Button(self, **spec)
            elif w_type == 'Combobox':
                spec_combo = {key: spec.get(key) for key in {'width', 'state'} if spec.get(key) is not None}
                combo_obj = Combobox(self, **spec_combo)
                self.widgets[w_name] = combo_obj
                combo_obj.default = (spec.get('default_txt'), )     # When default text was not set, set it to None.
                combo_obj['values'] = combo_obj.default
                combo_obj.current(0)                                # Set the item to be default text.
                combo_obj.bind('<<ComboboxSelected>>', spec['sel_action'])
            else:
                print(w_type + ': ' + 'No such widget type.')
            self.widgets[w_name].type = w_type
            self.widgets[w_name].grid(**grid)

    def update_disp_label(self, lbl_name, record=None):
        txt_tmp = ''
        disp_keys = self.widgets[lbl_name].disp_attr_key
        if record and disp_keys:
            dic = getattr(record, disp_keys[0])
            for i in range(1, len(disp_keys)):
                txt_tmp += ((dic.get(disp_keys[i]) or '') + ' ')
        self.widgets[lbl_name].configure(text=txt_tmp)

    def update_all_displbl(self, record=None):
        for key, wid in self.widgets.items():
            if wid.type == 'DispLabel':
                self.update_disp_label(key, record)

    def config_combo_list(self, combo_name, record_dict=None):
        dic = {None: self.disp_records}.get(record_dict, record_dict)
        combo = self.widgets[combo_name]
        combo['values'] = combo.default + tuple(dic)
        combo.current(0)

    def select_combo_record(self, combo_name, record_dict=None):
        dic = {None: self.disp_records}.get(record_dict, record_dict)
        combo = self.widgets[combo_name]
        index = combo.current()
        self.update_all_displbl(dic.get(combo['values'][index], None))


# The first frame of the window
request = ContentFrame(top_window, column=0, row=0)
wid_name_type = [('cn_lbl', 'StaticLabel'), ('cn_ent', 'Entry'), ('rqst_btn', 'Button')]
grid_para = [dict(column=0, row=0), dict(column=1, row=0, padx=15), dict(column=2, row=0)]
spec_para = [dict(text='City Name:'), dict(width=12), dict(text="Request", command=clicked_request_btn)]
request.add_widget(wid_name_type, grid_para, spec_para)

# The second frame, for the latest record
latest = ContentFrame(top_window, column=0, row=1, sticky=W)
wid_name_type = [('title', 'StaticLabel'), ('dt_lbl', 'StaticLabel'), ('dt_disp', 'DispLabel'),
                 ('aqi_lbl', 'StaticLabel'), ('aqi_disp', 'DispLabel')]
grid_para = [dict(column=0, row=0, sticky=W), dict(column=0, row=1, sticky=E), dict(column=1, row=1, sticky=N, padx=10),
             dict(column=0, row=2, sticky=E), dict(column=1, row=2, sticky=N, padx=10)]
spec_para = [dict(text='  Latest record:'), dict(text='Date&Time:'), dict(width=15, disp=['date_time', 'date', 'time']),
             dict(text='AQI:'), dict(width=15, disp=['air_quality', 'quality', 'AQI'])]
latest.add_widget(wid_name_type, grid_para, spec_para)

# The third frame, for detailed latest records
details = ContentFrame(top_window, column=0, row=2, sticky=W)
wid_name_type = [('title', 'StaticLabel'), ('site_combo', 'Combobox'),
                 ('aqi_lbl', 'StaticLabel'), ('pm2.5_lbl', 'StaticLabel'), ('pm10_lbl', 'StaticLabel'),
                 ('aqi_disp', 'DispLabel'), ('pm2.5_disp', 'DispLabel'), ('pm10_disp', 'DispLabel')]
grid_para = [dict(column=0, row=0, sticky=W), dict(column=1, row=0, sticky=N, padx=5),
             dict(column=0, row=1, sticky=E), dict(column=0, row=2, sticky=E), dict(column=0, row=3, sticky=E),
             dict(column=1, row=1, sticky=N), dict(column=1, row=2, sticky=N), dict(column=1, row=3, sticky=N)]
spec_para = [dict(text='  Detailed records:'),
             dict(width=18, state='readonly', default_txt='Pick a monitor site',
                  sel_action=lambda event: details.select_combo_record('site_combo')),
             dict(text='AQI:'), dict(text='PM2.5:'), dict(text='PM10:'),
             dict(width=15, disp=['air_quality', 'quality', 'AQI']), dict(width=15, disp=['air_quality', 'PM2.5Hour']),
             dict(width=15, disp=['air_quality', 'PM10Hour'])]
details.add_widget(wid_name_type, grid_para, spec_para)

# The forth frame, for recent records
recent = ContentFrame(top_window, column=0, row=3, sticky=W)
wid_name_type = [('title', 'StaticLabel'), ('date_combo', 'Combobox'),
                 ('aqi_lbl', 'StaticLabel'), ('aqi_disp', 'DispLabel')]
grid_para = [dict(column=0, row=0, sticky=W), dict(column=1, row=0, sticky=N, padx=10, pady=10),
             dict(column=0, row=1, sticky=E), dict(column=1, row=1, sticky=N, padx=10)]
spec_para = [dict(text='  Recent historical\n \t records:'),
             dict(width=12, state='readonly', default_txt='Pick a date',
                  sel_action=lambda event: recent.select_combo_record('date_combo')),
             dict(text='AQI:'), dict(width=15, disp=['air_quality', 'quality', 'AQI'])]
recent.add_widget(wid_name_type, grid_para, spec_para)

top_window.mainloop()
