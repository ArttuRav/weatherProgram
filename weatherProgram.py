# File name: weatherProgram.py
# Author: Arttu Ravantti 
# Description: 

import tkinter as tk
import requests
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
import re
import os

class WeatherProgram(tk.Tk):

    def __init__(self):
        super().__init__()

        # Creating window
        self.title('Weather program')
        self.resizable(0, 0)
        self.geometry('700x515')
        self['bg'] = 'lightblue'

        # Labels for error messages
        self.cityNotEnteredLabel = tk.Label(self, text='', font=('lucida', 10), background='lightblue')
        self.cityNotFoundLabel = tk.Label(self, text='', font=('lucida', 10), background='lightblue')

        # Canvases for visuals
        self.canvasLeft = tk.Canvas(self, bg='white', height=400, width=300).place(x='10', y='100')
        self.canvasRight = tk.Canvas(self, bg='white', height=400, width=340).place(x='345', y='100')

        # Labels for date and time
        self.dateLabel = tk.Label(self, text=self.getDate(), font=('lucida', 10), background='lightblue')
        self.timeLabel = tk.Label(self, text=self.getTime(), font=('lucida', 10), background='lightblue')

        # Data text labels
        self.tempTextLabel = tk.Label(self, text='temperature', font=('lucida', 12), background='white').place(x='15', y='100')
        self.feelsTextLabel = tk.Label(self, text='feels like', font=('lucida', 12), background='white').place(x='15', y='125')
        self.pressureTextLabel = tk.Label(self, text='pressure', font=('lucida', 12), background='white').place(x='15', y='150')
        self.humidityTextLabel = tk.Label(self, text='humidity', font=('lucida', 12), background='white').place(x='15', y='175')
        self.visibilityTextLabel = tk.Label(self, text='visibility', font=('lucida', 12), background='white').place(x='15', y='200')
        self.descriptionTextLabel = tk.Label(self, text='description', font=('lucida', 12), background='white').place(x='15', y='225')

        # Data labels
        self.temperatureLabel = tk.Label(self, background='white', text='', font=('lucida', 12))
        self.feelsLikeLabel = tk.Label(self, background='white', text='', font=('lucida', 12))
        self.pressureLabel = tk.Label(self, background='white', text='', font=('lucida', 12))
        self.humidityLabel = tk.Label(self, background='white', text='', font=('lucida', 12))
        self.visibilityLabel = tk.Label(self, background='white', text='', font=('lucida', 12))
        self.descriptionLabel = tk.Label(self, background='white', text='', font=('lucida', 12))

        # Search bar entry
        self.entryCity = ttk.Entry(self, width='24', font=('lucida 13'))
        self.entryCity.insert(0, 'Enter a city...') # Adding a default value to be displayed
        self.entryCity.bind('<Button-1>', self.clearEntryDefault) # Removing the default value when clicked

        # Icon for updating data
        cwd = os.getcwd()
        imagePath = "\Images\\refreshIcon.png"
        imagePathComplete = cwd + imagePath
        refreshIconImage = Image.open(imagePathComplete)
        refreshIcon = ImageTk.PhotoImage(refreshIconImage)

        # Search and refresh buttons
        self.searchButton = ttk.Button(self, text='Search', command=self.checkInput)
        self.refreshButton = tk.Button(self, image=refreshIcon, background='lightblue', borderwidth=0, width=20, height=20, command=self.updateLabels)
        self.refreshButton.image = refreshIcon # Creating a reference to the image

        # Placements
        self.entryCity.place(x='15', y='40')
        self.searchButton.place(x='240', y='40')
        self.refreshButton.place(x='295', y='73')
        self.dateLabel.place(x='15', y='5')
        self.timeLabel.place(x='100', y='5')

        self.updateDateTime()

    # Checking input to show user errors when needed
    def checkInput(self):
        self.cityName = self.getCity()

        # Checking if a city is entered
        if ((len(self.cityName) == 0) or (self.entryCity.get() == 'Enter a city...')):
            print('Error: no city entered')
            self.placeNoCityEnteredLabel()
            self.clearDataLabels()

        # Checking if the entered city exists in the database
        elif ((CurrentForecast.isValidCity(self) == False) and (self.entryCity.get() != 'Enter a city...')):
            print('Error: city not found')
            self.placeCityNotFoundLabel()
            self.clearDataLabels()

        # Placing data and clearing errors
        else:
            self.updateLabels()
            self.placeData()
            self.cityNotFoundLabel.config(text='')
            self.cityNotEnteredLabel.config(text='')

    # Function for clearing entry when clicked
    def clearEntryDefault(self, event):
        self.entryCity.delete(0, 'end')

    # Getter for city
    def getCity(self):
        self.cityName = self.entryCity.get()

        return self.cityName

    # Getter for data
    def getData(self, index):
        dataDict = CurrentForecast.getCurrentForecast(self)

        if (dataDict is not None): # Checking that the dictionary exists
            dictToList = list(dataDict.values())[index]
            if (type(dictToList) != str): # Checking type of value to only round values that are not type(str)
                toRounded = round(dictToList), 3
                toRounded = re.sub('[()]', '', str(toRounded))

                if (((list(dataDict)[index]) == 'temp') or ((list(dataDict)[index]) == 'ftemp')):
                    roundedCelcius = toRounded + u'\N{DEGREE SIGN}C' # Adding the degree sign and C to temperature based values

                    return roundedCelcius
                else:
                    return toRounded 
            else:
                return dictToList

    # Function to update date and time
    def updateDateTime(self):
        self.timeLabel.config(text=self.getTime())
        self.dateLabel.config(text=self.getDate())

        self.after(1000, self.updateDateTime)

    def getDate(self):
        now = datetime.now()

        return now.strftime('%B %d')

    def getTime(self):
        now = datetime.now()

        return now.strftime('%H:%M')

    # Setting data to labels
    def updateLabels(self):
        self.temperatureLabel.config(text=self.getData(0))
        self.feelsLikeLabel.config(text=self.getData(1))
        self.pressureLabel.config(text=self.getData(2))
        self.humidityLabel.config(text=self.getData(3))
        self.visibilityLabel.config(text=self.getData(4))
        self.descriptionLabel.config(text=self.getData(5))

    # Placing data
    def placeData(self):
        self.temperatureLabel.place(x='190', y='100')
        self.feelsLikeLabel.place(x='190', y='125')
        self.pressureLabel.place(x='190', y='150')
        self.humidityLabel.place(x='190', y='175')
        self.visibilityLabel.place(x='190', y='200')
        self.descriptionLabel.place(x='190', y='225')

    # Placing 'no city entered' error label
    def placeNoCityEnteredLabel(self):
        self.cityNotFoundLabel.config(text='') # Clearing 'city not found' error
        self.cityNotFoundLabel.lower() # Lowering the 'city not found' label to avoid clipping
        self.cityNotEnteredLabel.config(text='No city entered')
        self.cityNotEnteredLabel.place(x='240', y='5')

    # Placing 'city not found' error label
    def placeCityNotFoundLabel(self):
        self.cityNotEnteredLabel.config(text='') # Clearing 'city not entered' error
        self.cityNotEnteredLabel.lower() # Lowering the 'city not entered' label to avoid clipping
        self.cityNotFoundLabel.config(text='City not found')
        self.cityNotFoundLabel.place(x='240', y='5')

    # Clearing data labels if city does not exist or one is not entered
    def clearDataLabels(self):
        self.temperatureLabel.config(text='')
        self.feelsLikeLabel.config(text='')
        self.pressureLabel.config(text='')
        self.humidityLabel.config(text='')
        self.visibilityLabel.config(text='')
        self.descriptionLabel.config(text='')


