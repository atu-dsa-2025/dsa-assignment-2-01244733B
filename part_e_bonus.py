# BCP 210: Data Structures and Algorithms I
# Coursework Assignment 2 — Part E: Bonus Challenge
# Academic Year 2025/2026
#
# This part is OPTIONAL but can earn up to 10 bonus marks.
#
# Instructions:
#   - Implement all TODO sections.
#   - Do NOT change function signatures.
#   - No external libraries permitted.
# ============================================================================


# ============================================================================
# SAMPLE DATA — provided, do not modify
# ============================================================================

sessions = [
    ('R1', 8,  10),    # index 0
    ('R1', 9,  11),    # index 1 -- conflicts with index 0
    ('R1', 11, 13),    # index 2 -- no conflict with index 1
    ('R2', 8,  12),    # index 3
    ('R2', 10, 14),    # index 4 -- conflicts with index 3
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
#   {'R1': [(0, 1)], 'R2': [(3, 4)]}
# ============================================================================

def build_conflict_map(sessions):
    """
    Find all conflicting session pairs grouped by room.

    Args:
        sessions (list[tuple]): List of (room_id, start_time, end_time).

    Returns:
        dict: Mapping room_id -> list of (index_i, index_j) conflict pairs.

    Time complexity:  O(N + R * K^2) -- where N is total sessions, R is number of rooms, and K is the max sessions in a single room.
    Space complexity: O(N) -- to store the grouped indices and the resulting conflict map.
    """
    # Step 1: Group session indices by room_id using a dictionary.
    room_groups = {}
    for i, (room_id, start_time, end_time) in enumerate(sessions):
        if room_id not in room_groups:
            room_groups[room_id] = []
        room_groups[room_id].append(i)
        
    # Step 2: For each room, compare all pairs of sessions for conflicts.
    conflict_map = {}
    for room_id, indices in room_groups.items():
        conflicts = []
        # Compare every pair (i, j) where i < j
        for a in range(len(indices)):
            for b in range(a + 1, len(indices)):
                i = indices[a]
                j = indices[b]
                # A conflict happens if the later session starts before the earlier one ends
                if sessions[j][1] < sessions[i][2]:
                    conflicts.append((i, j))
        conflict_map[room_id] = conflicts
        
    return conflict_map


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

    How the Stack is used: (explain your approach in a comment here)
    """
    # How the Stack is used: We push sessions onto the stack as we process them. Since they are sorted by start time, we only need to check if the current session starts before the most recently pushed session (the top of the stack) finishes. If it does, we found our first conflict! If it doesn't, there's no conflict with that session, so we can pop it off to keep checking.
    stack = []
    
    for session in room_sessions:
        index, start, end = session
        
        while len(stack) > 0:
            top_index, top_start, top_end = stack[-1]
            
            # Check for conflict
            if start < top_end:
                # We found the first conflict!
                # Ensure we return the indices in (smaller, larger) order
                return (min(top_index, index), max(top_index, index))
            else:
                # No conflict, this previous session has ended before the current one started
                stack.pop()
                
        stack.append(session)
        
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
        Grouping step: O(N) -- we iterate through the list of N sessions once.
        Pairwise comparison per room: O(K^2) -- where K is the number of sessions in a specific room.
        Overall worst case: O(N^2) -- this happens if all N sessions are scheduled in exactly one room, causing the pairwise comparison to check all N(N-1)/2 pairs.
        Space complexity: O(N) -- we store exactly N indices in the room dictionary and up to N^2 pairs in the worst case (though normally bounded closer to O(N)).

    Improvement via sort + linear scan:
        If we sort the sessions in each room by their start times first, we don't have to check every single pair. We can just iterate through the sorted list and compare each session's start time with the previous session's end time.
        New overall complexity: O(N log N) -- grouping is O(N), sorting all rooms takes at most O(N log N), and the linear scan takes O(N).

    BST vs sorted array for conflict detection:
        A sorted array is generally better here. A BST keyed on start time takes O(N log N) to build and is great if we need to dynamically add or remove new sessions over time. However, since our list of sessions is static (already provided upfront), just sorting an array in O(N log N) and scanning it is much simpler and has less memory overhead than building a full tree structure.
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
    print(f"  Result:   {conflict_map}")
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

    # Room R1 sessions, sorted by start
    r1_sessions = [(0, 8, 10), (1, 9, 11), (2, 11, 13)]
    first_conflict = detect_first_conflict(r1_sessions)
    print(f"  R1 first conflict: {first_conflict}  [Expected: (0, 1)]")
    print(f"  PASS: {first_conflict == (0, 1)}")

    # Room R3 (no conflict)
    r3_sessions = [(0, 8, 9), (1, 9, 10), (2, 10, 11)]
    no_conflict = detect_first_conflict(r3_sessions)
    print(f"  R3 first conflict: {no_conflict}  [Expected: None]")
    print(f"  PASS: {no_conflict is None}")

    # E3 — written analysis
    print("\n--- E3: Complexity Analysis ---")
    print(e3_analysis())
