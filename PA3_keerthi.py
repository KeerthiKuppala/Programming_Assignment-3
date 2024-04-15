import csv
from datetime import datetime
import random
import string

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class Patient:
    def __init__(self, patient_id, gender, race, age, ethnicity, insurance, zip_code):
        self.patient_id = patient_id
        self.gender = gender
        self.race = race
        self.age = age
        self.ethnicity = ethnicity
        self.insurance = insurance
        self.zip_code = zip_code
        self.visits = []

    def add_visit(self, visit):
        self.visits.append(visit)

class Visit:
    def __init__(self, visit_id, visit_time, department, chief_complaint):
        self.visit_id = visit_id
        self.visit_time = visit_time
        self.department = department
        self.chief_complaint = chief_complaint
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

class Note:
    def __init__(self, note_id, note_type):
        self.note_id = note_id
        self.note_type = note_type

class Hospital:
    def __init__(self):
        self.patients = {}

    def add_patient(self, patient):
        self.patients[patient.patient_id] = patient

    def remove_patient(self, patient_id):
        if patient_id in self.patients:
            del self.patients[patient_id]
            print("Patient and associated records removed successfully.")
        else:
            print("Patient not found.")

    def retrieve_patient(self, patient_id):
        if patient_id in self.patients:
            patient = self.patients[patient_id]
            print("Patient information for ID:", patient_id)
            info_needed = input("Enter the information needed ('all' to display all information, or specify: gender, race, age, ethnicity, insurance, zip code, visits): ").strip().lower()
            if info_needed == 'all':
                print("Gender:", patient.gender)
                print("Race:", patient.race)
                print("Age:", patient.age)
                print("Ethnicity:", patient.ethnicity)
                print("Insurance:", patient.insurance)
                print("Zip code:", patient.zip_code)
                print("Visits:")
                for visit in patient.visits:
                    print("Visit ID:", visit.visit_id)
                    print("Visit time:", visit.visit_time.strftime('%Y-%m-%d'))
                    print("Department:", visit.department)
                    print("Chief complaint:", visit.chief_complaint)
            elif info_needed in ['gender', 'race', 'age', 'ethnicity', 'insurance', 'zip code', 'visits']:
                if info_needed == 'gender':
                    print("Gender:", patient.gender)
                elif info_needed == 'race':
                    print("Race:", patient.race)
                elif info_needed == 'age':
                    print("Age:", patient.age)
                elif info_needed == 'ethnicity':
                    print("Ethnicity:", patient.ethnicity)
                elif info_needed == 'insurance':
                    print("Insurance:", patient.insurance)
                elif info_needed == 'zip code':
                    print("Zip code:", patient.zip_code)
                elif info_needed == 'visits':
                    print("Visits:")
                    for visit in patient.visits:
                        print("Visit ID:", visit.visit_id)
                        print("Visit time:", visit.visit_time.strftime('%Y-%m-%d'))
                        print("Department:", visit.department)
                        print("Chief complaint:", visit.chief_complaint)
            else:
                print("Invalid information requested.")
        else:
            print("Patient not found.")

    def count_visits_on_date(self, date):
        total_visits = 0
        for patient in self.patients.values():
            for visit in patient.visits:
                if visit.visit_time.date() == date.date():
                    total_visits += 1
        return total_visits

    def get_patient_count_by_insurance(self):
        insurance_count = {}
        for patient in self.patients.values():
            if patient.insurance not in insurance_count:
                insurance_count[patient.insurance] = 1
            else:
                insurance_count[patient.insurance] += 1
        return insurance_count

    def get_patient_count_by_demographics(self, attribute):
        count_by_attribute = {}
        for patient in self.patients.values():
            value = getattr(patient, attribute)
            if value not in count_by_attribute:
                count_by_attribute[value] = 1
            else:
                count_by_attribute[value] += 1
        return count_by_attribute

    def get_patient_count_by_department(self):
        department_count = {}
        for patient in self.patients.values():
            for visit in patient.visits:
                department = visit.department
                if department not in department_count:
                    department_count[department] = 1
                else:
                    department_count[department] += 1
        return department_count

def read_patient_data(file_path):
    hospital = Hospital()
    with open(file_path, 'r') as file:
        if file_path.lower().endswith('.csv'):
            reader = csv.DictReader(file)
            for row in reader:
                patient_id = row['Patient_ID']
                if patient_id not in hospital.patients:
                    patient = Patient(patient_id, row['Gender'], row['Race'], int(row['Age']), row['Ethnicity'], row['Insurance'], row['Zip_code'])
                    hospital.add_patient(patient)
                visit_id = row['Visit_ID']
                visit_time = datetime.strptime(row['Visit_time'], '%Y-%m-%d')
                department = row['Visit_department']
                chief_complaint = row['Chief_complaint']
                visit = Visit(visit_id, visit_time, department, chief_complaint)
                patient = hospital.patients[patient_id]
                patient.add_visit(visit)
        elif file_path.lower().endswith('.txt'):
            # Skip header row
            next(file)
            for line in file:
                data = line.strip().split(',')
                patient_id = data[1]  # Adjust index to skip the first column
                if patient_id not in hospital.patients:
                    patient = Patient(patient_id, data[6], data[5], int(data[8]), data[7], data[10], data[9])
                    hospital.add_patient(patient)
                try:
                    visit_time = datetime.strptime(data[3], '%Y-%m-%d')
                except ValueError:
                    visit_time = datetime.now()  # Use current date as fallback
                department = data[4]
                chief_complaint = data[11]
                visit = Visit(data[2], visit_time, department, chief_complaint)
                patient = hospital.patients[patient_id]
                patient.add_visit(visit)
        else:
            print("Unsupported file format.")
    return hospital

