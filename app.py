from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QMessageBox
from PyQt5.QtGui import QIcon, QFontDatabase
from gui.views import MainView, LoadView, ApplicantTabView, FinishConfirmationView
from applicants import Applicants, ApplicantsWorker
from gui.util import Config
import sys


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flexxbuy TaskBuddy")
        self.setWindowIcon(QIcon('static/icon.png'))
        self.setGeometry(200, 200, 800, 600)
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: white")
        self.config = Config.getInstance()

        self.worker = ApplicantsWorker()

        self.initUI()
        self.setCurrentIndex(self.mainView)

    def initUI(self):
        self.mainView = self.addWidget(MainView(self))
        self.loadView = self.addWidget(LoadView(self))
        self.appView = self.addWidget(ApplicantTabView(self))
        self.confirmationView = self.addWidget(FinishConfirmationView(self))

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
