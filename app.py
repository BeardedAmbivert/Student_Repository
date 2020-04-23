from typing import Dict, List

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DB_FILE = r'C:\Users\rajek\PycharmProjects\Student_Repository\student_repo.sqlite'


@app.route('/')
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

        return render_template('student_record.html', title='Home', heading='Student Repository', students=data)


if __name__ == '__main__':
    app.run(debug=True)
