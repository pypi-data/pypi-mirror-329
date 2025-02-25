def flash_sort(arr):
    """
    Flashsort is a distribution-based sorting algorithm that performs faster than
    comparison-based algorithms like quicksort or mergesort in certain scenarios.
    It works by grouping elements into buckets based on their range and then 
    sorting these groups. The final sorting step uses a traditional sorting method.

    Time Complexity:
        - Worst Case: O(n^2) (similar to quicksort in the worst case).
        - Best Case: O(n) for nearly sorted or uniformly distributed data.

    Space Complexity:
        O(n) due to the additional space used for creating the buckets.

    Args:
        arr (list): A list of elements to be sorted. The elements should be 
                    comparable (i.e., they should support comparison operators).

    Returns:
        list: The sorted list in ascending order.

    Key Features:
        - Highly efficient for large datasets with uniform distribution.
        - Involves creating buckets and using a quick sort on them.
        - Suitable when there are uniform distribution and specific range of elements.

    More Information:
        https://en.wikipedia.org/wiki/Flashsort
    """
    n = len(arr)
    if n <= 1:
        return arr

    # Find the minimum and maximum values in the array
    min_val = min(arr)
    max_val = max(arr)

    # Initialize the buckets
    m = int(0.25 * n)  # The number of buckets
    if m == 0:
        m = 1
    bucket = [[] for _ in range(m)]

    # Step 1: Distribute the elements into buckets based on their range
    for i in range(n):
        index = int((arr[i] - min_val) / (max_val - min_val) * (m - 1))
        bucket[index].append(arr[i])

    # Step 2: Sort each bucket using another sorting method (e.g., insertion sort)
    sorted_arr = []
    for i in range(m):
        if len(bucket[i]) > 0:
            bucket[i].sort()  # Insertion sort could be used here for small groups
            sorted_arr.extend(bucket[i])

    return sorted_arr
