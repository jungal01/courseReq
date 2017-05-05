from flask import Flask, render_template, request
from psycopg2 import connect
import os

conn = connect(os.environ['DATABASE_URL'])
cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def allCourses():
    cur.execute('select number, title, dept from course_requirement cr join course c on cr.course = c.id;')
    return render_template('course.html',
                            all = cur.fetchall(),
                            columns = [x.number for x in cur.description])

@app.route('/dept')
def departments():
    conn.get_db()
    dept = request.args['selected_dept']
    cur = conn.cursor()
    cur.execute('select number, title from course where dept = %s order by title;', (dept,))
    return render_template('course.html',
                            deptCourses = cur.fetchall(),
                            depts = [],
                            columns = [x.name for x in cur.description])

@app.route('/course')
def course():
    conn = get_db()
    course = request.args['selected_course']
    cur = conn.cursor()
    cur.execute('''select title, description, fulfills
                   from course_requirement cr join course c on (cr.course=c.id) join requirement r on (cr.requirement=r.id)
                   where number= %s;''', (course,))
    return render_template('course.html',
                            courses = cur.fetchall(),
                            course = [],
                            columns = [x.name for x in cur.description])

@app.route('/reqs')
def allReqs():
    conn = get_db()
    required = request.args['selected_req']
    cur = conn.cursor()
    cur.execute('''select number, title
                   from course_requirement cr join course c on (cr.course=c.id) join requirement r on (cr.requirement=r.id)
                   where fulfills= %s order by number;''', (required,))
    return render_template('course.html',
                            reqs = cur.fetchall(),
                            req = [],
                            columns = [x.name for x in cur.description])


if __name__ == '__main__':
    app.run(debug=True, port=8009)
