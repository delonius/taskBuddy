from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

def handleButtonNext(tab):
    tab.incrementIndex()
    tab.updateInterface()


def handleButtonPrev(tab):
    tab.decrementIndex()
    tab.updateInterface()


def bindLinkButtons(applicant):
    highriseUrl = f"https://flexxbuyapps.highrisehq.com/people/{applicant.highriseID}"
    QDesktopServices.openUrl(QUrl(highriseUrl))