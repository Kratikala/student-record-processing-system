
import json
from pathlib import Path

FILE_PATH = Path(__file__).parent / "students.json"


def load_students():
    if not FILE_PATH.exists() or FILE_PATH.stat().st_size == 0:
        return []

    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: students.json contains invalid JSON.")
        return []


def save_students(students):
    with open(FILE_PATH, "w") as file:
        json.dump(students, file, indent=4)


def get_marks():
    while True:
        try:
            marks = [float(m.strip()) for m in input(
                "Enter marks separated by commas: "
            ).split(",")]

            if not marks or any(m < 0 or m > 100 for m in marks):
                print("Marks must be between 0 and 100.")
                continue

            return marks
        except ValueError:
            print("Enter valid numbers separated by commas.")


def get_attendance():
    while True:
        try:
            attendance = float(input("Enter attendance percentage: "))
            if 0 <= attendance <= 100:
                return attendance
            print("Attendance must be between 0 and 100.")
        except ValueError:
            print("Enter a valid number.")


def add_student(students):
    student_id = input("Student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    if any(s["student_id"] == student_id for s in students):
        print("That student ID already exists.")
        return

    student = {
        "student_id": student_id,
        "name": input("Name: ").strip(),
        "department": input("Department: ").strip(),
        "marks": get_marks(),
        "attendance": get_attendance()
    }

    if not student["name"] or not student["department"]:
        print("Name and department cannot be empty.")
        return

    students.append(student)
    save_students(students)
    print("Student added successfully.")


def view_students(students):
    if not students:
        print("No student records found.")
        return

    for s in students:
        print(
            f'ID: {s["student_id"]} | Name: {s["name"]} | '
            f'Department: {s["department"]} | '
            f'Average: {sum(s["marks"]) / len(s["marks"]):.2f}% | '
            f'Attendance: {s["attendance"]}%'
        )


def search_student(students):
    student_id = input("Enter student ID to search: ").strip()

    for s in students:
        if s["student_id"] == student_id:
            print(s)
            print(f'Average marks: {sum(s["marks"]) / len(s["marks"]):.2f}%')
            return

    print("Student not found.")


def update_student(students):
    student_id = input("Enter student ID to update: ").strip()

    for s in students:
        if s["student_id"] == student_id:
            print("1. Update name")
            print("2. Update department")
            print("3. Update marks")
            print("4. Update attendance")

            choice = input("Choose field: ")

            if choice == "1":
                value = input("New name: ").strip()
                if value:
                    s["name"] = value
                else:
                    print("Name cannot be empty.")
                    return
            elif choice == "2":
                value = input("New department: ").strip()
                if value:
                    s["department"] = value
                else:
                    print("Department cannot be empty.")
                    return
            elif choice == "3":
                s["marks"] = get_marks()
            elif choice == "4":
                s["attendance"] = get_attendance()
            else:
                print("Invalid choice.")
                return

            save_students(students)
            print("Student updated successfully.")
            return

    print("Student not found.")


def delete_student(students):
    student_id = input("Enter student ID to delete: ").strip()

    for s in students:
        if s["student_id"] == student_id:
            students.remove(s)
            save_students(students)
            print("Student deleted successfully.")
            return

    print("Student not found.")


def performance_report(students):
    if not students:
        print("No records available.")
        return

    averages = [
        (s, sum(s["marks"]) / len(s["marks"]))
        for s in students if s["marks"]
    ]

    if not averages:
        print("No marks available.")
        return

    class_average = sum(avg for _, avg in averages) / len(averages)
    top_student, top_average = max(averages, key=lambda item: item[1])
    low_attendance = [s for s in students if s["attendance"] < 75]

    print(f"Students: {len(students)}")
    print(f"Class average: {class_average:.2f}%")
    print(
        f'Top performer: {top_student["name"]} '
        f'({top_average:.2f}%)'
    )
    print("Attendance below 75%:")

    if low_attendance:
        for s in low_attendance:
            print(f'{s["name"]}: {s["attendance"]}%')
    else:
        print("None")


def main():
    students = load_students()

    while True:
        print("\n=== Student Record Management System ===")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Performance Report")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            performance_report(students)
        elif choice == "7":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
