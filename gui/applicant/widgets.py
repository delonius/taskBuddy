from datetime import datetime, timedelta
from gui.util import Config
from gui.applicant.styles import *
from gui.applicant.actions import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QTextCharFormat, QIcon
from PyQt5.QtWidgets import (
    QLabel, QPushButton, QGroupBox, QFormLayout, QWidget, QTabWidget,
    QTreeWidget, QTreeWidgetItem, QHeaderView, QPlainTextEdit, QComboBox, QMessageBox
)
from highton.models import Note, Task


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
        self.currentChanged.connect(self.syncData)

    def update(self, applicant):
        self.clear()
        self.applicant = applicant
        self.tabs = []
        self.addTabs()
        self.root.createBox.setTitle("Add")
        self.root.createPanel.setHidden(False)
        self.root.editTaskPanel.setHidden(True)

    def addTabs(self):
        for dupe in self.applicant.duplicates:
            self.tabs.append(dupe)

        self.tabs = self.sortTabs()

        for i in range(len(self.tabs)):
            self.addTab(ApplicantPanel(self.tabs[i], self, self.root, 10),
                        self.tabs[i].createdAt.split(' ')[0])
        self.insertTab(0, ApplicantPanel(
            self.applicant, self, self.root, 10), 'Active')
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

    def syncData(self):
        index = self.currentIndex()
        self.root.setTaskWidget.update(self.tabs[index])
        self.root.setNoteWidget.update(self.tabs[index])
        self.root.createPanel.addNotePanel.update(self.tabs[index])
        self.root.createPanel.addTaskPanel.update(self.tabs[index])
        self.root.editTaskPanel.update(self.tabs[index])
        self.root.createBox.setTitle("Add")
        self.root.createPanel.setHidden(False)
        self.root.editTaskPanel.setHidden(True)
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
        self.root.createPanel.addNotePanel.update(self.applicant)
        self.root.createPanel.addTaskPanel.update(self.applicant)
        self.root.createBox.setTitle("Add")
        self.root.createPanel.setHidden(False)
        self.root.editTaskPanel.setHidden(True)

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
            value.setGeometry(95, y, 274, 20)
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


class TaskPanel(QTreeWidget):
    def __init__(self, parent, root, applicant):
        super().__init__(parent)
        style = taskPanelStyle()
        self.root = root
        self.setGeometry(10, 30, 348, 190)
        self.setStyleSheet(style)
        self.setAlternatingRowColors(True)
        self.setRootIsDecorated(False)
        self.applicant = applicant
        self.config = Config.getInstance()
        self.setHeaderLabels(['index', 'User', 'Due', 'Task'])
        self.setColumnHidden(0, True)
        self.setColumnWidth(1, 35)
        self.setColumnWidth(2, 100)
        self.itemDoubleClicked.connect(self.setEditTask)

        self.update(self.applicant)

    def update(self, applicant):
        self.applicant = applicant
        self.clear()
        self.root.editTaskPanel.update(self.applicant)

        newChangedTasks = self.applicant.newTasks + self.applicant.changedTasks
        newChangedTasks.sort(key=lambda task: task.due_at, reverse=False)

        for task in newChangedTasks:
            if str(task.owner_id) in self.config.users:
                abbrev = self.config.users[str(task.owner_id)]['abbrev']
                dueAtRaw = datetime.fromisoformat(str(task.due_at))
                dueAt = dueAtRaw.strftime(f"%m/%d-%#I%p")
                categoryId = task.category_id
                index = None
                if task in self.applicant.newTasks:
                    index = "new " + str(self.applicant.newTasks.index(task))
                elif task in self.applicant.changedTasks:
                    index = "changed " + \
                        str(self.applicant.changedTasks.index(task))
                task = QTreeWidgetItem(
                    self, [index, abbrev, dueAt, task.body])
                if categoryId:
                    task.setBackground(
                        3, QColor(self.config.taskCategories[str(categoryId)]['color']))
                    task.setForeground(3, QColor('white'))
                fontFormat = QFont()
                fontFormat.setWeight(QFont.Bold)
                task.setFont(1, fontFormat)
                task.setFont(2, fontFormat)
                task.setFont(3, fontFormat)

        for task in self.applicant.existingTasks:
            if str(task.owner_id) in self.config.users:
                abbrev = self.config.users[str(task.owner_id)]['abbrev']
                dueAt = task.due_at.strftime(f"%m/%d-%#I%p")
                categoryId = task.category_id
                index = "existing " + \
                    str(self.applicant.existingTasks.index(task))
                task = QTreeWidgetItem(
                    self, [index, abbrev, dueAt, task.body])
                if categoryId:
                    task.setBackground(
                        3, QColor(self.config.taskCategories[str(categoryId)]['color']))
                    task.setForeground(3, QColor('white'))

    def setEditTask(self, item, n):
        taskList = item.data(0, 0).split(' ')[0]
        index = int(item.data(0, 0).split(' ')[1])
        self.root.editTaskPanel.update(self.applicant)
        task = None
        if taskList == 'new':
            task = self.applicant.newTasks[index]
        elif taskList == 'changed':
            task = self.applicant.changedTasks[index]
        elif taskList == 'existing':
            task = self.applicant.existingTasks[index]
            task.due_at = task.due_at

        self.root.editTaskPanel.setEditTask(task)

        editTaskPanel = self.root.editTaskPanel
        self.root.createBox.setTitle("Edit Task")
        self.root.createPanel.setHidden(True)
        editTaskPanel.setHidden(False)
        userIndex = 0
        typeIndex = 0

        if task.owner_id != self.config.id:
            userIndex = editTaskPanel.userBox.findText(
                self.config.users[str(task.owner_id)]['name'])

        if task.category_id:
            typeIndex = editTaskPanel.typeBox.findText(
                self.config.taskCategories[str(task.category_id)]['name'])
        daysIndex = editTaskPanel.daysBox.findText(
            str(task.due_at.day - datetime.now().day))
        hours = task.due_at.strftime("%#I")
        amPmIndex = 0
        if task.due_at.strftime("%p") == 'PM':
            amPmIndex = 1
        hoursIndex = editTaskPanel.hoursBox.findText(hours)

        editTaskPanel.taskInput.setPlainText(task.body)
        editTaskPanel.userBox.setCurrentIndex(userIndex)
        editTaskPanel.typeBox.setCurrentIndex(typeIndex)
        editTaskPanel.daysBox.setCurrentIndex(daysIndex)
        editTaskPanel.hoursBox.setCurrentIndex(hoursIndex)
        editTaskPanel.amPmBox.setCurrentIndex(amPmIndex)


