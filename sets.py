

def get_unique(*args):
    s = set()
    [s.update(arg) for arg in args]
    return list(s)


# BEGIN
def get_unique(*args):
    result = set()
    for data in args:
        result |= set(data)
    return [*result]
# END


