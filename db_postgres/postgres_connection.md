**Основы SQL**

- [Работа с SQL](https://ru.hexlet.io/courses/sql-basics/lessons/psql/theory_unit#_%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0_%D1%81_sql)
- [Клиент DBeaver](https://ru.hexlet.io/courses/sql-basics/lessons/psql/theory_unit#_%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82_dbeaver)
- [Выводы](https://ru.hexlet.io/courses/sql-basics/lessons/psql/theory_unit#_%D0%B2%D1%8B%D0%B2%D0%BE%D0%B4%D1%8B)

SQL — это структурированный язык запросов. В этом уроке научимся подключаться к базе данных и работать с ней используя утилиту *psql*.

Psql — это интерактивная консольная утилита, которая позволяет взаимодействовать с базой данных через командную строку. Клиент *psql* это стандартный способ для подключения к БД и его можно установить вместе с СУБД.

Для начала, чтобы подключиться к базе данных с помощью psql, необходимо выполнить команду:

`psql -H server_address -U username -d dbname`

Где *server_address* - адрес сервера СУБД, username - это ваше имя пользователя, а dbname - название базы данных, к которой вы хотите подключиться. После выполнения этой команды, вам будет предложено ввести пароль.

`psql -h 65.108.223.44 -d coursesdb -U student
Password **for** user student:
*# вводим пароль student*`

После успешного подключения, вы увидите приглашение psql для ввода команд и название текущей базы данных. Например:

`Password for user student:
psql (14.11 (Ubuntu 14.11-0ubuntu0.22.04.1), server 12.18)
Type "help" for help.

coursesdb=>`

Утилита PSQL имеет команды, которые позволяют изучить структуру базы данных. Посмотрим, какие таблицы есть в этой БД:

`psql (14.11 (Ubuntu 14.11-0ubuntu0.22.04.1), server 12.17)
Type "help" for help.

coursesdb=> \dt
             List of relations
 Schema |      Name      | Type  |  Owner
--------+----------------+-------+----------
 public | course_members | table | postgres
 public | course_reviews | table | postgres
 public | courses        | table | postgres
 public | topics         | table | postgres
 public | users          | table | postgres
(5 rows)

coursesdb=>`

`\dt` - это специальная команда в *psql*. С ее помощью мы вывели список всех таблиц в этой базе данных. Список всех доступных команд можно посмотреть с помощью справки `\?`.

Мы видим, что после вывода списка таблиц снова вывелось приглашение `coursesdb⇒` Это и есть REPL. После выполнения команды печатается её результат и снова выводится приглашение о вводе новой команды.

Мы подключились к базе данных и изучили ее структуру. Теперь попробуем выполнить запросы.

## **Работа с SQL**

Сделаем запрос с помощью *psql*:

`coursesdb=> SELECT id, first_name, last_name FROM users ORDER BY first_name ASC LIMIT 5;
 id | first_name | last_name
----+------------+-----------
 16 | Abe        | Funk
  8 | Abigale    | Turner
 34 | Alejandrin | Nicolas
 13 | Alfreda    | Hermann
 33 | Alfredo    | Sipes
(5 rows)

coursesdb=>`

Утилита вывела 5 записей из таблицы *users*. Выведены поля *id*, *first_name*, *last_name*. Записи отсортированы по имени в алфавитном порядке.

Все запросы в *psql* выполняются только если их отправить клавишей Enter

Чтобы запрос выполнился, нужно соблюсти два условия.

1. В конце запроса должна быть точка с запятой
2. В конце запроса необходимо нажать Enter для его отправки.

`coursesdb**=>** **SELECT** id, first_name, last_name **FROM** users **ORDER** **BY** first_name **ASC** **LIMIT** 5
coursesdb**->** ;
 id **|** first_name **|** last_name
*----+------------+-----------*16 **|** Abe        **|** Funk
  8 **|** Abigale    **|** Turner
 34 **|** Alejandrin **|** Nicolas
 13 **|** Alfreda    **|** Hermann
 33 **|** Alfredo    **|** Sipes
(5 **rows**)

coursesdb**=>**`

Если запрос можно вводить не целиком, а построчно, то утилита будет ожидать ввода точки с запятой для завершения построения запроса.

`coursesdb**=>** **SELECT**coursesdb**->**     id,
coursesdb**->**     first_name,
coursesdb**->**     last_name
coursesdb**->** **FROM** users
coursesdb**->** **ORDER** **BY** first_name
coursesdb**->** **LIMIT** 5;
 id **|** first_name **|** last_name
*----+------------+-----------*16 **|** Abe        **|** Funk
  8 **|** Abigale    **|** Turner
 34 **|** Alejandrin **|** Nicolas
 13 **|** Alfreda    **|** Hermann
 33 **|** Alfredo    **|** Sipes
(5 **rows**)

coursesdb**=>**`

Psql — это базовый клиент для работы с СУБД PostgreSQL. Рассмотрим графические клиенты на примере DBeaver.

## **Клиент DBeaver**

DBeaver — бесплатный универсальный клиент для работы с различными СУБД. Его основные преимущества — распространенный, бесплатный и доступен на множестве платформ. Установить его можно по инструкции

https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6IjIxNzRiMDk2NjA5OGQwNjVhYmYyMDI0YTZjZmQ3ZjYyLnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=edf8f72f1829857106f0fcc16c27c352705b72849a4ccc0090c394ee1cce1960

Повторим те же действия, что выполняли *psql*

Подключаемся к базе данных. Здесь нужно выбрать нужную СУБД. Потребуется указать адрес сервера, базу данных, имя пользователя и пароль. С помощью Test Connection можно проверить подключение

https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6Ijg0N2Q5YjA1YzA2NDkzMDk2NDcxYTI0NmFkMjA0NzczLnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=0f865d932bf007e6c8e28add1bc30a7f38fbbfaa615b4c642f58e47c8fc001a4

Структура база данных. DBeaver показывает структуру БД в своем интерфейсе

https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6ImI0MjU3OTg5YjAwMDcwZDI0YTZiOTBkODM4NjQwNmNhLnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=7088a46eca66359791ab371bb35fd5ceb4631adabfb94e0f1db3df7df5fb702e

Создание базы данных и выполнения запросов. Создать Базу и таблицу можно как через интерфейс DBeaver, так и с помощью SQL. Для выполнения SQL запросов необходимо в верхнем меню выбрать SQL Editor - New SQL Script. Под полем ввода SQL находится поле вывода результата. Если запрос что-то возвращает, то результат появится здесь. Сам результат можно скопировать в один из популярных текстовых форматов данных

https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6ImJhMzNmZmZjNGY0ZTQyZTg0YTZkNjE0MWNkZGU2OGNjLnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=bc85c252b5603cb7f7c2dd83c929b18d052be457bbcdc78dda8a92f1ef609bed

## **Выводы**

Мы познакомились с утилитой *psql*. Это стандартный клиент для подключения к PostgreSQL. В *psql* можно изучать структуру базы данных, создавать новые базы, таблицы и выполнять SQL запросы.

Все SQL запросы в *psql* должны содержать в конце точку запятой. Запрос не выполняется до того, как мы его отправим на сервер.

Помимо *psql* существуют и другие клиенты для работы с СУБД, например DBeaver. Они позволяют работать с базами данных через графический интерфейс и имеют те же возможности, что и *psql*.

https://www.psycopg.org/docs/usage.html