from typing import List

array_type = List[int]


def merge_sort(array: array_type) -> array_type:
    if len(array) > 1:
        midPoint = len(array)//2

        leftArray = merge_sort(array[:midPoint])
        rightArray = merge_sort(array[midPoint:])

        leftCounter = 0
        rightCounter = 0
        arrayCounter = 0

        while leftCounter < len(leftArray) and rightCounter < len(rightArray):
            if leftArray[leftCounter] < rightArray[rightCounter]:
                array[arrayCounter] = leftArray[leftCounter]
                leftCounter += 1
            else:
                array[arrayCounter] = rightArray[rightCounter]
                rightCounter += 1
            arrayCounter += 1

        while leftCounter < len(leftArray):
            array[arrayCounter] = leftArray[leftCounter]
            leftCounter += 1
            arrayCounter += 1

        while rightCounter < len(rightArray):
            array[arrayCounter] = rightArray[rightCounter]
            rightCounter += 1
            arrayCounter += 1

    return array
