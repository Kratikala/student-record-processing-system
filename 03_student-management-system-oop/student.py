class Student:
    def __init__(
        self,
        student_id,
        name,
        department,
        marks,
        attendance,
        status="Active"
    ):
        if not student_id.strip():
            raise ValueError("Student ID cannot be empty.")

        if not name.strip():
            raise ValueError("Student name cannot be empty.")

        if not department.strip():
            raise ValueError("Department cannot be empty.")

        if not marks:
            raise ValueError("At least one mark is required.")

        for mark in marks:
            if not isinstance(mark, (int, float)) or not 0 <= mark <= 100:
                raise ValueError("Marks must be between 0 and 100.")

        if not isinstance(attendance, (int, float)):
            raise ValueError("Attendance must be a number.")

        if not 0 <= attendance <= 100:
            raise ValueError("Attendance must be between 0 and 100.")

        if status not in ("Active", "Inactive"):
            raise ValueError("Status must be Active or Inactive.")

        self._student_id = student_id.strip()
        self._name = name.strip()
        self._department = department.strip()
        self._marks = list(marks)
        self._attendance = float(attendance)
        self._status = status

    @property
    def student_id(self):
        return self._student_id

    @property
    def name(self):
        return self._name

    @property
    def department(self):
        return self._department

    @property
    def marks(self):
        return self._marks.copy()

    @property
    def attendance(self):
        return self._attendance

    @property
    def status(self):
        return self._status

    def calculate_average(self):
        return sum(self._marks) / len(self._marks)

    def update_info(self, name=None, department=None,
                    marks=None, attendance=None, status=None):
        if name is not None:
            if not name.strip():
                raise ValueError("Name cannot be empty.")
            self._name = name.strip()

        if department is not None:
            if not department.strip():
                raise ValueError("Department cannot be empty.")
            self._department = department.strip()

        if marks is not None:
            if not marks:
                raise ValueError("At least one mark is required.")

            if any(
                not isinstance(mark, (int, float))
                or not 0 <= mark <= 100
                for mark in marks
            ):
                raise ValueError("Marks must be between 0 and 100.")

            self._marks = list(marks)

        if attendance is not None:
            if not isinstance(attendance, (int, float)):
                raise ValueError("Attendance must be a number.")

            if not 0 <= attendance <= 100:
                raise ValueError("Attendance must be between 0 and 100.")

            self._attendance = float(attendance)

        if status is not None:
            if status not in ("Active", "Inactive"):
                raise ValueError("Status must be Active or Inactive.")
            self._status = status

    def to_dict(self):
        return {
            "student_id": self._student_id,
            "name": self._name,
            "department": self._department,
            "marks": self._marks,
            "attendance": self._attendance,
            "status": self._status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            department=data["department"],
            marks=data["marks"],
            attendance=data["attendance"],
            status=data.get("status", "Active")
        )