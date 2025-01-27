subjects = ["Math", "Physics", "Chemistry", "Biology", "History", "Geography", "English", "Polish", "Art"]

def add_student(journal, student_id, name, surname, age, contact, additional_info=""):
    journal[student_id] = {
        "name": name,
        "surname": surname,
        "age": age,
        "contact": contact,
        "additional_info": additional_info,
        "grades": {subject: [] for subject in subjects},
        "attendance": {subject: [] for subject in subjects}
    }

def add_grade(journal, student_id, subject, grade):
    if student_id in journal and subject in journal[student_id]["grades"]:
        journal[student_id]["grades"][subject].append(grade)

def add_attendance(journal, student_id, subject, attended):
    if student_id in journal and subject in journal[student_id]["attendance"]:
        journal[student_id]["attendance"][subject].append(attended)

def get_avg_grade(journal, student_id):
    if student_id in journal:
        all_grades = [grade for grades in journal[student_id]["grades"].values() for grade in grades]
        
        if all_grades:
            avg_grade = sum(all_grades) / len(all_grades)
            return round(avg_grade, 2)
        else:
            return 0
    return 0

def get_total_attendance(journal, student_id):
    if student_id in journal:
        total_attendance = sum([1 for attendances in journal[student_id]["attendance"].values() for attended in attendances if attended])
        return total_attendance
    return 0

def save_data(journal, filename="school_data.txt"):
    with open(filename, "w") as file:
        for student_id, student_data in journal.items():
            file.write(f"Student ID: {student_id}\n")
            file.write(f"Name: {student_data['name']} {student_data['surname']}\n")
            file.write(f"Age: {student_data['age']}\n")
            file.write(f"Contact: {student_data['contact']}\n")
            file.write(f"Additional Info: {student_data['additional_info']}\n")
            file.write("Grades:\n")
            for subject, grades in student_data["grades"].items():
                file.write(f"  {subject}: {', '.join(map(str, grades))}\n")
            file.write("Attendance:\n")
            for subject, attendance in student_data["attendance"].items():
                file.write(f"  {subject}: {', '.join(map(str, attendance))}\n")
            file.write("\n")

def load_data(journal, filename="school_data.txt"):
    with open(filename, "r") as file:
        content = file.read().split("\n\n")
        for student_block in content:
            if student_block.strip():
                lines = student_block.splitlines()
                student_id = int(lines[0].split(":")[1].strip())
                name, surname = lines[1].split(":")[1].strip().split()
                age = int(lines[2].split(":")[1].strip())
                contact = lines[3].split(":")[1].strip()
                additional_info = lines[4].split(":")[1].strip()
                add_student(journal, student_id, name, surname, age, contact, additional_info)
                load_grades(journal, student_id, lines)
                load_attendance(journal, student_id, lines)

def load_grades(student_id, lines):
    for i, section in enumerate(lines[6:]):
        if section.startswith("Grades:"):
            for grade_line in lines[7:]:
                if ":" in grade_line:
                    subject, grades = grade_line.split(":")
                    subject = subject.strip()
                    grades = list(map(int, grades.strip().split(", ")))
                    for grade in grades:
                        add_grade(student_id, subject, grade)

def load_attendance(student_id, lines):
    for i, section in enumerate(lines[6:]):
        if section.startswith("Attendance:"):
            for attend_line in lines[8:]:
                if ":" in attend_line:
                    subject, attendance = attend_line.split(":")
                    subject = subject.strip()
                    attendance = list(map(lambda x: x.strip().lower() == 'true', attendance.strip().split(", ")))
                    for attended in attendance:
                        add_attendance(student_id, subject, attended)

if __name__ == "__main__":
    students_data = [
        (1, "Bartek", "Nowak", 17, "123456789", "Good student"),
        (2, "Anna", "Kowalska", 16, "987654321", "Hardworking"),
        (3, "Jan", "Kowal", 18, "555555555", "Excellent in math"),
        (4, "Kasia", "Malinowska", 15, "555555666", "Athlete"),
        (5, "Marek", "Nowakowski", 19, "444444444", "Leader"),
        (6, "Karolina", "Laskowska", 20, "333333333", "Creative"),
        (7, "Piotr", "Zieliński", 16, "666666666", "Focused"),
        (8, "Magda", "Lewandowska", 17, "777777777", "Motivated"),
        (9, "Tomek", "Bąk", 18, "888888888", "Dedicated"),
        (10, "Kasia", "Jabłońska", 19, "999999999", "Athletic"),
        (11, "Adam", "Szymański", 17, "100000000", "Diligent"),
        (12, "Olga", "Mazur", 16, "200000000", "Artistic")
    ]

    students = {}
    for student in students_data:
        student_id, name, surname, age, contact, additional_info = student
        add_student(students, student_id, name, surname, age, contact, additional_info)
        for subject in subjects:
            add_grade(students, student_id, subject, 4)
            add_attendance(students, student_id, subject, True)

    for student_id in students:
        avg_grade = get_avg_grade(students, student_id)
        total_attendance = get_total_attendance(students, student_id)
        print(f"Average grade for {students[student_id]['name']}: {avg_grade}")
        print(f"Total attendance for {students[student_id]['name']}: {total_attendance}")
    
    save_data(students, "school_data.txt")
    print("\nData saved to file 'school_data.txt'."
