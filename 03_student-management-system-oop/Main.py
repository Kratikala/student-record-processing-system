from student import Student
from file_manager import FileManager
from student_manager import StudentManager
from report_generator import ReportGenerator


def get_marks():
    raw_marks = input("Enter marks separated by commas: ")

    try:
        marks = [float(value.strip()) for value in raw_marks.split(",")]

        if not marks:
            raise ValueError("Enter at least one mark.")

        if any(not 0 <= mark <= 100 for mark in marks):
            raise ValueError("Marks must be between 0 and 100.")

        return marks

    except ValueError as error:
        raise ValueError(f"Invalid marks: {error}") from error


def get_attendance():
    try:
        attendance = float(input("Enter attendance percentage: "))

        if not 0 <= attendance <= 100:
            raise ValueError("Attendance must be between 0 and 100.")

        return attendance

    except ValueError as error:
        raise ValueError(f"Invalid attendance: {error}") from error


def add_student(manager):
    student_id = input("Enter student ID: ").strip()
    name = input("Enter name: ").strip()
    department = input("Enter department: ").strip()
    marks = get_marks()
    attendance = get_attendance()

    student = Student(
        student_id, name, department, marks, attendance
    )

    manager.add_student(student)
    print("Student added successfully.")


def view_students(manager):
    students = manager.get_all_students()

    if not students:
        print("No student records found.")
        return

    for student in students:
        print(ReportGenerator.student_report(student))
        print("-" * 35)


def search_student(manager):
    student_id = input("Enter student ID to search: ").strip()
    student = manager.find_student(student_id)

    if student is None:
        print("Student not found.")
    else:
        print(ReportGenerator.student_report(student))


def update_student(manager):
    student_id = input("Enter student ID to update: ").strip()
    student = manager.find_student(student_id)

    if student is None:
        print("Student not found.")
        return

    print("Leave a field empty to keep its current value.")

    name = input(f"Name [{student.name}]: ").strip()
    department = input(
        f"Department [{student.department}]: "
    ).strip()

    marks = None
    if input("Update marks? (y/n): ").strip().lower() == "y":
        marks = get_marks()

    attendance = None
    if input("Update attendance? (y/n): ").strip().lower() == "y":
        attendance = get_attendance()

    status = input(
        f"Status (Active/Inactive) [{student.status}]: "
    ).strip()

    manager.update_student(
        student_id,
        name=name or None,
        department=department or None,
        marks=marks,
        attendance=attendance,
        status=status.title() if status else None
    )

    print("Student updated successfully.")


def delete_student(manager):
    student_id = input("Enter student ID to delete: ").strip()
    manager.delete_student(student_id)
    print("Student deleted successfully.")


def main():
    try:
        file_manager = FileManager()
        manager = StudentManager(file_manager)

    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"Could not load student data: {error}")
        return

    while True:
        print("\n===== Student Management System =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Overall Performance Report")
        print("7. Save and Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                add_student(manager)

            elif choice == "2":
                view_students(manager)

            elif choice == "3":
                search_student(manager)

            elif choice == "4":
                update_student(manager)

            elif choice == "5":
                delete_student(manager)

            elif choice == "6":
                print(
                    ReportGenerator.performance_report(
                        manager.get_all_students()
                    )
                )

            elif choice == "7":
                manager.save_data()
                print("Data saved. Goodbye!")
                break

            else:
                print("Invalid choice. Please select 1-7.")

        except (ValueError, OSError, KeyError, TypeError) as error:
            print(f"Operation failed: {error}")


if __name__ == "__main__":
    main()