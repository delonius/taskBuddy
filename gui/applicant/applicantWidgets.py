from gui.applicant.actions import bindHighriseButton, bindFlexxportalButton, bindGatewayButton
from gui.applicant.styles import (
    applicantPanelStyle,
    applicantTabPanelStyle,
    applicantPanelValueStyle,
    highriseButtonStyle,
    gatewayButtonStyle
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QTabWidget,
    QWidget,
    QLabel,
    QPushButton
)
from datetime import datetime

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
        emailText = ""
        if self.applicant.email == 'N/A':
            emailText = self.applicant.email
        else:
            emailText = f'<a href="mailto:{self.applicant.email}">{self.applicant.email}</a>'
        self.values['loanID'].setText(self.applicant.loanID)
        self.values['email'].setText(emailText)
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
        emailText = ""
        if self.applicant.email == 'N/A':
            emailText = self.applicant.email
        else:
            emailText = f'<a href="mailto:{self.applicant.email}">{self.applicant.email}</a>'
        emailValue = QLabel(self)
        emailValue.setText(emailText)
        emailValue.setOpenExternalLinks(True)
        values['email'] = emailValue
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
            if value != values['email']:
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
