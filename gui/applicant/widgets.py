from PyQt5.QtWidgets import QLabel, QPushButton, QGroupBox, QFormLayout, QWidget, QTabWidget, QTreeWidget, QTreeWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from gui.applicant.styles import *
from gui.applicant.actions import *
from gui.util import Config
from datetime import datetime, timedelta


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


class ApplicantTabPanel(QTabWidget):
    def __init__(self, applicant, parent, root):
        super().__init__(parent)
        self.applicant = applicant
        self.root = root
        self.tabs = []
        self.clear()
        self.addTabs()
        self.setGeometry(0, 25, 382, 265)
        style = applicantTabPanelStyle()
        self.setStyleSheet(style)
        #self.currentChanged.connect(self.updateTasks)

    def update(self, applicant):
        self.clear()
        self.applicant = applicant
        self.tabs = []
        self.addTabs()

    def addTabs(self):
        for dupe in self.applicant.duplicates:
            self.tabs.append(dupe)

        self.tabs = self.sortTabs()

        for i in range(len(self.tabs)):
            self.addTab(ApplicantPanel(self.tabs[i], self, self.root, 10),
                        self.tabs[i].createdAt.split(' ')[0])
        self.insertTab(0, ApplicantPanel(self.applicant, self, self.root, 10), 'Active')
        self.setCurrentIndex(0)

    def sortTabs(self):
        tmp = self.tabs[:]
        for i in range(len(tmp)):
            createdAt = tmp[i].createdAt
            tmp[i] = datetime.strptime(createdAt, "%m/%d/%y %I:%M%p")
        tmp.sort()
        tmp = tmp[::-1]
        for dupe in self.applicant.duplicates:
            index = tmp.index(datetime.strptime(
                dupe.createdAt, "%m/%d/%y %I:%M%p"))
            tmp[index] = dupe
        return tmp

    def updateTasks(self):
        widget = self.widget(self.currentIndex())
        self.root.setTaskWidget.update(widget.applicant)


class ApplicantPanel(QWidget):
    def __init__(self, applicant, parent, root, y=30):
        super().__init__(parent)
        self.applicant = applicant
        self.parent = parent
        self.root = root
        self.values = None
        self.y = y
        self.highriseButton = None
        self.gatewayButton = None

        self.addLabels()
        self.addValues()
        self.addButtons()
        self.configureButtons()

    def update(self, applicant):
        self.applicant = applicant
        self.values['loanID'].setText(self.applicant.loanID)
        self.values['email'].setText(self.applicant.email)
        self.values['phone'].setText(self.applicant.phone)
        if self.applicant.isReApp:
            self.values['merchant'].setText(
                f"{self.applicant.merchant} - {self.applicant.company}")
        else:
            self.values['merchant'].setText(self.applicant.merchant)
        self.values['amountRequest'].setText(
            f"{self.applicant.amountRequest}")
        self.values['createdAt'].setText(self.applicant.createdAt)
        self.highriseButton.clicked.disconnect()
        self.gatewayButton.clicked.disconnect()
        self.configureButtons()
        self.root.setTaskWidget.update(self.applicant)

    def addLabels(self):
        labels = []
        y = self.y
        style = applicantPanelStyle()
        labels.append(QLabel("Loan ID: ", self))
        labels.append(QLabel("Email: ", self))
        labels.append(QLabel("Phone: ", self))
        labels.append(QLabel("Merchant: ", self))
        labels.append(QLabel("Request: ", self))
        labels.append(QLabel("Created: ", self))

        for label in labels:
            label.setGeometry(10, y, 80, 20)
            label.setStyleSheet(style)
            y = y + 30

    def addValues(self):
        values = {}
        y = self.y
        style = applicantPanelValueStyle()
        values['loanID'] = QLabel(self.applicant.loanID, self)
        values['email'] = QLabel(self.applicant.email, self)
        values['phone'] = QLabel(self.applicant.phone, self)
        if self.applicant.isReApp:
            values['merchant'] = QLabel(
                f"{self.applicant.merchant} - {self.applicant.company}", self)
        else:
            values['merchant'] = QLabel(self.applicant.merchant, self)
        values['amountRequest'] = QLabel(self.applicant.amountRequest, self)
        values['createdAt'] = QLabel(self.applicant.createdAt, self)

        for value in values.values():
            value.setGeometry(95, y, 270, 20)
            value.setStyleSheet(style)
            value.setTextInteractionFlags(Qt.TextSelectableByMouse)
            y = y + 30

        self.values = values

    def addButtons(self):
        self.highriseButton = highriseButton(self, self.y)
        self.gatewayButton = gatewayButton(self, self.y)

    def configureButtons(self):
        self.highriseButton.clicked.connect(
            lambda: bindHighriseButton(self.applicant))

        if self.applicant.company == 'Flexxportal':
            self.gatewayButton.clicked.connect(
                lambda: bindFlexxportalButton(self.applicant))
            self.gatewayButton.setText("Portal")
        else:
            self.gatewayButton.clicked.connect(
                lambda: bindGatewayButton(self.applicant))
            self.gatewayButton.setText("Gateway")


def highriseButton(parent, y):
    style = highriseButtonStyle()
    highriseButton = QPushButton("Highrise", parent)
    highriseButton.setGeometry(50, y + 185, 120, 30)
    highriseButton.setStyleSheet(style)

    return highriseButton


def gatewayButton(parent, y):
    style = gatewayButtonStyle()
    gatewayButton = QPushButton("Gateway", parent)
    gatewayButton.setGeometry(210, y + 185, 120, 30)
    gatewayButton.setStyleSheet(style)

    return gatewayButton


class TaskPanel(QTreeWidget):
    def __init__(self, parent, applicant):
        super().__init__(parent)
        style = taskPanelStyle()
        self.setGeometry(10, 30, 348, 190)
        self.setStyleSheet(style)
        self.setAlternatingRowColors(True)
        self.applicant = applicant
        self.config = Config.getInstance()
        self.setHeaderLabels(['User', 'Due', 'Task'])
        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 75)

        self.update(self.applicant)


    def update(self, applicant):
        self.applicant = applicant
        self.clear()
        for task in self.applicant.existingTasks:
            abbrev = self.config.users[str(task.author_id)]['abbrev']
            dueAtRaw = datetime.fromisoformat(str(task.due_at)) + timedelta(hours=-5)
            dueAt = dueAtRaw.strftime(f"%m/%d-%#I%p")
            QTreeWidgetItem(
                self, [abbrev, dueAt, task.body])
