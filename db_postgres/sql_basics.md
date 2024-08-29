installing and connection to study db:

```jsx
# installing psql writer
$ brew install libpq
$ echo 'export PATH="/usr/local/opt/libpq/bin:$PATH"' >> ~/.zshrc
$ source ~/.zshrc

# connection
$ psql -h 65.108.223.44 -d coursesdb -U student

```

sql examples in postgres

```sql
create table events (
    id bigint,
    name varchar(50),
    date date,
    time time,
    location varchar(100),
    description text
);

insert into events (
    id,
    name,
    date,
    time,
    location,
    description
) values(
    1, 
    'Arnold',
    '2023-01-23',
    '21:00:03',
    'LA',
    'Lorem ipsum'
);

insert into events (
    id,
    name,
    date,
    time,
    location,
    description
) values(
    2, 
    'Tim',
    '2023-01-26',
    '21:00:04',
    'SF',
    'Dolorem'
);

--
INSERT INTO article_categories (name) VALUES ('Интересное'), ('Популярное');
```

primary key

```sql
-- Одновременное использование и первичного ключа и автогенерации
id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
```

```sql
NULL

is
is not

where smth == Null --вернет пустую таблицу 
```

```sql
create table order_details (
    id bigint primary key generated always as identity,
    order_id bigint not null unique,
    product_id bigint not null,
    quantiy bigint not null
);

insert into order_details (order_id, product_id, quantiy) 
values(1, 42, 100),
(2, 666, 1),
(3, 999, 15);
```

Find by string

```sql
like -- регистро**зависим** 
ilike -- регистроНЕзависим
```

Regular expressions in postgres sql:

```sql
SIMILAR TO ‘[]’

-- examples:
WHERE username SIMILAR TO '%[a-z]';
WHERE username SIMILAR TO '%[0-9]';
WHERE username NOT SIMILAR TO '%[0-9]';
WHERE email SIMILAR TO '%@%.%';

WHERE email SIMILAR TO '%@%.__';
WHERE email SIMILAR TO '%.___';

-----------

-- Найти все имена, начинающиеся с буквы "A"
SELECT * FROM users WHERE name ~ '^A';

-- Найти имена, содержащие две буквы "o" подряд
SELECT * FROM users WHERE name ~ 'o{2}';

-- Найти имена, начинающиеся с буквы "a" или "A", игнорируя регистр
SELECT * FROM users WHERE name ~* '^a';

-- Найти все имена, начинающиеся с букв от "A" до "F"
SELECT * FROM users WHERE name ~ '^[A-F]';

-----------

-- Найти все имена, начинающиеся с буквы "A"
SELECT * FROM users WHERE name SIMILAR TO 'A%';

-- Найти имена, содержащие две буквы "o" подряд
SELECT * FROM users WHERE name SIMILAR TO '%o{2}%';

-- Найти имена, начинающиеся с буквы "a" или "A", игнорируя регистр
SELECT * FROM users WHERE name SIMILAR TO '(a|A)%';

-- Найти все имена, начинающиеся с букв от "A" до "F"
SELECT * FROM users WHERE name SIMILAR TO '[A-F]%';

-- Найти строки, содержащие слово "John"
SELECT * FROM users WHERE name SIMILAR TO '%\\yJohn\\y%';

-----------

-- Найти подряд 3 цифры - через квантификатор {}, внутри которого указано, 
-- сколько раз должен встретиться искомый паттерн.  В данном случае цифра
WHERE telephone  SIMILAR TO '[0-9]{3}'

select 
    first_name
    , email 

from users
where 
    (created_at >= '2022-07-01' and created_at <= '2022-07-31') 
    and email not similar to '%@%.%';

----
    
WHERE birthday BETWEEN '2022-01-01' AND '2022-02-01';

```

docs: https://www.postgresql.org/docs/current/functions-matching.html 

BETWEEN

```sql
>= and <=
```

ORDER BY

```sql
-- пустые строки в конце
ORDER BY {...} DESC 
NULLS 
LAST
-- FIRST - пустые строки вначале
```

