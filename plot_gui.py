from tkinter import *
from get_data import *

top_window = Tk()
top_window.title('Get Chinese city AQIs')
# top_window.geometry('350x200')


def clicked_search_btn():
    global result
    result = CityAQI(txt_cityname.get())
    configure_latest_record()


def configure_latest_record():
    global result
    res_tmp = result.latest_rec.date_time
    txt_tmp = (res_tmp.get('date') or '') + ' ' + (res_tmp.get('time') or '')
    lbl_latest_dt_disp.configure(text=txt_tmp)
    res_tmp = result.latest_rec.air_quality
    txt_tmp = (res_tmp.get('AQI') or '') + ' ' + (res_tmp.get('quality') or '')
    lbl_latest_aqi_disp.configure(text=txt_tmp)


result = CityAQI('')


# The first frame of the window
search_frame = Frame(top_window)
search_frame.pack(side=TOP)

lbl_cityname = Label(search_frame, text='City Name:\t')
lbl_cityname.grid(column=0, row=0)

txt_cityname = Entry(search_frame, width=12)
txt_cityname.grid(column=1, row=0)

btn_search = Button(search_frame, text="Search", command=clicked_search_btn)
btn_search.grid(column=2, row=0)


# The second frame, for the latest record
latest_frame = Frame(top_window)
latest_frame.pack()

lbl_latest = Label(latest_frame, text='Latest record:')
lbl_latest.grid(column=0, row=0)

lbl_latest_dt = Label(latest_frame, text='\t Date Time:')
lbl_latest_dt.grid(column=0, row=1)
lbl_latest_dt_disp = Label(latest_frame, width=15)
lbl_latest_dt_disp.grid(column=1, row=1)

lbl_latest_aqi = Label(latest_frame, text='\t AQI:')
lbl_latest_aqi.grid(column=0, row=2)
lbl_latest_aqi_disp = Label(latest_frame, width=15)
lbl_latest_aqi_disp.grid(column=1, row=2)


top_window.mainloop()
