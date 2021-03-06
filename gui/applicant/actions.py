from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, QDate, Qt
from gui.main.actions import processChanges


def handleButtonNext(tab):
    tab.incrementIndex()
    tab.updateInterface()


def handleButtonPrev(tab):
    tab.decrementIndex()
    tab.updateInterface()


def bindHighriseButton(applicant):
    highriseUrl = f"https://flexxbuyapps.highrisehq.com/people/{applicant.highriseID}"
    QDesktopServices.openUrl(QUrl(highriseUrl))


def bindGatewayButton(applicant):
    gatewayUrl = f"https://reporting.mktplacegateway.com/loanApplication/{applicant.loanID}"
    QDesktopServices.openUrl(QUrl(gatewayUrl))


def bindFlexxportalButton(applicant):
    flexxportalUrl = f"https://app.flexxbuy.com/r/application/{applicant.loanID}/details/"
    QDesktopServices.openUrl(QUrl(flexxportalUrl))

def showCalendar(window):
    window.calendar.setHidden(False)