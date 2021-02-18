from PyQt5.QtCore import QThread, pyqtSignal
from models import Applicants
from datetime import timedelta
from requests.auth import HTTPBasicAuth
from util import Config
import requests
import time

class FetchWorker(QThread):
    update_progress = pyqtSignal(int)
    update_progress_label = pyqtSignal(str, str)
    worker_success = pyqtSignal(bool)

    def run(self):
        applicants = Applicants.getInstance()
        for loanID in applicants.getLoanIDs():
            self.update_progress_label.emit("fetch", loanID)
            applicant = applicants.fetchHighriseApplicant(loanID)
            if applicant == "duplicate" or loanID in applicants.allIDs or not applicant:
                applicants.applicants.append([])
                self.update_progress.emit(applicants.getApplicantCount())
                continue
            applicants.allIDs.append(applicant)
            self.update_progress_label.emit("name", applicant.name)
            time.sleep(1)
            self.update_progress_label.emit("duplicates", "")
            applicant.findDuplicates()
            self.update_progress_label.emit("tasks", "")
            applicant.findTasks()
            applicant.addToGroup(applicants)
            if applicant.isReApp:
                applicant.addReAppCompany()
            self.update_progress.emit(applicants.getApplicantCount())
            self.update_progress_label.emit("clear", "")
        if len(applicants.allIDs) > 0:
            self.worker_success.emit(True)
        else:
            self.worker_success.emit(False)


class FinishWorker(QThread):
    update_progress = pyqtSignal(int)
    update_progress_label = pyqtSignal(str)
    worker_success = pyqtSignal(bool)
    progress = 0

    def run(self):
        applicants = Applicants.getInstance()
        applicantList = applicants.getFinalApplicantList()
        config = Config.getInstance()

        def createTask(task):
            task = task
            task.due_at = task.due_at + timedelta(hours=5)
            task.create()

        def updateTask(task):
            task = task
            task.due_at = task.due_at + timedelta(hours=5)
            task.update()

        def deleteTask(task):
            task = task
            url = f"https://flexxbuyapps.highrisehq.com/tasks/{task.id}.xml"
            auth = HTTPBasicAuth(
                username=config.auth['token'], password="")
            headers = {
                "User-Agent": "Flexxbuy (http://www.flexxbuy.com)",
                "Content-Type": "application/xml"
            }
            requests.delete(url=url, headers=headers, auth=auth)

        for applicant in applicantList:
            self.update_progress_label.emit(applicant.name)
            newTasks = applicant.newTasks
            newNotes = applicant.newNotes
            changedTasks = applicant.changedTasks
            deleteTasks = applicant.deleteTasks
            for dupe in applicant.duplicates:
                newTasks = newTasks + dupe.newTasks
                newNotes = newNotes + dupe.newNotes
                changedTasks = changedTasks + dupe.changedTasks
                deleteTasks = deleteTasks + dupe.deleteTasks
            for task in newTasks:
                createTask(task)
            for task in changedTasks:
                if task.id:
                    updateTask(task)
            for task in deleteTasks:
                deleteTask(task)
            for note in newNotes:
                note.create()

            self.progress = self.progress + 1
            self.update_progress.emit(self.progress)
        self.worker_success.emit(True)