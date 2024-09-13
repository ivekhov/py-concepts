# DAO


Работать напрямую с запросами в коде не очень удобно. Много низкоуровневых деталей, много повторяющегося, шаблонного, кода. Постоянная необходимость преобразовывать данные в одну и другую сторону. Чтобы решить эту проблему, работу с базой можно скрыть за какой-то абстракцией. Один из вариантов такой изоляции называют Data Access Object или просто DAO.

Концепция DAO очень простая, она сводится к созданию сущности под каждую таблицу в базе данных. Далее реализуются методы или функции, которые сохраняют, удаляют или ищут сущности в этой таблице. В случае пользователей, наш класс DAO может выглядеть так


```python
# models.py
from dataclasses import dataclass
from typing import Optional

# так как класс нам нужен лишь для хранения данных, то используем датакласс
@dataclass
class User:
    username: str
    phone: str
    id: Optional[int] = None


# db.py
import psycopg2
from psycopg2.extras import DictCursor

def get_db_connection():
    return psycopg2.connect(
        dbname="your_database",
        user="your_username",
        password="your_password",
        host="your_host",
        cursor_factory=DictCursor
    )


def commit(conn):
    conn.commit()

def save_user(conn, user):
    with conn.cursor() as cur:
        if user.id is None:
            cur.execute(
                "INSERT INTO users (username, phone) VALUES (%s, %s) RETURNING id;",
                (user.username, user.phone)
            )
            user.id = cur.fetchone()['id']
        else:
            cur.execute(
                "UPDATE users SET username = %s, phone = %s WHERE id = %s;",
                (user.username, user.phone, user.id)
            )
    return user


def find_user(conn, user_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
        result = cur.fetchone()
        if result:
            return User(**result)
    return None


```


```python
usage

from models import User
import db

conn = db.get_connection()


user = User(username="John Doe", phone="1234567890")
user.id # None

new_user = db.save_user(conn, user)
# делаем коммит после каждого изменения
db.commit(conn)
new_user.id # тут уже выводится какой-то id

found_user = db.find_user(conn, 42)
db.commit(conn)
found_user # здесь выводится найденный user

# закрываем соединение
conn.close()
```


```python


# BEGIN (write your solution here)

def save_lesson(conn, lesson):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        if lesson.id is None:
            cur.execute(
                '''
                INSERT INTO lessons (name, text, course_id) VALUES (%s, %s, %s) RETURNING id;
                ''',
                (lesson.name, lesson.text, lesson.course_id)
            )
            lesson.id = cur.fetchone().id
        else:
            cur.execute(
                "UPDATE lessons SET name = %s, text = %s, course_id = %s WHERE id = %s;",
                (lesson.name, lesson.text, lesson.course_id, lesson.id)
            )
    return lesson.id


def find_lesson(conn, lesson_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT * FROM lessons WHERE id = %s;", (lesson_id,))
        result = cur.fetchone()
        if result:
            return Lesson(
                id=result.id,
                name=result.name,
                text=result.text,
                course_id=result.course_id
                )
    return None


def get_course_lessons(conn, course_id):
    lessons = []
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT * FROM lessons WHERE course_id = %s;", (course_id, ))
        for row in cur.fetchall():
            lessons.append(Lesson(
                    id=row.id,
                    name=row.name,
                    text=row.text,
                    course_id=row.course_id
                    ))
        return lessons



# END



```