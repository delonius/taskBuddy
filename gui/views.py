from PyQt5.QtWidgets import QWidget, QTabWidget, QLabel
from PyQt5.QtCore import Qt
from gui.main.widgets import *
from gui.load.widgets import *
from gui.applicant.generalWidgets import *
from gui.applicant.applicantWidgets import *
from gui.applicant.taskNoteWidgets import *
from gui.applicant.addEditWidgets import *
from models import Applicants
from gui.main.styles import tabsStyle


class MainView(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.inputBox = inputBox(self)
        self.divider = divider(self)
        self.logo = logo(self)
        self.label = instructionLabel(self)
        self.fetchButton = fetchButton(self)
        self.bottomRibbon = bottomRibbon(self)


class LoadView(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.progressBar = progressBar(self)
        self.fetchLabel = fetchLabel(self)
        self.nameLabel = nameLabel(self)
        self.dupesLabel = dupesLabel(self)
        self.tasksLabel = tasksLabel(self)


class ApplicantTabView(QTabWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setStyleSheet(tabsStyle())
        self.setCornerWidget(finishButton(self, self.app), Qt.TopRightCorner)

    def addTabs(self):
        applicants = Applicants.getInstance()
        sortedApps = {
            "Flexxbuy": applicants.flexxbuyApps,
            "ePay": applicants.epayApps,
            "iQualify": applicants.iqualifyApps,
            "Portal": applicants.flexxportalApps,
            "Re-Applied": applicants.reApps
        }

        for key, value in sortedApps.items():
            if len(value) > 0:
                self.addTab(ApplicantView(value, self.app), f"{key} - {len(value)}")


class ApplicantView(QWidget):
    def __init__(self, appList, app):
        super().__init__()
        self.appList = appList
        self.app = app
        self.index = 0
        self.activeApplicant = self.appList[self.index]
        self.nextButton = nextButton(self)
        self.prevButton = prevButton(self)
        self.indexTracker = indexTracker(self)
        self.applicantBox = applicantGroupBox(self)
        self.taskBox = taskBox(self)
        self.createBox = createBox(self)
        self.editTaskPanel = AddTaskPanel(
            self.createBox, self, self.activeApplicant, editMode=True)
        self.setTaskWidget = TaskPanel(
            self.taskBox, self, self.activeApplicant)
        self.noteBox = noteBox(self)
        self.setNoteWidget = NotePanel(self.noteBox, self.activeApplicant)
        self.applicantPanel = ApplicantPanel(
            self.activeApplicant, self.applicantBox, self)
        self.applicantTabPanel = ApplicantTabPanel(
            self.activeApplicant, self.applicantBox, self)
        self.createPanel = CreatePanel(
            self.createBox, self, self.activeApplicant)
        self.editTaskPanel.setHidden(True)

        self.updateInterface()

        if len(self.appList) == 1:
            self.indexTracker.setHidden(True)
            self.nextButton.setHidden(True)

        if self.activeApplicant.duplicates:
            self.applicantPanel.setHidden(True)
            self.applicantTabPanel.setHidden(False)
        else:
            self.applicantPanel.setHidden(False)
            self.applicantTabPanel.setHidden(True)

    def incrementIndex(self):
        self.index = self.index + 1

    def decrementIndex(self):
        self.index = self.index - 1

    def getIndex(self):
        return self.index

    def updateInterface(self):
        self.indexTracker.setText(
            f"{self.index + 1} / {len(self.appList)}")
        self.activeApplicant = self.appList[self.index]
        self.applicantBox.setTitle(self.activeApplicant.name)
        self.createBox.setTitle("Add")
        self.editTaskPanel.update(self.activeApplicant)
        self.createPanel.setHidden(False)
        self.editTaskPanel.setHidden(True)

        if self.activeApplicant.duplicates:
            self.applicantPanel.setHidden(True)
            self.applicantTabPanel.setHidden(False)
            self.applicantTabPanel.update(self.activeApplicant)
        else:
            self.applicantPanel.setHidden(False)
            self.applicantTabPanel.setHidden(True)
            self.applicantPanel.update(self.activeApplicant)

        if self.index > 0:
            self.prevButton.setHidden(False)
        else:
            self.prevButton.setHidden(True)

        if self.index + 1 == len(self.appList):
            self.nextButton.setHidden(True)
        else:
            self.nextButton.setHidden(False)


class FinishConfirmationView(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.confirmationText = confirmationText(self)
        self.backButton = backButton(self, self.app)
        self.continueButton = continueButton(self, self.app)
        

class FinishLoadView(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.progressBar = progressBar(self)
        self.processLabel = processLabel(self)

class FinalConfirmationView(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.confirmationText = finalConfirmationText(self)
        self.exitButton = exitButton(self, self.app)