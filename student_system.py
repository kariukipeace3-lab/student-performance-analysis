import csv
from abc import ABC, abstractmethod


class Student(ABC):
    """Abstract base class for every student in the system."""

    def __init__(self, student_id, first_name, last_name, programme):
        self._student_id = student_id
        self._first_name = first_name
        self._last_name = last_name
        self._programme = programme
        self._marks = {}

    @property
    def student_id(self):
        return self._student_id

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value: raise ValueError("First name cannot be empty")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value: raise ValueError("Last name cannot be empty")
        self._last_name = value

    @property
    def programme(self):
        return self._programme

    @programme.setter
    def programme(self, value):
        if not value: raise ValueError("Programme cannot be empty")
        self._programme = value

    @property
    def full_name(self):
        return f"{self._first_name} {self._last_name}"

    @property
    def marks(self):
        return dict(self._marks)

    def add_mark(self, subject, score):
        if not (0 <= score <= 100):
            raise ValueError(f"Mark for {subject} must be between 0 and 100")
        self._marks[subject] = score

    def calculate_average(self, *marks):
        if not marks:
            if not self._marks: return 0.0
            values = list(self._marks.values())
        elif len(marks) == 1 and isinstance(marks[0], (list, tuple)):
            values = list(marks[0])
        else:
            values = list(marks)

        for v in values:
            if not (0 <= v <= 100):
                raise ValueError(f"Mark {v} is outside the range 0-100")
        return sum(values) / len(values)

    def grade(self):
        avg = self.calculate_average()
        if avg >= 80: return "A"
        elif avg >= 70: return "B"
        elif avg >= 60: return "C"
        elif avg >= 50: return "D"
        else: return "E"

    @abstractmethod
    def describe(self):
        pass


class AIUStudent(Student):
    """A regular (non-scholarship) student at AIU."""

    def __init__(self, student_id, first_name, last_name, programme, marks=None):
        super().__init__(student_id, first_name, last_name, programme)
        if marks:
            for subject, score in marks.items():
                self.add_mark(subject, score)

    def describe(self):
        return f"Regular student | Grade: {self.grade()} | Average: {self.calculate_average():.2f}"


class ScholarshipStudent(AIUStudent):
    """A student who holds a scholarship. Inherits from AIUStudent."""

    def __init__(self, student_id, first_name, last_name, programme, marks=None, scholarship_amount=0.0):
        super().__init__(student_id, first_name, last_name, programme, marks)
        self.scholarship_amount = scholarship_amount

    @property
    def scholarship_amount(self):
        return self._scholarship_amount

    @scholarship_amount.setter
    def scholarship_amount(self, value):
        if value < 0: raise ValueError("Scholarship amount cannot be negative")
        self._scholarship_amount = float(value)

    def is_eligible(self):
        return self.calculate_average() >= 85

    def describe(self):
        return (f"Scholarship student (KES {self.scholarship_amount:,.2f}) | "
                f"Grade: {self.grade()} | Average: {self.calculate_average():.2f}")


class PerformanceAnalyzer:
    """Analyzes a collection of Student objects."""

    def __init__(self, students):
        self.students = students

    def highest_average(self):
        if not self.students: return None
        return max(self.students, key=lambda s: s.calculate_average())

    def lowest_average(self):
        if not self.students: return None
        return min(self.students, key=lambda s: s.calculate_average())

    def class_average(self):
        if not self.students: return 0.0
        return sum(student.calculate_average() for student in self.students) / len(self.students)

    # ------------------------------------------------------------------
    # TASK 7: REPORT GENERATION
    # ------------------------------------------------------------------
    def generate_report(self):
        """Prints a full performance report for all students."""
        print("=" * 60)
        print("               STUDENT PERFORMANCE REPORT")
        print("=" * 60)

        for student in self.students:
            print(f"\nStudent ID:  {student.student_id}")
            print(f"Name:        {student.full_name}")
            print(f"Programme:   {student.programme}")
            print(f"Marks:       {student.marks}")
            print(f"Average:     {student.calculate_average():.2f}")
            print(f"Grade:       {student.grade()}")

            # Scholarship eligibility
            if isinstance(student, ScholarshipStudent):
                status = "ELIGIBLE" if student.is_eligible() else "NOT ELIGIBLE"
                print(f"Scholarship: KES {student.scholarship_amount:,.2f} | Status: {status}")
            else:
                # Check if a regular student would be eligible for a scholarship
                if student.calculate_average() >= 85:
                    print("Scholarship: NOT ENROLLED (Average is high enough to qualify!)")
                else:
                    print("Scholarship: NOT ENROLLED")

            print("-" * 60)

        # Class Summary
        print("\n" + "=" * 60)
        print("                  CLASS SUMMARY")
        print("=" * 60)
        top = self.highest_average()
        bottom = self.lowest_average()
        print(f"Highest Average: {top.full_name} ({top.calculate_average():.2f})")
        print(f"Lowest Average:  {bottom.full_name} ({bottom.calculate_average():.2f})")
        print(f"Class Average:   {self.class_average():.2f}")
        print("=" * 60)


# ------------------------------------------------------------------
# TASK 7: LOADING DATA FROM CSV
# ------------------------------------------------------------------
def load_students_from_csv(filename):
    """Reads a CSV file and returns a list of AIUStudent objects."""
    students = []
    
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            student_id = row['StudentID']
            fname = row['FName']
            lname = row['LName']
            programme = row['Programme']
            
            # Create the marks dictionary
            marks = {
                "Math": float(row['Math']),
                "English": float(row['English']),
                "Science": float(row['Science'])
            }
            
            # Create the student object
            student = AIUStudent(student_id, fname, lname, programme, marks)
            students.append(student)
            
    return students


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. Load the students from the CSV file
    students = load_students_from_csv("students.csv")
    
    # 2. Create the analyzer
    analyzer = PerformanceAnalyzer(students)
    
    # 3. Generate the final report
    analyzer.generate_report()