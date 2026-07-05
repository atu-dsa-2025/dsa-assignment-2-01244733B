# BCP 210: Data Structures and Algorithms I
# Coursework Assignment 2 — Part E: Bonus Challenge
# Academic Year 2025/2026
#
# This part is OPTIONAL but can earn up to 10 bonus marks.
#
# Instructions:
# - Implement all TODO sections.
# - Do NOT change function signatures.
# - No external libraries permitted.
# ============================================================================

# ============================================================================
# SAMPLE DATA — provided, do not modify
# ============================================================================

sessions = [
    ('R1', 8, 10),   # index 0
    ('R1', 9, 11),   # index 1 -- conflicts with index 0
    ('R1', 11, 13),  # index 2 -- no conflict with index 1
    ('R2', 8, 12),   # index 3
    ('R2', 10, 14),  # index 4 -- conflicts with index 3
]

# ============================================================================
# E1 (4 Marks)
# Build a conflict map: for each room_id, find ALL pairs of session indices
# that conflict within that room.
#
# Two sessions i and j (i < j) conflict if:
#   sessions[j][start] < sessions[i][end]
# i.e. the later session starts before the earlier one ends.
#
# Expected output for sample data:
# {'R1': [(0, 1)], 'R2': [(3, 4)]}
# ============================================================================

def build_conflict_map(sessions):
    """
    Find all conflicting session pairs grouped by room.

    Args:
        sessions (list[tuple]): List of (room_id, start_time, end_time).

    Returns:
        dict: Mapping room_id -> list of (index_i, index_j) conflict pairs.

    Time complexity: O(N^2)
    Space complexity: O(N)
    """
    from collections import defaultdict

    conflict_map = defaultdict(list)
    # Ensure every room that appears in the input is present in the output,
    # even if it ends up with no conflicts (an empty list).
    for room_id, _, _ in sessions:
        if room_id not in conflict_map:
            conflict_map[room_id] = []

    for i in range(len(sessions)):
        room_i, start_i, end_i = sessions[i]
        for j in range(i + 1, len(sessions)):
            room_j, start_j, _ = sessions[j]
            if room_i == room_j and start_j < end_i:
                conflict_map[room_i].append((i, j))

    return dict(conflict_map)

# ============================================================================
# E2 (3 Marks)
# Using a Stack, detect the FIRST conflicting pair in a single room's sessions.
# Sessions are provided as a list of (index, start_time, end_time) tuples,
# already sorted by start_time.
#
# Return the first conflicting pair (index_i, index_j), or None if no conflict.
# ============================================================================

def detect_first_conflict(room_sessions):
    """
    Process sessions for one room in order and find the first conflict using a Stack.

    A conflict occurs when the next session's start_time is less than the
    end_time of the most recently pushed (active) session on the stack.

    Args:
        room_sessions (list[tuple]): List of (original_index, start, end),
                                     sorted by start time.

    Returns:
        tuple | None: (index_i, index_j) of the first conflict, or None.

    How the Stack is used: Active (not-yet-ended) sessions are kept on the
    stack. Before processing each new session, any sessions on top of the
    stack that have already ended (end_time <= current start_time) are
    popped off, since they can no longer conflict. If a session remains on
    top of the stack and its end_time is greater than the current session's
    start_time, the two overlap -- that's the first conflict found.
    """
    stack = []
    for idx, start, end in room_sessions:
        while stack and stack[-1][2] <= start:
            stack.pop()

        if stack and start < stack[-1][2]:
            prev_idx = stack[-1][0]
            return (min(prev_idx, idx), max(prev_idx, idx))

        stack.append((idx, start, end))

    return None

# ============================================================================
# E3 (3 Marks) — Written question
# Analyse the complexity of your E1 solution.
# Discuss whether sorting + linear scan or a BST would improve performance.
# ============================================================================

def e3_analysis():
    """
    Write your analysis here covering:
      1. The time and space complexity of your E1 solution.
      2. How sorting sessions per room + a single linear scan changes the complexity.
      3. Whether a BST keyed on start_time would offer any advantage over sorting.
    """
    return """
    E1 complexity analysis:
        The solution compares every pair of sessions (i, j) with i < j,
        giving O(N^2) comparisons overall in the worst case (e.g. all
        sessions in one room). Space is O(N) for storing the conflict map
        entries in the worst case.
        Overall: Time O(N^2), Space O(N)

    Improvement via sort + linear scan:
        If we group sessions by room (O(N)) and then sort each room's
        sessions by start_time (O(M log M) per room, where M is sessions in
        that room), a single linear/stack-based sweep (as in E2) can then
        detect overlaps in O(M) per room. Summed across rooms this gives an
        overall O(N log N) solution instead of O(N^2) -- a significant
        improvement for large N.

    BST vs sorted array for conflict detection:
        A BST keyed on start_time could support similar ordered traversal and
        range queries in O(log N) per operation, but building and balancing
        a BST carries extra overhead (node objects, pointer rebalancing) for
        no real benefit here, since we only need one static, ordered pass
        over each room's sessions. A simple sort followed by a linear scan is
        simpler to implement, has lower constant factors, and achieves the
        same asymptotic complexity, so it is the more practical choice for
        this use case.
    """

# ============================================================================
# TEST HARNESS — do not modify
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Part E: Bonus Challenge -- Exam Invigilation Scheduler")
    print("=" * 60)

    # E1 — build conflict map
    print("\n--- E1: build_conflict_map ---")
    conflict_map = build_conflict_map(sessions)
    print(f"  Result: {conflict_map}")
    expected_map = {'R1': [(0, 1)], 'R2': [(3, 4)]}
    print(f"  Expected: {expected_map}")
    print(f"  PASS: {conflict_map == expected_map}")

    # E1 — edge case: no conflicts
    no_conflict_sessions = [
        ('R3', 8, 9), ('R3', 9, 10), ('R3', 10, 11)
    ]
    nc_map = build_conflict_map(no_conflict_sessions)
    print(f"\n  No-conflict sessions result: {nc_map}")
    print(f"  Expected: {{'R3': []}}")
    print(f"  PASS: {nc_map == {'R3': []}}")

    # E2 — detect first conflict using a stack
    print("\n--- E2: detect_first_conflict ---")
    r1_sessions = [(0, 8, 10), (1, 9, 11), (2, 11, 13)]
    first_conflict = detect_first_conflict(r1_sessions)
    print(f"  R1 first conflict: {first_conflict}  [Expected: (0, 1)]")
    print(f"  PASS: {first_conflict == (0, 1)}")

    r3_sessions = [(0, 8, 9), (1, 9, 10), (2, 10, 11)]
    no_conflict = detect_first_conflict(r3_sessions)
    print(f"  R3 first conflict: {no_conflict}  [Expected: None]")
    print(f"  PASS: {no_conflict is None}")

    # E3 — written analysis
    print("\n--- E3: Complexity Analysis ---")
    print(e3_analysis())
