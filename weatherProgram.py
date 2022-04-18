# File name: weatherProgram.py
# Author: Arttu Ravantti 
# Description: 

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
        # Lines for visuals
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

        # Data labels
        self.cur_temp_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.feels_like_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.visibility_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.description_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.wind_speed_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))

        # Search bar
        self.search_bar_entry = ttk.Entry(self, width='20', font=('lucida 13'))
        self.search_bar_entry.insert(0, 'Enter a city...') # Adding a default value to be displayed
        self.search_bar_entry.bind('<Button-1>', self.clear_entry_default) # Removing the default value when clicked

        # Icon for updating data
        cwd = os.getcwd()
        refresh_img_path_base = "\\Images\\refreshIcon.png"
        refresh_img_path_full = cwd + refresh_img_path_base
        refresh_icon = ImageTk.PhotoImage(Image.open(refresh_img_path_full))

        # Icon for description
        self.desc_icon_label = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')

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
        SevenDayForecast.data_of_weekday(self, 2) # Temporary. To Run functions that aren't attached to anything else yet.

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
                        return self.get_direction_from_degree(current_data_dict_list[7])
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

    # Method name
    def get_direction_from_degree(self, angle):
        val = int((angle / 22.5) + 0.5)
        dir_array = ['N','NNE','NE','ENE','E','ESE', 'SE', 'SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']

        return dir_array[(val % 16)]

    # Setting data to labels
    def update_labels(self):
        self.city_name_label.config(text=self.get_city())
        self.desc_icon_label.config(image=self.get_desc_icons())

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
        self.city_name_label.place(x='100', y='70')
        self.desc_icon_label.place(x='190', y='139')
        self.description_label.place(x='18', y='162')
        self.clear_entry_default(self)

        self.cur_temp_label.place(x='190', y='200')
        self.feels_like_label.place(x='190', y='225')
        self.pressure_label.place(x='190', y='250')
        self.humidity_label.place(x='190', y='275')
        self.visibility_label.place(x='190', y='300')
        self.wind_speed_label.place(x='190', y='325')
        self.wind_deg_label.place(x='190', y='350')

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

    def get_desc_icons(self):
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

    def get_daily_forecast(self):
        if (SevenDayForecast.valid_city_daily(self) == True):
            self.daily = self.daily_data['daily']

            return self.daily

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
    def weekday_from_timestamp(self, index):
        self.daily = SevenDayForecast.get_daily_forecast(self)

        timestamp_date = self.daily[index]['dt']
        year = int(datetime.utcfromtimestamp(timestamp_date).strftime('%Y'))
        month = int(datetime.utcfromtimestamp(timestamp_date).strftime('%m'))
        day = int(datetime.utcfromtimestamp(timestamp_date).strftime('%d'))
            
        date = datetime(year, month, day)
        weekday = date.weekday()
        
        return weekday
    
    # Getting data of given week day number (0-6), starting from Monday
    def data_of_weekday(self, index):
        weekday = SevenDayForecast.weekday_from_timestamp(self, index)

        print(self.daily[weekday])


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
    def get_and_move_icon(self):
        daily_data_placeholder = SevenDayForecast.get_daily_forecast(self)

        icon_base_url = 'http://openweathermap.org/img/wn/'
        cwd = os.getcwd() + '\\'

        daily_icon_list = []

        for i in range(8):
            var_daily_data = daily_data_placeholder['daily']
            weather = var_daily_data[i]['weather']
            icon_code = weather[0]['icon']
            icon_file_name = icon_code + '.png'
            icon_complete_url = icon_base_url + icon_code + '@2x.png'

            daily_icon_list.append(icon_code)

        urllib.request.urlretrieve(icon_complete_url, icon_file_name)
        
        src_path = cwd + icon_file_name
        dest_path = cwd + 'Images\\' + icon_file_name

        shutil.move(src_path, dest_path) # Moving the file to dest_path

        return daily_icon_list
        



if __name__ == '__main__':
    program_window = WeatherProgram()
    program_window.mainloop()
