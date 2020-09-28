"""
Classes for creating a University repository which stores information for students and instructors and majors
"""

import os
import sqlite3
from collections import defaultdict
from typing import Dict, List, DefaultDict, Tuple, IO, Iterator
from prettytable import PrettyTable


class _Major:
    """Store information regarding each major"""

    def __init__(self):
        """ Constructor for Majors class """
        self._required: List = list()
        self._electives: List = list()

    def store_major(self, type_course: str, course: str) -> None:
        """ stores required and elective courses """
        if type_course == "R":
            self._required.append(course)
        else:
            self._electives.append(course)

    def get_required(self):
        """return list of required courses"""
        return self._required

    def get_electives(self):
        """return list of elective courses"""
        return self._electives


class _Student:
    """Store student information"""

    def __init__(self, cwid: str, name: str, major: str, required: List, electives: List) -> None:
        """class constructor"""
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._remaining_required: List[str] = required.copy()
        self._remaining_electives: List[str] = electives.copy()
        self._courses: Dict[str, float] = dict()

    def store_course_grade(self, course: str, grade: float) -> None:
        """store information for grades scored by the student"""
        self._courses[course] = grade
        if grade > 0:
            if course in self._remaining_required:
                self._remaining_required.remove(course)
            elif course in self._remaining_electives:
                self._remaining_electives.clear()

    def calculate_gpa(self) -> float:
        """Calculate gpa for student"""
        return round((sum(self._courses.values()) / len(self._courses)), 2)

    def info(self) -> List:
        """return student information for pretty table"""
        return [self._cwid, self._name, self._major, list(self._courses.keys()), self._remaining_required,
                self._remaining_electives, self.calculate_gpa()]


class Instructor:
    """Store instructor information"""

    def __init__(self, cwid: str, name: str, dept: str) -> None:
        """class constructor for Instructors"""
        self.cwid: str = cwid
        self.name: str = name
        self.dept: str = dept
        self.courses: DefaultDict[str, list] = defaultdict(list)

    def store_course_student(self, course_info: tuple) -> None:
        """storing student registered in each course"""
        course, student_id = course_info
        self.courses[course].append(student_id)

    def info(self) -> List:
        """ return information needed for pretty table """
        return [[self.cwid, self.name, self.dept, k, len(v)] for k, v in self.courses.items()]