class NotePanel(QTreeWidget):
    def __init__(self, parent, applicant):
        super().__init__(parent)
        style = taskPanelStyle()
        self.setGeometry(10, 30, 360, 130)
        self.setStyleSheet(style)
        self.setAlternatingRowColors(True)
        self.setRootIsDecorated(False)
        self.applicant = applicant
        self.deletingNote = None
        self.config = Config.getInstance()
        self.setHeaderLabels(['index', 'User', 'Date', 'Note'])
        self.setColumnHidden(0, True)
        self.setColumnWidth(1, 35)
        self.setColumnWidth(2, 35)
        self.itemDoubleClicked.connect(self.setDeleteNote)

        self.update(self.applicant)

    def update(self, applicant):
        self.applicant = applicant
        self.clear()

        for note in self.applicant.newNotes[::-1]:
            abbrev = ''
            createdAtRaw = note.created_at
            createdAt = createdAtRaw.strftime(f"%#m/%#d")
            body = note.body.replace('\n', ' ')
            index = "new " + str(self.applicant.newNotes.index(note))
            if str(note.author_id) in self.config.users:
                abbrev = self.config.users[str(note.author_id)]['abbrev']
            if not 'leadUuid' in note.body:
                noteItem = QTreeWidgetItem(
                    self, [index, abbrev, createdAt, body])
                fontFormat = QFont()
                fontFormat.setWeight(QFont.Bold)
                noteItem.setFont(1, fontFormat)
                noteItem.setFont(2, fontFormat)
                noteItem.setFont(3, fontFormat)
                tooltip = tooltip = f"{createdAtRaw.strftime('%#m/%#d/%Y')} || {note.body}"
                noteItem.setToolTip(3, tooltip)

        for note in self.applicant.existingNotes:
            abbrev = ''
            createdAtRaw = note.created_at
            createdAt = createdAtRaw.strftime(f"%#m/%#d")
            body = note.body.replace('\n', ' ')
            index = "exiting " + str(self.applicant.existingNotes.index(note))
            if str(note.author_id) in self.config.users:
                abbrev = self.config.users[str(note.author_id)]['abbrev']
            if not 'leadUuid' in note.body:
                noteItem = QTreeWidgetItem(
                    self, [index, abbrev, createdAt, body])
                tooltip = f"{createdAtRaw.strftime('%#m/%#d/%Y')} || {note.body}"
                noteItem.setToolTip(3, tooltip)

    def setDeleteNote(self, item, n):
        noteList = item.data(0, 0).split(' ')[0]
        index = int(item.data(0, 0).split(' ')[1])
        if noteList == "new":
            self.deletingNote = self.applicant.newNotes[index]
            msg = QMessageBox()
            msg.setText("Are you sure you want to delete this note?")
            msg.setWindowTitle("Warning")
            msg.setWindowIcon(QIcon('static/icon.png'))
            msg.setIcon(QMessageBox.Warning)
            msg.addButton(QMessageBox.Yes)
            msg.addButton(QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            msg.buttonClicked.connect(self.deleteNote)
            msg.exec_()

    def deleteNote(self, i):
        if i.text() == '&Yes':
            self.applicant.newNotes.remove(self.deletingNote)
            self.deletingNote = None
            self.update(self.applicant)


class CreatePanel(QTabWidget):
    def __init__(self, parent, root, applicant):
        super().__init__(parent)
        self.root = root
        self.applicant = applicant
        style = applicantTabPanelStyle()
        self.setGeometry(0, 25, 370, 205)
        self.setStyleSheet(style)
        self.addTaskPanel = AddTaskPanel(self, self.root, self.applicant)
        self.addNotePanel = AddNotePanel(self, self.root, self.applicant)

        self.addTab(self.addTaskPanel, "Task")
        self.addTab(self.addNotePanel, "Note")


class AddTaskPanel(QWidget):
    def __init__(self, parent, root, applicant, editMode=False):
        super().__init__(parent)
        self.applicant = applicant
        self.root = root
        self.editTask = None
        self.editMode = editMode
        self.config = Config.getInstance()
        self.addWidgets()
        self.populateFields()

    def setEditTask(self, task):
        self.editTask = task

    def addWidgets(self):
        y = 0
        x = 0
        if self.editMode:
            y = 56
            x = 2
        self.taskLabel = QLabel("Task: ", self)
        self.taskLabel.setGeometry(20 + x, 10 + y, 50, 30)
        self.taskLabel.setStyleSheet(
            "font-family: Helvetica; font-weight: bold;")

        self.userLabel = QLabel("User: ", self)
        self.userLabel.setGeometry(20 + x, 50 + y, 50, 30)
        self.userLabel.setStyleSheet(
            "font-family: Helvetica; font-weight: bold;")

        self.typeLabel = QLabel("Type: ", self)
        self.typeLabel.setGeometry(200 + x, 50 + y, 50, 30)
        self.typeLabel.setStyleSheet(
            "font-family: Helvetica; font-weight: bold;")

        self.dueAtLabel = QLabel("When: ", self)
        self.dueAtLabel.setGeometry(20 + x, 90 + y, 50, 30)
        self.dueAtLabel.setStyleSheet(
            "font-family: Helvetica; font-weight: bold;")

        self.dueAtInfoLabel = QLabel("days, at ", self)
        self.dueAtInfoLabel.setGeometry(135 + x, 90 + y, 100, 30)
        self.dueAtInfoLabel.setStyleSheet(
            "font-family: Helvetica; font-weight: bold;")

        self.inputBoxStyle = inputBoxStyle()
        self.taskInput = QPlainTextEdit(self)
        self.taskInput.setGeometry(70 + x, 13 + y, 280, 30)
        self.taskInput.setStyleSheet(self.inputBoxStyle)

        self.userBox = QComboBox(self)
        self.userBox.setGeometry(70 + x, 53 + y, 120, 30)

        self.typeBox = QComboBox(self)
        self.typeBox.setGeometry(250 + x, 53 + y, 100, 30)

        self.daysBox = QComboBox(self)
        self.daysBox.setGeometry(70 + x, 93 + y, 60, 30)

        self.hoursBox = QComboBox(self)
        self.hoursBox.setGeometry(200 + x, 93 + y, 60, 30)

        self.amPmBox = QComboBox(self)
        self.amPmBox.setGeometry(270 + x, 93 + y, 60, 30)

        if not self.editMode:
            self.addButton = QPushButton("Add Task", self)
            self.addButton.setGeometry(125 + x, 135 + y, 120, 30)
            self.addButton.setStyleSheet(gatewayButtonStyle())
            self.addButton.clicked.connect(self.addTask)
        else:
            self.addButton = QPushButton("Save Task", self)
            self.addButton.setGeometry(47 + x, 135 + y, 120, 30)
            self.addButton.setStyleSheet(gatewayButtonStyle())
            self.addButton.clicked.connect(self.addTask)

            self.deleteButton = QPushButton("Delete Task", self)
            self.deleteButton.setGeometry(195 + x, 135 + y, 120, 30)
            self.deleteButton.setStyleSheet(deleteButtonStyle())
            self.deleteButton.clicked.connect(self.deletePrompt)

    def populateFields(self):
        self.userBox.addItems(['Me'])
        for user, value in self.config.users.items():
            if not user == str(self.config.id):
                name = value['name']
                self.userBox.addItems([name])

        self.typeBox.addItems(['None'])
        for category, value in self.config.taskCategories.items():
            name = value['name']
            self.typeBox.addItems([name])

        for i in range(1, 31):
            self.daysBox.addItems([str(i)])

        for i in range(1, 13):
            self.hoursBox.addItems([str(i)])
            self.hoursBox.setCurrentIndex(7)

        self.amPmBox.addItems(['AM', 'PM'])

    def update(self, applicant):
        self.applicant = applicant

    def addTask(self):
        body = self.taskInput.toPlainText()
        if body:
            days = int(self.daysBox.currentText())
            hour = int(self.hoursBox.currentText())
            if self.amPmBox.currentText() == 'PM':
                hour = hour + 12
                if hour == 24:
                    hour = 0
            dueAt = datetime.now().replace(
                hour=hour, minute=0, second=0, microsecond=0) + timedelta(days=days)
            task = Task()
            task.body = body
            task.subject_type = "Party"
            task.subject_id = self.applicant.highriseID
            category = None
            for key, value in self.config.taskCategories.items():
                if value['name'] == self.typeBox.currentText():
                    category = key
            if category:
                task.category_id = category
            task.due_at = dueAt
            ownerId = self.config.id
            for key, value in self.config.users.items():
                if self.userBox.currentText() == value['name']:
                    ownerId = key
            task.owner_id = ownerId

            if self.editTask:
                unchanged = True
                if not self.editTask.body == task.body:
                    unchanged = False
                if not str(self.editTask.owner_id) == str(task.owner_id):
                    unchanged = False
                if not str(self.editTask.due_at) == str(task.due_at):
                    unchanged = False
                if not str(self.editTask.category_id) == str(task.category_id):
                    unchanged = False
                if not unchanged:
                    if self.editTask in self.applicant.existingTasks:
                        task.id = self.editTask.id
                        self.applicant.existingTasks.remove(self.editTask)
                        self.applicant.changedTasks.append(task)
                    elif self.editTask in self.applicant.newTasks:
                        self.applicant.newTasks.remove(self.editTask)
                        self.applicant.newTasks.append(task)
                    elif self.editTask in self.applicant.changedTasks:
                        self.applicant.changedTasks.remove(self.editTask)
                        self.applicant.changedTasks.append(task)
                    self.root.setTaskWidget.update(self.applicant)
                    self.root.applicantPanel.update(self.applicant)
                    self.resetInterface()
                self.root.createPanel.setHidden(False)
                self.root.editTaskPanel.setHidden(True)
                self.root.setTaskWidget.update(self.applicant)
                self.root.applicantTabPanel.syncData()
                self.root.createBox.setTitle("Add")
                self.editTask = None
                self.root.applicantPanel.update(self.applicant)
                self.resetInterface()
            else:
                self.applicant.newTasks.append(task)
                self.root.setTaskWidget.update(self.applicant)
                self.root.applicantPanel.update(self.applicant)
                self.resetInterface()
            if self.root.applicantTabPanel.isHidden():
                self.root.updateInterface()

    def deletePrompt(self):
        msg = QMessageBox()
        msg.setText("Are you sure you want to delete this task?")
        msg.setWindowTitle("Warning")
        msg.setWindowIcon(QIcon('static/icon.png'))
        msg.setIcon(QMessageBox.Warning)
        msg.addButton(QMessageBox.Yes)
        msg.addButton(QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.buttonClicked.connect(self.deleteTask)
        msg.exec_()

    def deleteTask(self, i):
        if i.text() == '&Yes':
            task = self.editTask

            if task in self.applicant.newTasks:
                self.applicant.newTasks.remove(task)
            if task in self.applicant.existingTasks:
                self.applicant.existingTasks.remove(task)
                self.applicant.deleteTasks.append(task)
            if task in self.applicant.changedTasks:
                self.applicant.changedTasks.remove(task)
                if task.id:
                    self.applicant.deleteTasks.append(task)
            self.root.setTaskWidget.update(self.applicant)
            self.root.createPanel.setHidden(False)
            self.root.editTaskPanel.setHidden(True)

    def resetInterface(self):
        self.taskInput.setPlainText("")
        self.userBox.setCurrentIndex(0)
        self.typeBox.setCurrentIndex(0)
        self.daysBox.setCurrentIndex(0)
        self.hoursBox.setCurrentIndex(7)
        self.amPmBox.setCurrentIndex(0)


class AddNotePanel(QWidget):
    def __init__(self, parent, root, applicant):
        super().__init__(parent)
        self.applicant = applicant
        self.root = root
        self.config = Config.getInstance()

        self.inputBoxStyle = inputBoxStyle()
        self.textBox = QPlainTextEdit(self)
        self.textBox.setGeometry(17, 20, 330, 100)
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
