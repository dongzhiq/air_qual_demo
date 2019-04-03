from tkinter import *
from tkinter.ttk import *
from get_data import *

top_window = Tk()
top_window.title('Get Chinese city AQIs')
top_window.geometry('285x195')


def clicked_request_btn():
    global result
    result = CityAQI(txt_cityname.get())
    update_record()


def update_record():
    global result
    # configure the latest record
    res_tmp = result.latest_rec.date_time
    txt_tmp = (res_tmp.get('date') or '') + ' ' + (res_tmp.get('time') or '')
    lbl_latest_dt_disp.configure(text=txt_tmp)
    res_tmp = result.latest_rec.air_quality
    txt_tmp = (res_tmp.get('AQI') or '') + ' ' + (res_tmp.get('quality') or '')
    lbl_latest_aqi_disp.configure(text=txt_tmp)
    # configure recent records
    combo_recent.current(0)
    lbl_recent_aqi_disp.configure(text='')
    combo_recent['values'] = ('Pick a date',) + tuple(result.recent_rec.keys())
    # configure detailed latest records
    combo_details.current(0)
    lbl_details_aqi_disp.configure(text='')
    combo_details['values'] = ('Pick a monitor site',) + tuple(result.detailed_latest_rec.keys())


def select_recent_record(self):
    global result
    if combo_recent.current():
        res_tmp = result.recent_rec[combo_recent.get()].air_quality
        txt_tmp = (res_tmp.get('AQI') or '') + ' ' + (res_tmp.get('quality') or '')
        lbl_recent_aqi_disp.configure(text=txt_tmp)
    else:
        lbl_recent_aqi_disp.configure(text='')


def select_detailed_record(self):
    global result
    if combo_details.current():
        res_tmp = result.detailed_latest_rec[combo_details.get()].air_quality
        txt_tmp = (res_tmp.get('AQI') or '') + ' ' + (res_tmp.get('quality') or '') + '\n' + (res_tmp.get('PM2.5') or '') + '\n' + (res_tmp.get('PM10') or '')
        lbl_details_aqi_disp.configure(text=txt_tmp)
    else:
        lbl_details_aqi_disp.configure(text='')


result = CityAQI('')


# The first frame of the window
search_frame = Frame(top_window)
search_frame.grid(column=0, row=0)

lbl_cityname = Label(search_frame, text='City Name:')
lbl_cityname.grid(column=0, row=0)

txt_cityname = Entry(search_frame, width=12)
txt_cityname.grid(column=1, row=0, padx=15)

btn_search = Button(search_frame, text="Request", command=clicked_request_btn)
btn_search.grid(column=2, row=0)


# The second frame, for the latest record
latest_frame = Frame(top_window)
latest_frame.grid(column=0, row=1, sticky=W)

lbl_latest = Label(latest_frame, text='  Latest record:')
lbl_latest.grid(column=0, row=0, sticky=W)

lbl_latest_dt = Label(latest_frame, text='Date&Time:')
lbl_latest_dt.grid(column=0, row=1, sticky=E)
lbl_latest_dt_disp = Label(latest_frame, width=15)
lbl_latest_dt_disp.grid(column=1, row=1, sticky=N, padx=10)

lbl_latest_aqi = Label(latest_frame, text='AQI:')
lbl_latest_aqi.grid(column=0, row=2, sticky=E)
lbl_latest_aqi_disp = Label(latest_frame, width=15)
lbl_latest_aqi_disp.grid(column=1, row=2, sticky=N, padx=10)


# The third frame, for recent records
recent_frame = Frame(top_window)
recent_frame.grid(column=0, row=2, sticky=W)

lbl_recent = Label(recent_frame, text='  Recent records:')
lbl_recent.grid(column=0, row=0, sticky=W)

combo_recent = Combobox(recent_frame, width=12, state='readonly')
combo_recent['values'] = ('Pick a date',)
combo_recent.current(0)  # set the selected item
combo_recent.grid(column=1, row=0, sticky=N, padx=10)
combo_recent.bind('<<ComboboxSelected>>', select_recent_record)

lbl_recent_aqi = Label(recent_frame, text='AQI:')
lbl_recent_aqi.grid(column=0, row=1, sticky=E)
lbl_recent_aqi_disp = Label(recent_frame, width=15)
lbl_recent_aqi_disp.grid(column=1, row=1, sticky=N, padx=10)


# The forth frame, for detailed latest records
details_frame = Frame(top_window)
details_frame.grid(column=0, row=3, sticky=W)

lbl_details = Label(details_frame, text='  Detailed records:')
lbl_details.grid(column=0, row=0, sticky=W)

combo_details = Combobox(details_frame, width=18, state='readonly')
combo_details['values'] = ('Pick a monitor site',)
combo_details.current(0)  # set the selected item
combo_details.grid(column=1, row=0, sticky=N, padx=5)
combo_details.bind('<<ComboboxSelected>>', select_detailed_record)

lbl_details_aqi = Label(details_frame, text='AQI:\nPM2.5:\nPM10:\n')
lbl_details_aqi.grid(column=0, row=1, sticky=E)
lbl_details_aqi_disp = Label(details_frame, width=15)
lbl_details_aqi_disp.grid(column=1, row=1, sticky=N, padx=10)

top_window.mainloop()
