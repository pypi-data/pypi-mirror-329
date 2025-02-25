def shell_sort(arr):
    """
    Shell Sort is an optimization of Insertion Sort that allows the exchange of items 
    that are far apart. It works by sorting elements at a specific interval (gap) and 
    gradually reducing the gap until it becomes 1.

    Time Complexity:
        - Best Case: O(n log n) when using optimal gap sequences.
        - Average Case: O(n^(3/2)) depending on the gap sequence.
        - Worst Case: O(n²) in some implementations.

    Space Complexity:
        O(1) since sorting is done in-place.

    Args:
        arr (list): A list of elements to be sorted.

    Returns:
        list: The sorted list.

    Key Features:
        - Improves Insertion Sort by reducing the number of swaps.
        - Uses different gap sequences (e.g., Knuth’s sequence) for better efficiency.

    More Information:
        https://en.wikipedia.org/wiki/Shellsort
    """

    n = len(arr)
    gap = n // 2  # Start with a large gap, then reduce it

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            # Shift earlier elements in the sorted sequence to make room for arr[i]
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp  # Insert temp at its correct position
        gap //= 2  # Reduce the gap

    return arr
