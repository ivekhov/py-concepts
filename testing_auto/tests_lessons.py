"""
def test_cart():
    cart = make_cart()
    assert not len(cart.get_items())

    cart.add_item({'name': 'car', 'price': 3}, 5)
    assert len(cart.get_items()) == 1
    assert cart.get_cost() == 15
    assert cart.get_count() == 5

    cart.add_item({'name': 'house', 'price': 10}, 2)
    assert len(cart.get_items()) == 2
    assert cart.get_cost() == 35
    assert cart.get_count() == 7
"""

"""
function 

# BEGIN
def fill(coll, value, begin=0, end=None):
    if end is None:
        end = len(coll)
    chunk = [value for _ in coll[begin:end]]
    coll[begin:end] = chunk
# END
"""

"""
tests


# BEGIN
def test_fill_default(collection, fill):
    fill(collection, '*')
    assert collection == ['*', '*', '*', '*']


def test_fill_start_ge_length(collection, fill):
    fill(collection, '*', 10, 12)
    assert collection == [1, 2, 3, 4]


def test_fill_start_ge_end(collection, fill):
    fill(collection, '*', 2, 2)
    assert collection == [1, 2, 3, 4]


def test_fill_end_ge_length(collection, fill):
    fill(collection, '*', 0, 10)
    assert collection == ['*', '*', '*', '*']
# END
"""
