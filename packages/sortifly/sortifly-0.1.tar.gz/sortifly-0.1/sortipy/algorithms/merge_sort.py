def merge_sort(arr):
    """
    Merge Sort is a divide-and-conquer sorting algorithm that splits the list into smaller sublists, 
    sorts them recursively, and then merges them back together in order.

    Time Complexity:
        Best, Average, and Worst Case: O(n log n) because the list is divided into halves (log n levels) 
        and each level requires O(n) operations to merge.

    Space Complexity:
        O(n) due to the additional space needed for merging sublists.

    Args:
        arr (list): A list of elements to be sorted. The elements should be 
                    comparable (i.e., they should support comparison operators).

    Returns:
        list: The sorted list.

    More Information:
        For further reading on Merge Sort, visit:
        https://en.wikipedia.org/wiki/Merge_sort
    """

    if len(arr) <= 1:
        return arr  # A list with one or zero elements is already sorted

    # Split the list into two halves
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    # Merge the sorted halves
    return merge(left_half, right_half)


def merge(left, right):
    """
    Helper function to merge two sorted lists into a single sorted list.
    """
    merged = []
    i = j = 0

    # Compare elements from both lists and merge them in order
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Add any remaining elements from both lists
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged
