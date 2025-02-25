def flip(arr, i):
    """
    Flip the sublist from index 0 to i, reversing the order of elements.

    Args:
        arr (list): The list of elements.
        i (int): The index until which the list needs to be flipped.

    Returns:
        list: The flipped list.
    """
    return arr[:i+1][::-1] + arr[i+1:]

def pancake_sort(arr):
    """
    Pancake Sort is a comparison-based sorting algorithm that works by repeatedly 
    flipping the largest unsorted element to its correct position using a flip 
    operation, which reverses a sublist of the array.

    Time Complexity:
        - Worst Case: O(n^2) as each flip potentially involves scanning the entire list.
        - Best Case: O(n) if the array is already sorted, but it still requires the flips.

    Space Complexity:
        O(1) as it performs in-place sorting without using extra space.

    Args:
        arr (list): A list of elements to be sorted. The elements should be 
                    comparable (i.e., they should support comparison operators).

    Returns:
        list: The sorted list in ascending order.

    Key Features:
        - It is an in-place algorithm.
        - Simple to implement but inefficient for large datasets.
        - Interesting algorithm for educational purposes.

    More Information:
        https://en.wikipedia.org/wiki/Pancake_sort
    """
    n = len(arr)
    for i in range(n-1, 0, -1):
        # Find the index of the largest element in the unsorted part
        max_index = arr.index(max(arr[:i+1]))
        
        if max_index == i:
            continue  # Element is already in the correct position
        
        # Flip the largest element to the front (if it's not already there)
        if max_index != 0:
            arr = flip(arr, max_index)
        
        # Flip it to its correct position
        arr = flip(arr, i)
        
    return arr
