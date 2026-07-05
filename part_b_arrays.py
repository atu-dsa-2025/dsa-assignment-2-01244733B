# BCP 210: Data Structures and Algorithms I
# Coursework Assignment 2 — Part B: Arrays and the Two-Pointer Technique
# Academic Year 2025/2026
#
# Instructions:
# - Implement all functions marked TODO.
# - Do NOT change function signatures or the test harness below.
# - You may only use standard Python built-in types.
# ============================================================================

# ============================================================================
# B1 (5 Marks)
# Implement binary search on a SORTED array.
# Must run in O(log N) time.
# Return the index of the target, or -1 if not found.
# After your implementation, write the best-case and worst-case complexities
# inside the docstring below.
# ============================================================================

def binary_search(arr, target):
    """
    Perform binary search on a sorted array.

    Args:
        arr (list): A sorted list of integers.
        target (int): The value to search for.

    Returns:
        int: The index of target in arr, or -1 if not found.

    Complexity analysis (fill these in):
        Best-case time complexity: O(1) -- target found at the first middle element
        Worst-case time complexity: O(log N) -- target absent, or search space
        must be halved all the way down to a single element
    """
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# ============================================================================
# B2 (6 Marks)
# Find two distinct values in a SORTED array that sum to target.
# Must use the two-pointer technique: O(N) time, O(1) space.
# Return the pair as a tuple (left_value, right_value) or None if not found.
#
# Demonstrate by finding a pair summing to 13 in the catalogue below.
# ============================================================================

catalogue = [-8, -3, 0, 1, 4, 6, 9, 12, 15, 21]


def find_pair_with_sum(arr, target):
    """
    Find two values in a sorted array that sum to target (two-pointer approach).

    Args:
        arr (list): A sorted list of integers.
        target (int): The desired sum.

    Returns:
        tuple: (left_value, right_value) if a pair exists, otherwise None.

    Complexity:
        Time: O(N)
        Space: O(1)
    """
    left, right = 0, len(arr) - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return (arr[left], arr[right])
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return None

# ============================================================================
# B3 (5 Marks)
# Rotate the array to the RIGHT by k positions IN-PLACE.
# Must run in O(N) time and O(1) space.
# Hint: use the triple-reversal technique.
#
# Example: rotate_array([1, 2, 3, 4, 5], 2) modifies the list to [4, 5, 1, 2, 3]
# ============================================================================

def rotate_array(arr, k):
    """
    Rotate a list to the right by k positions in-place.

    Args:
        arr (list): A list of integers (modified in-place).
        k (int): Number of positions to rotate right.

    Returns:
        None (modifies arr in place).

    Complexity:
        Time: O(N)
        Space: O(1)
    """
    n = len(arr)
    if n <= 1:
        return
    k = k % n
    if k == 0:
        return

    def reverse(left, right):
        while left < right:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1

    # Triple reversal
    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)

# ============================================================================
# B4 (4 Marks)
# Written question — no code required.
# Explain what amortised O(1) means for Python list append operations.
# Return your explanation as a string.
# ============================================================================

def b4_explanation():
    """
    Explain:
      1. What happens internally when a Python list runs out of capacity.
      2. Why a single append can cost O(N) in the worst case.
      3. Why the amortised cost per append is still considered O(1).
    """
    return """
    Explanation of amortised O(1) for Python list append:
    1. Python lists are backed by dynamic arrays with spare capacity. When the
       underlying array is full, a new, larger array (typically ~1.5-2x the
       old size) is allocated and every existing element is copied over.
    2. That particular append which triggers the resize therefore costs O(N),
       since it must copy all N existing elements into the new array.
    3. Because resizes happen at exponentially growing intervals (not every
       append), the total copying work across N appends sums to O(N) overall.
       Dividing that total cost by N appends gives an amortised cost of O(1)
       per append, even though occasional individual appends are O(N).
    """

# ============================================================================
# TEST HARNESS — do not modify
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Part B: Arrays and the Two-Pointer Technique")
    print("=" * 60)

    # B1 — Binary search tests
    print("\n--- B1: Binary Search ---")
    b1_tests = [
        (catalogue, -8, 0),   # leftmost element
        (catalogue, 21, 9),   # rightmost element
        (catalogue, 6, 5),    # middle element
        (catalogue, 99, -1),  # not present
        (catalogue, 0, 2),    # zero value
    ]
    b1_pass = True
    for arr, tgt, expected in b1_tests:
        result = binary_search(arr, tgt)
        status = "PASS" if result == expected else f"FAIL (got {result}, expected {expected})"
        print(f"  binary_search(catalogue, {tgt:3d}) = {str(result):4s}  [{status}]")
        if result != expected:
            b1_pass = False
    print(f"  All B1 tests passed: {b1_pass}")

    # B2 — Two-pointer pair tests
    print("\n--- B2: Two-Pointer Pair Sum ---")
    pair = find_pair_with_sum(catalogue, 13)
    print(f"  find_pair_with_sum(catalogue, 13) = {pair}")
    if pair is not None and sum(pair) == 13:
        print("  PASS: pair sums to 13")
    else:
        print("  FAIL: pair does not sum to 13 or is None")

    no_pair = find_pair_with_sum(catalogue, 999)
    print(f"  find_pair_with_sum(catalogue, 999) = {no_pair} "
          f"[{'PASS' if no_pair is None else 'FAIL'}]")

    # B3 — Rotation tests
    print("\n--- B3: In-Place Array Rotation ---")
    b3_tests = [
        ([1, 2, 3, 4, 5], 2, [4, 5, 1, 2, 3]),
        ([1, 2, 3, 4, 5], 5, [1, 2, 3, 4, 5]),  # full rotation = no change
        ([1, 2, 3, 4, 5], 7, [4, 5, 1, 2, 3]),  # k > len
        ([42], 1, [42]),                        # single element
    ]
    b3_pass = True
    for arr, k, expected in b3_tests:
        arr_copy = arr[:]
        rotate_array(arr_copy, k)
        status = "PASS" if arr_copy == expected else f"FAIL (got {arr_copy}, expected {expected})"
        print(f"  rotate({arr}, k={k}) -> {arr_copy}  [{status}]")
        if arr_copy != expected:
            b3_pass = False
    print(f"  All B3 tests passed: {b3_pass}")

    # B4 — Written explanation
    print("\n--- B4: Amortised O(1) Explanation ---")
    print(b4_explanation())
