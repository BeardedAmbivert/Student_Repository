"""
Classes for creating a University repository which stores information for students and instructors
"""

import os
from collections import defaultdict
from typing import Dict, List, DefaultDict, Tuple, Any
from prettytable import PrettyTable
from HW08_Aditya_Kulkarni import file_reader


class _Major:
    """Store information regarding each major"""
    def __init__(self):
        """  """
        self._required = list()
        self._electives = list()
        self.major_info: DefaultDict[str, list] = defaultdict(list)

    def store_major(self, type_course: str, course: str) -> None:
        """ stores required and elective courses """
        if type_course == "R":
            self._required.append(course)
        else:
            self._electives.append(course)

    def get_required(self):
        return self._required

    def get_electives(self):
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
        return round((sum(self._courses.values())/len(self._courses)), 2)

    def info(self) -> List:
        """return student information for pretty table"""
        return [self._cwid, self._name, self._major, list(self._courses.keys()), self._remaining_required, self._remaining_electives, self.calculate_gpa()]


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
    grade_map = {"A": 4.0, "A-": 3.75, "B+": 3.25, "B": 3.0, "B-": 2.75, "C+": 2.25, "C": 2.0, "C-": 0, "D+": 0, "D": 0, "D-": 0, "F": 0}

    def __init__(self, path: str) -> None:
        """store students, instructors and pretty table"""
        self._path: str = path
        self._students: Dict[str, _Student] = dict()  # _students[cwid] = Student()
        self._instructors: Dict[str, Instructor] = dict()  # _instructors[cwid] instructors()
        self._majors: Dict[str, _Major] = dict()  # _instructors[cwid] instructors()
        self._read_major(os.path.join(self._path, 'majors.txt'))
        self._read_students(os.path.join(self._path, 'students.txt'))
        self._read_instructors(os.path.join(self._path, 'instructors.txt'))
        self._read_grades(os.path.join(self._path, 'grades.txt'))

    def _read_students(self, path: str) -> None:
        """read student file"""
        try:
            for cwid, name, major in file_reader(path, 3, ';', True):
                self._students[cwid] = _Student(cwid, name, major,
                                                self._majors[major].get_required(),
                                                self._majors[major].get_electives())
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def _read_instructors(self, path: str) -> None:
        """read instructor file"""
        try:
            for cwid, name, dept in file_reader(path, 3, '|', True):
                self._instructors[cwid] = Instructor(cwid, name, dept)
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def _read_major(self, path: str) -> None:
        try:
            for major, type_course, course in file_reader(path, 3, '\t', True):
                if major not in self._majors:
                    self._majors[major] = _Major()
                    self._majors[major].store_major(type_course, course)
                else:
                    self._majors[major].store_major(type_course, course)
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def _read_grades(self, path: str) -> None:
        """read grades file"""
        try:
            for s_cwid, course, grade, i_cwid in file_reader(path, 4, '|', True):

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
        pt: PrettyTable = PrettyTable(field_names=["Major", "Required Courses", "Electives"])
        for m_cwid in self._majors.keys():
            pt.add_row([m_cwid, self._majors[m_cwid].get_required(), self._majors[m_cwid].get_electives()])
        print(pt)

    def student_pretty_table(self) -> None:
        """Display student info"""
        pt: PrettyTable = PrettyTable(field_names=["CWID", "Name", "Major", "Completed Courses",
                                                   "Remaining Required", "RemainingElectives", "GPA"])
        for s_cwid in self._students.keys():
            pt.add_row(self._students[s_cwid].info())
        print(pt)

    def instructor_pretty_table(self) -> None:
        """Display instructor info"""
        pt: PrettyTable = PrettyTable(field_names=["CWID", "Name", "Dept", "Course", "Students"])
        for i_cwid in self._instructors.keys():
            for rec in self._instructors[i_cwid].info():
                pt.add_row(rec)
        print(pt)


def main():
    """define the university"""
    stevens_univ: University = University('C:\\Users\\rajek\\PycharmProjects\\Student_Repository')
    stevens_univ.major_pretty_table()
    stevens_univ.student_pretty_table()
    stevens_univ.instructor_pretty_table()


if __name__ == '__main__':
    main()
