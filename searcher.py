from bs4 import BeautifulSoup
from selenium import webdriver #pip install selenium
from re import compile
import time
import datetime as dt
from speedtest import Speedtest #pip install speedtest-cli
from os import path 
if __name__ =="__main__":
    print('please don\'t direct run crawler')
else:
    print('importing crawler...')
    time.sleep(0.05)
    print('imported successfully')

airplanes_trip =0
airplanes_agoda =0
airplanes_wingon =0

class AirplaneInfo: #class of data
    def __init__(self,plane_id, website, airline_name, departure_time, arrival_time, duration, price, departure_airport, arrival_airport):
        self.plane_id=plane_id
        self.website = website
        self.airline_name = airline_name
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.price = price
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport

    def get_plane_id(self):
        return self.plane_id

    def get_website(self):
        return self.website

    def get_airline_name(self):
        return self.airline_name

    def get_departure_time(self):
        return self.departure_time

    def get_arrival_time(self):
        return self.arrival_time

    def get_duration(self):
        return self.duration

    def get_price(self):
        return self.price

    def get_departure_airport(self):
        return self.departure_airport

    def get_arrival_airport(self):
        return self.arrival_airport

class Air_management: #ADT
    def __init__(self): 
      self.airplane_dict= {}
      #wingontravel
    def web_infor_wingontravel(self, start, destination, go_time, back_time): #create the url
        wingontravel_base_url = 'https://www.wingontravel.com/flight/tickets-roundtrip'
        wingontravel_custom_url = f'{wingontravel_base_url}-{start.lower()}-{destination.lower()}?outbounddate={go_time}&inbounddate={back_time}&fromairport=&toairport=&adults=1&children=0&cabintype=tourist'
        return wingontravel_custom_url
        
    def get_airplane_info_wingontravel(self, wingontravel_custom_url):
        #driver = webdriver.Chrome() 
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.get(wingontravel_custom_url) #open the web of the url
        print('crawler is working...')

        last_height = driver.execute_script('return document.body.scrollHeight') #get the height of the website

        while True:
            for i in range(1, 20):
                driver.execute_script(f'window.scrollTo(0, {last_height*i/12});')
                if download_speed<3: #avoid network speed too low make accidently close the website
                    time.sleep(2)
                else:
                    time.sleep(1)
            new_height = driver.execute_script('return document.body.scrollHeight') #get the latest height of the webiste
            if new_height == last_height:
                break
            last_height = new_height

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        global airplanes_wingon
        airplanes_wingon = soup.find_all('div', class_='flight flight-list-item')

        for airplane in airplanes_wingon: #find the airplane information accroding to the html of website
            website = wingontravel_custom_url
            airline_name = airplane.find('span', class_='el-popover__reference').text.strip() if airplane.find('span', class_='el-popover__reference') else 'N/A' # find the data in html if not return N/A
            departure_time = airplane.find('div', attrs ={'class':'departure-sec','class':'time-detail'}).text.strip() if airplane.find('div', attrs ={'class':'departure-sec','class':'time-detail'})else 'N/A'
            arrival_time = airplane.find('div', attrs={'class':'arrival-sec'}).text.split('機場')[0][0:5] if airplane.find('div', attrs={'class':'arrival-sec'})else 'N/A' 
            duration = airplane.find('div', class_='flight-transit flight-transit-direct').text.strip() if airplane.find('div', class_='flight-transit flight-transit-direct') else 'N/A'
            price = airplane.find('span', class_='price-sec__amount').text.strip().replace(",", '') if airplane.find('span', class_='price-sec__amount') else 'N/A' 
            departure_airport = airplane.find('span', class_='airport-code el-popover__reference').text.strip() +' '+ airplane.find('span', class_='airport-terminal').text.strip() if airplane.find('span', class_='airport-code el-popover__reference') else 'N/A'
            arrival_airport = airplane.find('div', attrs={'class':'arrival-sec'}).text.split('機場')[1].replace('T', ' T') if airplane.find('div', attrs={'class':'arrival-sec'})else 'N/A'
            plane_id = airplane.find('span', class_='ref-text el-popover__reference').text.strip() if airplane.find('span', class_='ref-text el-popover__reference') else 'N/A'

            new_plane = AirplaneInfo(
                plane_id,
                website,
                airline_name,
                departure_time,
                arrival_time,
                duration,
                int(price),
                departure_airport,
                arrival_airport
            )
            self.airplane_dict[plane_id] = new_plane # store new_plane infor using plane id as a key into hash table

        driver.quit()

      #agoda
    def web_infor_agoda(self, start, destination, go_time, back_time):#ditto
        agoda_base_url = 'https://www.agoda.com/zh-hk/flights/results'
        agoda_custom_url = f'{agoda_base_url}?tag=d6fcd095-e1e3-7daf-821e-fcd388164f54&gclid=CjwKCAjwwr6wBhBcEiwAfMEQsxgQNJNQQzC90nu07BTYyKbSXbOAJ1Gnp-6860FN045pu5GyRId2vhoCHnEQAvD_BwE&site_id=1891459&departureFrom={start}&departureFromType=1&arrivalTo={destination}&arrivalToType=1&departDate={go_time}&returnDate={back_time}&searchType=2&cabinType=Economy&adults=1&sort=8'
        return agoda_custom_url

    def get_airplane_info_agoda(self, agoda_custom_url):
        driver = webdriver.Chrome() 
        driver.minimize_window()
        driver.get(agoda_custom_url)
        print('crawler is working...')

        last_height = driver.execute_script('return document.body.scrollHeight')
        while True:
            if detail_mode == True:
                for i in range(1, 20):
                    driver.execute_script(f'window.scrollTo(0, {last_height*i/12});')
                    if download_speed<2:
                        time.sleep(2)
                    else:
                        time.sleep(1)
                new_height = driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                last_height = new_height
                
            else:
            
                for i in range(1, 10):
                    driver.execute_script(f'window.scrollTo(0, {last_height*i/12});')
                    if download_speed<3:
                        time.sleep(2)
                    else:
                        time.sleep(1)
                new_height = driver.execute_script('return document.body.scrollHeight')
                if new_height == last_height:
                    break
                last_height = new_height

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        global airplanes_agoda
        airplanes_agoda = soup.find_all('div', class_=compile('sc-fzoxKX jXmLAO'))

        for airplane in airplanes_agoda:#find the airplane information accroding to the html of website
            website = agoda_custom_url
            airline_name = airplane.find('p', {'data-testid':'carrier-name'}).text.strip() if airplane.find('p', {'data-testid':'carrier-name'}) else 'N/A'
            departure_time = airplane.find('h3', {'data-testid':'departure-time'}).text.strip() if airplane.find('h3', {'data-testid':'departure-time'}) else 'N/A'
            arrival_time = airplane.find('div', {'data-testid':'arrival-time'}).text.strip() if airplane.find('div', {'data-testid':'arrival-time'}) else 'N/A'
            duration = airplane.find('p', {'data-testid':'duration'}).text.strip() if airplane.find('p',{'data-testid':'duration'}) else 'N/A'
            price = airplane.find('span', class_='sc-fzpans sc-fzplWN jCUxHt').text.strip().replace(",", '') if airplane.find('span', class_='sc-fzpans sc-fzplWN jCUxHt') else 'N/A'
            departure_airport = airplane.find('p', class_='sc-fzpans sc-fzplWN koEkfC').text.strip() if airplane.find('p', class_='sc-fzpans sc-fzplWN koEkfC') else 'N/A'
            arrival_airport = airplane.find('p', {'data-testid':'destination'}).text.strip() if airplane.find('p', {'data-testid':'destination'}) else 'N/A'
            plane_id = airplane.find('p', {'data-testid':'flight-number'}).text.strip() if airplane.find('p', {'data-testid':'flight-number'}) else 'N/A'
            if plane_id == 'N/A':
                pass
            else:
                plane_id = plane_id.split(' • ')
                #print(plane_id)
                plane_id = plane_id[1]

                new_plane = AirplaneInfo(
                plane_id,
                website,
                airline_name,
                departure_time,
                arrival_time,
                duration,
                int(price),
                departure_airport,
                arrival_airport
            )
                self.airplane_dict[plane_id] = new_plane
          
        driver.quit()  

    #trip.com
    def web_infor_trip(self,start, destination, go_time, back_time):#ditto
        tripcom_base_url = 'https://hk.trip.com/flights/ShowFareFirst?curr=HKD&flighttype=RT'
        trip_custom_url = f'{tripcom_base_url}&dcity={start}&acity={destination}&startdate={go_time}&returndate={back_time}&to=list'
        return trip_custom_url

    def get_airplane_info_trip(self,trip_custom_url):
        #driver = webdriver.Chrome()  
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        driver.get(trip_custom_url)
        print('crawler is working...')

        last_height = driver.execute_script('return document.body.scrollHeight')

        while True:
            for i in range(1, 20):
                driver.execute_script(f'window.scrollTo(0, {last_height*i/12});')
                if download_speed<2:
                    time.sleep(1)
                else:
                    time.sleep(0.25)
            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == last_height:
                break
            last_height = new_height

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        global airplanes_trip
        airplanes_trip = soup.find_all('div', class_='result-item J_FlightItem')
        

        for airplane in airplanes_trip:
            website = trip_custom_url
            airline_name = airplane.find('div', class_='flights-name').text.strip() if airplane.find('div', class_='flights-name') else 'N/A'
            departure_time = airplane.find('span', {'data-testid': compile(r'flight-time-\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')}).text.strip() if airplane.find('span', {'data-testid': compile(r'flight-time-\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')}) else 'N/A'
            arrival_time = airplane.find_all('span', {'data-testid': compile(r'flight-time-\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')})[-1].text.strip() if airplane.find_all('span', {'data-testid': compile(r'flight-time-\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')}) else 'N/A'
            duration = airplane.find('div', {'data-testid': 'flightInfoDuration'}).text.strip() if airplane.find('div', {'data-testid': 'flightInfoDuration'}) else 'N/A'
            price = airplane.find('span', class_=compile('ThemeColor8 f-20 o-price-flight_.{3} no-cursor_.{3}')).text.strip().split('$')[1].replace(",", '') if airplane.find('span', class_=compile('ThemeColor8 f-20 o-price-flight_.{3} no-cursor_.{3}')) else 'N/A'
            departure_airport = airplane.find_all('span', class_=compile(r'flight-info-stop__code_.{3}'))[0].text.strip() if airplane.find_all('span', class_=compile(r'flight-info-stop__code_.{3}')) else 'N/A'
            arrival_airport = airplane.find_all('span', class_=compile(r'flight-info-stop__code_.{3}'))[-1].text.strip() if airplane.find_all('span', class_=compile(r'flight-info-stop__code_.{3}')) else 'N/A'
            plane_id = airplane.find('div', class_=compile(r'select-area_.{3}'))['data-shoppingid'].split('-')[0]if airplane.find('div', class_=compile(r'select-area_.{3}'))['data-shoppingid'].split('-')[0]else 'N/A'
                    

            new_plane = AirplaneInfo(
            plane_id,
            website,
            airline_name,
            departure_time,
            arrival_time,duration,
            int(price),
            departure_airport,
            arrival_airport
            )
            self.airplane_dict[plane_id] = new_plane
          
        driver.quit()  
   
    def display(self,plane):
                print(f'Website: {plane.get_website()}')
                print(f'ID: {plane.get_plane_id()}')
                print(f'Airline: {plane.get_airline_name()}')
                print(f'Departure Time: {plane.get_departure_time()}')
                print(f'Arrival Time: {plane.get_arrival_time()}')
                print(f'Duration: {plane.get_duration()}')
                print(f'Price: HK$ {plane.get_price()}')
                print(f'Departure Airport: {plane.get_departure_airport()}')
                print(f'Arrival Airport: {plane.get_arrival_airport()}')
                print('---')
    
    '''
    def sort_and_print(plane_total):
        listed = list(plane_total.airplane_dict.values())
        listed.sort(key =lambda plane: plane.get_price())
        for plane in listed:
            plane_total.display(plane)
    '''
    def sort_and_cheapest(plane_total):
        listed = list(plane_total.airplane_dict.values())
        listed.sort(key =lambda plane: plane.get_price()) # As Professor Roy Li said bulid in sort will be faster than others sort so we use build-in sort
        '''
        for plane in listed:
            print("CHEAPEST!!!")
            plane_total.display(plane)
            break
        '''
        return listed

        
    def add_into_one(trip_planes,agoda_planes,wingon_planes,plane_total): #add 3 webiste infor into one for display
        
        if len(airplanes_trip) !=0:
            for plane_id in trip_planes.airplane_dict:
                plane = trip_planes.airplane_dict[plane_id]
                plane_id = f'{plane_id}_TRIP'
                plane_total.airplane_dict[plane_id] = plane
        if len(airplanes_agoda) !=0:
            for plane_id in agoda_planes.airplane_dict:
                plane = agoda_planes.airplane_dict[plane_id]
                plane_id = f'{plane_id}_AGODA'
                plane_total.airplane_dict[plane_id] = plane
        if len(airplanes_wingon) !=0: #find found plane ===0 wont do 
            for plane_id in wingon_planes.airplane_dict:
                plane = wingon_planes.airplane_dict[plane_id]
                plane_id = f'{plane_id}_WINGON'
                plane_total.airplane_dict[plane_id] = plane

    def cheapest_in_each_web(trip_planes,agoda_planes,wingon_planes): #function for dsiaply cheapest in each web
        cheapest_price = None
        for plane_id in trip_planes.airplane_dict:
            plane = trip_planes.airplane_dict[plane_id]
            if cheapest_price==None or plane.get_price() == cheapest_price:
                cheapest_price = plane.get_price()
                print("Cheapest in trip.com")
                print(f'Website: {plane.get_website()}')
                print(f'ID: {plane.get_plane_id()}')
                print(f'Airline: {plane.get_airline_name()}')
                print(f'Departure Time: {plane.get_departure_time()}')
                print(f'Arrival Time: {plane.get_arrival_time()}')
                print(f'Duration: {plane.get_duration()}')
                print(f'Price: HK$ {plane.get_price()}')
                print(f'Departure Airport: {plane.get_departure_airport()}')
                print(f'Arrival Airport: {plane.get_arrival_airport()}')
                print('---')
            else:
                break
        cheapest_price =None    
        for plane_id in agoda_planes.airplane_dict:
            plane = agoda_planes.airplane_dict[plane_id]
            if cheapest_price==None or plane.get_price() == cheapest_price:
                cheapest_price= plane.get_price()
                print("Cheapest in agoda")
                print(f'Website: {plane.get_website()}')
                print(f'ID: {plane.get_plane_id()}')
                print(f'Airline: {plane.get_airline_name()}')
                print(f'Departure Time: {plane.get_departure_time()}')
                print(f'Arrival Time: {plane.get_arrival_time()}')
                print(f'Duration: {plane.get_duration()}')
                print(f'Price: HK$ {plane.get_price()}')
                print(f'Departure Airport: {plane.get_departure_airport()}')
                print(f'Arrival Airport: {plane.get_arrival_airport()}')
                print('---')
            else:
                break
        cheapest_price = None   
        for plane_id in wingon_planes.airplane_dict:
            plane = wingon_planes.airplane_dict[plane_id]
            if cheapest_price==None or plane.get_price() == cheapest_price:
                cheapest_price= plane.get_price()
                print("Cheapest in wingontravel")
                print(f'Website: {plane.get_website()}')
                print(f'ID: {plane.get_plane_id()}')
                print(f'Airline: {plane.get_airline_name()}')
                print(f'Departure Time: {plane.get_departure_time()}')
                print(f'Arrival Time: {plane.get_arrival_time()}')
                print(f'Duration: {plane.get_duration()}')
                print(f'Price: HK$ {plane.get_price()}')
                print(f'Departure Airport: {plane.get_departure_airport()}')
                print(f'Arrival Airport: {plane.get_arrival_airport()}')
                print('---')
            else:
                break

        




