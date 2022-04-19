
import sorting
import timeit

from typing import List

array_type = List[int]


def timing_wrapper(sorting_function: callable, array: array_type):
    print(f'Algorithm: {sorting_function.__name__} - ' +
          f'Time Taken: {timeit.timeit(str(sorting_function(array)), number=1_000_000)} - ' +
          f'Sorted output: {array}\n')


if __name__ == '__main__':
    array = [9, 8, 5, 3, 2, 1]

    timing_wrapper(sorting.merge_sort, array)
    timing_wrapper(sorted, array)