def read_user_credentials(file_path):
    users = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user = User(row['username'], row['password'], row['role'])
            users.append(user)
    return users

def generate_unique_visit_id(patient):
    while True:
        visit_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if all(visit_id != visit.visit_id for visit in patient.visits):
            return visit_id

def generate_statistics(hospital):
    print("Select statistics to generate:")
    print("1. Patient count by insurance type")
    print("2. Patient count by demographics groups (age, race, gender, ethnicity)")
    print("3. Patient count by visit department")
    choice = input("Enter your choice (1/2/3): ")
    if choice == "1":
        insurance_count = hospital.get_patient_count_by_insurance()
        print("Insurance Count:")
        for insurance, count in insurance_count.items():
            print(f"{insurance}: {count}")
    elif choice == "2":
        demographics = ["age", "race", "gender", "ethnicity"]
        for attribute in demographics:
            count_by_attribute = hospital.get_patient_count_by_demographics(attribute)
            print(f"Patient count by {attribute}:")
            for value, count in count_by_attribute.items():
                print(f"{value}: {count}")
    elif choice == "3":
        department_count = hospital.get_patient_count_by_department()
        print("Patient count by visit department:")
        for department, count in department_count.items():
            print(f"{department}: {count}")
    else:
        print("Invalid choice.")

def main(credential_file_path, patient_file_path):
    users = read_user_credentials(credential_file_path)
    hospital = read_patient_data(patient_file_path)

    username = input("Enter username: ")
    password = input("Enter password: ")

    user = None
    for u in users:
        if u.username == username and u.password == password:
            user = u
            break

    if user:
        print("Login successful!")
        if user.role == "management":
            generate_statistics(hospital)
        elif user.role == "admin":
            date_str = input("Enter date (YYYY-MM-DD): ")
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                total_visits = hospital.count_visits_on_date(date)
                print("Total visits on", date.strftime('%Y-%m-%d'), ":", total_visits)
            except ValueError:
                print("Invalid date format.")
        elif user.role in ["nurse", "clinician"]:
            while True:
                action = input("Choose an action (add_patient, remove_patient, retrieve_patient, count_visits, stop): ").strip().lower()
                
                if action == "stop":
                    break
                elif action == "add_patient":
                    patient_id = input("Enter Patient_ID: ")
                    if patient_id in hospital.patients:
                        visit_time_str = input("Enter Visit_time (YYYY-MM-DD): ")
                        visit_time = datetime.strptime(visit_time_str, '%Y-%m-%d')
                        patient = hospital.patients[patient_id]
                        visit_id = generate_unique_visit_id(patient)
                        visit_department = input("Enter Visit_department: ")
                        chief_complaint = input("Enter Chief_complaint: ")
                        visit = Visit(visit_id, visit_time, visit_department, chief_complaint)
                        patient.add_visit(visit)
                    else:
                        gender = input("Enter Gender: ")
                        race = input("Enter Race: ")
                        age = int(input("Enter Age: "))
                        ethnicity = input("Enter Ethnicity: ")
                        insurance = input("Enter Insurance: ")
                        zip_code = input("Enter Zip code: ")
                        patient = Patient(patient_id, gender, race, age, ethnicity, insurance, zip_code)
                        hospital.add_patient(patient)
                        print("Patient added successfully.")
                elif action == "remove_patient":
                    patient_id = input("Enter Patient_ID: ")
                    hospital.remove_patient(patient_id)
                elif action == "retrieve_patient":
                    patient_id = input("Enter Patient_ID: ")
                    hospital.retrieve_patient(patient_id)
                elif action == "count_visits":
                    date_str = input("Enter date (YYYY-MM-DD): ")
                    try:
                        date = datetime.strptime(date_str, '%Y-%m-%d')
                        total_visits = hospital.count_visits_on_date(date)
                        print("Total visits on", date.strftime('%Y-%m-%d'), ":", total_visits)
                    except ValueError:
                        print("Invalid date format.")
                else:
                    print("Invalid action.")
    else:
        print("Invalid username or password.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python Program_Name.py Credential_file_path Patient_file_path")
        sys.exit(1)
    credential_file_path = sys.argv[1]
    patient_file_path = sys.argv[2]
    main(credential_file_path, patient_file_path)
