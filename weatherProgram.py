# File name: weatherProgram.py
# Author: Arttu Ravantti 
# Description: 

import tkinter as tk
import requests, json
from tkinter import END, ttk
from datetime import datetime
import re

class WeatherProgram(tk.Tk):

    def __init__(self):
        super().__init__()

        # Creating window
        self.title('Weather program')
        self.resizable(0, 0)
        self.geometry('700x600')
        self['bg'] = 'lightblue'

        self.canvas1 = tk.Canvas(self, bg='white', height=400, width=300).place(x='10', y='100')

        self.dateLabel = tk.Label(self, text=self.getDate(), font=('lucida', 10), background='lightblue')
        self.timeLabel = tk.Label(self, text=self.getTime(), font=('lucida', 10), background='lightblue')
        self.dateLabel.place(x='15', y='5')
        self.timeLabel.place(x='100', y='5')

        self.tempTextLabel = tk.Label(self, text='Temperature', font=('lucida sans', 12), background='white').place(x='15', y='100')
        self.feelsTextLabel = tk.Label(self, text='Feels like', font=('lucida sans', 12), background='white').place(x='15', y='125')

        self.cityName = 'Helsinki'

        self.temperatureLabel = tk.Label(self, background='white', text=self.displayInfo(0), font=('lucida sans', 12))
        self.feelsLikeLabel = tk.Label(self, background='white', text=self.displayInfo(1), font=('lucida sans', 12))

        # self.newThreadTime = Thread(target=self.update).start()

        self.entryCity = ttk.Entry(
            self,
            width='24',
            font='40')

        self.searchButton = ttk.Button(
            self,
            text='Search',
            command=lambda:[self.getCity(), self.placeInfo()]) # NEEDS FIXING

        self.entryCity.insert(0, 'Enter a city...') # Adding a default value to be displayed
        self.entryCity.bind('<Button-1>', self.clearEntryDefault) # Removing the default value when clicked

        # Placements
        self.entryCity.place(x='15', y='40')
        self.searchButton.place(x='240', y='40')

        self.update()


    def clearEntryDefault(self, event):
        self.entryCity.delete(0, 'end')

    def getCity(self):
        self.cityName = str(self.entryCity.get())

        return self.cityName

    def displayInfo(self, index):
        infoList = WeatherInfo.jsonToString(self)
        
        toCelcius = round(self.infoList[index] - 273.15), 3
        toCelcius = re.sub('[()]', '', str(toCelcius))
        toString = str(toCelcius) + ' C'

        return toString

    def getDate(self):
        now = datetime.now()

        return now.strftime('%B %d')

    def getTime(self):
        now = datetime.now()

        return now.strftime('%H:%M')

    def update(self):
        self.timeLabel.config(text=self.getTime())

        self.after(1000, self.update)

    def placeInfo(self):
        # self.temperatureLabel.config(text = self.displayInfo(0))
        # self.feelsLikeLabel.config(text = self.displayInfo(1))
        self.temperatureLabel.place(x='125', y='100')
        self.feelsLikeLabel.place(x='125', y='125')


class WeatherInfo():

    def __init__(self):
        super().__init__()

    def jsonToString(self):

        # API information
        self.apiKey = '936b51d488d6f3918dcaee06b7c69a9f'
        self.baseURL = 'http://api.openweathermap.org/data/2.5/weather?q='

        self.completeURL = self.baseURL + self.cityName + '&APPID=' + self.apiKey
        self.response = requests.get(self.completeURL)
        self.data = self.response.json()

        self.main = self.data['main']
        self.weather = self.data['weather']

        self.temperature = self.main['temp']
        self.feelsTemp = self.main['feels_like']
        self.pressure = self.main['pressure']
        self.humidity = self.main['humidity']
        self.visibility = self.data['visibility']
        self.description = self.weather[0]['description']

        self.infoList = [self.temperature, self.feelsTemp, self.pressure, self.humidity, self.visibility, self.description]

        return self.infoList


if __name__ == '__main__':
    programWindow = WeatherProgram()
    programWindow.mainloop()