OFFSET

```sql

-- Пропустит первые 10 записей за счет части OFFSET 10
FROM users ORDER BY id LIMIT 10 OFFSET 10;

```

DISTINCT

После `DISTINCT ON` в круглых скобках мы указываем поле, по которому будет проверяться уникальность 

```sql
SELECT DISTINCT ON (course_id)
    course_id,
    created_at
FROM course_members
ORDER BY course_id, created_at;
```

```sql
select 
    buyer_id, 
    count(id) as orders_count, 
    sum(price) as total_price 
from orders 
group by buyer_id
having count(id)  >= 2
order by total_price desc;
```

```sql
-- INSERT 
INSERT INTO users (username, email, first_name, last_name, birthday, gender, id, created_at, password_digest)
VALUES ('Bond007', 'tsconnery30@yahoo.com', 'Sean', 'Connery', '1930-08-25', 'male', 102, '2023-05-01', '33333'),
('Bond008', 'tsconnery131@yahoo.com', 'Sean', 'Connery', '1930-08-25', 'male', 102, '2023-05-01', '33333');

-- UPDATE
UPDATE users SET username = 'Neo' WHERE email = 'theone@yahoo.com';
```

Пример создания ограничения `UNIQUE`:

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username VARCHAR(50),
    email VARCHAR(255) UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP
);

INSERT INTO users (created_at, email, first_name, last_name, username) VALUES ('2022-06-14 18:31:05.296', 'Trevion53@yahoo.com', 'Lucienne', 'Feil', 'Duncan3');
INSERT INTO users (created_at, email, first_name, last_name, username) VALUES ('2022-06-14 02:04:13.104', 'Baylee52@yahoo.com', 'Ramiro', 'Wolf', 'Michaela11');
INSERT INTO users (created_at, email, first_name, last_name, username) VALUES ('2022-06-14 02:28:26.058', 'Casimer_Cronin@yahoo.com', 'Maureen', 'Romaguera', 'Margarete_Hegmann6');

```

```sql
INSERT INTO users (first_name, email) VALUES ('Gregory', 'gregory@google.com');
UPDATE users SET email = 'johny@hotmail.com' WHERE first_name = 'John';
DELETE FROM users WHERE first_name = 'Alex';
```


Если добавить значение повторно, то запрос завершится с ошибкой

Ограничение `NOT NULL` требует, чтобы значение в столбце не было `NULL`. Это означает, что при добавлении или обновлении записи в таблице, значение в столбце с ограничением `NOT NULL` должно быть обязательно указано

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP
);

```

Запрос `ALTER TABLE` используют, чтобы изменять структуру столбца таблицы базы данных. Он включает четыре операции:

- Добавление колонки
- Переименование колонки
- Удаление колонки
- Обновление колонки

```sql
ALTER TABLE users ADD COLUMN birthday DATE;

-- Чтобы переименовать колонку, нужно сделать следующий запрос:
ALTER TABLE users RENAME COLUMN name TO first_name;

-- Delete column
ALTER TABLE users DROP COLUMN age;
```

Команда по изменению параметров колонки наиболее сложная. Практически у каждого элемента, который поддается обновлению, есть собственный синтаксис для этого обновления. Вот несколько базовых примеров:

```sql
CREATE TABLE courses (
    id bigint PRIMARY KEY,
    name varchar(255) NOT NULL,
    body text,
    created_at timestamp
);

-- Установка ограничения уникальности в таблице courses для колонки name
ALTER TABLE courses
ADD UNIQUE (name);

-- Изменение типа данных в таблице courses для колонки created_at
-- и снятие ограничения NOT NULL в таблице courses для колонки name
ALTER TABLE courses
ALTER COLUMN created_at SET DATA TYPE DATE,
ALTER COLUMN name DROP NOT NULL;

-- Установка ограничения NOT NULL в таблицу courses для колонки name
ALTER TABLE courses
ALTER COLUMN name SET NOT NULL;
```

Наиболее распространенные команды:

