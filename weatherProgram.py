# File name: weatherProgram.py
# Author: Arttu Ravantti 
# Description: 

import tkinter as tk
import requests, json
from tkinter import END, ttk

class WeatherProgram(tk.Tk):

    def __init__(self):
        super().__init__()

        # weatherData = WeatherInfo(self)

        # Creating window
        self.title('Weather program')
        self.resizable(0, 0)
        self.geometry('700x600')
        self['bg'] = 'lightblue'

        # Creating label
        # self.searchText = ttk.Label(
            # self,
            # text='Search city: ',
            # font = ('Digital-7', 40))

        self.entryCity = ttk.Entry(
            self,
            width='15',
            font='40')

        self.searchButton = ttk.Button(
            self,
            text='Search',
            command=lambda:[self.getCity(), WeatherInfo.printData(self)])

        self.entryCity.insert(0, 'Enter a city...') # Adding a default value to be displayed
        self.entryCity.bind('<Button-1>', self.clearEntryDefault) # Removing the default value when clicked

        # Placements
        self.entryCity.place(x='120', y='50')
        self.searchButton.place(x='270', y='50')


    def clearEntryDefault(self, event):
        self.entryCity.delete(0, 'end')

    def getCity(self):
        self.cityName = str(self.entryCity.get())

        return self.cityName

class WeatherInfo():

    def __init__(self):
        super().__init__()

    def printData(self):
        # API information
        self.apiKey = '936b51d488d6f3918dcaee06b7c69a9f'
        self.baseURL = 'http://api.openweathermap.org/data/2.5/weather?q='

        self.completeURL = self.baseURL + WeatherProgram.getCity(self) + '&APPID=' + self.apiKey
        self.response = requests.get(self.completeURL)
        self.data = self.response.json()

        print(self.data)


if __name__ == '__main__':
    programWindow = WeatherProgram()
    programWindow.mainloop()