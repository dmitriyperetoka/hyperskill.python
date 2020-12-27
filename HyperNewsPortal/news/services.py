def insertion_sort(array):
    for q in range(len(array)):
        w = q - 1
        key = array[q]

        while array[w]['link'] > key['link'] and w >= 0:
            array[w + 1] = array[w]
            w -= 1

        array[w + 1] = key


def binary_search(array, target):
    left, right = 0, len(array) - 1

    while left <= right:
        middle = (left + right) // 2

        if array[middle]['link'] == target:
            return middle
        elif array[middle]['link'] < target:
            right = middle - 1
        else:
            left = middle + 1

    return False
