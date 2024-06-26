# class Counter:
#     def __init__(self, value=0):
#         self.value = max(value, 0)
#         value = max(value, 0)

#     def inc(self, delta=1):
#         return Counter(max((self.value + delta), 0))

#     def dec(self, delta=1):
#         # return Counter(self.value - delta) # prev version
#         return self.inc(-delta) # cooler


def test_counter():
    c = Counter(-42)
    assert c.value == 0
    assert c.inc().inc(5).dec(2).value == 4
    assert c.inc().inc().dec().value == 1
    assert c.dec().dec().value == 0  # 0 is the minimum value
    d = c.inc(100)
    assert d.dec().value == 99
    forty_two = Counter(42)
    assert forty_two.value == 42

class HourClock:
    def __init__(self):
        self.position = 0
    

    # getter of attribute hours
    @property
    def hours(self):
        return self.position

    
    # setter of attribute hours
    @hours.setter    
    def hours(self, new_position):
        self.position = new_position % 12

def test_clock():
    clock = HourClock()
    assert clock.hours == 0
    clock.hours += 6
    clock.hours += 5
    assert clock.hours == 11
    clock.hours += 4
    assert clock.hours == 3
    clock.hours -= 4
    assert clock.hours == 11
    clock.hours = 123
    assert clock.hours == 3


class Counter(object):
    """A simple integral counter."""

    def __init__(self):
        """Initialize a new counter with zero as starting value."""
        self.value = 0

    def inc(self, amount=1):
        """Increment counter's value."""
        self.value = max(self.value + amount, 0)

    def dec(self, amount=1):
        """Decrement counter's value."""
        self.inc(-amount)

class LimitedCounter(Counter):
    def __init__(self, limit):
        super().__init__()  # Вызываем конструктор предка
        self.limit = limit  # Дополнительный атрибут для наследника

    def inc(self, amount=1):
        # if self.value + amount > self.limit:
        #     self.value = self.limit
        # else:
        #     super().inc(amount)
        self.value = min((self.value + amount), self.limit)

    def dec(self, amount):
        self.value = max(0, (self.value - amount))



class LimitedCounter2(Counter):
    """A counter with limited maximal value.
        
    Решение основано на замене атрибута value на свойство,
    setter которого ограничивает значение счетчика.
    Такой подход позволяет сохранить свойства класса даже
    если пользователь будет менять значение счетчика через
    присваивание напрямую атрибуту value.
    
    Если вы просто унаследуете Counter и переопределите
    метод inc, то такое решение тоже будет правильным.
    Данное решение нарочно демонстрирует альтернативный подход :)
    
    """

    def __init__(self, limit):
        """Initialize a new counter with some limit."""
        self.limit = limit
        # Свойство должно где-то хранить фактическое значение
        # счетчика, для чего вводится "скрытый" ("приватный")
        # атрибут _actual_value:
        self._actual_value = 0
        # Инициализация методом родителя делается в конце,
        # потому что предок уже в __init__ присваивает атрибуту
        # value значение 0. А это значит, что будет вызван setter,
        # который использует атрибуты limit и _actual_value.
        super().__init__()

    @property
    def value(self):
        return self._actual_value

    @value.setter
    def value(self, new_value):
        self._actual_value = min(max(new_value, 0), self.limit)
# END


def test_counter2():
    counter = Counter()
    counter.inc()
    counter.inc(7)
    assert counter.value == 8
    counter.dec(10)
    assert counter.value == 0
    counter.inc(7)
    counter.inc(7)
    assert counter.value == 14


def test_limitedcounter():
    counter = LimitedCounter(limit=10)
    counter.inc()
    counter.inc(7)
    assert counter.value == 8
    counter.dec(10)
    assert counter.value == 0
    counter.inc(7)
    counter.inc(7)
    assert counter.value == 10


### decorators and Exceptions



def suppress(errors, *, or_return=None):
    def wrapper(function):
        def inner(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except errors as e:
                return or_return

        return inner

    return wrapper



# BEGIN
from functools import wraps

def suppress_example(exception, *, or_return=None):
    """Suppress exceptions of provided class(es) and return a value instead."""
    def wrapper(function):
        @wraps(function)
        def inner(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except exception:
                return or_return
        return inner
    return wrapper
# END



# tests

def walk(path, structure):
    """Walk down to structure using path."""
    if not path:
        return structure
    key, *rest_path = path
    return walk(rest_path, structure[key])


def test_walk():
    assert walk([0], 'Cat') == 'C'
    assert walk(['a', 1], {'a': ('foo', 'bar')}) == 'bar'
    assert walk(['x', 1, 0], {'x': ('foo', 'bar')}) == 'b'


def test_suppress():
    @suppress(ZeroDivisionError, or_return=0)
    def safe_div(a, *, b):
        return a // b

    assert safe_div(10, b=3) == 3
    assert safe_div(10, b=0) == 0


def test_suppress_walk():
    safe_walk = suppress((KeyError, IndexError))(walk)

    assert safe_walk([1], "") is None
    assert safe_walk(['a'], {}) is None
    assert safe_walk([0, 0, 1], (("?", 100), 200)) is None



def main():
    # test_counter()
    # test_clock()
    # test_counter2()
    # test_limitedcounter()

    # walk(path, structure)
    test_walk()
    test_suppress()
    test_suppress_walk()


if __name__ == '__main__':
    main()