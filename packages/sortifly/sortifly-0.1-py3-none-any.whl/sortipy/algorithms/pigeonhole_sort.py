def pigeonhole_sort(arr):
    """
    Pigeonhole Sort is an integer sorting algorithm that works best when the number 
    of elements and the range of values are close. It places each element into a 
    "pigeonhole" (bucket) corresponding to its value and then reconstructs the sorted array.

    Time Complexity:
        - Best Case: O(n) when elements are uniformly distributed.
        - Worst Case: O(n + range) where "range" is the difference between max and min values.

    Space Complexity:
        O(range) due to the use of extra memory for pigeonholes.

    Args:
        arr (list): A list of integers to be sorted.

    Returns:
        list: The sorted list.

    Key Features:
        - Efficient when the range of numbers is small relative to the number of elements.
        - Uses additional memory proportional to the range of input values.

    More Information:
        https://en.wikipedia.org/wiki/Pigeonhole_sort
    """

    if not arr:
        return arr

    # Find the minimum and maximum values
    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1  # Number of pigeonholes

    # Create pigeonholes (empty buckets)
    pigeonholes = [[] for _ in range(size)]

    # Place each element in its respective pigeonhole
    for num in arr:
        pigeonholes[num - min_val].append(num)

    # Flatten the pigeonholes into a sorted array
    sorted_arr = []
    for hole in pigeonholes:
        sorted_arr.extend(hole)

    return sorted_arr
