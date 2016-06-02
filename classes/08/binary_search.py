"""You're going to write a binary search function.
You should use an iterative approach - meaning
using loops.
Your function should take two inputs:
a Python list to search through, and the value
you're searching for.
Assume the list only has distinct elements,
meaning there are no repeated values, and 
elements are in a strictly increasing order.
Return the index of value, or -1 if the value
doesn't exist in the list."""

def binary_search(input_array, value):
    """Your code goes here."""
    li = 0
    ri = len(input_array) - 1
    while (li <= ri) and (li >= 0) and (ri >= 0):
        mi = li + (ri - li) / 2
        if value == input_array[mi]:
            return mi
        if value < input_array[mi]:
            # search in left part
            ri = mi - 1
        else:
            # search in right part
            li = mi + 1
    return -1

test_list = [1,3,9,11,15,19,29]
test_val1 = 25
test_val2 = 15
print binary_search(test_list, test_val1)
print binary_search(test_list, test_val2)
