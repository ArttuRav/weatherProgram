# File name: weatherProgram.py
# Author: Arttu Ravantti 
# Description: 

from calendar import week
import tkinter as tk
from tkinter.font import BOLD
import requests
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
import re
import os
import timeit
from sympy import true
import config
import collections
import urllib.request
import shutil

class WeatherProgram(tk.Tk):

    def __init__(self):
        super().__init__()

        # Creating window
        self.title('Weather program')
        self.resizable(0, 0)
        self.geometry('700x515')
        self['bg'] = 'gray'

        # Labels for error messages
        self.city_not_entered_label = tk.Label(self, text='', font=('lucida', 10), background='gray')
        self.city_not_found_label = tk.Label(self, text='', font=('lucida', 10), background='gray')
        self.nothing_to_update_label = tk.Label(self, text='', font=('lucida', 10), background='gray')

        # Canvas for visuals
        self.canvas_time_date = tk.Canvas(self, bg='gray', height=22, width=125, highlightthickness=1, highlightbackground='black').place(x='12', y='4')
        self.canvas_data = tk.Canvas(self, bg='lightgray', highlightthickness=1, highlightbackground='black', height=400, width=675)

        # Lines for visuals on canvas
        self.canvas_data.create_line(260,0,260,401, fill='gray', width=5) # vertical separator
        self.canvas_data.create_line(0,31,677,31, fill='gray', width=5) # horizontal 1
        self.canvas_data.create_line(0,93,677,93, fill='gray', width=5) # horizontal 2

        # Labels for date and time
        self.date_label = tk.Label(self, text=self.get_date(), font=('lucida', 10), background='gray')
        self.time_label = tk.Label(self, text=self.get_time(), font=('lucida', 10), background='gray')

        # Text labels for data
        self.description_text_label = tk.Label(self, text='DESCRIPTION', font=('calibri', 11, BOLD), background='lightgray').place(x='18', y='138')
        self.temp_text_label = tk.Label(self, text='TEMPERATURE', font=('calibri', 11, BOLD), background='lightgray').place(x='18', y='200')
        self.feels_text_label = tk.Label(self, text='FEELS LIKE', font=('calibri', 11, BOLD), background='lightgray').place(x='18', y='225')
        self.pressure_text_label = tk.Label(self, text='PRESSURE', font=('calibri', 11, BOLD), background='lightgray').place(x='18', y='250')
        self.humidity_text_label = tk.Label(self, text='HUMIDITY', font=('calibri', 11, BOLD), background='lightgray').place(x='18', y='275')
        self.visibility_text_label = tk.Label(self, text='VISIBILITY', font=('calibri', 11, BOLD), background='lightgray').place(x='18', y='300')
        self.windS_text_label = tk.Label(self, text='WIND SPEED', font=('calibri', 11, BOLD), background='lightgray').place(x='18', y='325')
        self.windD_text_label = tk.Label(self, text='WIND DIRECTION', font=('calibri', 11, BOLD), background='lightgray').place(x='18', y='350')

        # Text labels for day indicator
        self.day_label_monday = tk.Label(self, text='Mon', font=('calibri', 11, BOLD), background='lightgray').place(x='285', y='102')
        self.day_label_tuesday = tk.Label(self, text='Tue', font=('calibri', 11, BOLD), background='lightgray').place(x='345', y='102')
        self.day_label_wednesday = tk.Label(self, text='Wed', font=('calibri', 11, BOLD), background='lightgray').place(x='405', y='102')
        self.day_label_thursday = tk.Label(self, text='Thu', font=('calibri', 11, BOLD), background='lightgray').place(x='465', y='102')
        self.day_label_friday = tk.Label(self, text='Fri', font=('calibri', 11, BOLD), background='lightgray').place(x='525', y='102')
        self.day_label_saturday = tk.Label(self, text='Sat', font=('calibri', 11, BOLD), background='lightgray').place(x='585', y='102')
        self.day_label_sunday = tk.Label(self, text='Sun', font=('calibri', 11, BOLD), background='lightgray').place(x='645', y='102')
        self.current_day = tk.Label(self, text='Current', font=('calibri', 11, BOLD), background='lightgray').place(x='110', y='102')

        # Label to store city name
        self.city_name_label = tk.Label(self, text='', font=('calibri', 14), background='gray')

        # Data labels current
        self.cur_temp_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.feels_like_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.visibility_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.description_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.wind_speed_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))

        # Data labels daily
        self.mon_date_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.mon_sunrise_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.mon_sunset_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.mon_temp_max_label = tk.Label(self, background='lightgray', text='-', font=('calibri', 12))
        self.mon_temp_min_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.mon_pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.mon_humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.mon_wind_s_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.mon_wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12)) # Monday
        
        self.tue_date_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.tue_sunrise_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.tue_sunset_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.tue_temp_max_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.tue_temp_min_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.tue_pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.tue_humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.tue_wind_s_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.tue_wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12)) # Tuesday

        self.wed_date_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.wed_sunrise_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.wed_sunset_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.wed_temp_max_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.wed_temp_min_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.wed_pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.wed_humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.wed_wind_s_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.wed_wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12)) # Wednesday

        self.thu_date_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.thu_sunrise_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.thu_sunset_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.thu_temp_max_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.thu_temp_min_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.thu_pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.thu_humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.thu_wind_s_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.thu_wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12)) # Thursday

        self.fri_date_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fri_sunrise_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fri_sunset_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fri_temp_max_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fri_temp_min_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fri_pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fri_humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fri_wind_s_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fri_wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12)) # Friday

        self.sat_date_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sat_sunrise_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sat_sunset_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sat_temp_max_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sat_temp_min_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sat_pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sat_humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sat_wind_s_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sat_wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12)) # Saturday

        self.sun_date_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sun_sunrise_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sun_sunset_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sun_temp_max_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sun_temp_min_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sun_pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sun_humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sun_wind_s_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sun_wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12)) # Sunday

        # Search bar
        self.search_bar_entry = ttk.Entry(self, width='20', font=('lucida 13'))
        self.search_bar_entry.insert(0, 'Enter a city...') # Adding a default value to be displayed
        self.search_bar_entry.bind('<Button-1>', self.clear_entry_default) # Removing the default value when clicked

        # Icon for updating data
        cwd = os.getcwd()
        refresh_img_path_base = "\\Images\\refreshIcon.png"
        refresh_img_path_full = cwd + refresh_img_path_base
        refresh_icon = ImageTk.PhotoImage(Image.open(refresh_img_path_full))

        # Icon for current description
        self.desc_icon_label = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')

        # Icons for daily descriptions
        self.mon_icon_label = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')
        self.tue_icon_label = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')
        self.wed_icon_label = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')
        self.thu_icon_label = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')
        self.fri_icon_label = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')
        self.sat_icon_label = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')
        self.sun_icon_label = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')

        # Search and refresh buttons
        self.search_button = ttk.Button(self, text='Search', command=self.check_input)
        self.refresh_button = tk.Button(self, image=refresh_icon, background='gray', borderwidth=0, width=20, height=20, command=self.update_labels)
        self.refresh_button.image = refresh_icon # Creating a reference to the image

        # Placements that can't / shouldn't be done while declaring
        self.search_bar_entry.place(x='11', y='40')
        self.search_button.place(x='199', y='40')
        self.refresh_button.place(x='253', y='73')
        self.date_label.place(x='15', y='5')
        self.time_label.place(x='100', y='5')
        self.canvas_data.place(x='10', y='100')

        # Calling an update function to keep time and date updated
        self.update_date_time()

    # Checking input to show user errors when needed
    def check_input(self):
        self.start = timeit.default_timer()

        self.city_name = self.get_city()

        # Checking if a city is entered
        if ((len(self.city_name) == 0) or (self.search_bar_entry.get() == 'Enter a city...')):
            print('Error: no city entered')
            self.place_no_city_entered_label()
            self.clear_data_labels()

        # Checking if the entered city exists in the database
        elif (CurrentForecast.valid_city_current(self) == False):
            print('Error: city not found')
            self.place_city_not_found_label()
            self.clear_data_labels()

        # Placing data and clearing errors
        else:
            self.update_labels()
            self.place_data()
            for i in range(8):
                print(SevenDayForecast.data_of_weekday(self, i))

    # Function for clearing entry when clicked
    def clear_entry_default(self, event):
        self.search_bar_entry.delete(0, 'end')

    # Getter for city
    def get_city(self):
        self.city_name = self.search_bar_entry.get()

        # Making sure cityName gets a value and using console print to note error
        if (len(self.search_bar_entry.get()) == 0):
            self.city_name = self.city_name_label.cget("text")

        return self.city_name.capitalize()

    # Getter for data
    def get_data(self, index):
        try:
            current_data_dict = CurrentForecast.get_current_forecast(self)
            current_data_dict_list = list(current_data_dict.values())

            if (current_data_dict is not None): # Checking that the dictionary exists
                data_value = list(current_data_dict.values())[index]
                if (type(data_value) != str): # Checking type of value to only round values that are not type(str)
                    to_rounded = round((data_value), 2)
                    to_rounded = re.sub('[()]', '', str(to_rounded))

                    # Adding approriate units to data output
                    if (((list(current_data_dict)[index]) == 'temp') or ((list(current_data_dict)[index]) == 'ftemp')):
                        rounded_celcius = to_rounded + u'\N{DEGREE SIGN}C'
                        return rounded_celcius
                    elif ((list(current_data_dict)[index]) == 'pressure'):
                        return to_rounded + ' hPa'
                    elif ((list(current_data_dict)[index]) == 'humidity'):
                        return to_rounded + ' %'
                    elif ((list(current_data_dict)[index]) == 'visibility'):
                        return to_rounded + ' m'
                    elif ((list(current_data_dict)[index] == 'windspeed')):
                        return to_rounded + ' m/s'
                    elif ((list(current_data_dict)[index] == 'winddeg')):
                        return SevenDayForecast.get_direction_from_degree(self, current_data_dict_list[7])
                    else:
                        return to_rounded
                else:
                    return data_value
        except AttributeError:
            pass

    # Updating date and time
    def update_date_time(self):
        self.time_label.config(text=self.get_time())
        self.date_label.config(text=self.get_date())

        self.after(1000, self.update_date_time)

    # Method name
    def get_date(self):
        now = datetime.now()

        return now.strftime('%B %d')

    # Method name
    def get_time(self):
        now = datetime.now()

        return now.strftime('%H:%M')

    # Setting data to labels
    def update_labels(self):
        self.city_name_label.config(text=self.get_city())
        self.desc_icon_label.config(image=self.get_current_icon())

        self.cur_temp_label.config(text=self.get_data(0))
        self.feels_like_label.config(text=self.get_data(1))
        self.pressure_label.config(text=self.get_data(2))
        self.humidity_label.config(text=self.get_data(3))
        self.visibility_label.config(text=self.get_data(4))
        self.description_label.config(text=self.get_data(5))
        self.wind_speed_label.config(text=self.get_data(6))
        self.wind_deg_label.config(text=self.get_data(7))

    # Placing data
    def place_data(self):
        # Miscellanious labels
        self.city_name_label.place(x='100', y='70')
        self.desc_icon_label.place(x='190', y='139')
        self.description_label.place(x='18', y='162')
        self.clear_entry_default(self) # Clearing search bar

        # Current data labels
        self.cur_temp_label.place(x='190', y='200')
        self.feels_like_label.place(x='190', y='225')
        self.pressure_label.place(x='190', y='250')
        self.humidity_label.place(x='190', y='275')
        self.visibility_label.place(x='190', y='300')
        self.wind_speed_label.place(x='190', y='325')
        self.wind_deg_label.place(x='190', y='350')

        # Daily data labels
        self.mon_temp_max_label.place(x='286', y='140')

        # Clearing possible error messages
        self.city_not_found_label.config(text='') 
        self.city_not_entered_label.config(text='')
        self.nothing_to_update_label.config(text='')

        self.stop = timeit.default_timer()
        print("Time to retreive and place data:", self.stop - self.start)

    # Placing 'no city entered' error label
    def place_no_city_entered_label(self):
        self.city_not_found_label.config(text='') # Clearing 'city not found' error
        self.city_not_found_label.lower() # Lowering other error messages to avoid clipping
        self.nothing_to_update_label.lower()
        self.city_not_entered_label.config(text='No city entered')
        self.city_not_entered_label.place(x='190', y='5')

    # Placing 'city not found' error label
    def place_city_not_found_label(self):
        self.city_not_entered_label.config(text='') # Clearing 'city not entered' error
        self.city_not_entered_label.lower() # Lowering other error messages to avoid clipping
        self.nothing_to_update_label.lower()
        self.city_not_found_label.config(text='City not found')
        self.city_not_found_label.place(x='190', y='5')

    def place_nothing_to_update_label(self):
        self.city_not_entered_label.config(text='')
        self.city_not_found_label.lower() # Lowering other error messages to avoid clipping
        self.city_not_entered_label.lower()
        self.nothing_to_update_label.config(text='Nothing to update')
        self.nothing_to_update_label.place(x='190', y='5')

    # Clearing data labels if city does not exist or one is not entered
    def clear_data_labels(self):
        self.city_name_label.config(text='')
        self.cur_temp_label.config(text='')
        self.feels_like_label.config(text='')
        self.pressure_label.config(text='')
        self.humidity_label.config(text='')
        self.visibility_label.config(text='')
        self.description_label.config(text='')
        self.wind_speed_label.config(text='')
        self.wind_deg_label.config(text='')

    def get_current_icon(self):
        try:
            current_data_dict = CurrentForecast.get_current_forecast(self)
            dict_to_list = list(current_data_dict.values())

            if (dict_to_list[8] is not None):
                cwd = os.getcwd() + '\\'
                current_desc_icon_file = dict_to_list[8] + '.png'
                src_path = cwd + current_desc_icon_file
                dest_path = cwd + 'Images\\' + current_desc_icon_file
                final_icon_url = 'http://openweathermap.org/img/wn/' + dict_to_list[8] + '@2x.png'
                urllib.request.urlretrieve(final_icon_url, current_desc_icon_file)
                shutil.move(src_path, dest_path)

                desc_icon_img = Image.open(dest_path)
                desc_icon_img_resized = desc_icon_img.resize((45, 45), Image.ANTIALIAS)
                desc_icon_img_final = ImageTk.PhotoImage(desc_icon_img_resized)
                self.desc_icon_label.image = desc_icon_img_final

                return desc_icon_img_final
        except AttributeError:
            print('AttributeError')
            self.place_nothing_to_update_label()


