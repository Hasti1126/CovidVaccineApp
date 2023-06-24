from tkinter import *
from tkinter import messagebox

from datetime import datetime

import pytz

IST=pytz.timezone('Asia/Kolkata')
import requests

software_version='v1.1'
# Color value reference
top_left_frame_bg  = "#bfaa0b"
top_right_frame_bg = '#ccbf2d'

app= Tk() #object of TK Class

# App Geometry and components
app.geometry("700x480+400+200")# size of window
app.title(f"Vaccine Availability Checker {software_version}")
app.iconbitmap('covid.ico') #icon image #tkinter supports on ico file type
app.resizable(True, True)
app.config(background = '#7a6c01') #backggroundColor


def refresh_api_call(PINCODE, DATE):
    header = {'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'}
    request_link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={PINCODE}&date={DATE}"
    response = requests.get(request_link, headers = header)
    resp_JSON = response.json()
    return resp_JSON

#When we click on search button this function gets activated	
def search_vaccine_avl():
    clear_result_box()
    PINCODE = pincode_text_var.get().strip()#strip method to strip extra spaces
    DATE = date_text_var.get()
    resp_JSON = refresh_api_call(PINCODE, DATE)

    try:
        if len(resp_JSON['sessions']) == 0:
            messagebox.showinfo("INFO","Vaccine not yet arrived for the given date")#pop up a messagebox

        for sess in resp_JSON['sessions']:
            age_limit           = sess['min_age_limit']
            center_name         = sess['name']
            pincode             = sess['pincode']
            vaccine_name        = sess['vaccine']
            available_capacity  = sess['available_capacity']
            qnty_dose_1         = sess['available_capacity_dose1']
            qnty_dose_2         = sess['available_capacity_dose2']
            slot_date           = sess['date']

            if available_capacity > 0:
                curr_status = 'Available'
            else:
                curr_status = 'NA'
            
            if age_limit == 45:
                age_grp = '45+'
            else:
                age_grp = '18-44'



            result_box_avl.insert(END, f"{curr_status:^6s}")#6 string space center alingment
            result_box_avl.insert(END,"\n")
            result_box_cent.insert(END, f"{center_name:<30s}")
            result_box_cent.insert(END,"\n")
            result_box_age.insert(END, f"{age_grp:<6s}")
            result_box_age.insert(END,"\n")
            result_box_vacc.insert(END, f"{vaccine_name:<8s}")
            result_box_vacc.insert(END,"\n")
            result_box_D1.insert(END, f"{qnty_dose_1:>5}")
            result_box_D1.insert(END,"\n")
            result_box_D2.insert(END, f"{qnty_dose_2:>5}")
            result_box_D2.insert(END,"\n")
            result_box_D1_D2.insert(END, f"{available_capacity:<5}")
            result_box_D1_D2.insert(END,"\n")
    except KeyError as KE:
        messagebox.showerror("ERROR","No Available center(s) for the given Pincode and date")
        print (pincode_text_var.get())




# Add Frame
frame1= Frame(app,height=120,width=180,bg=top_left_frame_bg,bd=1,relief=FLAT)
frame1.place(x=0,y=0)
frame2= Frame(app,height=120,width=520,bg=top_right_frame_bg,bd=1,relief=FLAT)
frame2.place(x=180,y=0)
frame3= Frame(app,height=30,width=700,bg='black',bd=1,relief=RAISED)
frame3.place(x=0,y=120)

#Entry Box

pincode_text_var=StringVar()
pincode_text=Entry(app,width=11,bg='#eaf2ae',fg='black', font='verdana 11',textvariable=pincode_text_var)
pincode_text.place(x=220,y=40)
pincode_text['textvariable']=pincode_text_var

date_text_var=StringVar()
date_text=Entry(app,width=11,bg='#eaf2ae',fg='black', font='verdana 11',textvariable=date_text_var)
date_text.place(x=380,y=40)
date_text['textvariable']=date_text_var

#Button
Search_Botton_img = PhotoImage( file = 'sear.png' )
Search_Botton=Button(app,bg=top_right_frame_bg,relief=FLAT,command = search_vaccine_avl ,image=Search_Botton_img, height=100, width=120)
Search_Botton.place(x=555,y=0)