class Node: #BINARY TREE    
    def __init__(self, plane_id, website, airline_name, departure_time, arrival_time, duration, price, departure_airport, arrival_airport):
        self.plane_id = plane_id
        self.website = website
        self.airline_name = airline_name
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.price = price
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.left = None
        self.right = None

    def insert_price(self, plane_id, website, airline_name, departure_time, arrival_time, duration, price, departure_airport, arrival_airport):# insert child node base on price
        
        if price < self.price:#  samller put in left child node
            if self.left is None:
                self.left = Node(website,plane_id,  airline_name, departure_time, arrival_time, duration, price, departure_airport, arrival_airport)# create one node cuz dont have node there
                return self.left
            else:
                self.left.insert_price(website,plane_id, airline_name, departure_time, arrival_time, duration, price, departure_airport, arrival_airport)#recursion
        elif price >= self.price:# bigger or same put in right child node
            if self.right is None:
                self.right = Node(website, plane_id,  airline_name, departure_time, arrival_time, duration, price, departure_airport, arrival_airport)# create one node cuz dont have node there
                return self.right
            else:
                self.right.insert_price(website, plane_id, airline_name, departure_time, arrival_time, duration, price, departure_airport, arrival_airport)#recursion

    def asc_traversal(self): #display in order
        if self.left:
            self.left.asc_traversal()
        print(f'{self.website}\n{self.plane_id}\n HKD{self.price}\n Airline:{self.airline_name}\n Departure Time :{self.departure_time}\n Arrival Time :{self.arrival_time}\nDuration :{self.duration}\n Departure Airport :{self.departure_airport} \nArrival Airport:{self.arrival_airport}\n---')  
        if self.right:
            self.right.asc_traversal() #recursion
    def pre_traversal(self):#display pre oder how the tree insert 
        if self.left:
            self.left.asc_traversal() #recursion
        print(f'{self.website}\n{self.plane_id}\n HKD{self.price}\n Airline:{self.airline_name}\n Departure Time :{self.departure_time}\n Arrival Time :{self.arrival_time}\nDuration :{self.duration}\n Departure Airport :{self.departure_airport} \nArrival Airport:{self.arrival_airport}\n---')  
        if self.right:
            self.right.pre_traversal()
