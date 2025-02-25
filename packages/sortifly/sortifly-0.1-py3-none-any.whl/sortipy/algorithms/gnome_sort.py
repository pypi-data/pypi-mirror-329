def gnome_sort(arr):
    """
    Gnome Sort is a simple comparison-based sorting algorithm that works by comparing 
    adjacent elements and swapping them if they are in the wrong order. It behaves similarly 
    to an insertion sort but uses a different method of positioning elements.

    Time Complexity:
        - Best Case: O(n) when the list is already sorted.
        - Worst Case: O(n²) due to the nested loop behavior (similar to Bubble Sort).

    Space Complexity:
        O(1) as it sorts the list in place without using extra memory.

    Args:
        arr (list): A list of elements to be sorted. The elements should be 
                    comparable (i.e., they should support comparison operators).

    Returns:
        list: The sorted list.

    Key Features:
        - Simple and intuitive.
        - Comparable to insertion sort, but slightly less efficient.
        - In-place sorting (does not require extra memory).
    
    More Information:
        https://en.wikipedia.org/wiki/Gnome_sort
    """

    index = 0
    while index < len(arr):
        if index == 0 or arr[index - 1] <= arr[index]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr
