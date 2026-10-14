# List of dictionaries storing student information
students = [
    {
        "name": "Dass",
        "age": 20,
        "department": "CSE",
        "marks": [78, 85, 72],
        "attendance": 91
    },
    {
        "name": "Chandra",
        "age": 20,
        "department": "CSE",
        "marks": [65, 71, 68],
        "attendance": 84
    },
    {
        "name": "Namita",
        "age": 20,
        "department": "CSE",
        "marks": [87, 64, 77],
        "attendance": 72
    }
]

# Calculate the average marks of one student
def calculate_average(student):
    marks = student["marks"]
    average = sum(marks) / len(marks)
    return average


# Check whether a student passes or fails
def check_results(student):
    if calculate_average(student) >= 40:
        return "PASS"
    else:
        return "FAIL"


# Find the student with the highest average marks
def top_performer(students):
    top = students[0]

    for student in students:
        if calculate_average(student) > calculate_average(top):
            top = student

    return top


# Find students whose attendance is below a given threshold
def filter_by_attendence(students, threshold):
    attendance = []

    for student in students:
        if student["attendance"] < threshold:
            attendance.append(student)

    return attendance


# Find students whose average marks are below a given threshold
def filter_by_marks(students, threshold):
    marks = []

    for student in students:
        if calculate_average(student) < threshold:
            marks.append(student)

    return marks


# Display the complete details of every student
def display_students(students):
    for student in students:
        print("Name:", student["name"])
        print("Age:", student["age"])
        print("Department:", student["department"])
        print("Marks:", student["marks"])
        print("Attendance:", student["attendance"], "%")
        print("Average:", round(calculate_average(student)))
        print("Result:", check_results(student))


# Display the class summary
def class_summary(students):
    print("\nClass Summary")
    print("-" * 30)

    # Count the total number of students
    total_students = len(students)
    print("Total Students:", total_students)

    # Calculate the average of all individual subject marks
    total_marks = 0
    number_of_marks = 0

    for student in students:
        for mark in student["marks"]:
            total_marks += mark
            number_of_marks += 1

    # Avoid division by zero if the class has no marks
    if number_of_marks > 0:
        class_avg = total_marks / number_of_marks
        print(f"Average Class Mark: {class_avg:.1f}")
    else:
        print("Average Class Mark: N/A")

    # Display the top-performing student
    if total_students > 0:
        top = top_performer(students)
        top_average = calculate_average(top)

        print("\nTop Performer:")
        print(f"{top['name']} - Average: {top_average:.1f}%")
    else:
        print("\nTop Performer: N/A")

    # Display students with attendance below 75%
    print("\nAttendance Below 75%:")
    low_attendance = filter_by_attendence(students, 75)

    if low_attendance:
        for student in low_attendance:
            print(f"{student['name']} - {student['attendance']}%")
    else:
        print("No students below 75% attendance.")

    # Display the pass/fail result of each student
    print("\nResult:")

    for student in students:
        print(f"{student['name']} - {check_results(student)}")


# Run the program
print("STUDENT RECORDS")
print("=" * 30)
display_students(students)

# Demonstrate filtering students with average marks below 75
print("\nStudents with average marks below 75:")
low_marks = filter_by_marks(students, 75)

if low_marks:
    for student in low_marks:
        print(f"{student['name']} - "f"Average: {calculate_average(student):.1f}")
else:
    print("No students found.")

# Print the final class summary
class_summary(students)

    
       