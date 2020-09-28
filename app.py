from typing import Dict, List

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from Student_Repository_Aditya_Kulkarni import University as university

app = Flask(__name__)

DB_FILE = r'student_repo.sqlite'


@app.route('/')
def index():
    # if 'majors' in request.form:
    #     return redirect(url_for('student_record'))
    # elif 'watch' in request.form:
    #     pass  # do something else
    info: Dict = {
        'buttons': {
            'major': {'name': 'Majors', 'url': 'majors'},
            'instructor': {'name': 'Instructor Record', 'url': '/instructors'},
            'student_record': {'name': 'Student Record', 'url': '/studentRecord'},
            'student_grades': {'name': 'Student Grades', 'url': '/studentGrades'}
        }
    }
    return render_template('index.html', title='Home', heading='Student Repository', body=info)


@app.route('/student_table')
def student_record():
    _query: str = """select s.Name as Name, s.CWID, g.Course, g.Grade, i.Name as Instructor
                                  from students s
                                    join grades g on s.CWID = g.StudentCWID
                                    join instructors i on g.InstructorCWID = i.CWID
                                  order by s.Name;"""
    try:
        db: sqlite3.Connection = sqlite3.connect(DB_FILE)
    except sqlite3.OperationalError as e:
        print(e)
    else:
        data: List[Dict[str, str]] = \
            [{'student': student, 'cwid': cwid, 'course': course, 'grade': grade, 'instructor': instructor}
             for student, cwid, course, grade, instructor in db.execute(_query)]
        db.close()
    print(f"data: {data}")
    # students = list(student_repo.student_pretty_table())
    # print(students)
    return render_template('student_record.html', title='Home', heading='Student Repository',
                           students=data)


@app.route('/faculty_table')
def faculty_record():
    _query: str = """select s.Name as Name, s.CWID, g.Course, g.Grade, i.Name as Instructor
                                      from students s
                                        join grades g on s.CWID = g.StudentCWID
                                        join instructors i on g.InstructorCWID = i.CWID
                                      order by s.Name;"""
    try:
        db: sqlite3.Connection = sqlite3.connect(DB_FILE)
    except sqlite3.OperationalError as e:
        print(e)
    else:
        data: List[Dict[str, str]] = \
            [{'student': student, 'cwid': cwid, 'course': course, 'grade': grade, 'instructor': instructor}
             for student, cwid, course, grade, instructor in db.execute(_query)]
        db.close()
    print(f"data: {data}")
    # students = list(student_repo.student_pretty_table())
    # print(students)
    return render_template('faculty_record.html', title='Home', heading='Student Repository',
                           students=data)


if __name__ == '__main__':
    student_repo: university = university(os.path.dirname(os.getcwd()))
    app.run(debug=True)
