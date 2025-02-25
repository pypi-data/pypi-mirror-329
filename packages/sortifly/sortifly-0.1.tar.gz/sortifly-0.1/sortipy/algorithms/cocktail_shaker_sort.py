def cocktail_shaker_sort(arr):
    """
    Cocktail Shaker Sort (also known as Bidirectional Bubble Sort) is a variation of 
    Bubble Sort that sorts in both directions on each pass through the list. This 
    reduces the number of swaps needed compared to regular Bubble Sort.

    Time Complexity:
        - Best Case: O(n) when the list is already sorted.
        - Average and Worst Case: O(n²) due to the nested loops.

    Space Complexity:
        O(1) since sorting is done in-place.

    Args:
        arr (list): A list of elements to be sorted.

    Returns:
        list: The sorted list.

    Key Features:
        - More efficient than Bubble Sort in some cases.
        - Moves large elements to the end and small elements to the beginning 
          in a single iteration.

    More Information:
        https://en.wikipedia.org/wiki/Cocktail_shaker_sort
    """

    n = len(arr)
    swapped = True
    start = 0
    end = n - 1

    while swapped:
        swapped = False

        # Forward pass (Bubble Sort from left to right)
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        # If no swaps happened, the list is sorted
        if not swapped:
            break

        # Reduce the endpoint since the largest element is at the correct position
        end -= 1

        swapped = False

        # Backward pass (Bubble Sort from right to left)
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

        # Increase the starting point since the smallest element is at the correct position
        start += 1

    return arr
