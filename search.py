print('Please wait...')
print('This will take around 1 minute')

from tkinter import *
from tkcalendar import DateEntry #pip install tkcalendar
from tkinter import ttk
import tksheet #pip install tksheet
import math
import datetime
import searcher # our module for searching flight tickets
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver

# MAPSetting

import folium
import googlemaps
from geopy.distance import geodesic
from tkhtmlview import HTMLLabel
import webbrowser
import os

API_KEY = 'AIzaSyDxFfFC6vBzAwCAbAA8cQ8ay2O-3hPRL1w'

map_client = googlemaps.Client(API_KEY)



def onselect_d(evt): #react to selection
    w = evt.widget
    index = int(w.curselection()[0])
    txtvalue = w.get(index)
    d_city_e.delete(0,"end")
    d_city_e.insert(0,txtvalue)
    update_d_code(searcher.codesofcity(d_city_e.get()))

def onselect_code_d(evt): #react to selection
    w = evt.widget
    index = int(w.curselection()[0])
    txtvalue = w.get(index)
    d_code_e.delete(0,"end")
    d_code_e.insert(0,txtvalue)

def checkkey_d_code(event): 
    value = event.widget.get()
    if value == '': #if nothing have been chosen
        data = searcher.codesofcity(d_city_e.get())
    else:
        data = [choices for  choices in searcher.codesofcity(d_city_e.get()) if value.lower() in choices.lower()]
    update_d_code(data)

def update_d_code(data):#update the ones showing
    d_code_select.delete(0, 'end')
    for item in data:
        d_code_select.insert('end', item)

def confirm_departure_airport():
    global departure_airport
    if_valid=False
    for airportcode in searcher.airportchoice:
        if d_code_e.get().lower() == airportcode.lower():
            departure_airport = d_code_e.get()
            d_code_e.config(state='disabled')
            if_valid=True
            msg4.config(text='')
            #print(depcal.get_date())
            break
    if not if_valid:
        msg4.config(text='Warning: wrong airport code')

def trytoproceed(): #check if dates and airports are valid
    global departure_date,return_date
    html_label = HTMLLabel(searchwindow, html = '')
    open_button = Button(searchwindow, text="View Fly Map", command=openmap)
    open_button.place(x=175, y=0)

    if not(departure_airport and arrival_airport): #if haven't choose airports, exit the function
        msg6.config(text='departure airport and/or arrival airport not selected')
        return
    
    departure_date, return_date = depcal.get_date(),retcal.get_date()

    if not searcher.checkdate(departure_date, return_date): #check if input dates is valid
        errormsg.config(text='cannot travel from/to the past!',fg='red')
        return #exit if invalid
    import random
    random_plane =random.randint(0,4)
    if random_plane == 1:
        pic ='✈'
    if random_plane == 2:
        pic ='✈️'
    if random_plane == 3:
        pic ='🛩️'
    else:
        pic='.'
    msg6.config(text=f'Please wait{pic}{pic}{pic}',fg='red', font='helv 24')
    msg6.place(x=250,y=300)


    for eachwidget in widgetstoclear: #hide widgets
        eachwidget.place_forget()
    
    for eachbtndentry in btn_and_dentry: #destroy widgets
        eachbtndentry.destroy()

    #proceed to search flight tickets
    searchargs = [departure_date,return_date]
    searchwindow.after(1000,proceedsearch,*searchargs)
    

