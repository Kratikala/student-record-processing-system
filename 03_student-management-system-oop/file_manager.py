import json
from pathlib import Path
from student import Student


class FileManager:
    def __init__(self, filename="students.json"):
        self.file_path = Path(__file__).parent / filename

    def save_students(self, students):
        data = [student.to_dict() for student in students]

        try:
            with self.file_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

        except OSError as error:
            raise OSError(f"Could not save student data: {error}") from error

    def load_students(self):
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Student data must be a JSON list.")

            return [Student.from_dict(item) for item in data]

        except json.JSONDecodeError as error:
            raise ValueError(
                "The student data file contains invalid JSON."
            ) from error

        except OSError as error:
            raise OSError(
                f"Could not read student data: {error}"
            ) from error