- `ADD` — добавление ограничения: например, ключа или уникальности
- `SET` — установка значения: например, типа данных
- `DROP` — удаление ограничения

В рамках одного обновления можно группировать операции, но существует ряд исключений. Например, группировке не поддается операция `RENAME` — ее нужно выполнять отдельным запросом, иначе СУБД завершит запрос с ошибкой.

## Удаление записей

```sql
DELETE FROM table_name 
WHERE ...
```

## **Выводы**

В этом уроке мы разобрали тип запроса `ALTER`, который отвечает за изменение таблицы базы данных. Мы узнали, что с его помощью можно добавлять, переименовывать, удалять и обновлять колонки.

Первые три операции достаточно простые. При этом переименование или удаление колонок — небезопасные процессы. Если удалить колонки в работающей базе данных, это приведет к ошибкам, когда мы будем вставлять или обновлять записи. Любые выборки, включающие эту колонку, также завершатся с ошибкой.

Такие операции выполняют редко и только тогда, когда есть уверенность, что эти колонки никто не использует. Еще обновление колонки может серьезно влиять на производительность. А если данных много, то они будут обновляться продолжительное время — часы и даже дни.

```sql
alter table users add unique (email);
alter table users drop column age;
alter table users alter column name set not null;
alter table users rename column name to first_name;
alter table users add column created_at timestamp;

--- правильная последовательность команд:
ALTER TABLE users
ADD UNIQUE (email),
ADD COLUMN created_at timestamp;

ALTER TABLE users RENAME COLUMN name TO first_name;
ALTER TABLE users DROP COLUMN age;

ALTER TABLE users ALTER COLUMN first_name SET NOT NULL;
```

ACID

Транзакции

**атомарность** — когда операция либо завершается успешно, либо не проходит

```sql
BEGIN;
SELECT amount FROM accounts WHERE user_id = 10;
UPDATE accounts SET amount = amount - 50 WHERE user_id = 10;
UPDATE accounts SET amount = amount + 50 WHERE user_id = 30;
COMMIT;
```

## **Требования к транзакционной системе**

В информатике есть набор требований к транзакционной системе, которые гарантируют ее надежность — **ACID**. К ним относятся:

- Atomicity (Атомарность)
- Consistency (Согласованность)
- Isolation (Изолированность)
- Durability (Устойчивость)

Разберем каждое требование подробнее

### **Atomicity (Атомарность)**

Любая транзакция не может быть частично завершена — она либо выполнена, либо нет.

### **Consistency (Согласованность)**

Завершившаяся транзакция должна сохранять согласованность базы данных. Каждая успешная транзакция фиксирует только допустимые результаты, при том, что в процессе работы транзакции данные могут оказываться несогласованными.

В примере  снятие денег с одного счета приводит к тому, что данные рассинхронизированы. Но когда транзакция завершается, этого нет.

Гарантию согласованности данных нельзя полностью обеспечить только средствами базы данных, например, различными ограничениями. Поддержка этого требования включает в себя работу со стороны программистов, которые пишут необходимый для этого код.

### **Isolation (Изолированность)**

Когда транзакция выполняется, параллельные транзакции не должны оказывать влияния на ее результат. Ни одна транзакция не может увидеть изменения, которые сделаны другими незавершенными транзакциями. Изолированность — дорогое требование, поэтому в реальных БД существуют режимы, которые изолируют транзакцию не полностью — уровни изолированности Repeatable Read и ниже.

### **Durability (Устойчивость)**

Изменения, которые сделаны успешно завершенной транзакцией, должны остаться сохраненными после возвращения системы в работу. И это не должно зависеть от проблем на нижних уровнях, к примеру, обесточивание системы или сбои в оборудовании. Если пользователь получил подтверждение от системы, что транзакция выполнена, он будет уверен, что ничего не отменится из-за какого-либо сбоя.

```sql
begin;
delete from user_items where (username = 'lord_mormont' and item = 'Longclaw');
insert into  user_items (username, item, received_at) values('jon', 'Longclaw', now());
commit;
```