class CurrentForecast():

    def get_current_forecast(self):
        if (CurrentForecast.valid_city_current(self) == True): # Checking that the city entered has data
            main = self.current_data['main']
            weather = self.current_data['weather']

            cur_temp = main['temp']
            feels_temp = main['feels_like']
            pressure = main['pressure']
            humidity = main['humidity']
            visibility = self.current_data['visibility']
            wind = self.current_data['wind']
            wind_speed = wind['speed']
            wind_deg = wind['deg']
            description = weather[0]['description']
            description_icon = weather[0]['icon']

            # Using a dictionary to store and return the data. This is done to be able to match keys for data formatting.
            current_data_dict = {'temp': cur_temp, 'ftemp':feels_temp, 'pressure':pressure, \
                        'humidity':humidity, 'visibility':visibility, 'description':description, \
                        'windspeed':wind_speed, 'winddeg':wind_deg, 'icon':description_icon}

            return current_data_dict

    def valid_city_current(self):
        current_base_url = 'http://api.openweathermap.org/data/2.5/weather?q='

        city = WeatherProgram.get_city(self)
        current_complete_url = current_base_url + city + '&units=metric' + '&APPID=' + config.api_key
        current_response = requests.get(current_complete_url)
        self.current_data = current_response.json()

        # Checking that the city entered exists in the database
        if (self.current_data['cod'] == 200):
            return True
        else:
            return False


