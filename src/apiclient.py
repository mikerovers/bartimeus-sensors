import requests as request
import sys
from settingsmanager import SettingsManager
from uuid import getnode as get_mac
import netifaces

class ApiClient():
    def __init__(self):
        self.settings = SettingsManager()
        self.baseUrl = "http://localhost:3000/api"

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
        URL = self.baseUrl + "/availability"
        r = request.post(URL, data = {
            "id": cameraId,
            "available": value
        })

        if r.status_code != 200:
            print('Something went wrong with updateing the room\'s availability.')
            