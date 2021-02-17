from PyQt5.QtWidgets import QProgressBar, QLabel
from PyQt5.QtCore import Qt
from gui.load.styles import progressBarStyle


def progressBar(window):
    style = progressBarStyle()
    bar = QProgressBar(window)
    bar.setGeometry(100, 200, 600, 30)
    bar.setMaximum(0)
    bar.setTextVisible(True)
    bar.setAlignment(Qt.AlignCenter)
    bar.setStyleSheet(style)
    bar.setFormat("%v / %m")
    return bar

def fetchLabel(window):
    label = QLabel("", window)
    label.setGeometry(150, 250, 600, 30)
    label.setStyleSheet("font-family: Helvetica; font-size: 16px;")
    return label

def nameLabel(window):
    label = QLabel("", window)
    label.setGeometry(150, 280, 600, 30)
    label.setStyleSheet("font-family: Helvetica; font-size: 16px;")
    return label

def dupesLabel(window):
    label = QLabel("", window)
    label.setGeometry(200, 310, 600, 30)
    label.setStyleSheet("font-family: Helvetica; font-size: 14px;")
    return label

def tasksLabel(window):
    label = QLabel("", window)
    label.setGeometry(200, 340, 600, 30)
    label.setStyleSheet("font-family: Helvetica; font-size: 14px;")
    return label

def processLabel(window):
    label = QLabel("", window)
    label.setGeometry(150, 250, 600, 30)
    label.setStyleSheet("font-family: Helvetica; font-size: 16px;")
    return label