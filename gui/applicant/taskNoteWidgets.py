from gui.applicant.styles import taskPanelStyle
from util import Config
from datetime import datetime
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem,
    QHeaderView
)

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