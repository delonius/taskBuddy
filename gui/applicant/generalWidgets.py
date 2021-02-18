from PyQt5.QtCore import Qt
from gui.applicant.actions import handleButtonPrev, handleButtonNext 
from gui.main.actions import loadFinishView
from PyQt5.QtWidgets import (
    QGroupBox, 
    QLabel,
    QPushButton
)
from gui.applicant.styles import (
    applicantBoxStyle,
    buttonStyle,
    finishButtonStyle,
    trackerStyle
)


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


def finishButton(window, app):
    style = finishButtonStyle()
    button = QPushButton("Finish", window)
    button.setStyleSheet(style)
    button.clicked.connect(lambda: loadFinishView(app))

    return button


def applicantGroupBox(window):
    style = applicantBoxStyle()
    groupBox = QGroupBox(window)
    groupBox.setGeometry(20, 20, 380, 290)
    groupBox.setStyleSheet(style)

    return groupBox


def noteBox(window):
    style = applicantBoxStyle()
    noteBox = QGroupBox(window)
    noteBox.setGeometry(20, 310, 380, 170)
    noteBox.setStyleSheet(style)
    noteBox.setTitle("Notes")

    return noteBox


def taskBox(window):
    style = applicantBoxStyle()
    taskBox = QGroupBox(window)
    taskBox.setGeometry(410, 20, 368, 230)
    taskBox.setStyleSheet(style)
    taskBox.setTitle("Tasks")

    return taskBox


def createBox(window):
    style = applicantBoxStyle()
    createBox = QGroupBox(window)
    createBox.setGeometry(410, 250, 368, 230)
    createBox.setStyleSheet(style)
    createBox.setTitle("Add")

    return createBox