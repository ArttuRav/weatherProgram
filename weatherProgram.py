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
import extra_function
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
        self.geometry('1075x515')
        self['bg'] = 'gray'

        # Labels for error messages
        self.city_not_entered_label = tk.Label(self, text='', font=('lucida', 10), background='gray')
        self.city_not_found_label = tk.Label(self, text='', font=('lucida', 10), background='gray')
        self.nothing_to_update_label = tk.Label(self, text='', font=('lucida', 10), background='gray')

        # Canvas for visuals
        self.canvas_time_date = tk.Canvas(self, bg='gray', height=22, width=125, highlightthickness=1, highlightbackground='black').place(x='12', y='4')
        self.canvas_data = tk.Canvas(self, bg='lightgray', highlightthickness=1, highlightbackground='black', height=400, width=1052)

        # Lines for visuals on canvas (numbered left-right and up-down)
        self.canvas_data.create_line(412,0,412,401, fill='gray', width=5) # vertical 2
        self.canvas_data.create_line(502,0,502,401, fill='gray', width=5) # vertical 3
        self.canvas_data.create_line(592,0,592,401, fill='gray', width=5) # vertical 4
        self.canvas_data.create_line(682.5,0,682.5,401, fill='gray', width=5) # vertical 5
        self.canvas_data.create_line(772,0,772,401, fill='gray', width=5) # vertical 6
        self.canvas_data.create_line(862,0,862,401, fill='gray', width=5) # vertical 6
        self.canvas_data.create_line(952,0,952,401, fill='gray', width=5) # vertical 7
        self.canvas_data.create_line(0,31,1054,31, fill='black', width=5) # horizontal 1
        self.canvas_data.create_line(0,93,1054,93, fill='gray', width=5) # horizontal 2
        self.canvas_data.create_line(260,0,260,401, fill='black', width=5) # vertical 1

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
        self.day_label_first = tk.Label(self, text='1', font=('calibri', 11, BOLD), background='lightgray')
        self.day_label_second = tk.Label(self, text='2', font=('calibri', 11, BOLD), background='lightgray')
        self.day_label_third = tk.Label(self, text='3', font=('calibri', 11, BOLD), background='lightgray')
        self.day_label_fourth = tk.Label(self, text='4', font=('calibri', 11, BOLD), background='lightgray')
        self.day_label_fifth = tk.Label(self, text='5', font=('calibri', 11, BOLD), background='lightgray')
        self.day_label_sixth = tk.Label(self, text='6', font=('calibri', 11, BOLD), background='lightgray')
        self.day_label_seventh = tk.Label(self, text='7', font=('calibri', 11, BOLD), background='lightgray')
        self.current_day = tk.Label(self, text='Current', font=('calibri', 11, BOLD), background='lightgray').place(x='188', y='102')

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
        self.first_date_label = tk.Label(self, background='gray', text='', font=('calibri', 8))
        self.first_sunrise_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.first_sunset_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.first_temp_max_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.first_temp_min_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.first_pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.first_humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.first_wind_s_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.first_wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12)) # First slot
        
        self.second_date_label = tk.Label(self, background='gray', text='', font=('calibri', 8))
        self.second_sunrise_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.second_sunset_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.second_temp_max_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.second_temp_min_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.second_pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.second_humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.second_wind_s_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.second_wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12)) # Second slot

        self.third_date_label = tk.Label(self, background='gray', text='', font=('calibri', 8))
        self.third_sunrise_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.third_sunset_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.third_temp_max_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.third_temp_min_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.third_pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.third_humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.third_wind_s_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.third_wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12)) # Third slot

        self.fourth_date_label = tk.Label(self, background='gray', text='', font=('calibri', 8))
        self.fourth_sunrise_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fourth_sunset_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fourth_temp_max_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fourth_temp_min_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fourth_pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fourth_humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fourth_wind_s_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fourth_wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12)) # Fourth slot

        self.fifth_date_label = tk.Label(self, background='gray', text='', font=('calibri', 8))
        self.fifth_sunrise_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fifth_sunset_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fifth_temp_max_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fifth_temp_min_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fifth_pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fifth_humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fifth_wind_s_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.fifth_wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12)) # Fifth slot

        self.sixth_date_label = tk.Label(self, background='gray', text='', font=('calibri', 8))
        self.sixth_sunrise_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sixth_sunset_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sixth_temp_max_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sixth_temp_min_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sixth_pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sixth_humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sixth_wind_s_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.sixth_wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12)) # Sixth slot

        self.seventh_date_label = tk.Label(self, background='gray', text='', font=('calibri', 8))
        self.seventh_sunrise_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.seventh_sunset_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.seventh_temp_max_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.seventh_temp_min_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.seventh_pressure_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.seventh_humidity_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.seventh_wind_s_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12))
        self.seventh_wind_deg_label = tk.Label(self, background='lightgray', text='', font=('calibri', 12)) # Seventh slot

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

        self.day_icon_first = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')
        self.day_icon_second = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')
        self.day_icon_third = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')
        self.day_icon_fourth = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')
        self.day_icon_fifth = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')
        self.day_icon_sixth = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')
        self.day_icon_seventh = tk.Label(self, image='', background='lightgray', borderwidth=1, relief='solid')

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
        self.day_label_first.place(x='437', y='102')
        self.day_label_second.place(x='527', y='102')
        self.day_label_third.place(x='617', y='102')
        self.day_label_fourth.place(x='707', y='102')
        self.day_label_fifth.place(x='797', y='102')
        self.day_label_sixth.place(x='887', y='102')
        self.day_label_seventh.place(x='977', y='102')

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

        # Current weather data
        self.cur_temp_label.config(text=self.get_data(0))
        self.feels_like_label.config(text=self.get_data(1))
        self.pressure_label.config(text=self.get_data(2))
        self.humidity_label.config(text=self.get_data(3))
        self.visibility_label.config(text=self.get_data(4))
        self.description_label.config(text=self.get_data(5))
        self.wind_speed_label.config(text=self.get_data(6))
        self.wind_deg_label.config(text=self.get_data(7))

        if (config.api_key_index == 1):
            temp_list = SevenDayForecast.valid_city_daily(self)
            extra_function.calls_exceeded(temp_list[1])

        # Day text labels for 7-day forecast
        self.day_label_first.config(text=self.weekday_name_order(0))
        self.day_label_first.config(text=self.weekday_name_order(0))
        self.day_label_second.config(text=self.weekday_name_order(1))
        self.day_label_third.config(text=self.weekday_name_order(2))
        self.day_label_fourth.config(text=self.weekday_name_order(3))
        self.day_label_fifth.config(text=self.weekday_name_order(4))
        self.day_label_sixth.config(text=self.weekday_name_order(5))
        self.day_label_seventh.config(text=self.weekday_name_order(6))

        # Description icons for 7-day forecast
        self.day_icon_first.config(image=self.get_daily_icons(0))
        self.day_icon_second.config(image=self.get_daily_icons(1))
        self.day_icon_third.config(image=self.get_daily_icons(2))
        self.day_icon_fourth.config(image=self.get_daily_icons(3))
        self.day_icon_fifth.config(image=self.get_daily_icons(4))
        self.day_icon_sixth.config(image=self.get_daily_icons(5))
        self.day_icon_seventh.config(image=self.get_daily_icons(6))

        self.first_date_label.config(text=SevenDayForecast.get_daily_data(self, 1, 0))
        self.second_date_label.config(text=SevenDayForecast.get_daily_data(self, 1, 1))
        self.third_date_label.config(text=SevenDayForecast.get_daily_data(self, 1, 2))
        self.fourth_date_label.config(text=SevenDayForecast.get_daily_data(self, 1, 3))
        self.fifth_date_label.config(text=SevenDayForecast.get_daily_data(self, 1, 4))
        self.sixth_date_label.config(text=SevenDayForecast.get_daily_data(self, 1, 5))
        self.seventh_date_label.config(text=SevenDayForecast.get_daily_data(self, 1, 6))

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
        self.first_date_label.place(x='439', y='75')
        self.second_date_label.place(x='529', y='75')
        self.third_date_label.place(x='619', y='75')
        self.fourth_date_label.place(x='709', y='75')
        self.fifth_date_label.place(x='799', y='75')
        self.sixth_date_label.place(x='889', y='75')
        self.seventh_date_label.place(x='979', y='75')

        # 7-day forecast description icons
        self.day_icon_first.place(x='443.25', y='140')
        self.day_icon_second.place(x='533.25', y='140')
        self.day_icon_third.place(x='623.25', y='140')
        self.day_icon_fourth.place(x='713.25', y='140')
        self.day_icon_fifth.place(x='803.25', y='140')
        self.day_icon_sixth.place(x='893.25', y='140')
        self.day_icon_seventh.place(x='983.25', y='140')

        # Clearing possible error messages
        self.city_not_found_label.config(text='')
        self.city_not_entered_label.config(text='')
        self.nothing_to_update_label.config(text='')

        self.stop = timeit.default_timer()
        print("Time to retreive and place data:", self.stop - self.start)

    # Placing 'no city entered' error label
    def place_no_city_entered_label(self):
        self.city_not_found_label.config(text='') # Clearing errors
        self.nothing_to_update_label.config(text='')
        self.city_not_found_label.lower() # Lowering other error messages to avoid clipping
        self.nothing_to_update_label.lower()
        self.city_not_entered_label.config(text='No city entered')
        self.city_not_entered_label.place(x='190', y='5')

    # Placing 'city not found' error label
    def place_city_not_found_label(self):
        self.city_not_entered_label.config(text='') # Clearing errors
        self.nothing_to_update_label.config(text='')
        self.city_not_entered_label.lower() # Lowering other error messages to avoid clipping
        self.nothing_to_update_label.lower()
        self.city_not_found_label.config(text='City not found')
        self.city_not_found_label.place(x='190', y='5')

    # Placing 'nothing to update' error label
    def place_nothing_to_update_label(self):
        self.city_not_found_label.config(text='')
        self.city_not_entered_label.config(text='')
        self.city_not_found_label.lower() # Lowering other error messages to avoid clipping
        self.city_not_entered_label.lower()
        self.nothing_to_update_label.config(text='nothing to update')
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

    def get_daily_icons(self, day):
        full_daily_data = SevenDayForecast.data_of_weekdays(self)
        if (full_daily_data is None):
            pass
        else:
            one_day_data = list(full_daily_data[day].values())

            self.icon_label_list = [self.day_icon_first, self.day_icon_second, self.day_icon_third, \
                                self.day_icon_fourth, self.day_icon_fifth, self.day_icon_sixth, self.day_icon_seventh]

            if (one_day_data is not None):
                icon_daily_file = one_day_data[-1]
                dest_path = DescriptionIconsDaily.daily_get_and_move_icon(self, icon_daily_file)

                day_icon_img = Image.open(dest_path)
                day_icon_img_resized = day_icon_img.resize((45, 45), Image.ANTIALIAS)
                day_icon_img_final = ImageTk.PhotoImage(day_icon_img_resized)
                self.icon_label_list[day].image = day_icon_img_final

            return day_icon_img_final
        

    # Calling the method with the day number returns the integer of the weekday (0-6, starting from Monday)
    def weekday_of_daily_data(self, day):
        placeholder_daily_data = SevenDayForecast.data_of_weekdays(self)
        if (placeholder_daily_data is None):
            pass
        else:
            one_day_data_list = list(placeholder_daily_data[day].values())

            return one_day_data_list[0]

    def weekday_name_order(self, day):
        data_weekday_int = self.weekday_of_daily_data(day)

        if (data_weekday_int == 0):
            return 'Mon'
        elif (data_weekday_int == 1):
            return 'Tue'
        elif (data_weekday_int == 2):
            return 'Wed'
        elif (data_weekday_int == 3):
            return 'Thu'
        elif (data_weekday_int == 4):
            return 'Fri'
        elif (data_weekday_int == 5):
            return 'Sat'
        elif (data_weekday_int == 6):
            return 'Sun'


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
        current_complete_url = current_base_url + city + '&units=metric' + '&APPID=' + config.api_key_default
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

        if (config.api_key_index == 0):
            api_key = config.api_key_default
        else:
            api_key = config.api_key_backup

        onecall_base_url = 'http://api.openweathermap.org/data/2.5/onecall?'
        daily_complete_url = onecall_base_url + 'lat=' + lat + '&lon=' + lon + '&exclude=current,minutely,hourly,alerts' + '&appid=' + api_key

        daily_response = requests.get(daily_complete_url)
        self.daily_data = daily_response.json()

        try:
            if (self.daily_data['lat'] is not None):
                return True
            else:
                return False
        except KeyError:
            temp_list = [False, daily_complete_url]

            return temp_list

    # Returning the data sorted by date
    def daily_ordered_data(self, complete_url=None):
        if (type(SevenDayForecast.valid_city_daily(self)) == list):
            temp_list = SevenDayForecast.valid_city_daily(self)
            if (temp_list[0] == False):
                config.api_key_index = 1
                self.daily = extra_function.calls_exceeded(temp_list[1])
                
                if (self.daily['cod'] == 429):
                    pass
                else:
                    placeholder_dict = {}

                    for i in range(len(self.daily)):
                        weekday_data = self.daily[i]
            
                        timestamp_date = self.daily[i]['dt']
                        year = int(datetime.utcfromtimestamp(timestamp_date).strftime('%Y'))
                        month = int(datetime.utcfromtimestamp(timestamp_date).strftime('%m'))
                        day = int(datetime.utcfromtimestamp(timestamp_date).strftime('%d'))
                        date_datetime = datetime(year, month, day)

                        placeholder_dict[date_datetime] = weekday_data
        
                    sorted_dict = collections.OrderedDict(sorted(placeholder_dict.items(), key=lambda item: item[0]))

                    return sorted_dict
        else:
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
        
            sorted_dict = collections.OrderedDict(sorted(placeholder_dict.items(), key=lambda item: item[0]))

            return sorted_dict

    
    # Method for returning the sorted and separated data
    def data_of_weekdays(self):
        daily_sorted_data = SevenDayForecast.daily_ordered_data(self)
        if (daily_sorted_data is None):
            pass
        else:
            list_daily_sorted_data = list(daily_sorted_data.values())
            list_daily_sorted_keys = list(daily_sorted_data)

            # Declaring a dictionary for each day there is data of
            dict_1st, dict_2nd, dict_3rd, dict_4th, dict_5th, dict_6th, dict_7th, dict_8th = {}, {}, {}, {}, {}, {}, {}, {}

            # Storing the dictionaries in a list to easily move to the next dictionary, when a day's data has been filled
            dict_list = [dict_1st, dict_2nd, dict_3rd, dict_4th, \
                        dict_5th, dict_6th, dict_7th, dict_8th]

            dict_index = 0

            # Keys for data values
            key_list = ['weekday', 'date', 'd_sunrise', 'd_sunset', 'd_temp_max', 'd_temp_min', \
                        'd_pressure', 'd_humidity', 'd_wind_speed', 'd_wind_deg', 'd_icon']

            for i in range(8):
                day_data = list_daily_sorted_data[i]
                day_weather = day_data['weather']
                daily_temp = day_data['temp']

                daily_sunrise = SevenDayForecast.time_from_timestamp(self, day_data['sunrise'])
                daily_sunset = SevenDayForecast.time_from_timestamp(self, day_data['sunset'])
                daily_temp_max = daily_temp['max']
                daily_temp_min = daily_temp['min']
                daily_pressure = day_data['pressure']
                daily_humidity = day_data['humidity']
                daily_wind_s = day_data['wind_speed']
                daily_wind_deg = SevenDayForecast.get_direction_from_degree(self, day_data['wind_deg'])
                daily_icon = day_weather[0]['icon']

                date_datetime = list_daily_sorted_keys[i]
                date_final = date_datetime.strftime('%d.%m.%Y')
                weekday = date_datetime.weekday()

                # Values listed, so that they can be iterated over in a for loop
                value_list = [weekday, date_final, daily_sunrise, daily_sunset, daily_temp_max, \
                            daily_temp_min, daily_pressure, daily_humidity, daily_wind_s, daily_wind_deg, daily_icon]

                value_index = 0

                # This for loop adds the values to the correct dictionaries, paired with matching keys
                for key in key_list:
                    dict_list[dict_index][key] = value_list[value_index]
                    value_index += 1
                    if (value_index > 10):
                        dict_index += 1
                        value_index = 0

            return dict_list

    # Method name
    def time_from_timestamp(self, date_timestamp):
        
        return datetime.utcfromtimestamp(date_timestamp).strftime('%H:%M')

    # Method name
    def get_direction_from_degree(self, angle):
        val = int((angle / 22.5) + 0.5)
        dir_array = ['N','NNE','NE','ENE','E','ESE', 'SE', 'SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']

        return dir_array[(val % 16)]

    # When called, index is used for picking the desired value, and day of the value
    def get_daily_data(self, index, day):
        try:
            daily_data_dicts = SevenDayForecast.data_of_weekdays(self)
            if (daily_data_dicts is None):
                pass
            else:
                one_day_data = daily_data_dicts[day]

                if (one_day_data is not None): # Checking that the dictionary exists
                    daily_data_value = list(one_day_data.values())[index]
                    if (type(daily_data_value) != str): # Making sure strings don't end up being rounded, since it wouldn't work
                        daily_data_rounded = round((daily_data_value), 2)
                        daily_data_rounded = re.sub('[()]', '', str(daily_data_rounded))

                        # Adding units to data outputs
                        if (((list(daily_data_dicts)[index]) == 'd_temp_max') or ((list(daily_data_dicts)[index]) == 'd_temp_min')):
                            return daily_data_rounded + u'\N{DEGREE SIGN}C'
                        elif ((list(daily_data_dicts)[index]) == 'd_pressure'):
                            return daily_data_rounded + ' hPa'
                        elif ((list(daily_data_dicts)[index]) == 'd_humidity'):
                            return daily_data_rounded + ' %'
                        elif ((list(daily_data_dicts)[index]) == 'd_wind_speed'):
                            return daily_data_rounded + ' m/s'
                        else:
                            return daily_data_rounded
                    else:
                        return daily_data_value
        except AttributeError:
            pass


