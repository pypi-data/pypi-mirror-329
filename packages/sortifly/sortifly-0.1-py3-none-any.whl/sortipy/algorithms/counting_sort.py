def counting_sort(arr):
    """
    Counting Sort is a non-comparison-based sorting algorithm that sorts an array by 
    counting the occurrences of each unique element and placing them in the correct position.

    Time Complexity:
        Best, Average, and Worst Case: O(n + k) where n is the number of elements 
        and k is the range of input values.

    Space Complexity:
        O(k) due to the additional counting array.

    Args:
        arr (list): A list of non-negative integers to be sorted.

    Returns:
        list: The sorted list.

    Limitations:
        - Works only for non-negative integers.
        - Not suitable for large number ranges due to high space complexity.

    More Information:
        For further reading on Counting Sort, visit:
        https://en.wikipedia.org/wiki/Counting_sort
    """

    if not arr:
        return arr  # Return empty array if input is empty

    # Find the maximum value to determine the range of the count array
    max_val = max(arr)

    # Initialize count array with zeros
    count = [0] * (max_val + 1)

    # Count occurrences of each element
    for num in arr:
        count[num] += 1

    # Reconstruct the sorted array
    sorted_arr = []
    for i in range(len(count)):
        sorted_arr.extend([i] * count[i])  # Append the value 'i', 'count[i]' times

    return sorted_arr
