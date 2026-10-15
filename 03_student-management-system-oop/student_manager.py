class StudentManager:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.students = []
        self.load_data()

    def load_data(self):
        self.students = self.file_manager.load_students()

        ids = [student.student_id for student in self.students]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate student IDs found in the data file.")

    def save_data(self):
        self.file_manager.save_students(self.students)

    def add_student(self, student):
        if self.find_student(student.student_id):
            raise ValueError("A student with this ID already exists.")

        self.students.append(student)
        self.save_data()

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student

        return None

    def get_all_students(self):
        return self.students.copy()

    def update_student(self, student_id, **updates):
        student = self.find_student(student_id)

        if student is None:
            raise ValueError("Student not found.")

        student.update_info(**updates)
        self.save_data()

    def delete_student(self, student_id):
        student = self.find_student(student_id)

        if student is None:
            raise ValueError("Student not found.")

        self.students.remove(student)
        self.save_data()