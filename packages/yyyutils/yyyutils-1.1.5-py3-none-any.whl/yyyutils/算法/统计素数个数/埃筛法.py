"""
埃筛法的实质是为每个数指定一个标记位，每个素数找到其所有能合成的合数并标记，以减少遍历
TODO: 实现某个区间内的埃筛法
"""
from yyyutils.decorator_utils import DecoratorUtils


@DecoratorUtils.run_time
def sieve(n):
    """
    埃筛法
    :param n: 
    :return:
    """
    if n <= 1 or not isinstance(n, int):
        return 0
    is_prime = [True] * (n + 1)
    count = 0
    for i in range(2, n):
        if is_prime[i]:
            count += 1
            not_prime = i * i
            while not_prime < n:
                is_prime[not_prime] = False
                not_prime += i
    return count


if __name__ == "__main__":
    print(sieve(1000000))