def proceedsearch(departuredate,returndate): #proceed to search for flight tickets
 try:
    AIRPLANE_TRIP = searcher.Air_management()
    trip_custom_url = AIRPLANE_TRIP.web_infor_trip(departure_airport, arrival_airport, departuredate, returndate)
    AIRPLANE_TRIP.get_airplane_info_trip(trip_custom_url)
    for plane_id in AIRPLANE_TRIP.airplane_dict:
        plane = AIRPLANE_TRIP.airplane_dict[plane_id]
        #AIRPLANE_TRIP.display(plane)
    print('Please be patient... 1/3 done...')
    global AIRPLANE_AGODA
    AIRPLANE_AGODA = searcher.Air_management()
    agoda_custom_url = AIRPLANE_AGODA.web_infor_agoda(departure_airport, arrival_airport, departuredate, returndate)
    AIRPLANE_AGODA.get_airplane_info_agoda(agoda_custom_url)
    for plane_id in AIRPLANE_AGODA.airplane_dict:
        plane = AIRPLANE_AGODA.airplane_dict[plane_id]
        #AIRPLANE_AGODA.display(plane)
    print('Please be patient... 2/3 done...')
    AIRPLANE_WINGON = searcher.Air_management()
    wingontravel_custom_url = AIRPLANE_WINGON.web_infor_wingontravel(departure_airport, arrival_airport, departuredate, returndate)
    AIRPLANE_WINGON.get_airplane_info_wingontravel(wingontravel_custom_url)
    for plane_id in AIRPLANE_WINGON.airplane_dict:
        plane = AIRPLANE_WINGON.airplane_dict[plane_id]
        #AIRPLANE_WINGON.display(plane)
    print('Please be patient... almost done...')
    AIRPLANE_TOTAL =searcher.Air_management()
    searcher.Air_management.add_into_one(AIRPLANE_TRIP,AIRPLANE_AGODA,AIRPLANE_WINGON,AIRPLANE_TOTAL) #add all searched flights to airplane_total
    #searcher.Air_management.sort_and_print(AIRPLANE_TOTAL)
    #searcher.Air_management.cheapest_in_each_web(AIRPLANE_TRIP,AIRPLANE_AGODA,AIRPLANE_WINGON)
    root_bulit_price =False
    root = None
    tree_time =datetime.datetime.now()
    for plane in AIRPLANE_TOTAL.airplane_dict:
                plane = AIRPLANE_TOTAL.airplane_dict[plane]

                if not root_bulit_price:
                    root =searcher.Node(plane.website,plane.plane_id,plane.airline_name,plane.plane_id,plane.arrival_time,plane.duration,int(plane.price),plane.departure_airport,plane.arrival_airport)
                    root_bulit_price =True
                if root_bulit_price:
                    root.insert_price(plane.website,plane.plane_id,plane.airline_name,plane.departure_time,plane.arrival_time,plane.duration,int(plane.price),plane.departure_airport,plane.arrival_airport)
    root_bulit_price =False
    root.asc_traversal()
    tree_end_time =datetime.datetime.now()
    sort_time= datetime.datetime.now()
    sorted_by_price_list = searcher.Air_management.sort_and_cheapest(AIRPLANE_TOTAL) #return a sorted list of planes(obj)
    display_result(sorted_by_price_list)
    sort_end_time =datetime.datetime.now()

    print(f'Sort time:{sort_end_time -sort_time}s')
    print(f'Tree time:{tree_end_time-tree_time}s')
 except (TypeError, AttributeError):
      if len ( AIRPLANE_TOTAL.airplane_dict) ==0:
        print('Opps ! No plane has been found according to your chosen attributes')
        msgx =Label(searchwindow,text='')
        msgx.config(text='Opps ! No plane has been found according to your chosen attributes',fg='red', font='helv 18')
        msgx.place(x=0,y=300)
      else:
          pass
    

def checkkey_d_city(event): #react to keyboard
    value = event.widget.get()
    if value == '': #if nothing have been chosen
        data = []+searcher.citychoice
    else:
        data = [choices for choices in searcher.citychoice if value.lower() in choices.lower()]
    update_d_city(data)

def update_d_city(data):#update the ones showing
    d_city_select.delete(0, 'end')
    for item in data:
        d_city_select.insert('end', item)

def checkkey_a_code(event): 
    value = event.widget.get()
    
    if value == '': #if nothing have been chosen
        data = searcher.codesofcity(a_city_e.get())
    else:
        data = [choices for  choices in searcher.codesofcity(a_code_e.get()).remove(departure_airport) if value.lower() in choices.lower()]
    update_a_code(data)

def update_a_code(data):#update the ones showing in listbox
    a_code_select.delete(0, 'end')
    for item in data:
        a_code_select.insert('end', item)

def onselect_code_a(evt): #show the selected one to the entry box
    w = evt.widget
    index = int(w.curselection()[0])
    txtvalue = w.get(index)
    a_code_e.delete(0,"end")
    a_code_e.insert(0,txtvalue)
    
