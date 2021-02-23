from gui.applicant.styles import (
    inputBoxStyle,
    applicantTabPanelStyle,
    gatewayButtonStyle,
    deleteButtonStyle,
    calendarStyle,
    dateButtonStyle,
    taskInputStyle
)
from gui.applicant.actions import showCalendar
from highton.models import Note, Task
from util import Config
from datetime import datetime, timedelta
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (
    QWidget,
    QTabWidget,
    QLabel,
    QPushButton,
    QPlainTextEdit,
    QComboBox,
    QMessageBox,
    QCalendarWidget
)


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

        self.dueAtInfoLabel = QLabel("at", self)
        self.dueAtInfoLabel.setGeometry(165 + x, 90 + y, 100, 30)
        self.dueAtInfoLabel.setStyleSheet(
            "font-family: Helvetica; font-weight: bold;")

        self.templateBox = QComboBox(self)
        self.templateBox.setGeometry(70 + x, 13 + y, 280, 30)
        self.templateBox.activated.connect(self.taskBoxSelection)

        self.taskInputStyle = taskInputStyle()
        self.taskInput = QPlainTextEdit(self)
        self.taskInput.setGeometry(72 + x, 15 + y, 254, 28)
        self.taskInput.setStyleSheet(self.taskInputStyle)
        self.taskInput.setHidden(True)

        self.userBox = QComboBox(self)
        self.userBox.setGeometry(70 + x, 53 + y, 120, 30)

        self.typeBox = QComboBox(self)
        self.typeBox.setGeometry(250 + x, 53 + y, 100, 30)

        self.dateBox = QPushButton(self)
        self.dateBox.setGeometry(70 + x, 93 + y, 90, 30)
        self.dateBox.clicked.connect(lambda: showCalendar(self))
        self.dateBox.setStyleSheet(dateButtonStyle())

        self.hoursBox = QComboBox(self)
        self.hoursBox.setGeometry(200 + x, 93 + y, 60, 30)

        self.amPmBox = QComboBox(self)
        self.amPmBox.setGeometry(270 + x, 93 + y, 60, 30)

        self.calendar = QCalendarWidget(self.root.createBox)
        self.calendar.setGeometry(1, 0, 367, 226)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setStyleSheet(calendarStyle())
        self.calendar.setGridVisible(True)
        self.calendar.setHidden(True)
        self.calendar.clicked.connect(self.selectDate)

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

    def taskBoxSelection(self, index):
        if self.templateBox.itemText(index) == '<Custom Task>':
            self.taskInput.setHidden(False)
            self.taskInput.setFocus()
        else:
            self.taskInput.setHidden(True)

    def selectDate(self, date):
        pyDate = date.toPyDate()
        self.dateBox.setText(pyDate.strftime('%m/%d/%Y'))
        self.calendar.setHidden(True)

    def populateFields(self):
        self.userBox.addItems(['Me'])
        for user, value in self.config.users.items():
            if not user == str(self.config.id):
                name = value['name']
                self.userBox.addItems([name])

        for item in self.config.taskTemplates.keys():
            self.templateBox.addItems([item])
        self.templateBox.addItems(['<Custom Task>'])

        self.typeBox.addItems(['None'])
        for category, value in self.config.taskCategories.items():
            name = value['name']
            self.typeBox.addItems([name])

        weekendDays = ['Fri', 'Sat', 'Sun']
        setDay = datetime.today()
        if datetime.now().hour >= 17:
            setDay += timedelta(days=1)
        while setDay.strftime('%a') in weekendDays:
            setDay += timedelta(days=1)

        self.dateBox.setText(setDay.strftime('%m/%d/%Y'))
        self.calendar.setSelectedDate(setDay)

        for i in range(1, 13):
            self.hoursBox.addItems([str(i)])
        self.hoursBox.setCurrentIndex(7)

        self.amPmBox.addItems(['AM', 'PM'])

    def update(self, applicant):
        self.applicant = applicant

    def addTask(self):
        body = None
        if self.taskInput.isHidden():
            body = self.templateBox.currentText()
        else:
            body = self.taskInput.toPlainText()
        if body:
            hour = int(self.hoursBox.currentText())
            if self.amPmBox.currentText() == 'PM':
                hour = hour + 12
                if hour == 24:
                    hour = 0
            parsedDate = datetime.strptime(self.dateBox.text(), '%m/%d/%Y')
            dueAt = parsedDate.replace(
                hour=hour, minute=0, second=0, microsecond=0)
            task = Task()
            task.body = body
            task.subject_type = "Party"
            task.subject_id = self.applicant.highriseID
            task.public = True
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
        self.taskInput.setHidden(True)
        self.userBox.setCurrentIndex(0)
        self.typeBox.setCurrentIndex(0)
        self.hoursBox.setCurrentIndex(7)
        self.amPmBox.setCurrentIndex(0)
        weekendDays = ['Fri', 'Sat', 'Sun']
        setDay = datetime.today()
        if datetime.now().hour >= 17:
            setDay += timedelta(days=1)
        while setDay.strftime('%a') in weekendDays:
            setDay += timedelta(days=1)

        if self.templateBox.currentText() == '<Custom Task>':
            self.templateBox.setCurrentIndex(0)

        self.dateBox.setText(setDay.strftime('%m/%d/%Y'))


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
