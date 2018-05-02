import requests as request
import sys
import json
from settingsmanager import SettingsManager
from uuid import getnode as get_mac
import netifaces

class ApiClient():
    def __init__(self):
        self.settings = SettingsManager()
        self.baseUrl = "https://bartimeus-degoeie.herokuapp.com/api"

    def activateNewSensor(self):
        URL = self.baseUrl + "/camera"
        r = request.post(URL, data = { 'macAddress': get_mac() })

        if r.status_code != 201:
            print('Error during camera registring :( \n', r.text)
            sys.exit()

        result = r.json()

        self.settings.setValue('key', result["id"])
        self.settings.write()
        
        return result['id'] 

    def updateAvailability(self, cameraId, value):
        print(value)
        URL = self.baseUrl + "/camera/detection"
    
        realValue = None
        if value:
            realValue = 0
        else:
            realValue = 1

        print("Value", realValue)

        r = request.post(URL, data = {
            "cameraId": cameraId,
            "available": realValue
        })

        if r.status_code != 201:
            print('Something went wrong with updating the room\'s availability.', r.text)
        else:
            print('succes??', r.text)
            