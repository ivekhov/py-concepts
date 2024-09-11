## Курсор
Для получения результата после выполнения запроса используются следующие команды:

```sql
cursor.fetchone() — вернуть одну строку
cursor.fetchall() — вернуть все строки
cursor.fetchmany(size=10) — вернуть указанное количество строк

# Также курсоры итерируемы, так что получить результаты запросы можно обходом.

curs.execute('SELECT * FROM users;')
for row in curs:
    print(row)
```
Курсоры привязаны к соединению на весь срок жизни, и все команды выполняются в контексте одной сессии базы данных, обернутой соединением. Любые изменения, сделанные в базе данных одним курсором, немедленно видны другим курсорам. Потому, хорошей практикой при работе с базой данных является закрытие курсора и соединения с базой. Для автоматизации этого процесса удобно взаимодействовать через контекстный менеджер, используя конструкцию with :
```python
with conn.cursor as curs:
    curs.execute('SELECT * FROM users;')
    all_users = curs.fetchall()
```

## Фабрика

По умолчанию результат возвращается в виде кортежа. Такое поведение возможно изменить, передав параметр cursor_factory в момент открытия объекта cursor. Так вместо обычного курсора вернется его подкласс с новыми возможностями.

Наиболее полезные подклассы курсоров:

- RealDictCursor - возвращает данные в виде словаря
- NamedTupleCursor - возвращает данные в виде именованного кортежа, более легковесной альтернативы словарю
- LoggingCursor - логгирует все запросы в файл или объект логгера

```python
from psycopg2.extras import NamedTupleCursor

with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
    curs.execute('SELECT * FROM users WHERE name=%s;', ('Alfred',))
    alfred = curs.fetchone()
    alfred # (id=10, name='Alfred', age='90')
```

## Серверные курсоры
Когда выполняется запрос к базе данных, курсор получает все записи, возвращаемые базой, бэкендом, передавая их в клиентский процесс. Если запрос возвращает большое количество данных, то и будет выделен пропорционально большой объем памяти на стороне клиента.

Если набор данных слишком велик для практической обработки на стороне клиента, то можно создать курсор на стороне сервера. Используя такой курсор, можно передавать клиенту только контролируемое количество данных, не храня весь объем полностью в памяти.

В Psycopg2 серверные курсоры называются именованными курсорами. Именованный курсор создается с помощью метода cursor() с указанием параметра name. Такой курсор ведет себя как обычный курсор, позволяя пользователю перемещаться по набору данных с помощью метода scroll() и читать данные с помощью методов fetchone()и fetchmany(). По умолчанию можно перемещаться только вперед, но если вам нужно перемещаться назад, нужно объявить ваш курсор scrollable.

```python
with conn.cursor(name='cursor_name', scrollable=True) as curs:
    curs.execute('SELECT * FROM users;')
    result = curs.fetchall()
```
https://www.psycopg.org/docs/extras.html#connection-and-cursor-subclasses

https://www.psycopg.org/docs/usage.html#server-side-cursors


## Example
```python

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

conn.close()


###
def create_post(conn, post):

    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(
            'insert into posts (title, content, author_id) values (%s, %s, %s)', 
            (post.get('title'), post.get('content'), post.get('author_id'))
    )

###
def create_post(conn, post):
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(
            'insert into posts (title, content, author_id) values (%s, %s, %s) RETURNING id;', 
            (post.get('title'), post.get('content'), post.get('author_id'))
        )
        curs.fetchone()[0]
        conn.commit()


```