class SevenDayForecast():

    def valid_city_daily(self):
        city_coordinates = GeoLocation.get_latitude_longitude(self)
        lat = city_coordinates.lat
        lon = city_coordinates.lon

        onecall_base_url = 'http://api.openweathermap.org/data/2.5/onecall?'
        dailyCompleteUrl = onecall_base_url + 'lat=' + lat + '&lon=' + lon + '&exclude=current,minutely,hourly,alerts' + '&appid=' + config.api_key

        daily_response = requests.get(dailyCompleteUrl)
        self.daily_data = daily_response.json()

        if (self.daily_data['daily'] is not None):
            return True
        else:
            return False

    # Getting an integer corresponding to a day of the week from timestamp format
    def daily_ordered_data(self):
        if (SevenDayForecast.valid_city_daily(self) == True):
            self.daily = self.daily_data['daily']

        placeholder_dict = {}

        for i in range(len(self.daily)):
            weekday_data = self.daily[i]
            
            timestamp_date = self.daily[i]['dt']
            year = int(datetime.utcfromtimestamp(timestamp_date).strftime('%Y'))
            month = int(datetime.utcfromtimestamp(timestamp_date).strftime('%m'))
            day = int(datetime.utcfromtimestamp(timestamp_date).strftime('%d'))
            
            date_datetime = datetime(year, month, day)

            placeholder_dict[date_datetime] = weekday_data
        
        ordered_dict = collections.OrderedDict(sorted(placeholder_dict.items(), key=lambda item: item[0]))

        return ordered_dict
    

    # week day
    def data_of_weekday(self, index):
        daily_sorted_data = SevenDayForecast.daily_ordered_data(self)
        list_daily_sorted_data = list(daily_sorted_data.values())
        list_daily_sorted_keys = list(daily_sorted_data)

        day_data = list_daily_sorted_data[index]
        daily_temp = day_data['temp']

        daily_sunrise = SevenDayForecast.time_from_timestamp(self, day_data['sunrise'])
        daily_sunset = SevenDayForecast.time_from_timestamp(self, day_data['sunset'])
        daily_temp_max = daily_temp['max']
        daily_temp_min = daily_temp['min']
        daily_pressure = day_data['pressure']
        daily_humidity = day_data['humidity']
        daily_wind_s = day_data['wind_speed']
        daily_wind_deg = SevenDayForecast.get_direction_from_degree(self, day_data['wind_deg'])

        date_datetime = list_daily_sorted_keys[index]
        date_final = date_datetime.strftime('%d-%m-%Y')
        weekday = date_datetime.weekday()

        daily_data_dict = {'weekday':weekday, 'date':date_final, 'd_sunrise':daily_sunrise, 'd_sunset':daily_sunset, 'd_temp_max':daily_temp_max, \
                        'd_temp_min':daily_temp_min, 'd_pressure':daily_pressure, 'd_humidity':daily_humidity, \
                        'd_wind_speed':daily_wind_s, 'd_wind_deg':daily_wind_deg}

        return daily_data_dict

    # Test for function to assign data to variables
    def time_from_timestamp(self, date_timestamp):
        
        return datetime.utcfromtimestamp(date_timestamp).strftime('%H:%M')

    # Method name
    def get_direction_from_degree(self, angle):
        val = int((angle / 22.5) + 0.5)
        dir_array = ['N','NNE','NE','ENE','E','ESE', 'SE', 'SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']

        return dir_array[(val % 16)]

    def weekday_description_icon(self, index):
        weekday_icon_code = DescriptionIconsDaily.daily_get_and_move_icon(self, index)

        cwd = os.getcwd() + '\\'
        daily_desc_icon_file = weekday_icon_code + '.png'
        daily_desc_icon_path = cwd + 'Images\\' + daily_desc_icon_file

        daily_icon_img = Image.open(daily_desc_icon_path)
        daily_icon_img_resized = daily_icon_img.resize((45, 45), Image.ANTIALIAS)
        daily_icon_img_final = ImageTk.PhotoImage(daily_icon_img_resized)
        
        return daily_icon_img_final