class Node_ID: #BINARY TREE 
    def __init__(self, plane_id, website, airline_name, departure_time, arrival_time, duration, price, departure_airport, arrival_airport):
        self.plane_id = plane_id
        self.website = website
        self.airline_name = airline_name
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.price = price
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.left = None
        self.right = None

    def insert_ID(self, plane_id, website, airline_name, departure_time, arrival_time, duration, price, departure_airport, arrival_airport):# insert child node base on plane_id
        
        if plane_id < self.plane_id:# bigger or same put in right child node
            if self.left is None:
                self.left = Node_ID(website,plane_id,  airline_name, departure_time, arrival_time, duration, price, departure_airport, arrival_airport) #build node
                return self.left
            else:
                self.left.insert_ID(website,plane_id, airline_name, departure_time, arrival_time, duration, price, departure_airport, arrival_airport)#recursion go left
        elif plane_id >= self.plane_id:# bigger or same put in right child node
            if self.right is None:
                self.right = Node_ID(website, plane_id,  airline_name, departure_time, arrival_time, duration, price, departure_airport, arrival_airport)#build node
                return self.right
            else:
                self.right.insert_ID(website, plane_id, airline_name, departure_time, arrival_time, duration, price, departure_airport, arrival_airport)#recursion go right

    def find_ID(self, target_plane_id):
        
        if self.plane_id >target_plane_id :
            if self.left is None:
                return False
            else:
                self.left.find_ID(target_plane_id)  # Go left
        elif  self.plane_id < target_plane_id:
            if self.right is None:
                return False
            else:
                self.right.find_ID(target_plane_id)  # Go right
        else:
                return True            
            
            

    # test