class GeoLocation():
    
    # Using an API to get latitude and longitude for given city
    def get_latitude_longitude(self):
        geo_base_url = 'http://api.openweathermap.org/geo/1.0/direct?q='
        city = WeatherProgram.get_city(self)
        geo_complete_url = geo_base_url + city + '&APPID=' + config.api_key_default

        geo_response = requests.get(geo_complete_url)
        geo_data = geo_response.json()

        lat = str(geo_data[0]['lat'])
        lon = str(geo_data[0]['lon'])

        location_tuple = collections.namedtuple('returns', ['lat', 'lon'])
        location = location_tuple(lat, lon)

        return location


class DescriptionIconsDaily(SevenDayForecast):
    
    # Function to get icons for an image description of the weather
    def daily_get_and_move_icon(self, icon_daily_code):
        icon_base_url = 'http://openweathermap.org/img/wn/'
        cwd = os.getcwd() + '\\'

        icon_daily_file = icon_daily_code + '.png'
        complete_url = icon_base_url + icon_daily_code + '@2x.png'

        urllib.request.urlretrieve(complete_url, icon_daily_file) # Getting the file
        
        src_path = cwd + icon_daily_file
        dest_path = cwd + 'Images\\' + icon_daily_file

        shutil.move(src_path, dest_path) # Moving the file to dest_path

        return dest_path
        


if __name__ == '__main__':
    program_window = WeatherProgram()
    program_window.mainloop()
