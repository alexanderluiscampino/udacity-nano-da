"""Implement quick sort in Python.
Input a list.
Output a sorted list."""


def quicksort(array):
    def swap(ai, bi):
        if ai == bi:
            return
        tmp = array[bi]
        array[bi] = array[ai]
        array[ai] = tmp

    def partition(l, r):
        pivot = array[r]
        i = l
        for j in range(l, r):
            if array[j] <= pivot:
                swap(i, j)
                i += 1
        swap(i, r)
        return i
    
    def qs(l, r):
        if l < r:
            pi = partition(l, r)
            qs(l, pi - 1)
            qs(pi + 1, r)

    qs(0, len(array) - 1)
    return array

test = [21, 4, 1, 3, 9, 20, 25, 6, 21, 14]
print quicksort(test)

