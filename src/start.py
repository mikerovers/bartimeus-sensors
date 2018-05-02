from motiondetector import MotionDetector
from settingsmanager import SettingsManager
from apiclient import ApiClient
from threading import Timer
import argparse

class Start:   
    def __init__(self):
        self.showWindows = None
        self.parseArguments()
        self.settings = SettingsManager()
        self.motiondetector = MotionDetector(showWindows=self.showWindows)
        self.apiClient = ApiClient()
        self.motion = False
        self.timer = None
        self.onTimer = Timer(3.0, self.resetOnTimer)
        self.cameraId = None
        self.motionScore = 0.0

        self.initializeApp()

    def initializeApp(self):
        newKey = self.apiClient.activateNewSensor()
        self.cameraId = self.settings.getValue('key')
        self.motiondetector.run(self.motionDetected)

    def parseArguments(self):
        parser = argparse.ArgumentParser(description="Bartimeus argument parser.")
        parser.add_argument("-w", "--windows", required=False, help="Show windows with motion results.")
        args = parser.parse_args()


        if args.windows:
            print(args.windows)
            if int(args.windows) == 1:
                print('true')
                self.showWindows = True
            else:
                self.showWindows = False
        else:
            self.showWindows = False

    def turnOffRoom(self):
        print('timer afgelopen!')
        self.apiClient.updateAvailability(self.cameraId, False)
        self.motionScore = 0.0
        self.motion = False

    def turnOnRoom(self):
        print('turning on')
        self.apiClient.updateAvailability(self.cameraId, True)

        return None

    def resetOnTimer(self):
        self.motionScore = 0.0
        if self.onTimer != None:
            self.onTimer.cancel()

        self.onTimer = Timer(3, self.resetOnTimer)
        self.onTimer.start()

        print('Reset onTimer')
        
    def motionDetected(self, value):
        self.motionScore += value
        print("Motion score: ", self.motionScore)
        if self.motionScore > 500:
            self.resetOnTimer()
            if self.motion == False:
                self.turnOnRoom()
                self.motion = True
    
            if self.timer != None:
                self.timer.cancel()

            self.timer = Timer(3.0, self.turnOffRoom)
            self.timer.start()

if __name__ == '__main__':
    app = Start()