def onselect_a(evt): #show the selected one to the entry box
    w = evt.widget
    index = int(w.curselection()[0])
    txtvalue = w.get(index)
    a_city_e.delete(0,"end")
    a_city_e.insert(0,txtvalue)
    update_a_code(searcher.codesofcity(a_city_e.get()))

def checkkey_a_city(event):
    value = event.widget.get()
    if value == '': #if nothing have been chosen
        data = []+searcher.citychoice
    else:
        data = [choices for  choices in searcher.citychoice if value.lower() in choices.lower()]
    update_a_city(data)

def update_a_city(data): #update the list to be selected
    a_city_select.delete(0, 'end')
    for item in data:
        a_city_select.insert('end', item)

def confirm_arrival_airport(): #check if airport code is valid
    global arrival_airport
    if_valid=False
    for airportcode in searcher.airportchoice:
        if a_code_e.get().lower() == airportcode.lower():
            arrival_airport = a_code_e.get()
            a_code_e.config(state='disabled')
            if_valid=True
            msg5.config(text='')
            break
    if not if_valid:
        msg5.config(text='Warning: wrong airport code')
    
def changepage(event): #update the list showing in sheet
    curpage = int(pageselect.get())
    fromdataindex = (curpage-1)*row
    if curpage==maxpage:
        todataindex=dataqty
        showing_l.config(text=f'now showing {fromdataindex + 1} - {dataqty} out of {dataqty}')
    else:
        todataindex=curpage*row
        showing_l.config(text=f'now showing {fromdataindex + 1} - {todataindex} out of {dataqty}')
    sheet.set_sheet_data(datalst[fromdataindex:todataindex])

