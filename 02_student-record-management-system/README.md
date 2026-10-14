# Student Record Management System

A menu-driven Student Record Management System built using Python. The application allows users to add, view, search, update, and delete student records, generate performance reports, and store data persistently using JSON file handling.

## Features

- **Add Student:** Register students with a unique student ID, name, department, marks, and attendance.
- **View Students:** Display all student records, including average marks and attendance.
- **Search Student:** Find a student using their unique ID.
- **Update Student:** Modify a student's name, department, marks, or attendance.
- **Delete Student:** Remove a student record using their ID.
- **Performance Report:** Calculate class average, identify the top performer, and list students with attendance below 75%.
- **JSON Data Storage:** Save student records so they remain available after the program closes.
- **Input Validation:** Handle duplicate IDs, invalid marks, invalid attendance percentages, and missing student records.

## Used

- Python 3
- JSON
- File Handling
- Lists and Dictionaries
- Functions
- Exception Handling
- `pathlib` for file path management


## Data Storage

Student records are stored in `students.json`. The application loads saved records when it starts and writes changes to the file after successful additions, updates, and deletions.

Each student record contains:

- Student ID
- Name
- Department
- Marks
- Attendance percentage

