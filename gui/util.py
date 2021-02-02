
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