def display_result(sortedlist): #create the sheet for displaying search results
    global pageselect,row,maxpage,dataqty,showing_l,sheet,datalst
    titles = ['Flight no.','Departure','Arrival','Airline','Price (HKD)','More info']
    row=25
    
    sheet = tksheet.Sheet(searchwindow,theme="black",
                height=620,
                width=750)
    sheet.place(x=10,y=30)

    sheet.enable_bindings(("single_select", #config for sheet
                           "row_select",
                           "column_width_resize",
                           "arrowkeys",
                           "right_click_popup_menu",
                           "rc_select",
                           "copy",
                           "vertical"))
    sheet.headers(titles)

    #preparing data to be shown
    datalst = []
    for plane in sortedlist:
        departure = str(plane.get_departure_time()).strip() + '\t|' + str(plane.get_departure_airport()).strip()
        arrival = str(plane.get_arrival_time()).strip() + '\t|' + str(plane.get_arrival_airport()).strip()
        datalst.append([plane.get_plane_id(), departure, arrival, plane.get_airline_name(), plane.get_price(),plane.get_website()])
        
    #create widgets for switching page
    dataqty = len(datalst)
    maxpage=math.ceil(dataqty/row)

    pagelst = [x for x in range(1,maxpage+1)]

    pageselect = ttk.Combobox(state='readonly',values=pagelst,width=3)
    pageselect.place(x=560,y=0)
    pageselect.current(0)#set default option to index0
    pageselect.bind("<<ComboboxSelected>>",changepage)

    curpage = pageselect.current()+1
    if(dataqty):
        fromdataindex = (curpage-1)*row
    else:
        fromdataindex=0

    if dataqty>=row:
        todataindex=curpage*row
    else:
        todataindex=dataqty

    #showing status
    showing_l = Label(text=f'now showing {fromdataindex + 1} - {todataindex} out of {dataqty}')
    showing_l.place(x=610,y=00)

    Label(searchwindow,text=f'Outbound: {departure_date}    Inbound: {return_date}    Seat: Economy').place(x=300,y=0)

    sheet.set_sheet_data(datalst[fromdataindex:todataindex]) #show search results
    
    
    
        #---------------------------------
  
    # Map API part
    try:
        dep_ap = map_client.geocode(str(plane.get_departure_airport()))
        dep_ap_lat = dep_ap[0]['geometry']['location']['lat']
        dep_ap_lon = dep_ap[0]['geometry']['location']['lng']

        arv_ap = map_client.geocode(str(plane.get_arrival_airport()))
        arv_ap_lat = arv_ap[0]['geometry']['location']['lat']
        arv_ap_lon = arv_ap[0]['geometry']['location']['lng']
    except (IndexError , UnboundLocalError):
        print('Map error')
        #driver = webdriver.Chrome() 

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.get('https://openflights.org/html/apsearch')
        asv_airport =str(plane.get_departure_airport())
        dep_airport = str(plane.get_arrival_airport())
        driver.find_element(By.ID,"iata").send_keys(asv_airport) # send thr aiport code into input box
        driver.find_element(By.XPATH, "//input[@value='Search']").click()  #find the button and click it
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='button'][@value='Load'][contains(@onclick, 'doLoad')]"))).click()#find the button and click it
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'y')))
        sleep(2)
        dep_ap_lat =float(driver.find_element(By.ID, "y").get_attribute('value')) # get lat
        dep_ap_lon =float(driver.find_element(By.ID, "x").get_attribute('value')) #get lon
        driver.find_element(By.XPATH, "//input[@value='Clear']").click()#find the button and click it
        driver.find_element(By.ID,"iata").send_keys(dep_airport)

        driver.find_element(By.XPATH, "//input[@value='Search']").click()#find the button and click it
        load = "//input[@type='button'][@value='Load'][contains(@onclick, 'doLoad')]"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='button'][@value='Load'][contains(@onclick, 'doLoad')]"))).click()#wait the button come out if >10s it will stop like sleep(10) but add wait the button come it will stop the sleep
        sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'y'))) #wait the value come out if >10s it will stop like sleep(10) but add wait the value come it will stop the sleep
        arv_ap_lon = float(driver.find_element(By.ID, "x").get_attribute('value'))
        arv_ap_lat = float(driver.find_element(By.ID, "y").get_attribute('value'))

        driver.close()


    
        #---------------------------------------------------------------------------------------
        
        # Map Part
            
        # Create the variable
        
        center_coord =  [(dep_ap_lat + arv_ap_lat) / 2, (dep_ap_lon + arv_ap_lon) / 2]
        dep_coord =  [dep_ap_lat, dep_ap_lon]
        marker_radius = 5_000
            
        arv_coord = [arv_ap_lat, arv_ap_lon]
            
        line_coord = [
                    dep_coord,
                    arv_coord
            ]
        
        

        # Create a map
        map = folium.Map(center_coord, zoom_start = 3)

            
        # Add a circle marker on the map (Hong Kong Base)
        folium.vector_layers.Circle(
                location = dep_coord,
                tooltip = departure_airport,
                radius = marker_radius,
                color = "red", 
                fill = True,
                fill_color = "red"
            ).add_to(map)
            
            
        # add location marker    
        folium.Marker(
                location = dep_coord,
                tooltip = (departure_airport),
                popup = (f"Departure Airport: {departure_airport}")
            ).add_to(map)    
            
            
        folium.Marker(
                location = arv_coord,
                tooltip = (arrival_airport),
                popup = (f"Arrival Airport: {arrival_airport}")
            ).add_to(map)
            
            
        # calculate the distance of the line
        distance = geodesic(dep_coord, arv_coord).kilometers
            
            
        # add line
        folium.PolyLine(
                line_coord,
                color = "blue",
                weight = "10",
                opacity = 0.8,
                popup = (f"Distance: {distance} kilometers")
            ).add_to(map)
            

        # save the map
        global map_filepath
        map_filepath = "v7/flymap.html" 
        map.save(map_filepath)  
    

    
                

def openmap():
    map_filepath = "flymap.html"
    file_path = os.path.join(os.path.dirname(__file__), map_filepath)
    webbrowser.open(file_path)
    
        
#---------------------------------

    


