import math


def find_center_index(arr):
    if not isinstance(arr, list):
        raiser = TypeError("arr must be a list")
        raise raiser
    if len(arr) == 1:
        return 0
    sum = math.fsum(arr)
    total = 0
    for i in range(len(arr)):
        total += arr[i]
        sum -= arr[i]
        if total == sum:
            return i
        if total > sum:
            if total - sum == arr[i]:
                return i
            return -1
    return -1


if __name__ == '__main__':
    arr = [5, 6, 1, 7, 3]
    print(find_center_index(arr))
