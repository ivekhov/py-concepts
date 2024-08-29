def reverse(string):
    """Reverse string

    >>> reverse('')
    ''

    >>> reverse('Hexlet')
    'telxeH'

    >>> reverse('QWERTY')
    'YTREWQ'
    """

    return string[::-1]

# Нужно для запуска тестов
if __name__ == "__main__":
    import doctest
    doctest.testmod()


def invert_case():
    pass
