def sqrt(x):
    left, right = 0, x - 1
    while left <= right:
        mid = (left + right) // 2
        print([left, right, mid])
        if mid * mid <= x:
            left = mid + 1
        else:
            right = mid - 1
    return (left + right)//2


if __name__ == '__main__':
    print(sqrt(16))  # Output: 4
