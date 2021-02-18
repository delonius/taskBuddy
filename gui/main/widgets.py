from PyQt5.QtWidgets import QPlainTextEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPixmap
from gui.main.styles import (
    inputBoxStyle, fetchButtonStyle, instructionLabelStyle,
    backButtonStyle, continueButtonStyle
)
from gui.main.actions import handleFetchClick, backButtonClick, continueButtonClick
import sys


def inputBox(window):
    style = inputBoxStyle()
    inputBox = QPlainTextEdit(window)
    inputBox.setGeometry(QRect(40, 50, 360, 500))
    inputBox.setStyleSheet(style)

    return inputBox


def divider(window):
    divider = QLabel("", window)
    divider.setGeometry(450, 50, 2, 500)
    divider.setStyleSheet("background-color: #CCCCCC")
    return divider


def logo(window):
    logoBox = QLabel("Test", window)
    logoBox.setGeometry(515, 20, 300, 150)
    logoBox.setPixmap(QPixmap('static/logo.jpg'))

    return logoBox


def instructionLabel(window):
    style = instructionLabelStyle()
    text = "Welcome to TaskBuddy!\nPaste your list in the box,\nand click the button\nto get started!"
    label = QLabel(text, window)
    label.setStyleSheet(style)
    label.setGeometry(500, 175, 300, 150)

    return label


def fetchButton(window):
    style = fetchButtonStyle()
    fetchButton = QPushButton("Fetch\nApplicants", window)
    fetchButton.setGeometry(530, 420, 200, 100)
    fetchButton.setStyleSheet(style)

    fetchButton.clicked.connect(
        lambda: handleFetchClick(window.inputBox, window.app))

    return fetchButton


def bottomRibbon(window):
    ribbon = QLabel("", window)
    ribbon.setGeometry(QRect(0, 575, 800, 25))
    ribbon.setStyleSheet("background-color: #B5DC10")

    return ribbon


def confirmationText(window):
    text = "All done?\nClick 'Continue' to begin processing\nyour changes or 'Back' to return\nto the previous screen."
    label = QLabel(text, window)
    label.setGeometry(200, 150, 400, 300)
    label.setStyleSheet(instructionLabelStyle())
    label.setAlignment(Qt.AlignHCenter)

    return label


def backButton(window, app):
    button = QPushButton("Back", window)
    button.setGeometry(220, 350, 150, 50)
    button.setStyleSheet(backButtonStyle())
    button.clicked.connect(lambda: backButtonClick(app))

    return button

def continueButton(window, app):
    button = QPushButton("Continue", window)
    button.setGeometry(430, 350, 150, 50)
    button.setStyleSheet(continueButtonStyle())
    button.clicked.connect(lambda: continueButtonClick(app))

    return button

def finalConfirmationText(window):
    text = "Your changes have been \nadded successfully!\nThank you for using TaskBuddy!"
    label = QLabel(text, window)
    label.setGeometry(200, 150, 400, 300)
    label.setStyleSheet(instructionLabelStyle())
    label.setAlignment(Qt.AlignHCenter)

    return label

def exitButton(window, app):
    button = QPushButton("Exit", window)
    button.setGeometry(325, 325, 150, 50)
    button.setStyleSheet(backButtonStyle())
    button.clicked.connect(lambda: sys.exit())

    return button