class University:
    """University stores students and instructors at for the university and print pretty table"""
    grade_map: Dict[str, float] = {"A": 4.0, "A-": 3.75, "B+": 3.25, "B": 3.0, "B-": 2.75, "C+": 2.25, "C": 2.0,
                                   "C-": 0, "D+": 0, "D": 0, "D-": 0, "F": 0}

    @staticmethod
    def _file_reader(path: str, fields: int, sep: str = ',', header: bool = False) -> Iterator[Tuple[str]]:
        """ generator function to read field-separated text files and yield a tuple with all of the values \
        from a single line in the file """
        try:
            file: IO = open(path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to open the file")
        else:
            with file:
                line_num = 0
                for line in file:
                    line_num += 1
                    line = line.rstrip().split(sep)
                    if len(line) != fields:
                        raise ValueError(f"Line {line_num} has {len(line)} fields expected {fields}")
                    if header:
                        header = False
                    else:
                        yield line

    def __init__(self, path: str) -> None:
        """store students, instructors, grades and majors info"""
        self._path: str = path
        self._students: Dict[str, _Student] = dict()  # _students[cwid] = Student()
        self._instructors: Dict[str, Instructor] = dict()  # _instructors[cwid] instructors()
        self._majors: Dict[str, _Major] = dict()  # _instructors[cwid] instructors()
        self._read_major(os.path.join(self._path, 'majors.txt'))
        self._read_students(os.path.join(self._path, 'students.txt'))
        self._read_instructors(os.path.join(self._path, 'instructors.txt'))
        self._read_grades(os.path.join(self._path, 'grades.txt'))
        self._query: str = """select s.Name as Name, s.CWID, g.Course, g.Grade, i.Name as Instructor
                              from students s
                                join grades g on s.CWID = g.StudentCWID
                                join instructors i on g.InstructorCWID = i.CWID
                              order by s.Name;"""

    def _read_major(self, path: str) -> None:
        """read majors file"""
        try:
            for major, type_course, course in self._file_reader(path, 3, '\t', True):
                if major not in self._majors:
                    self._majors[major] = _Major()
                    self._majors[major].store_major(type_course, course)
                else:
                    self._majors[major].store_major(type_course, course)
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def _read_students(self, path: str) -> None:
        """read student file"""
        try:
            for cwid, name, major in self._file_reader(path, 3, '\t', True):
                if major in self._majors:
                    self._students[cwid] = _Student(cwid, name, major,
                                                    self._majors[major].get_required(),
                                                    self._majors[major].get_electives())
                else:
                    print(f"Found student registered in unknown major {major}")
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def _read_instructors(self, path: str) -> None:
        """read instructor file"""
        try:
            for cwid, name, dept in self._file_reader(path, 3, '\t', True):
                self._instructors[cwid] = Instructor(cwid, name, dept)
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def _read_grades(self, path: str) -> None:
        """read grades file"""
        try:
            for s_cwid, course, grade, i_cwid in self._file_reader(path, 4, '\t', True):
                if s_cwid in self._students:
                    self._students[s_cwid].store_course_grade(course, self.grade_map[grade])
                else:
                    print(f"Found grades for unknown student {s_cwid}")

                if i_cwid in self._instructors:
                    self._instructors[i_cwid].store_course_student((course, s_cwid))
                else:
                    print(f"Found grades for unknown student {i_cwid}")
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def major_pretty_table(self) -> None:
        """Display majors info in tabular form"""
        pt: PrettyTable = PrettyTable(field_names=["Major", "Required Courses", "Electives"])
        for m_cwid in self._majors.keys():
            pt.add_row([m_cwid, self._majors[m_cwid].get_required(), self._majors[m_cwid].get_electives()])
        print(pt)

    def student_pretty_table(self) -> None:
        """Display student info in tabular form"""
        pt: PrettyTable = PrettyTable(field_names=["CWID", "Name", "Major", "Completed Courses",
                                                   "Remaining Required", "RemainingElectives", "GPA"])
        for s_cwid in self._students.keys():
            pt.add_row(self._students[s_cwid].info())
        print(pt)

    def instructor_pretty_table(self) -> None:
        """Display instructor info in tabular form"""
        pt: PrettyTable = PrettyTable(field_names=["CWID", "Name", "Dept", "Course", "Students"])
        for i_cwid in self._instructors.keys():
            for rec in self._instructors[i_cwid].info():
                pt.add_row(rec)
        print(pt)

    def student_grades_table_db(self, db_path) -> None:
        """Display student and grades in tabular form"""
        try:
            db: sqlite3.Connection = sqlite3.connect(db_path)
        except sqlite3.OperationalError as e:
            print(e)
        else:
            pt: PrettyTable = PrettyTable(field_names=["Name", "CWID", "Course", "Grade", "Instructor"])
            try:
                for row in db.execute(self._query):
                    pt.add_row(row)
                print(pt)
                db.close()
            except sqlite3.OperationalError as e:
                print(e)

    def _student_grades_table_db_test(self, db_path) -> Tuple:
        """Generator to test sql query"""
        try:
            db: sqlite3.Connection = sqlite3.connect(db_path)
        except sqlite3.OperationalError as e:
            print(e)
        else:
            try:
                for row in db.execute(self._query):
                    yield row
                db.close()
            except sqlite3.OperationalError as e:
                print(e)


def main():
    """define the university"""
    stevens_univ: University = University(os.getcwd())
    stevens_univ.major_pretty_table()
    stevens_univ.student_pretty_table()
    stevens_univ.instructor_pretty_table()
    stevens_univ.student_grades_table_db("student_repo.sqlite")


# if __name__ == '__main__':
#     main()
