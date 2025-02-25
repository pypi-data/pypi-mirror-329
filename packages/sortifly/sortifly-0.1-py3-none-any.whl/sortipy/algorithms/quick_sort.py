def quick_sort(arr):
    """
    Quick Sort is a divide-and-conquer sorting algorithm that selects a pivot element, 
    partitions the list into elements smaller and greater than the pivot, and recursively 
    sorts the partitions.

    Time Complexity:
        Best and Average Case: O(n log n) due to recursive partitioning.
        Worst Case: O(n²) when the smallest or largest element is always chosen as the pivot.

    Space Complexity:
        O(log n) for recursive stack calls in the average case.
        O(n) in the worst case (when recursion depth is maximal).

    Args:
        arr (list): A list of elements to be sorted. The elements should be 
                    comparable (i.e., they should support comparison operators).

    Returns:
        list: The sorted list.

    More Information:
        For further reading on Quick Sort, visit:
        https://en.wikipedia.org/wiki/Quicksort
    """

    if len(arr) <= 1:
        return arr  # A list with one or zero elements is already sorted

    pivot = arr[len(arr) // 2]  # Choose middle element as pivot
    left = [x for x in arr if x < pivot]  # Elements smaller than pivot
    middle = [x for x in arr if x == pivot]  # Elements equal to pivot
    right = [x for x in arr if x > pivot]  # Elements greater than pivot

    return quick_sort(left) + middle + quick_sort(right)  # Recursively sort and combine
