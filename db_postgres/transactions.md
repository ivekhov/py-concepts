## Транзакции

При подключении к базе создается объект connection. Этот объект управляет всеми транзакциями в базе. Рассмотрим подробнее как работают соединения в Psycopg2.

По умолчанию, когда первая команда отправляется в базу данных, с помощью cursor, создается новая транзакция. Все последующие запросы в базу данных будут выполняться в контексте той же транзакции. И тут не только запросы первого курсора, но и запросы всех курсоров в рамках того же соединения. Если какая-либо команда завершится неудачно, транзакция будет прервана, и никакие дальнейшие команды не будут выполняться до вызова метода rollback().


Соединение отвечает за завершение своей транзакции, вызывая метод commit() или rollback(). Все изменения немедленно становятся постоянными в базе данных. Если соединение закрывается, с помощью метода close(), или уничтожается, с помощью del или выходя из области видимости, во время выполнения транзакции, то сервер отменит транзакцию.

## Коммиты

По умолчанию даже простой SELECT начинает транзакцию. А значит, пока мы не закоммитим действия, то сессия соединения так и останется в ожидании - "idle in transaction". Новички часто совершают подобную ошибку, недоумевая почему после запроса программа перестает отвечать. Ведь в режиме транзакции сессия удерживает блокировки на таблицу. Потому важно сохранять коммитом все изменения в базе, либо можно установить параметр соединения autocommit, тогда все запросы будут сохраняться автоматически.


```python
# здесь транзакция еще не началась
curs = conn.cursor()

# здесь исполняется запрос, теперь транзакция началась
cur.execute("SELECT count(*) FROM table")

curs_2 = conn.cursor()
# новый запрос исполняется в той же транзакции
curs_2.execute("INSERT INTO data VALUES (%s)", ("Hello",))

# так как не было commit(), то вставка INSERT выше будет отменена
conn.close()

###
conn = psycopg2.connect('postgresql://user:password@host:port/hexlet_test')
sql = "INSERT INTO users (username, phone) VALUES ('tommy', '123456789');"

curs = conn.cursor()
curs.execute(sql)

# мы не сделали коммит изменений, а значит вся операция будет отменена
conn.close()
```


```sql

# BEGIN
def create_post(conn, post):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO posts (title, content, author_id)
            VALUES (%(title)s, %(content)s, %(author_id)s)
            RETURNING id
        """, post)
        post_id = cur.fetchone()[0]
    conn.commit()
    return post_id


def add_comment(conn, comment):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO comments (post_id, author_id, content)
            VALUES (%(post_id)s, %(author_id)s, %(content)s)
            RETURNING id
        """, comment)
        comment_id = cur.fetchone()[0]
    conn.commit()
    return comment_id


def get_latest_posts(conn, n):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute("""
            SELECT
                p.*,
                c.id as comment_id,
                c.author_id as comment_author_id,
                c.content as comment_content,
                c.created_at as comment_created_at
            FROM posts p
            LEFT JOIN comments c ON p.id = c.post_id
            WHERE p.id IN (
                SELECT id FROM posts
                ORDER BY created_at DESC
                LIMIT %s
            )
            ORDER BY p.created_at DESC, c.created_at DESC
        """, (n,))

        rows = cur.fetchall()

        posts_dict = {}
        for row in rows:
            post_id = row['id']
            if not posts_dict.get(post_id):
                posts_dict[post_id] = {
                    'id': row['id'],
                    'title': row['title'],
                    'content': row['content'],
                    'author_id': row['author_id'],
                    'created_at': row['created_at'],
                    'comments': []
                }

            if row.get('comment_id'):
                posts_dict[post_id]['comments'].append({
                    'id': row['comment_id'],
                    'author_id': row['comment_author_id'],
                    'content': row['comment_content'],
                    'created_at': row['comment_created_at']
                })

        return list(posts_dict.values())
# END

```