'''
for country_name in country:
    x = country_name.split("\t")
    country_code.append(x)
for place in country_code:
    place.remove(place[1])
    y = place[1]
    z = y.replace("\n","")
    place[1]= z

    '''
'''
def start(airports):#search name tbc    
    country_1 = input("Enter start city in full name: ")
    for full_name in airports:
        if country_1.lower() == full_name[0].lower():
            flag = True
            code = full_name[1]
            break
    if flag:
        return code
    else:
        print("City not found ! Please try again")
        start(airports)

def destination(airports):
    flag = False 
    code = ""          
    country_2 = input("Enter departure city in full name: ")
    for full_name in airports:
        if country_2.lower() == full_name[0].lower():
            flag = True
            code = full_name[1]
            break
    if flag:
        return code
    else:
        print("City not found ! Please try again")
        destination(airports)
'''
'''
def departure_d():
    current = datetime.datetime.now()
    departure = str(input("Enter departure date:(YYYY-MM-DD) "))
    d2 = datetime.datetime.strptime(departure, "%Y-%m-%d") 
    if (d2 - current).days <= 0:
        print('warning: cannot travel to/from past!') 
        departure()
    else:
        return departure

def return_d(departure):
    return_d = str(input("Enter return date:(YYYY-MM-DD) "))  
    d1 = datetime.datetime.strptime(departure, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(return_d, "%Y-%m-%d") 
    if (d2 - d1).days <=0:
        print('warning: cannot travel to/from past!') 
        return_d(departure_d)
    else:
        return return_d
'''
def _daysapart(outbound,leave):
    return (leave-outbound).days

