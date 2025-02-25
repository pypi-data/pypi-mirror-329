def bitonic_sort(arr, low, cnt, dir):
    """
    Bitonic Sort is a comparison-based sorting algorithm that works by sorting 
    a sequence of elements in two phases: first, it forms a bitonic sequence 
    (a sequence that is first increasing and then decreasing), and then it sorts 
    the bitonic sequence into a fully sorted list.

    Time Complexity:
        - Best Case: O(n log² n) as the algorithm recursively splits the array and sorts.
        - Worst Case: O(n log² n) due to the divide-and-conquer approach.

    Space Complexity:
        O(log n) as the sorting is done in place (with recursive calls).

    Args:
        arr (list): A list of elements to be sorted.
        low (int): The starting index of the sublist to be sorted.
        cnt (int): The number of elements in the current sublist.
        dir (int): The direction in which the elements are to be sorted (1 for ascending, 0 for descending).
        
    Returns:
        list: The sorted list.
    
    Key Features:
        - Divide and conquer strategy.
        - Efficient for parallel computing because of its predictable comparison pattern.
        - Works best on hardware that supports parallel operations.

    More Information:
        https://en.wikipedia.org/wiki/Bitonic_sort
    """
    if cnt > 1:
        k = cnt // 2
        # Sort the first half in ascending order
        bitonic_sort(arr, low, k, 1)
        # Sort the second half in descending order
        bitonic_sort(arr, low + k, k, 0)
        # Merge the two halves into a sorted sequence
        bitonic_merge(arr, low, cnt, dir)

def bitonic_merge(arr, low, cnt, dir):
    """
    Merges two bitonic sequences into a single sorted sequence.
    """
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            if (arr[i] > arr[i + k]) == dir:
                arr[i], arr[i + k] = arr[i + k], arr[i]
        bitonic_merge(arr, low, k, dir)
        bitonic_merge(arr, low + k, k, dir)
    
def sort_bitonic(arr):
    """
    A wrapper function that sorts the entire array using the bitonic_sort function.
    """
    bitonic_sort(arr, 0, len(arr), 1)
    return arr
