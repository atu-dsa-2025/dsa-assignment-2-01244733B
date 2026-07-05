# BCP 210: Data Structures and Algorithms I
# Coursework Assignment 2 — Part B: Arrays and the Two-Pointer Technique
# Academic Year 2025/2026
#
# Instructions:
#   - Implement all functions marked TODO.
#   - Do NOT change function signatures or the test harness below.
#   - You may only use standard Python built-in types.
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
        arr    (list): A sorted list of integers.
        target (int):  The value to search for.

    Returns:
        int: The index of target in arr, or -1 if not found.

    Complexity analysis (fill these in):
        Best-case time complexity:  O(1)  -- target is exactly at the middle index on the first check.
        Worst-case time complexity: O(log N)  -- target is missing or at the extremes, causing the algorithm to divide the list repeatedly until empty.
    """
    low = 0
    high = len(arr) - 1
    
    while low <= high:
        middle_idx = (low + high) // 2
        
        if arr[middle_idx] == target:
            return middle_idx
        elif arr[middle_idx] < target:
            low = middle_idx + 1
        else:
            high = middle_idx - 1
            
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
        arr    (list): A sorted list of integers.
        target (int):  The desired sum.

    Returns:
        tuple: (left_value, right_value) if a pair exists, otherwise None.

    Complexity:
        Time: O(N)
        Space: O(1)
    """
    start = 0
    end = len(arr) - 1
    
    while start < end:
        total_sum = arr[start] + arr[end]
        
        if total_sum == target:
            return (arr[start], arr[end])
        elif total_sum < target:
            start += 1  # Sum is too low, move left pointer rightwards
        else:
            end -= 1    # Sum is too high, move right pointer leftwards
            
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
        k   (int):  Number of positions to rotate right.

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
        
    # Helper function to flip a portion of the array
    def flip_segment(idx1, idx2):
        while idx1 < idx2:
            # Perform the swap
            arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
            idx1 += 1
            idx2 -= 1
            
    # Flip everything
    flip_segment(0, n - 1)
    # Flip the first k items
    flip_segment(0, k - 1)
    # Flip the remaining items
    flip_segment(k, n - 1)


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

    1. When a Python list runs out of its pre-allocated capacity, it creates a new, larger array under the hood (usually doubling its size) and transfers all the existing items over to it.
    2. A single append can cost O(N) worst-case time because copying N existing elements into the newly allocated block of memory requires looping through all of them.
    3. The amortised cost is still O(1) because this expensive reallocation event is very rare. Since the list doubles its size, the next N appends will be fast O(1) inserts, meaning the heavy O(N) cost averages out to a constant time per operation over the long run.
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
        (catalogue, -8,  0),    # leftmost element
        (catalogue, 21,  9),    # rightmost element
        (catalogue,  6,  5),    # middle element
        (catalogue, 99, -1),    # not present
        (catalogue,  0,  2),    # zero value
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
    b2_tests = [
        (catalogue, 13,  (-8, 21)),   # expected pair
        (catalogue,  0,  (-8,  8) if False else None),  # placeholder; test actual answer
        (catalogue, -11, (-8, -3)),   # negative target
        (catalogue, 999, None),       # no pair
    ]
    # Run only the first (required) demonstration
    pair = find_pair_with_sum(catalogue, 13)
    print(f"  find_pair_with_sum(catalogue, 13) = {pair}")
    if pair is not None and sum(pair) == 13:
        print("  PASS: pair sums to 13")
    else:
        print("  FAIL: pair does not sum to 13 or is None")

    no_pair = find_pair_with_sum(catalogue, 999)
    print(f"  find_pair_with_sum(catalogue, 999) = {no_pair}  "
          f"[{'PASS' if no_pair is None else 'FAIL'}]")

    # B3 — Rotation tests
    print("\n--- B3: In-Place Array Rotation ---")
    b3_tests = [
        ([1, 2, 3, 4, 5], 2, [4, 5, 1, 2, 3]),
        ([1, 2, 3, 4, 5], 5, [1, 2, 3, 4, 5]),   # full rotation = no change
        ([1, 2, 3, 4, 5], 7, [4, 5, 1, 2, 3]),   # k > len
        ([42],             1, [42]),               # single element
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
