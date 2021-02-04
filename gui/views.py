from PyQt5.QtWidgets import QWidget, QTabWidget
from PyQt5.QtCore import Qt
from gui.main.widgets import inputBox, bottomRibbon, fetchButton, instructionLabel, logo, divider
from gui.load.widgets import progressBar, fetchLabel, nameLabel, dupesLabel, tasksLabel
from gui.applicant.widgets import indexTracker, prevButton, nextButton, applicantGroupBox, applicantPanel, finishButton, taskInfoBox, setTaskBox, setNoteBox
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
            "Flexxportal": applicants.flexxportalApps,
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
        self.applicantLabels, self.applicantValues = applicantPanel(
            self.applicantBox)
        self.taskInfoBox = taskInfoBox(self)
        self.setTaskBox = setTaskBox(self)
        self.setNoteBox = setNoteBox(self)

        self.updateInterface()

        if len(self.appList) == 1:
            self.indexTracker.setHidden(True)
            self.nextButton.setHidden(True)

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

        self.applicantValues['loanID'].setText(self.activeApplicant.loanID)
        self.applicantValues['email'].setText(self.activeApplicant.email)
        self.applicantValues['phone'].setText(self.activeApplicant.phone)
        self.applicantValues['merchant'].setText(self.activeApplicant.merchant)
        self.applicantValues['amountRequest'].setText(
            self.activeApplicant.amountRequest)
        self.applicantValues['date'].setText(self.activeApplicant.createdAt)

        if self.index > 0:
            self.prevButton.setHidden(False)
        else:
            self.prevButton.setHidden(True)

        if self.index + 1 == len(self.appList):
            self.nextButton.setHidden(True)
        else:
            self.nextButton.setHidden(False)
