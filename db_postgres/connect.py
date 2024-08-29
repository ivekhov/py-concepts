import psycopg2

try:
    # пытаемся подключиться к базе данных
    # в данном примере БД запущена из докер образа 
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='fG89ad0gFf', host='localhost')
    print('connected!')
except:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Can`t establish connection to database')


sql = "CREATE TABLE users (id BIGINT PRIMARY KEY generated always as identity, username VARCHAR(255), phone VARCHAR(255))"
# Запрос выполняется через создание объекта курсора
cursor = conn.cursor()
cursor.execute(sql)
cursor.close() # в конце закрывается

sql2 = "INSERT INTO users (username, phone) VALUES ('tommy', '123456789');"
cursor = conn.cursor()
cursor.execute(sql2)
cursor.close()

sql3 = "SELECT * FROM users;"
cursor = conn.cursor()
# Указатель на набор данных в памяти СУБД
cursor.execute(sql3)
for row in cursor:
    print(row)
cursor.close()

conn.commit() # Коммитим, т.е. сохраняем изменения в БД
conn.close() # Соединение нужно закрыть
print('Connection closed')

'''
def add_movies(conn):
    cursor = conn.cursor()
    sql = """insert into movies(title, release_year, duration) 
    values ('Godfather', 1972, 175), ('The Green Mile', 1999, 189);"""
    cursor.execute(sql)
    cursor.close()

def get_all_movies(conn):
    cursor = conn.cursor()
    sql = "select * from movies;"
    cursor.execute(sql)
    result = []
    for row in cursor:
        result.append(row)
    cursor.close()
    return result

sql = "INSERT INTO movies (title, release_year, duration) VALUES %s, %s;"
curs.execute(sql, (('Godfather', 1972, 175), ('The Green Mile', 1999, 189)))

'''
# Context managers 
# https://ru.hexlet.io/courses/python-sql/lessons/context-managers/theory_unit

conn = psycopg2.connect('postgresql://user:password@host:port/hexlet_test')
sql = "INSERT INTO users (username, phone) VALUES ('tommy', '123456789');"
with conn:
    with conn.cursor() as curs:
        curs.execute(sql)

conn.close() # закрываем соединение

# https://www.psycopg.org/docs/usage.html#with-statement





# EXAMPLE 

import psycopg2

conn = psycopg2.connect('postgresql://tirion:secret@localhost:5432/tirion')


# BEGIN (write your solution here)


def make_cars_table(conn):
    sql = '''
    create table cars(
        id serial primary key, 
        brand varchar(255),
        model varchar(255)
    );
    '''

#  serial instead of generated always as identity,

    with conn.cursor() as curs:
        curs.execute(sql)


def populate_cars_table(conn, cars):
    with conn.cursor() as curs:
        for car in cars:
            curs.execute(f"insert into cars (brand, model) values ('{car[0]}', '{car[1]}');")


def get_all_cars(conn):
    sql = '''
    select * from cars
    order by brand asc;
    '''
    with conn.cursor() as curs:
        curs.execute(sql)

        result = []
        for row in curs:
            result.append(row)
        return result
    
        # or
        # result = curs.fetchall()
        # return result


conn.close()
# END


