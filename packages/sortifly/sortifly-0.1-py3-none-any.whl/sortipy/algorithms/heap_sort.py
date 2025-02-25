def heap_sort(arr):
    """
    Heap Sort is a comparison-based sorting algorithm that uses a binary heap data structure 
    to build a max heap and repeatedly extract the maximum element to sort the array.

    Time Complexity:
        Best, Average, and Worst Case: O(n log n) due to heap construction and repeated removal of elements.

    Space Complexity:
        O(1) as it sorts the array in-place.

    Args:
        arr (list): A list of elements to be sorted. The elements should be 
                    comparable (i.e., they should support comparison operators).

    Returns:
        list: The sorted list.

    More Information:
        For further reading on Heap Sort, visit:
        https://en.wikipedia.org/wiki/Heapsort
    """

    def heapify(arr, n, i):
        """Maintains the max heap property by ensuring the largest element is at the root."""
        largest = i  # Assume root is the largest
        left = 2 * i + 1  # Left child index
        right = 2 * i + 2  # Right child index

        # Check if left child is larger than root
        if left < n and arr[left] > arr[largest]:
            largest = left

        # Check if right child is larger than the current largest
        if right < n and arr[right] > arr[largest]:
            largest = right

        # If the largest is not root, swap and continue heapifying
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)  # Recursively heapify the affected subtree

    n = len(arr)

    # Build a max heap (rearrange the array)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Move current root (max) to the end
        heapify(arr, i, 0)  # Restore heap property for the reduced heap

    return arr
