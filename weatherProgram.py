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
import timeit
import config
import collections

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
        self.tempTextLabel = tk.Label(self, text='Temperature', font=('calibri', 12), background='white').place(x='15', y='100')
        self.feelsTextLabel = tk.Label(self, text='Feels like', font=('calibri', 12), background='white').place(x='15', y='125')
        self.pressureTextLabel = tk.Label(self, text='Pressure', font=('calibri', 12), background='white').place(x='15', y='150')
        self.humidityTextLabel = tk.Label(self, text='Humidity', font=('calibri', 12), background='white').place(x='15', y='175')
        self.visibilityTextLabel = tk.Label(self, text='Visibility', font=('calibri', 12), background='white').place(x='15', y='200')
        self.descriptionTextLabel = tk.Label(self, text='Description', font=('calibri', 12), background='white').place(x='15', y='225')
        self.descriptionTextLabel = tk.Label(self, text='Wind speed', font=('calibri', 12), background='white').place(x='15', y='250')

        self.cityNameLabel = tk.Label(self, text='', font=('calibri', 12), background='lightblue')

        # Data labels
        self.curTempLabel = tk.Label(self, background='white', text='', font=('calibri', 12))
        self.feelsLikeLabel = tk.Label(self, background='white', text='', font=('calibri', 12))
        self.pressureLabel = tk.Label(self, background='white', text='', font=('calibri', 12))
        self.humidityLabel = tk.Label(self, background='white', text='', font=('calibri', 12))
        self.visibilityLabel = tk.Label(self, background='white', text='', font=('calibri', 12))
        self.descriptionLabel = tk.Label(self, background='white', text='', font=('calibri', 12))
        self.windSpeedLabel = tk.Label(self, background='white', text='', font=('calibri', 12))

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
        self.refreshButton = tk.Button(self, image=refreshIcon, background='lightblue', borderwidth=0, width=20, height=20, command=lambda:self.updateLabels())
        self.refreshButton.image = refreshIcon # Creating a reference to the image

        # Placements that can't / shouldn't be done while declaring
        self.entryCity.place(x='15', y='40')
        self.searchButton.place(x='240', y='40')
        self.refreshButton.place(x='295', y='73')
        self.dateLabel.place(x='15', y='5')
        self.timeLabel.place(x='100', y='5')

        self.updateDateTime()

    # Checking input to show user errors when needed
    def checkInput(self):
        # print('checkInput')
        self.start = timeit.default_timer()

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

    # Function for clearing entry when clicked
    def clearEntryDefault(self, event):
        # print('clearEntryDefault')
        self.entryCity.delete(0, 'end')

    # Getter for city
    def getCity(self):
        # print('getCity')
        cityName = self.entryCity.get()

        # Making sure cityNameLabel has a value
        if (len(self.cityNameLabel.cget('text')) != 0):
            cityName = self.cityNameLabel.cget('text')

        return cityName

    # Getter for data
    def getData(self, index):
        # print('getData')
        currentDataDict = CurrentForecast.getCurrentForecast(self)

        if (currentDataDict is not None): # Checking that the dictionary exists
            dictToList = list(currentDataDict.values())[index]
            if (type(dictToList) != str): # Checking type of value to only round values that are not type(str)
                toRounded = round((dictToList), 2)
                toRounded = re.sub('[()]', '', str(toRounded))

                # Adding approriate units to data output
                if (((list(currentDataDict)[index]) == 'temp') or ((list(currentDataDict)[index]) == 'ftemp')):
                    roundedCelcius = toRounded + u'\N{DEGREE SIGN}C'
                    return roundedCelcius
                elif ((list(currentDataDict)[index]) == 'pressure'):
                    return toRounded + ' hPa'
                elif ((list(currentDataDict)[index]) == 'humidity'):
                    return toRounded + ' %'
                elif ((list(currentDataDict)[index]) == 'visibility'):
                    return toRounded + ' m'
                elif ((list(currentDataDict)[index] == 'windSpeed')):
                    return toRounded + ' m/s'
                else:
                    return toRounded 
            else:
                return dictToList

    # Updating date and time
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
        # print('updateLabels')
        self.cityNameLabel.config(text=self.getCity())

        self.curTempLabel.config(text=self.getData(0))
        self.feelsLikeLabel.config(text=self.getData(1))
        self.pressureLabel.config(text=self.getData(2))
        self.humidityLabel.config(text=self.getData(3))
        self.visibilityLabel.config(text=self.getData(4))
        self.descriptionLabel.config(text=self.getData(5))
        self.windSpeedLabel.config(text=self.getData(6))

    # Placing data
    def placeData(self):
        # print('placeData')
        self.cityNameLabel.place(x='15', y='70')
        self.clearEntryDefault(self)

        self.curTempLabel.place(x='200', y='100')
        self.feelsLikeLabel.place(x='200', y='125')
        self.pressureLabel.place(x='200', y='150')
        self.humidityLabel.place(x='200', y='175')
        self.visibilityLabel.place(x='200', y='200')
        self.descriptionLabel.place(x='200', y='225')
        self.windSpeedLabel.place(x='200', y='250')

        # Clearing possible error messages
        self.cityNotFoundLabel.config(text='') 
        self.cityNotEnteredLabel.config(text='')

        self.stop = timeit.default_timer()
        print("Time to retreive and place data:", self.stop - self.start)

    # Placing 'no city entered' error label
    def placeNoCityEnteredLabel(self):
        # print('placeNoCityEnteredLabel')
        self.cityNotFoundLabel.config(text='') # Clearing 'city not found' error
        self.cityNotFoundLabel.lower() # Lowering the 'city not found' label to avoid clipping
        self.cityNotEnteredLabel.config(text='No city entered')
        self.cityNotEnteredLabel.place(x='240', y='5')

    # Placing 'city not found' error label
    def placeCityNotFoundLabel(self):
        # print('placeCityNotFoundLabel')
        self.cityNotEnteredLabel.config(text='') # Clearing 'city not entered' error
        self.cityNotEnteredLabel.lower() # Lowering the 'city not entered' label to avoid clipping
        self.cityNotFoundLabel.config(text='City not found')
        self.cityNotFoundLabel.place(x='240', y='5')

    # Clearing data labels if city does not exist or one is not entered
    def clearDataLabels(self):
        # print('clearDataLabels')
        self.curTempLabel.config(text='')
        self.feelsLikeLabel.config(text='')
        self.pressureLabel.config(text='')
        self.humidityLabel.config(text='')
        self.visibilityLabel.config(text='')
        self.descriptionLabel.config(text='')


