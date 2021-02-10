from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from applicants import Applicants


def handleFetchClick(inputBox, app):
    applicants = Applicants.getInstance()
    progressBar = app.widget(app.loadView).progressBar
    fetchLabel = app.widget(app.loadView).fetchLabel
    nameLabel = app.widget(app.loadView).nameLabel
    dupesLabel = app.widget(app.loadView).dupesLabel
    tasksLabel = app.widget(app.loadView).tasksLabel
    progressBar.setValue(0)
    applicants.parseListFromInput(inputBox.toPlainText())
    loanIDCount = applicants.getIDCount()
    progressBar.setMaximum(loanIDCount)

    def workerUpdateProgress():
        progressBar.setValue(applicants.getApplicantCount())

    def workerUpdateLabel(label, data):
        if label == "fetch":
            fetchLabel.setText(f"Fetching applicant from ID - {data}")
        if label == "name":
            nameLabel.setText(f"Located applicant - {data}")
        if label == "duplicates":
            dupesLabel.setText("--Finding duplicate applications...")
        if label == "tasks":
            tasksLabel.setText("--Finding existing tasks...")
        if label == "clear":
            fetchLabel.setText("")
            nameLabel.setText("")
            dupesLabel.setText("")
            tasksLabel.setText("")

    def workerSuccess(success):
        QApplication.alert(app)
        QApplication.beep()
        appView = app.widget(app.appView)
        appView.addTabs()
        app.setCurrentIndex(app.appView)

    if loanIDCount == 0:
        app.displayMessage('Warning',
                           'Invalid data. \nPlease paste your list in the box.', 'warning')
        inputBox.selectAll()
    else:
        app.setCurrentIndex(app.loadView)
        app.worker.start()
        app.worker.update_progress.connect(workerUpdateProgress)
        app.worker.update_progress_label.connect(workerUpdateLabel)
        app.worker.worker_success.connect(workerSuccess)
