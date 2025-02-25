class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


def main():
    # 建立循环链表
    n, k = map(int, input().split())
    head = Node(1)
    cur = head
    for i in range(2, n + 1):
        node = Node(i)
        cur.next = node
        cur = node
    cur.next = head

    # 约瑟夫问题
    while n