if __name__ == '__main__':
    #create and config a window
    searchwindow=Tk()
    searchwindow.title('search your flight')
    searchwindow.resizable(0,0)
    searchwindow.geometry("790x640")

    #creating labels
    initmsg = Label(searchwindow,text="Please wait...")
    initmsg.place(x=0,y=0)
    msg1 = Label(searchwindow, text='')
    msg1.place(x=0,y=20)
    errormsg = Label(searchwindow, text='')
    errormsg.place(x=0,y=80)
    msg2 = Label(searchwindow, text='')
    msg2.place(x=0,y=150)
    msg3=Label(searchwindow,text='')
    msg3.place(x=300,y=150)
    msg4=Label(searchwindow,text='')
    msg4.place(x=10,y=500)
    msg5=Label(searchwindow,text='')
    msg5.place(x=400,y=500)
    msg6=Label(searchwindow,text='')
    msg6.place(x=300,y=600)
    

    #creating buttons
    submitbtn = Button(searchwindow,command=trytoproceed,text='Search!')
    submitbtn.place(x=300,y=550)
    a_confirm_btn = Button(searchwindow,command=confirm_departure_airport,text='confirm departure airport')
    a_confirm_btn.place(x=60,y=380)
    d_confirm_btn = Button(searchwindow,command=confirm_arrival_airport,text='Confirm destination airport')
    d_confirm_btn.place(x=330,y=380)

    #widgets for choosing departure airport
    msg2 = Label(searchwindow,text='Departure city:')
    msg2.place(x=10,y=160)
    d_city_e = Entry(searchwindow)
    d_city_e.place(x=10,y=180)
    d_city_e.bind('<KeyRelease>', checkkey_d_city)

    d_city_select = Listbox(searchwindow)
    d_city_select.place(x=10,y=200)
    update_d_city(searcher.citychoice)
    d_city_select.bind('<<ListboxSelect>>', onselect_d)

    msg3 = Label(searchwindow,text='Departure Airport Code:')
    msg3.place(x=140,y=160)
    d_code_e = Entry(searchwindow)
    d_code_e.place(x=140,y=180)
    d_code_e.bind('<KeyRelease>', checkkey_d_code)

    d_code_select = Listbox(searchwindow)
    d_code_select.place(x=140,y=200)
    d_code_select.bind('<<ListboxSelect>>', onselect_code_d)
    update_d_code(searcher.codesofcity(d_city_e.get()))

    #widgets for choosing destination airport
    a=Label(searchwindow,text='Destination city:')
    a.place(x=300,y=160)
    a_city_e = Entry(searchwindow)
    a_city_e.place(x=300,y=180)
    a_city_e.bind('<KeyRelease>', checkkey_a_city)

    a_city_select = Listbox(searchwindow)
    a_city_select.place(x=300,y=200)
    update_a_city(searcher.citychoice)
    a_city_select.bind('<<ListboxSelect>>', onselect_a)

    b=Label(searchwindow,text='Destination airport code:')
    b.place(x=430,y=160)
    a_code_e = Entry(searchwindow)
    a_code_e.place(x=430,y=180)
    a_code_e.bind('<KeyRelease>', checkkey_a_code)

    a_code_select = Listbox(searchwindow)
    a_code_select.place(x=430,y=200)
    a_code_select.bind('<<ListboxSelect>>', onselect_code_a)

    #define initial values for both airports
    departure_airport=None
    arrival_airport=None

    #show download speed
    initmsg.config(text=searcher.msg1)

    #widgets for choosing date
    datemsg1 = Label(searchwindow,text='Please select departure date: ')
    datemsg1.place(x=0,y=40)
    datemsg2 = Label(searchwindow,text='Please select return date: ')
    datemsg2.place(x=0,y=60)

    depcal = DateEntry(searchwindow,selectmode='day',date_pattern='yyyy/mm/dd')
    retcal = DateEntry(searchwindow,selectmode='day',date_pattern='yyyy/mm/dd')
    depcal.place(x=180,y=40)
    retcal.place(x=180,y=60)

    
    #for later use(clear the widgets)
    widgetstoclear = [msg1,msg2,msg3,msg4,msg5,datemsg1,datemsg2,a_code_e,a_code_select,a_city_e,a_city_select,d_code_e,d_code_select,d_city_e,d_city_select,errormsg,a,b]
    btn_and_dentry = [depcal,retcal,submitbtn,a_confirm_btn,d_confirm_btn]

    searchwindow.mainloop()