from datetime import datetime, timedelta
from gui.util import Config
from gui.applicant.styles import *
from gui.applicant.actions import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QTextCharFormat
from PyQt5.QtWidgets import (
    QLabel, QPushButton, QGroupBox, QFormLayout, QWidget, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QHeaderView, QPlainTextEdit
)
from highton.models import Note



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


class ApplicantTabPanel(QTabWidget):
    def __init__(self, applicant, parent, root):
        super().__init__(parent)
        self.applicant = applicant
        self.root = root
        self.parent = parent
        self.tabs = []
        self.clear()
        self.addTabs()
        self.setGeometry(0, 25, 382, 265)
        style = applicantTabPanelStyle()
        self.setStyleSheet(style)
        self.currentChanged.connect(self.updateData)

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
        self.tabs.insert(0, self.applicant)
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

    def updateData(self):
        index = self.currentIndex()
        self.root.setTaskWidget.update(self.tabs[index])
        self.root.setNoteWidget.update(self.tabs[index])
        self.parent.setTitle(self.tabs[index].name)


class ApplicantPanel(QWidget):
    def __init__(self, applicant, parent, root, y=40):
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
        self.root.setTaskWidget.update(self.applicant)
        self.root.setNoteWidget.update(self.applicant)

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
        self.root.setNoteWidget.update(self.applicant)

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
        self.setRootIsDecorated(False)
        self.applicant = applicant
        self.config = Config.getInstance()
        self.setHeaderLabels(['User', 'Due', 'Task'])
        self.setColumnWidth(0, 35)
        self.setColumnWidth(1, 90)

        self.update(self.applicant)


    def update(self, applicant):
        self.applicant = applicant
        self.clear()
        for task in self.applicant.existingTasks:
            if str(task.author_id) in self.config.users:
                abbrev = self.config.users[str(task.author_id)]['abbrev']
                dueAtRaw = datetime.fromisoformat(str(task.due_at)) + timedelta(hours=-5)
                dueAt = dueAtRaw.strftime(f"%m/%d-%#I%p")
                categoryId = task.category_id
                task = QTreeWidgetItem(
                    self, [abbrev, dueAt, task.body])
                if categoryId:
                    task.setBackground(2, QColor(self.config.taskCategories[str(categoryId)]['color']))
                    task.setForeground(2, QColor('white'))


class NotePanel(QTreeWidget):
    def __init__(self, parent, applicant):
        super().__init__(parent)
        style = taskPanelStyle()
        self.setGeometry(10, 30, 360, 130)
        self.setStyleSheet(style)
        self.setAlternatingRowColors(True)
        self.setRootIsDecorated(False)
        self.applicant = applicant
        self.config = Config.getInstance()
        self.setHeaderLabels(['User', 'Date', 'Note'])
        self.setColumnWidth(0, 35)
        self.setColumnWidth(1, 35)

        self.update(self.applicant)


    def update(self, applicant):
        self.applicant = applicant
        self.clear()

        for note in self.applicant.newNotes[::-1]:
            abbrev = ''
            createdAtRaw = note.created_at
            createdAt = createdAtRaw.strftime(f"%#m/%#d")
            body = note.body.replace('\n', ' ')
            if str(note.author_id) in self.config.users:
                abbrev = self.config.users[str(note.author_id)]['abbrev']
            if not 'leadUuid' in note.body:  
                note = QTreeWidgetItem(
                    self, [abbrev, createdAt, body])
                fontFormat = QFont()
                fontFormat.setWeight(QFont.Bold)
                note.setFont(0, fontFormat)
                note.setFont(1, fontFormat)
                note.setFont(2, fontFormat)

        for note in self.applicant.existingNotes:
            abbrev = ''
            createdAtRaw = note.created_at
            createdAt = createdAtRaw.strftime(f"%#m/%#d")
            body = note.body.replace('\n', ' ')
            if str(note.author_id) in self.config.users:
                abbrev = self.config.users[str(note.author_id)]['abbrev']
            if not 'leadUuid' in note.body:  
                note = QTreeWidgetItem(
                    self, [abbrev, createdAt, body])



class CreatePanel(QTabWidget):
    def __init__(self, parent, root, applicant):
        super().__init__(parent)
        self.root = root
        self.applicant = applicant
        style = applicantTabPanelStyle()
        self.setGeometry(0, 25, 370, 205)
        self.setStyleSheet(style)
        self.addNotePanel = AddNotePanel(self, self.root, self.applicant)

        self.addTab(self.addNotePanel, "Note")



class AddNotePanel(QWidget):
    def __init__(self, parent, root, applicant):
        super().__init__(parent)
        self.applicant = applicant
        self.root = root
        self.config = Config.getInstance()

        self.inputBoxStyle = inputBoxStyle()
        self.textBox = QPlainTextEdit(self)
        self.textBox.setGeometry(20, 20, 330, 100)
        self.textBox.setStyleSheet(self.inputBoxStyle)

        self.buttonStyle = gatewayButtonStyle()
        self.button = QPushButton("Add Note", self)
        self.button.setGeometry(125, 135, 120, 30)
        self.button.setStyleSheet(self.buttonStyle)
        self.button.clicked.connect(self.addNote)

    def update(self, applicant):
        self.applicant = applicant


    def addNote(self):
        body = self.textBox.toPlainText()
        if body:
            note = Note()
            note.body = body
            note.author_id = self.config.id
            note.subject_type = "Party"
            note.subject_id = self.applicant.highriseID
            note.created_at = datetime.now()
            self.applicant.newNotes.append(note)
            self.root.setNoteWidget.update(self.applicant)
            self.textBox.setPlainText("")
