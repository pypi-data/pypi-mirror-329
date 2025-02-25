def bucket_sort(arr, bucket_size=5):
    """
    Bucket Sort is a distribution-based sorting algorithm that divides elements into buckets,
    sorts each bucket individually, and then merges them back into a sorted array.

    Time Complexity:
        - Best Case: O(n + k), where n is the number of elements and k is the number of buckets.
        - Average Case: O(n + n²/k + k)
        - Worst Case: O(n²) if all elements end up in the same bucket and a bad sorting method is used.

    Space Complexity:
        O(n + k) due to the extra space needed for buckets.

    Args:
        arr (list): A list of numerical values to be sorted.
        bucket_size (int): The maximum number of elements per bucket. Default is 5.

    Returns:
        list: The sorted list.

    Limitations:
        - Works best when input is uniformly distributed over a range.
        - Not efficient for small datasets compared to comparison-based sorting.

    More Information:
        For further reading on Bucket Sort, visit:
        https://en.wikipedia.org/wiki/Bucket_sort
    """

    if not arr:
        return arr  # Return empty list if input is empty

    # Find the minimum and maximum values
    min_val, max_val = min(arr), max(arr)

    # Compute the number of buckets needed
    bucket_count = (max_val - min_val) // bucket_size + 1
    buckets = [[] for _ in range(bucket_count)]

    # Distribute the elements into their respective buckets
    for num in arr:
        index = (num - min_val) // bucket_size
        buckets[index].append(num)

    # Sort each bucket and concatenate the results
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(sorted(bucket))  # Using Python's built-in Timsort

    return sorted_arr
