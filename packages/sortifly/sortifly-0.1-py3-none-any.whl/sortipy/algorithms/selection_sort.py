def selection_sort(arr):
    """
    The selection sort algorithm works by repeatedly finding the minimum element from the unsorted portion 
    of the list and swapping it with the first unsorted element.

    Time Complexity:
        Best, Average, and Worst Case: O(n²) because it always requires comparing every element with the rest.

    Space Complexity:
        O(1) as the sorting is done in-place, without using extra space.

    Args:
        arr (list): A list of elements to be sorted. The elements should be 
                    comparable (i.e., they should support comparison operators).

    Returns:
        list: The sorted list.

    More Information:
        For further reading on Selection Sort, visit:
        https://en.wikipedia.org/wiki/Selection_sort
    """
    
    # Traverse through all elements in the list
    for i in range(len(arr)):
        # Find the index of the smallest element in the unsorted part of the list
        min_index = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        
        # Swap the found minimum element with the first element of the unsorted part
        arr[i], arr[min_index] = arr[min_index], arr[i]
    
    return arr
