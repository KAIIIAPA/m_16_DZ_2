# TZ:
# 1. Создайте базу данных students.db
# 2. В базе данных должны существовать 2 таблицы: students и grades
# 3. В таблице students должны присутствовать следующие поля: id, name, age
# 4. В таблице grades должны присутствовать следующие поля: id, student_id, subject, grade
# 5.Так же нужно создать класс University со следующими атрибутами и методами:
# name - имя университета
# add_student(name, age) - метод добавления студента.
# add_grade(sudent_id, subject, grade) - метод  добавления оценки.
# get_students(subject=None) - метод для возврата списка студентов,
# в формате[(Ivan, 26, Python, 4.8), (Ilya, 24, PHP, 4.3)], где
# subject, если не является None(по умолчанию) и если такой предмет существует,
# выводит студентов только по этому предмету.

import sqlite3


class University:

    def __init__(self, name):
        self.name = name
        # 1.Создайте базу данных students.db
        # Создаем соединение с новой базой данных
        conn = sqlite3.connect('students.db')

        # 2.В базе данных должны существовать 2 таблицы: students и grades\
        # Создаем объект cursor, который позволяет выполнять команды SQL
        c = conn.cursor()

        # 2.1. В таблице students должны присутствовать следующие поля: id, name, age
        c.execute(""" CREATE TABLE students (
                 id INTEGER PRIMARY KEY, 
                 name STRING, 
                 age INTEGER)""")
        # 2.2. В таблице grades должны присутствовать следующие поля: id, student_id, subject, grade
        c.execute("""CREATE TABLE grades (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id INTEGER,
                  subject STRING, 
                  grade FLOAT, 
                  FOREIGN KEY (student_id) REFERENCES students(id))""")

        # Закрываем соединение с базой данных
        c.close()
        conn.close()

    def add_students(self, name, age):
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (name, age) VALUES ( ? , ? )", (name, age))
        conn.commit()
        conn.close()

    def add_grade(self, student_id, subject, grade):
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("INSERT INTO grades (student_id, subject, grade) VALUES ( ? , ?  , ?)",
                  (student_id, subject, grade))
        conn.commit()
        conn.close()

    def get_students(self, subject=None):
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        if subject is None:
            c.execute('SELECT s.name , s.age , g.subject , g.grade'
                      ' FROM students s '
                      'JOIN grades g ON s.id = g.student_id ')
        else:
            c.execute('SELECT s.name , s.age , g.subject , g.grade'
                      ' FROM students s JOIN grades g ON s.id = g.student_id '
                      'WHERE g.subject = ?', (subject,))
        result = c.fetchall()
        conn.close()
        return result


u1 = University(name='Urban')

u1.add_students(name='Ildar', age=28)
u1.add_students(name='Ivan', age=30)
u1.add_students(name='Oleg', age=35)
u1.add_students(name='Marat', age=40)

u1.add_grade(student_id=1, subject='Python', grade=4.55)
u1.add_grade(student_id=3, subject='Python', grade=5.00)
u1.add_grade(student_id=4, subject='C#', grade=4.05)
u1.add_grade(student_id=2, subject='JS', grade=3.99)

print(u1.get_students())
print(u1.get_students(subject='Python'))