class GeoLocation():
    
    # Using an API to get latitude and longitude for given city
    def get_latitude_longitude(self):
        geo_base_url = 'http://api.openweathermap.org/geo/1.0/direct?q='
        city = WeatherProgram.get_city(self)
        geo_complete_url = geo_base_url + city + '&APPID=' + config.api_key

        geo_response = requests.get(geo_complete_url)
        geo_data = geo_response.json()

        lat = str(geo_data[0]['lat'])
        lon = str(geo_data[0]['lon'])

        location_tuple = collections.namedtuple('returns', ['lat', 'lon'])
        location = location_tuple(lat, lon)

        return location


class DescriptionIconsDaily(SevenDayForecast):
    
    # Function to get icons for an image description of the weather
    def daily_get_and_move_icon(self, index):
        daily_data_placeholder = SevenDayForecast.data_of_weekday(self, index)
        weekday = SevenDayForecast.daily_ordered_data(self, index)

        icon_base_url = 'http://openweathermap.org/img/wn/'
        cwd = os.getcwd() + '\\'

        weather = daily_data_placeholder[weekday]['weather']
        icon_code = weather[0]['icon']
        icon_file_name = icon_code + '.png'
        icon_complete_url = icon_base_url + icon_code + '@2x.png'

        urllib.request.urlretrieve(icon_complete_url, icon_file_name)
        
        src_path = cwd + icon_file_name
        dest_path = cwd + 'Images\\' + icon_file_name

        shutil.move(src_path, dest_path) # Moving the file to dest_path

        return icon_code
        



if __name__ == '__main__':
    program_window = WeatherProgram()
    program_window.mainloop()
