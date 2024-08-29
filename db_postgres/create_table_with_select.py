import psycopg2


conn = psycopg2.connect(dbname='postgres', user='postgres', password='fG89ad0gFf', host='localhost')


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

        # result = []
        # for row in curs:
        #     result.append(row)
        # return result
    
        # or
        result = curs.fetchall()
        return result

if __name__ == '__main__':
    '$ poetry run python create_table.py'
    make_cars_table(conn)
    cars = [('kia', 'sorento'), ('bmv', 'x5')]
    populate_cars_table(conn, cars)
    select = get_all_cars(conn)
    for car in select:
        print(car)
    conn.close()
