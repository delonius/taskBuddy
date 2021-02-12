import json
from highton.highton_settings import HightonSettings
from highton.models import User

class Alert():
    __instance = None

    @staticmethod
    def getInstance():
        if Alert.__instance == None:
            Alert()
        return Alert.__instance

    def __init__(self, application, window):
        Alert.__instance == self
        self.application = application

    def run(self):
        self.application.alert(window)


class Config():
    __instance = None

    @staticmethod
    def getInstance():
        if Config.__instance == None:
            Config()
        return Config.__instance
    
    def __init__(self):
        Config.__instance = self
        with open('config.json') as f:
            data = json.load(f)
            self.users = data["users"]
            self.taskCategories = data["taskCategories"]
            self.auth = data["auth"]
            HightonSettings(username=self.auth["username"]+"@flexxbuyapps",
                        api_key=self.auth["token"])
            self.id = User.me().id
            