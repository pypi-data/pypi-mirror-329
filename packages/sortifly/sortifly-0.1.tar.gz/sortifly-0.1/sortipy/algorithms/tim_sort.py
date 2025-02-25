def tim_sort(arr):
    """
    TimSort is a hybrid sorting algorithm derived from Merge Sort and Insertion Sort. 
    It is optimized for real-world data and is used as the default sorting algorithm 
    in Python, Java, and other languages.

    Time Complexity:
        - Best Case: O(n) when the array is already sorted.
        - Average Case: O(n log n)
        - Worst Case: O(n log n)

    Space Complexity:
        O(n) due to temporary storage required for merging.

    Args:
        arr (list): A list of elements to be sorted.

    Returns:
        list: The sorted list.

    Key Features:
        - Efficient on nearly sorted or small datasets due to adaptive merging.
        - Uses a "minrun" threshold to split the list into smaller chunks for efficient sorting.

    Built-in Implementation:
        Python’s built-in `sorted()` and `list.sort()` use TimSort by default.

    More Information:
        https://en.wikipedia.org/wiki/Timsort
    """

    return sorted(arr)  # Python's built-in TimSort
