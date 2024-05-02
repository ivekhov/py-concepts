class Counter:
    def __init__(self, value=0):
        self.value = max(value, 0)
        value = max(value, 0)

    def inc(self, delta=1):
        return Counter(max((self.value + delta), 0))

    def dec(self, delta=1):
        # return Counter(self.value - delta) # prev version
        return self.inc(-delta) # cooler


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



def main():
    test_counter()


if __name__ == '__main__':
    main()