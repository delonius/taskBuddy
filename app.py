from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QMessageBox
from PyQt5.QtGui import QIcon, QFontDatabase
from models import Applicants
from workers import FetchWorker, FinishWorker
from util import Config
import sys
from gui.views import (
    MainView,
    LoadView,
    ApplicantTabView,
    FinishConfirmationView,
    FinishLoadView,
    FinalConfirmationView
)


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flexxbuy TaskBuddy")
        self.setWindowIcon(QIcon('static/icon.png'))
        self.setGeometry(200, 200, 800, 600)
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: white")
        self.config = Config.getInstance()

        self.fetchWorker = FetchWorker()
        self.finishWorker = FinishWorker()

        self.initUI()
        self.setCurrentIndex(self.mainView)

    def initUI(self):
        self.mainView = self.addWidget(MainView(self))
        self.loadView = self.addWidget(LoadView(self))
        self.appView = self.addWidget(ApplicantTabView(self))
        self.confirmationView = self.addWidget(FinishConfirmationView(self))
        self.finishLoadView = self.addWidget(FinishLoadView(self))
        self.finalConfirmationView = self.addWidget(FinalConfirmationView(self))

    def displayMessage(self, title, text, type=None):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setWindowIcon(QIcon('static/icon.png'))

        if type == 'warning':
            msg.setIcon(QMessageBox.Warning)
        else:
            msg.setIcon(QMessageBox.Information)
        msg.show()
        msg.exec_()
        return msg


app = QApplication(sys.argv)
QFontDatabase.addApplicationFont("static/IndieFlower-Regular.ttf")
window = MainWindow()
window.show()
sys.exit(app.exec_())
