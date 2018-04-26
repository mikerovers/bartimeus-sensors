from configparser import SafeConfigParser

class SettingsManager():
    def __init__(self):
        self.config = SafeConfigParser()
        self.config.read('config.ini')
        
    def getValue(self, key):
        try:
            returnself.config.get('sensor', key)
        except:
            return None

    def setValue(self, key, value):
        self.config.set('sensor', key, value)

    def write(self):
        with open('config.ini', 'w') as f:
            self.config.write(f)

    def initialize(self):
        self.config.add_section('sensor')

        self.write()