class CurrentForecast():

    def __init__(self, mainwin):
        self.mainwin = mainwin

    def getCurrentForecast(self):
        if (CurrentForecast.isValidCity(self) == True): # Checking that the city entered has data
            self.main = self.data['main']
            weather = self.data['weather']

            temperature = self.main['temp']
            feelsTemp = self.main['feels_like']
            pressure = self.main['pressure']
            humidity = self.main['humidity']
            visibility = self.data['visibility']
            description = weather[0]['description']

            dataDict = {'temp': temperature, 'ftemp':feelsTemp, 'pres':pressure, 'humid':humidity, 'visib':visibility, 'desc':description}

            return dataDict
        else:
            print('Error: city not found')

    def isValidCity(self):
        # API information
        self.apiKey = 'YOUR API KEY'
        self.baseURL = 'http://api.openweathermap.org/data/2.5/weather?q='

        self.city = WeatherProgram.getCity(self)
        self.completeURL = self.baseURL + self.city + '&units=metric' + '&APPID=' + self.apiKey
        response = requests.get(self.completeURL)
        self.data = response.json()
        
        # Checking that the city entered exists in the database
        if (self.data['cod'] == '404'):
            return False
        else:
            return True



if __name__ == '__main__':
    programWindow = WeatherProgram()
    programWindow.mainloop()