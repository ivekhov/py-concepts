import psycopg2
from psycopg2.extras import execute_batch, execute_values


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

        # bad 
        # for car in cars:
        #     curs.execute(f"insert into cars (brand, model) values ('{car[0]}', '{car[1]}');")
        
        # better
        execute_values(curs, 'insert into cars(brand, model) values %s', cars)


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



# batch insert
def make_products_table(conn):
    sql = '''
    create table products(
        id serial primary key, 
        name VARCHAR(255) NOT NULL,
        price NUMERIC NOT NULL,
        quantity INT NOT NULL
    );
    '''
    with conn.cursor() as curs:
        curs.execute(sql)



def batch_insert(conn, products):
    with conn.cursor() as curs:
        execute_batch(curs, 'insert into products (name, price, quantity) values (%(name)s, %(price)s, %(quantity)s)', products)

def get_all_products(conn):
    sql = 'select * from products order by price desc;'
    with conn.cursor() as curs:
        curs.execute(sql)
        result = curs.fetchall()
        return result

'''
def batch_insert(conn, products):
    with conn.cursor() as cur:
        values = [(p['name'], p['price'], p['quantity']) for p in products]

        insert_query = "INSERT INTO products (name, price, quantity) VALUES %s"

        execute_values(cur, insert_query, values)
    conn.commit()


def get_all_products(conn):
    with conn.cursor() as cur:
        sql = "SELECT * FROM products ORDER BY price DESC;"
        cur.execute(sql)
        result = cur.fetchall()
    conn.commit()
    return result
'''


def get_order_sum(conn, month):
    sql = '''
    select c.customer_name as customer_name, sum(o.total_amount) as amount
    from customers as c
    left join orders as o
        on o.customer_id = c.customer_id 
    where DATE_PART('MONTH', o.order_date)=%s
    group by c.customer_name;
    '''
    rows = []
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(sql, (month,))
        res = curs.fetchall()
        for customer in res:
            rows.append(f"Покупатель {customer.get('customer_name')} совершил покупок на сумму {customer.get('amount')}")
        return '\n'.join(rows)



### CURSOR
from psycopg2.extras import DictCursor

def create_post(conn, post):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(
            'insert into posts (title, content, author_id) values (%s, %s, %s) RETURNING id;', 
            (post.get('title'), post.get('content'), post.get('author_id'))
        )
        post_id = curs.fetchone()[0]
        conn.commit()
        return post_id











if __name__ == '__main__':
    '$ poetry run python create_table.py'

    # 1
    # make_cars_table(conn)
    # cars = [('kia', 'sorento'), ('bmv', 'x5'), ('audi', 'q5'), ('tesla', 'm3')]
    # populate_cars_table(conn, cars)

    # select = get_all_cars(conn)
    # for car in select:
    #     print(car)
    
    # 2 batch testing
    make_products_table(conn)
    products = [
        {'name': 'milk', 'price': 12, 'quantity': 20},
        {'name': 'bread', 'price': 3, 'quantity': 10},
        {'name': 'orange', 'price': 6, 'quantity': 5}
    ]
    get_all_products(conn)

    batch_insert(conn, products)
    select = get_all_products(conn)
    for row in select:
        print(row)

    conn.close()