class CurrentForecast():

    def getCurrentForecast(self):
        if (CurrentForecast.isValidCity(self) == True): # Checking that the city entered has data
            main = self.currentData['main']
            weather = self.currentData['weather']

            curTemp = main['temp']
            feelsTemp = main['feels_like']
            pressure = main['pressure']
            humidity = main['humidity']
            visibility = self.currentData['visibility']
            wind = self.currentData['wind']
            windSpeed = wind['speed']
            description = weather[0]['description']

            # Using a dictionary to store and return the data. This is done to be able to match keys for data formatting.
            currentDataDict = {'temp': curTemp, 'ftemp':feelsTemp, 'pressure':pressure, \
                        'humidity':humidity, 'visibility':visibility, 'description':description, \
                        'windSpeed':windSpeed}

            return currentDataDict
        else:
            print('Error: city not in database.')

    def isValidCity(self):
        baseURL = 'http://api.openweathermap.org/data/2.5/weather?q='

        city = WeatherProgram.getCity(self)
        completeURL = baseURL + city + '&units=metric' + '&APPID=' + config.apiKey
        response = requests.get(completeURL)
        self.currentData = response.json()

        # Checking that the city entered exists in the database
        if (self.currentData['cod'] == 200):
            return True
        else:
            return False


class SevenDayForecast(CurrentForecast):

    def getDailyForecast(self):
        cityCoordinates = geoLocation.getLatitudeLongitude(self)
        lat = cityCoordinates.lat
        lon = cityCoordinates.lon

        onecallBaseURL = 'http://api.openweathermap.org/data/2.5/onecall?'
        completeUrlDaily = onecallBaseURL + 'lat=' + lat + '&lon=' + lon + '&exclude=current,minutely,hourly,alerts' + '&appid=' + config.apiKey

        dailyResponse = requests.get(completeUrlDaily)
        self.dailyData = dailyResponse.json()

        if (self.dailyData['cod'] == 200):
            return True
        else:
            return False

    def validCityDaily(self):
        pass


class geoLocation():
    
    # Using an API to get latitude and longitude for given city
    def getLatitudeLongitude(self):
        geoBaseURL = 'http://api.openweathermap.org/geo/1.0/direct?q='
        city = WeatherProgram.getCity(self)
        geoCompleteURL = geoBaseURL + city + '&APPID=' + config.apiKey

        geoResponse = requests.get(geoCompleteURL)
        geoData = geoResponse.json()

        lat = str(geoData[0]['lat'])
        lon = str(geoData[0]['lon'])

        locTuple = collections.namedtuple('returns', ['lat', 'lon'])
        location = locTuple(lat, lon)

        return location



if __name__ == '__main__':
    programWindow = WeatherProgram()
    programWindow.mainloop()
