import math


def is_prime(num):
    start = 2
    for step in range(start, math.ceil(num // 2) + 1):
        if num % step == 0:
            return False
    return True

def say_prime_or_not(num):
    if is_prime(num):
        print('yes')
    else:
        print('no')


# BEGIN
def is_prime2(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def say_prime_or_not2(num):
    answer = 'yes' if is_prime(num) else 'no'
    print(answer)
# END