class ReportGenerator:
    @staticmethod
    def performance_label(average):
        if average >= 80:
            return "Excellent"
        elif average >= 70:
            return "Good"
        elif average >= 50:
            return "Average"
        else:
            return "Needs Improvement"

    @staticmethod
    def student_report(student):
        average = student.calculate_average()

        return (
            "Student Report\n"
            "---------------\n"
            f"{student.student_id} | {student.name} | "
            f"{student.department}\n"
            f"Average: {average:.1f}%\n"
            f"Attendance: {student.attendance:.0f}%\n"
            f"Status: {student.status}\n"
            f"Performance: "
            f"{ReportGenerator.performance_label(average)}"
        )

    @staticmethod
    def performance_report(students):
        if not students:
            return "No student records available."

        averages = [
            (student, student.calculate_average())
            for student in students
        ]

        class_average = sum(avg for _, avg in averages) / len(averages)
        top_student, top_average = max(
            averages, key=lambda item: item[1]
        )

        low_attendance = [
            student for student in students
            if student.attendance < 75
        ]

        lines = [
            "Overall Performance Report",
            "--------------------------",
            f"Total Students: {len(students)}",
            f"Class Average: {class_average:.1f}%",
            f"Top Performer: {top_student.name} "
            f"({top_average:.1f}%)",
            f"Students with Attendance Below 75%: "
            f"{len(low_attendance)}"
        ]

        return "\n".join(lines)