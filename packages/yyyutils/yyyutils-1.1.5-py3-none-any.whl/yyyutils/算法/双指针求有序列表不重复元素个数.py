"""
利用快慢指针，慢指针指向所有不重复数字的最后一个
"""


def count_unique(arr):
    slow, fast = 0, 1
    while fast < len(arr):
        if arr[fast] != arr[slow]:
            arr[slow + 1] = arr[fast]
            slow += 1
        fast += 1
    print(arr[:slow + 1])
    return slow + 1


if __name__ == '__main__':
    arr = [1, 2, 3, 3, 4, 5, 5, 5, 6, 7, 8, 9]
    print(count_unique(arr))
