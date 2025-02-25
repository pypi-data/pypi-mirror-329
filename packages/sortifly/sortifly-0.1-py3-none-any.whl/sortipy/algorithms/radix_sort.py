def counting_sort_for_radix(arr, exp):
    """
    A modified Counting Sort used as a subroutine in Radix Sort.
    It sorts elements based on the current digit represented by `exp`.

    Args:
        arr (list): The list of integers to be sorted.
        exp (int): The exponent representing the current digit place (1s, 10s, 100s, etc.).

    Returns:
        list: A partially sorted list based on the current digit.
    """
    n = len(arr)
    output = [0] * n  # Output array
    count = [0] * 10  # Count array for digits (0-9)

    # Count occurrences of each digit at the current place
    for num in arr:
        index = (num // exp) % 10
        count[index] += 1

    # Modify count[i] to store the actual position of the digit in output[]
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array by placing numbers in the correct position
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    # Copy the sorted values back to the original array
    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr):
    """
    Radix Sort is a non-comparative sorting algorithm that sorts numbers by processing 
    individual digits from least significant to most significant using Counting Sort.

    Time Complexity:
        Best, Average, and Worst Case: O(nk), where n is the number of elements, 
        and k is the number of digits in the largest number.

    Space Complexity:
        O(n + k) due to the auxiliary output array and counting array.

    Args:
        arr (list): A list of non-negative integers to be sorted.

    Returns:
        list: The sorted list.

    Limitations:
        - Only works with non-negative integers.
        - Inefficient for very large numbers with many digits.

    More Information:
        For further reading on Radix Sort, visit:
        https://en.wikipedia.org/wiki/Radix_sort
    """

    if not arr:
        return arr  # Return empty array if input is empty

    # Find the maximum number to determine the number of digits
    max_val = max(arr)
    exp = 1  # Represents the digit place (1s, 10s, 100s, ...)

    # Apply counting sort for each digit place (1s, 10s, 100s, etc.)
    while max_val // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10  # Move to the next digit place

    return arr
