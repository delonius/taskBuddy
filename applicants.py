from highton.highton_settings import HightonSettings
from highton.models import Person, Group
from PyQt5.QtCore import QThread, pyqtSignal
import time


class Applicants():
    __instance = None

    @staticmethod
    def getInstance():
        if Applicants.__instance == None:
            Applicants()
        return Applicants.__instance

    def __init__(self):
        if Applicants.__instance != None:
            raise Exception("This is a singleton class")
        else:
            Applicants.__instance = self

        HightonSettings(username='danw@flexxbuyapps',
                        api_key='562b762e42c6b8b09858d228f94e3a03')

        self.rawIDs = None
        self.applicants = []
        self.flexxbuyApps = []
        self.epayApps = []
        self.iqualifyApps = []
        self.flexxportalApps = []
        self.reApps = []

    def getLoanIDs(self):
        return self.rawIDs

    def getIDCount(self):
        return len(self.rawIDs)

    def getApplicantCount(self):
        return len(self.applicants)

    def getApplicants(self):
        return self.applicants

    def addToFlexxbuy(self, applicant):
        self.flexxbuyApps.append(applicant)

    def addToEpay(self, applicant):
        self.epayApps.append(applicant)

    def addToIqualify(self, applicant):
        self.iqualifyApps.append(applicant)

    def addToFlexxportal(self, applicant):
        self.flexxportalApps.append(applicant)

    def addToReApp(self, applicant):
        self.reApps.append(applicant)

    def parseListFromInput(self, text):
        text = text.replace(' ', '\n').replace('--', '')
        tmp = [item for item in text.split(
            '\n') if len(item) == 36 and '-' in item]
        rawIDs = []
        for i in tmp:
            if i not in rawIDs:
                rawIDs.append(i)
        self.rawIDs = rawIDs

    def fetchHighriseApplicant(self, loanID):
        query = Person.search(GateWayLoanId=loanID)
        if not query:
            return None
        else:
            person = query[0]
        applicant = Applicant(person, loanID)
        if applicant.name not in [app.name for app in self.applicants if app]:
            self.applicants.append(applicant)
            return applicant
        else:
            return "duplicate"


class Applicant():
    def __init__(self, applicant, loanID):
        self.applicant = applicant
        self.highriseID = applicant.id
        self.name = f"{applicant.first_name} {applicant.last_name}"
        self.loanID = loanID
        self.emailAddresses = applicant.contact_data.email_addresses
        self.email = self.emailAddresses[0] if self.emailAddresses else "N/A"
        self.phone = applicant.contact_data.phone_numbers[0]
        self.merchant = Group.get(applicant.group_id).name
        self.createdAt = applicant.created_at
        self.duplicates = []
        self.existingTasks = []

    def __str__(self):
        return f"{self.name}: {self.email} | {self.loanID}"

    def findDuplicates(self):
        querySet = []
        querySet += Person.search(self.name)
        querySet += Person.search(phone=self.phone)
        querySet += Person.search(email=self.email)
        for person in querySet:
            loanID = [
                field.value for field in person.subject_datas if field.subject_field_label == 'GateWayLoanId'][0]
            if f"{person.first_name} {person.last_name}".lower() == self.name.lower():
                if loanID != self.loanID:
                    loanIDs = [person.loanID for person in self.duplicates]
                    if loanID not in loanIDs:
                        self.duplicates.append(Applicant(person, loanID))
        for duplicate in self.duplicates:
            duplicate.findTasks()

    def findTasks(self):
        self.existingTasks = self.applicant.list_tasks()

    def addToGroup(self, applicants):
        applicants = applicants
        tags = [tag.name for tag in self.applicant.tags]
        users = [user.name for user in Group.get(
            self.applicant.group_id).users]

        if "reapp" in tags:
            applicants.addToReApp(self)
        elif "Submitted to Gateway" not in tags:
            applicants.addToFlexxportal(self)
        elif "Josh Utesch" in users:
            applicants.addToIqualify(self)
        elif "ePay apps" in users:
            applicants.addToEpay(self)
        else:
            applicants.addToFlexxbuy(self)


class ApplicantsWorker(QThread):
    update_progress = pyqtSignal(int)
    update_progress_label = pyqtSignal(str, str)
    worker_terminate = pyqtSignal(str)
    worker_success = pyqtSignal(bool)

    def run(self):
        process_failed = False
        applicants = Applicants.getInstance()
        for loanID in applicants.getLoanIDs():
            self.update_progress_label.emit("fetch", loanID)
            applicant = applicants.fetchHighriseApplicant(loanID)
            if applicant == "duplicate":
                applicants.applicants.append([])
                self.update_progress.emit(applicants.getApplicantCount())
                continue
            if not applicant:
                self.worker_terminate.emit(loanID)
                process_failed = True
                break
            self.update_progress_label.emit("name", applicant.name)
            time.sleep(1)
            self.update_progress_label.emit("duplicates", "")
            applicant.findDuplicates()
            self.update_progress_label.emit("tasks", "")
            applicant.findTasks()
            applicant.addToGroup(applicants)
            self.update_progress.emit(applicants.getApplicantCount())
            self.update_progress_label.emit("clear", "")
        self.worker_success.emit(process_failed)