# Labels
label_date_now = Label(text="Current Date", bg = top_left_frame_bg, font = 'Verdana 12 bold')
label_date_now.place(x=20, y=40)

label_time_now = Label(text="Current Time", bg = top_left_frame_bg, font = 'Verdana 12')
label_time_now.place(x=20, y=60)

label_pincode = Label(text="Pincode", bg = top_right_frame_bg, font = 'Verdana 11')
label_pincode.place(x=220, y=15)

label_date = Label(text="Date", bg = top_right_frame_bg, font = 'Verdana 11')
label_date.place(x=380, y=15)

label_dateformat = Label(text="[dd-mm-yyyy]", bg = top_right_frame_bg, font = 'Verdana 7')
label_dateformat.place(x=420, y=18)

label_search_vacc = Label(text="Search \nAvailable Vaccine", bg = top_right_frame_bg, font = 'Verdana 8')
label_search_vacc.place(x=570, y=70)

label_head_result = Label(text=" Status       \tCentre-Name\t              Age-Group    Vaccine       Dose_1     Dose_2     Total", bg = 'black', fg='white', font = 'Verdana 8 bold')
label_head_result.place(x=10, y=125)

## TEXT BOX
result_box_avl = Text(app, height = 20, width = 8, bg='#7a6c01',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_avl.place(x= 3 , y= 152)

result_box_cent = Text(app, height = 20, width = 30, bg='#7a6c01',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_cent.place(x= 75 , y= 152)

result_box_age = Text(app, height = 20, width = 8, bg='#7a6c01',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_age.place(x= 330 , y= 152)

result_box_vacc = Text(app, height = 20, width = 10, bg='#7a6c01',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_vacc.place(x= 400 , y= 152)

result_box_D1 = Text(app, height = 20, width = 7, bg='#7a6c01',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_D1.place(x= 490 , y= 152)

result_box_D2 = Text(app, height = 20, width = 7, bg='#7a6c01',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_D2.place(x= 555 , y= 152)

result_box_D1_D2 = Text(app, height = 20, width = 7, bg='#7a6c01',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_D1_D2.place(x= 630 , y= 152)

def update_clock():

	raw_TS=datetime.now(IST) #fetchs current time#raw timestamp
	date_now=raw_TS.strftime("%d %b %Y")#converts it into desired string format
	time_now=raw_TS.strftime("%H:%M:%S")#add %P IF IN am pm
	label_date_now.config(text=date_now)#adding it to the lablel
	label_time_now.config(text=time_now)
	label_time_now.after(1000,update_clock)#after every one second update time


update_clock()


def insert_today_date():
	raw_TS=datetime.now(IST)
	formatted_now = raw_TS.strftime("%d-%m-%Y")
	date_text_var.set(formatted_now)


# Check Box 
chkbox_today_var = IntVar()
today_date_chkbox = Checkbutton(app, text='Today', bg= top_right_frame_bg, variable=chkbox_today_var, onvalue= 1, offvalue=0, command = insert_today_date)
today_date_chkbox.place(x= 375, y= 65)


    

# Detect Automatic Pincode

def fill_pincode_with_radio():
    curr_pincode = get_pincode_ip_service(url)
    pincode_text_var.set(curr_pincode)


url = 'https://ipinfo.io/postal'
def get_pincode_ip_service(url):
    response_pincode = requests.get(url).text #get requests to  the server=> convert it into text(.text)
    return response_pincode #display the text

# Radio Buttons
curr_loc_var = StringVar()
radio_location = Radiobutton(app, text="Current location", bg= top_right_frame_bg, variable= curr_loc_var, value = curr_loc_var, command = fill_pincode_with_radio)
radio_location.place(x=215, y=65)






#Clear all  the data once used before appearing another data
def clear_result_box():
    result_box_avl.delete('1.0', END)
    result_box_cent.delete('1.0', END)
    result_box_age.delete('1.0', END)
    result_box_vacc.delete('1.0', END)
    result_box_D1.delete('1.0', END)
    result_box_D2.delete('1.0', END)
    result_box_D1_D2.delete('1.0', END)





app.mainloop()