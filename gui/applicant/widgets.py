from PyQt5.QtWidgets import QLabel, QPushButton, QGroupBox, QFormLayout
from PyQt5.QtCore import Qt
from gui.applicant.styles import trackerStyle, buttonStyle, applicantBoxStyle, finishButtonStyle
from gui.applicant.actions import handleButtonNext, handleButtonPrev


def indexTracker(window):
    style = trackerStyle()
    tracker = QLabel("", window)
    tracker.setGeometry(350, 500, 100, 20)
    tracker.setAlignment(Qt.AlignHCenter)
    tracker.setStyleSheet(style)
    return tracker


def prevButton(window):
    style = buttonStyle()
    button = QPushButton("Prev", window)
    button.setGeometry(20, 490, 100, 40)
    button.setStyleSheet(style)

    button.clicked.connect(lambda: handleButtonPrev(window))

    return button


def nextButton(window):
    style = buttonStyle()
    button = QPushButton("Next", window)
    button.setGeometry(680, 490, 100, 40)
    button.setStyleSheet(style)

    button.clicked.connect(lambda: handleButtonNext(window))

    return button


def finishButton(window):
    style = finishButtonStyle()
    button = QPushButton("Finish", window)
    button.setStyleSheet(style)

    return button


def applicantGroupBox(window):
    style = applicantBoxStyle()
    groupBox = QGroupBox(window)
    groupBox.setGeometry(20, 20, 380, 290)
    groupBox.setStyleSheet(style)

    return groupBox

def taskInfoBox(window):
    style = applicantBoxStyle()
    infoBox = QGroupBox(window)
    infoBox.setGeometry(20, 310, 380, 170)
    infoBox.setStyleSheet(style)
    infoBox.setTitle("Info")

    return infoBox

def setTaskBox(window):
    style = applicantBoxStyle()
    taskBox = QGroupBox(window)
    taskBox.setGeometry(410, 20, 368, 230)
    taskBox.setStyleSheet(style)
    taskBox.setTitle("Tasks")

    return taskBox

def setNoteBox(window):
    style = applicantBoxStyle()
    noteBox = QGroupBox(window)
    noteBox.setGeometry(410, 250, 368, 230)
    noteBox.setStyleSheet(style)
    noteBox.setTitle("Notes")

    return noteBox

def applicantPanel(parent):
    pass
