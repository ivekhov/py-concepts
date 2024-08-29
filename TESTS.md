## Doctest


```python

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

```

For missing rows chacking: 

```bash
poetry run pytest --cov-report term-missing --cov=FOLDER
```