def checkdate(outboundcal, inboundcal):
    current = dt.datetime.now().date() #a date object for today
    fromtoday = _daysapart(current,outboundcal)
    traveldays = _daysapart(outboundcal,inboundcal)
    if traveldays<0 or fromtoday<0:
        return False
    else:
        return True

def codesofcity(city):
    a_of_city = []
    for i in range(len(airports)):
        if airports[i][0].lower()==city.lower():
            a_of_city.append(airports[i][1])
    return a_of_city


initmsg = "Testing download speed..."
#download_speed = Speedtest(secure=True).download() / 1000000
download_speed = Speedtest(secure=True).download() / 1000000 
msg1 = f"Download Speed:{round(download_speed,2)} Mbps"
#upload_speed = speedtest.Speedtest().upload() / 1000000 
#CC GUI wanna show network speed or not
detail_mode = False

try:
    fin = open(r'country_code.txt', 'r')
except:
    fpath = path.join(path.dirname(__file__),"airportlist.txt")
    fin = open(fpath,'r')
    
airportlist = fin.readlines()
fin.close()

airports = []
citychoice = []
airportchoice=[]

for airport in airportlist:
    try:
        city, dummy, code = airport.strip().split('\t')
    except:
        print('errpr: '+airport)
    if city not in citychoice:
        citychoice.append(city)
    airportchoice.append(code)
    airports.append(tuple([city,code]))

#==============================
#start_city = start(airports)
#destination_city = destination(airports)
#
#departure_date = departure_d()
#return_date = return_d(departure_date)

