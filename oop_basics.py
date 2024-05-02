class Counter:
    value = 0
    def inc(self, delta=1):
        self.value += delta
    
    def dec(self, delta=1):
        self.value -= delta


def main():
    c = Counter()
    c.inc()
    c.inc()
    c.inc(40)
    c.value  # 42
    c.dec()
    c.dec(30)
    c.value  # 11
    c.dec(delta=100)
    c.value  # 0


if __name__ == '__main__':
    main()