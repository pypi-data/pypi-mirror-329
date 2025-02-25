def bubble_sort(arr): 
    """    
    The bubble sort algorithm works by repeatedly stepping through the list,
    comparing adjacent elements, and swapping them if they are in the wrong order.
    The pass through the list is repeated until the list is sorted.
    
    Time Complexity:
        Best Case: O(n) when the list is already sorted (optimized with `swapped` flag).
        Average and Worst Case: O(n²) due to the nested loops.

    Space Complexity:
        O(1) as the sorting is done in-place, without using extra space.
    
    Args:
        arr (list): A list of elements to be sorted. The elements should be 
                    comparable (i.e., they should support comparison operators).
    
    Returns:
        list (sorted)
    """

    n = len(arr)  # Define n to store the length of the array
    for i in range(n):
        # Flag to track if any elements were swapped
        swapped = False
        # Last i elements are already sorted, so no need to check them
        for j in range(0, n-i-1):
            # If the current element > next element, swap
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        
        # If no elements were swapped, the list is already sorted
        if not swapped:
            break

    return arr
