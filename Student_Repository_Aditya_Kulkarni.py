"""
Classes for creating a University repository which stores information for students and instructors
"""

import os
from collections import defaultdict
from typing import Dict, List, DefaultDict, Tuple, Any
from prettytable import PrettyTable
from HW08_Aditya_Kulkarni import file_reader


class Student:
    """Store student information"""

    def __init__(self, cwid: str, name: str, major: str) -> None:
        """class constructor"""
        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        self.courses: Dict = dict()

    def store_course_grade(self, course: str, grade: str) -> None:
        """store information for grades scored by the student"""
        self.courses[course] = grade

    def info(self) -> Tuple[str, str, list]:
        """return student information for pretty table"""
        return self.cwid, self.name, sorted(list(self.courses.keys()))


class Instructor:
    """Store student information"""

    def __init__(self, cwid: str, name: str, dept: str) -> None:
        """class constructor for Instructors"""
        self.cwid: str = cwid
        self.name: str = name
        self.dept: str = dept
        self.courses: DefaultDict[Any, Any] = defaultdict(list)

    def store_course_student(self, course_info: tuple) -> None:
        """storing student registered in each course"""
        course, student_id = course_info
        self.courses[course].append(student_id)

    def info(self) -> List:
        """
        return information needed for pretty table
        """
        return [[self.cwid, self.name, self.dept, k, len(v)] for k, v in self.courses.items()]


class University:
    """
    University stores students and instructors at
    for the university and print pretty table
    """

    def __init__(self, path: str) -> None:
        """
        store students, instructors and pretty table
        """
        self._path: str = path
        self._students: Dict[str, _Student] = dict()  # _students[cwid] = Student()
        self._instructors: Dict[str, _Instructor] = dict()  # _instructors[cwid] instructors()
        self._read_students(os.path.join(self._path, 'students.txt'))
        self._read_instructors(os.path.join(self._path, 'instructors.txt'))
        self._read_grades(os.path.join(self._path, 'grades.txt'))

    def _read_students(self, path: str) -> None:
        """read student file"""
        try:
            for cwid, name, major in file_reader(path, 3, '\t', False):
                self._students[cwid] = Student(cwid, name, major)
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def _read_instructors(self, path: str) -> None:
        """read instructor file"""
        try:
            for cwid, name, dept in file_reader(path, 3, '\t', False):
                self._instructors[cwid] = Instructor(cwid, name, dept)
        except(FileNotFoundError, ValueError) as e:
            print(e)

    def _read_grades(self, path: str) -> None:
        """read grades file"""
        try:
            for s_cwid, course, grade, i_cwid in file_reader(path, 4, '\t', False):

                if s_cwid in self._students:
                    self._students[s_cwid].store_course_grade(course, grade)
                else:
                    print(f"Found grades for unknown student {s_cwid}")

                if i_cwid in self._instructors:
                    self._instructors[i_cwid].store_course_student((course, s_cwid))
                else:
                    print(f"Found grades for unknown student {i_cwid}")

        except(FileNotFoundError, ValueError) as e:
            print(e)

    def student_pretty_table(self) -> None:
        """Display student info"""
        pt: PrettyTable = PrettyTable(field_names=["CWID", "Name", "Completed Courses"])
        for s_cwid in self._students.keys():
            pt.add_row(list(self._students[s_cwid].info()))
        print(pt)

    def instructor_pretty_table(self) -> None:
        """Display instructor info"""
        pt: PrettyTable = PrettyTable(field_names=["CWID", "Name", "Dept", "Course", "Students"])
        for i_cwid in self._instructors.keys():
            for rec in self._instructors[i_cwid].info():
                pt.add_row(rec)
        print(pt)


def main():
    """
   define the university
   """
    stevens_univ: University = University('C:\\Users\\rajek\\PycharmProjects\\untitled\\Project')
    stevens_univ.student_pretty_table()
    stevens_univ.instructor_pretty_table()


if __name__ == '__main__':
    main()
