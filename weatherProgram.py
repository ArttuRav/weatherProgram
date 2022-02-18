# File name: weatherProgram.py
# Author: Arttu Ravantti 
# Description: 

import tkinter as tk
import requests
from tkinter import END, ttk
from datetime import datetime
import re

class WeatherProgram(tk.Tk):

    def __init__(self):
        super().__init__()

        # API key
        self.apiKey = '936b51d488d6f3918dcaee06b7c69a9f'

        # Creating window
        self.title('Weather program')
        self.resizable(0, 0)
        self.geometry('700x515')
        self['bg'] = 'lightblue'

        self.cityNotEnteredLabel = tk.Label(self, text='', font=('lucida', 10), background='lightblue')
        self.cityNotFoundLabel = tk.Label(self, text='', font=('lucida', 10), background='lightblue')

        self.canvasLeft = tk.Canvas(self, bg='white', height=400, width=300).place(x='10', y='100')
        self.canvasRight = tk.Canvas(self, bg='white', height=400, width=340).place(x='345', y='100')

        currentForecast = CurrentForecast(self)

        self.dateLabel = tk.Label(self, text=self.getDate(), font=('lucida', 10), background='lightblue')
        self.timeLabel = tk.Label(self, text=self.getTime(), font=('lucida', 10), background='lightblue')
        self.dateLabel.place(x='15', y='5')
        self.timeLabel.place(x='100', y='5')

        self.tempTextLabel = tk.Label(self, text='Temperature', font=('lucida', 12), background='white').place(x='15', y='100')
        self.feelsTextLabel = tk.Label(self, text='Feels like', font=('lucida', 12), background='white').place(x='15', y='125')

        self.entryCity = ttk.Entry(self, width='24', font=('lucida 13'))

        self.temperatureLabel = tk.Label(self, background='white', text='', font=('lucida', 12))
        self.feelsLikeLabel = tk.Label(self, background='white', text='', font=('lucida', 12))

        self.searchButton = ttk.Button(self, text='Search', command=lambda:self.checkInput())

        self.entryCity.insert(0, 'Enter a city...') # Adding a default value to be displayed
        self.entryCity.bind('<Button-1>', self.clearEntryDefault) # Removing the default value when clicked

        # Placements
        self.entryCity.place(x='15', y='40')
        self.searchButton.place(x='240', y='40')

        self.update()

    def checkInput(self):
        self.cityName = self.getCity()

        if len(self.cityName) == 0 or (self.entryCity.get() == 'Enter a city...'):
            self.cityNotFoundLabel.config(text=' ')
            self.cityNotFoundLabel.lower()
            self.placeNoCityEnteredLabel()
            print('Error: no city entered.')
        if (CurrentForecast.isValidCity(self) == True and (self.entryCity.get() != 'Enter a city...')):
            self.cityNotEnteredLabel.config(text=' ')
            self.cityNotEnteredLabel.lower()
            self.placeCityNotFoundLabel()
            print('City not found.')
        else:
            self.updateLabels()
            self.placeData()
            self.cityNotFoundLabel.config(text='')

    def clearEntryDefault(self, event):
        self.entryCity.delete(0, 'end')

    def getCity(self):
        self.cityName = self.entryCity.get()

        return self.cityName

    def getData(self, index):
        infoList = CurrentForecast.getCurrentForecast(self)
        
        try:
            if (infoList is not None):
                toCelcius = round(infoList[index]), 3
                toCelcius = re.sub('[()]', '', str(toCelcius))
                celciusToString = toCelcius + ' C'

                return celciusToString
        except:
            print('An error occured.')

    def getDate(self):
        now = datetime.now()

        return now.strftime('%B %d')

    def getTime(self):
        now = datetime.now()

        return now.strftime('%H:%M')

    def update(self):
        self.timeLabel.config(text=self.getTime())

        self.after(1000, self.update)

    def updateLabels(self):
        self.temperatureLabel.config(text=self.getData(0))
        self.feelsLikeLabel.config(text=self.getData(1))

    def placeData(self):
        self.temperatureLabel.place(x='125', y='100')
        self.feelsLikeLabel.place(x='125', y='125')

    def placeNoCityEnteredLabel(self):
        self.cityNotEnteredLabel.config(text='No city entered')
        self.cityNotEnteredLabel.place(x='240', y='5')

    def placeCityNotFoundLabel(self):
        self.cityNotFoundLabel.config(text='City not found')
        self.cityNotFoundLabel.place(x='240', y='5')


class CurrentForecast(object):

    def __init__(self, mainwin):
        self.mainwin = mainwin

    def getCurrentForecast(self):

        try:
            if (self.data['cod'] != 404):
                self.main = self.data['main']
                weather = self.data['weather']

                temperature = self.main['temp']
                feelsTemp = self.main['feels_like']
                pressure = self.main['pressure']
                humidity = self.main['humidity']
                visibility = self.data['visibility']
                description = weather[0]['description']

                infoList = [temperature, feelsTemp, pressure, humidity, visibility, description]

                return infoList
            else:
                print('City not found.')
        except:
            WeatherProgram.placeNoCityEnteredLabel(self)

    def isValidCity(self):
        self.apiKey = '936b51d488d6f3918dcaee06b7c69a9f'
        self.baseURL = 'http://api.openweathermap.org/data/2.5/weather?q='
        self.city = WeatherProgram.getCity(self)
        self.completeURL = self.baseURL + self.city + '&units=metric' + '&APPID=' + self.apiKey
        response = requests.get(self.completeURL)
        self.data = response.json()
        
        if (self.data['cod'] == '404'):
            return True
        else:
            return False


if __name__ == '__main__':
    programWindow = WeatherProgram()
    programWindow.mainloop()
