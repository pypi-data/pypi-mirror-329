def insertion_sort(arr):
    """
    The insertion sort algorithm builds the sorted list one element at a time.
    It takes each element from the unsorted portion and inserts it into its correct 
    position in the sorted portion of the list.

    For more information, visit:
    - GeeksforGeeks: https://www.geeksforgeeks.org/insertion-sort/
    - Wikipedia: https://en.wikipedia.org/wiki/Insertion_sort
    
    Time Complexity:
        Best Case: O(n) when the list is already sorted.
        Average and Worst Case: O(n²) due to the nested loops for comparisons and shifts.
    
    Space Complexity:
        O(1) as the sorting is done in-place, without using extra space.
    
    Args:
        arr (list): A list of elements to be sorted. The elements should be 
                    comparable (i.e., they should support comparison operators).
    
    Returns:
        arr (list): The sorted list.
    """
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Move all elements that are greater than the current element (key) one position to the right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        # Insert the key at its correct position
        arr[j + 1] = key

    return arr
