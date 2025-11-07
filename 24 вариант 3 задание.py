import pandas as pd
from datetime import datetime

# СУЩНОСТИ
class User:
    def __init__(self, user_id, fullname, email, departament, role):
        self.user_id = user_id
        self.fullname = fullname
        self.email = email
        self.departament = departament
        self.role = role

class Application:
    def __init__(self, id_application, application_type, description, date_submit, priority=3):
        self.id_application = id_application
        self.application_type = application_type
        self.description = description
        self.date_submit = date_submit
        self.priority = priority
        self.deadline = None
        self.actual_complete_date = None
        self.comment = None
        self.application_status = "Новая"

class Comment:
    def __init__(self, comment_id, application_id, author_id, text, date_added):
        self.comment_id = comment_id
        self.application_id = application_id
        self.author_id = author_id
        self.text = text
        self.date_added = date_added

class Journal:
    def __init__(self):
        self.all_applications = []
        
# УПРАВЛЯЮЩИЙ КЛАСС
class ManagerApplication:
    def __init__(self):
        self.users = []
        self.journal = Journal()
        self.comments = []
        self.next_app_id = 1
        self.next_comment_id = 1
    
    def create_application(self, description, type):
        app_type = type
        app = Application(self.next_app_id, app_type, description, datetime.now())
        app.id_application = self.next_app_id
        self.next_app_id += 1
        self.journal.all_applications.append(app)
        return app
    
    def supplement_application(self, applicationId, priority, deadline):
        for app in self.journal.all_applications:
            if app.id_application == applicationId:
                app.priority = priority
                app.deadline = deadline
                app.application_status = "Назначена"
                return True
        return False
    
    def update_application_status(self, application_id, status):
        for app in self.journal.all_applications:
            if app.id_application == application_id:
                app.application_status = status
                return True
        return False
    
    def add_comment(self, application_id, author_id, text):
        comment = Comment(self.next_comment_id, application_id, author_id, text, datetime.now())
        self.next_comment_id += 1
        self.comments.append(comment)
        return comment
    
    def get_journal(self):
        return self.journal.all_applications
    
    def analyze_journal(self):
        type_count = {}
        for app in self.journal.all_applications:
            if app.application_type in type_count:
                type_count[app.application_type] += 1
            else:
                type_count[app.application_type] = 1
        return type_count
    
    def extract_type(self, description):
        types = ["нет сети", "не включается", "оборудование", "программное обеспечение", "медленная работа"]
        for t in types:
            if t in description.lower():
                return t
        return "другое"
    
# ГРАНИЧНЫЕ КЛАССЫ
class SubmittingApplication:
    def __init__(self, manager):
        self.manager = manager
    
    def enter_application_data(self, application_type, description):
        return {"type": application_type, "description": description}
    
    def submit_application(self, title, description, creator_id):
        return self.manager.create_application(title, description, creator_id)

class ApplicationSupplement:
    def __init__(self, manager):
        self.manager = manager
    
    def select_performer(self, performer_id):
        return performer_id
    
    def set_priority(self, priority):
        return priority
    
    def set_deadline(self, date):
        return date
    
    def confirm_supplement(self, application_id, performer_id, priority, deadline):
        return self.manager.supplementApplication(application_id, performer_id, priority, deadline)

class JournalView:
    def __init__(self, manager):
        self.manager = manager
    
    def show_journal(self):
        applications = self.manager.get_journal()
        print("\n=== Журнал заявок ===")
        for app in applications:
            print(f"#{app.id_application}: {app.application_type} - {app.application_status}")
    
    def filter_applications(self, filter_type=None):
        applications = self.manager.get_journal()
        if filter_type:
            return [app for app in applications if app.application_type == filter_type]
        return applications
    
    def show_application_details(self, application_id):
        applications = self.manager.get_journal()
        for app in applications:
            if app.id_application == application_id:
                print(f"\n=== Детали заявки #{app.id_application} ===")
                print(f"Тип: {app.application_type}")
                print(f"Описание: {app.description}")
                print(f"Статус: {app.application_status}")
                print(f"Приоритет: {app.priority}")
                return app
        return None
