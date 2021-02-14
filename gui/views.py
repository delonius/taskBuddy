from PyQt5.QtWidgets import QWidget, QTabWidget, QLabel
from PyQt5.QtCore import Qt
from gui.main.widgets import inputBox, bottomRibbon, fetchButton, instructionLabel, logo, divider
from gui.load.widgets import progressBar, fetchLabel, nameLabel, dupesLabel, tasksLabel
from gui.applicant.widgets import *
from applicants import Applicants
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
        self.setCornerWidget(finishButton(self), Qt.TopRightCorner)

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
                self.addTab(ApplicantView(value), f"{key} - {len(value)}")


class ApplicantView(QWidget):
    def __init__(self, appList):
        super().__init__()
        self.appList = appList
        self.index = 0
        self.activeApplicant = self.appList[self.index]
        self.nextButton = nextButton(self)
        self.prevButton = prevButton(self)
        self.indexTracker = indexTracker(self)
        self.applicantBox = applicantGroupBox(self)
        self.taskBox = taskBox(self)
        self.setTaskWidget = TaskPanel(
            self.taskBox, self, self.activeApplicant)
        self.noteBox = noteBox(self)
        self.setNoteWidget = NotePanel(self.noteBox, self.activeApplicant)
        self.applicantPanel = ApplicantPanel(
            self.activeApplicant, self.applicantBox, self)
        self.applicantTabPanel = ApplicantTabPanel(
            self.activeApplicant, self.applicantBox, self)
        self.createBox = createBox(self)
        self.createPanel = CreatePanel(
            self.createBox, self, self.activeApplicant)
        self.editTaskPanel = AddTaskPanel(
            self.createBox, self, self.activeApplicant, editMode=True)
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
