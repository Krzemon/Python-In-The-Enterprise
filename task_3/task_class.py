import json
import os

class Contact:
    def __init__(self, mother_number, father_number, address):
        self.mother_number = mother_number
        self.father_number = father_number
        self.address = address

    def __str__(self):
        return f"Mother number: {self.mother_number}, Father number: {self.father_number}, Address: {self.address}"


class Student:
    student_id = 1

    def __init__(self, name, surname, age, contact, additional_info=""):
        self.name = name
        self.surname = surname
        self.age = age
        self.contact = Contact(*contact)
        self.id = Student.student_id
        self.additional_info = additional_info
        self.grades = {}
        self.attendance = []
        Student.student_id += 1

    def add_grade(self, subject, grade):
        if subject not in self.grades:
            self.grades[subject] = []
        self.grades[subject].append(grade)

    def add_attendance(self, attended):
        self.attendance.append(attended)

    def get_avg_grade(self):
        total_grades = sum([sum(grades) for grades in self.grades.values()])
        total_subjects = sum([len(grades) for grades in self.grades.values()])
        return total_grades / total_subjects
    
    def get_avg_grade_in_subject(self, subject):
        if subject in self.grades:
            return sum(self.grades[subject]) / len(self.grades[subject])
        return 0
    
    def get_total_attendance(self):
        return sum(self.attendance)
    
    def __str__(self):
        return f"Name: {self.name}, Surname: {self.surname}, Age: {self.age}, ID: {self.id}, Additional Info: {self.additional_info}"


class SchoolClass():
    def __init__(self, class_name):
        self.class_name = class_name
        self.students = []
        self.subjects = []
        self.attendance = {}

    def add_subject(self, subject):
        if subject not in self.subjects:
            self.subjects.append(subject)

    def add_student(self, student):
        self.students.append(student)
        self.attendance[student.id] = []

    def get_class_avg(self):
        total_grades = sum([student.get_avg_grade() for student in self.students])
        return total_grades / len(self.students) if self.students else 0

    def get_attendance_summary(self):
        return {student.id: student.get_total_attendance() for student in self.students}

    def __str__(self):
        return f"Class: {self.class_name}, Subjects: {', '.join(self.subjects)}, Students: {', '.join([str(student) for student in self.students])}"

class School():
    def __init__(self, name):
        self.name = name
        self.classes = {}

    def add_class(self, school_class):
        self.classes[school_class.class_name] = school_class

    def add_subject_to_class(self, class_name, subject):
        if class_name in self.classes:
            self.classes[class_name].add_subject(subject)

    def get_school_avg(self):
        total_grades = sum([school_class.get_class_avg() for school_class in self.classes.values()])
        total_classes = len(self.classes)
        return total_grades / total_classes if total_classes else 0

    def save_data(self, file_name="school_data.json"):
        data = {}
        for school_class in self.classes.values():
            class_data = []
            for student in school_class.students:
                student_data = {
                    'name': student.name,
                    'surname': student.surname,
                    'age': student.age,
                    'grades': student.grades,
                    'attendance': student.attendance
                }
                class_data.append(student_data)
            data[school_class.class_name] = class_data

        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self, file_name="school_data.json"):
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                data = json.load(f)
                for class_name, class_data in data.items():
                    school_class = SchoolClass(class_name)
                    for student_data in class_data:
                        student = Student(
                            student_data['name'], student_data['surname'],
                            student_data['age'], ("", "", ""),
                            student_data.get('additional_info', "")
                        )
                        student.grades = student_data['grades']
                        student.attendance = student_data['attendance']
                        school_class.add_student(student)
                    self.add_class(school_class)
        else:
            print("No data file found. Starting with an empty school.")

    def __str__(self):
        return f"School: {self.name}, Classes: {', '.join(self.classes.keys())}"

if __name__ == "__main__":
    contact_1 = ("123456789", "987654321", "Kawiory")
    contact_2 = ("555555555", "444444444", "Czarnowiejska")

    student_1 = Student("Bartek", "Nowak", 17, contact_1)
    student_1.add_grade("Math", 5)
    student_1.add_grade("Physics", 4)
    student_1.add_attendance(True)
    student_1.add_attendance(False)

    student_2 = Student("Anna", "Kowalska", 16, contact_2)
    student_2.add_grade("Math", 4)
    student_2.add_grade("Polish language", 5)
    student_2.add_attendance(True)
    student_2.add_attendance(True)

    school = School("1 LO")

    class_a = SchoolClass("Class A")
    class_a.add_subject("Math")
    class_a.add_subject("Physics")
    class_a.add_student(student_1)
    class_a.add_student(student_2)

    school.add_class(class_a)

    print(school)
    print(f"Class A average grade: {class_a.get_class_avg():.2f}")
    print(f"Bartek's average grade: {student_1.get_avg_grade():.2f}")
    print(f"Anna's Math average grade: {student_2.get_avg_grade_in_subject('Math'):.2f}")
    print(f"Bartek's total attendance: {student_1.get_total_attendance()}")
    
    school.save_data()

    new_school = School("1 LO")
    new_school.load_data("school_data.json")
    print(new_school)