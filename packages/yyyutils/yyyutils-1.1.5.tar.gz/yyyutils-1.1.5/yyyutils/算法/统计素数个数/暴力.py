from yyyutils.decorator_utils import DecoratorUtils


@DecoratorUtils.run_time
def count_primes(n):
    count = 0
    for i in range(2, n + 1):
        count += 1 if is_prime(i) else 0
    return count


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


if __name__ == '__main__':
    print(count_primes(1000000))
