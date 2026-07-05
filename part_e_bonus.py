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
    sessions_by_room = {}
    for idx, (room_id, start_time, end_time) in enumerate(sessions):
        if room_id not in sessions_by_room:
            sessions_by_room[room_id] = []
        sessions_by_room[room_id].append(idx)
        
    # Step 2: For each room, compare all pairs of sessions for conflicts.
    conflict_map = {}
    for room_id, idx_list in sessions_by_room.items():
        conflicts = []
        # Compare every pair (i, j) where i < j
        for idx1 in range(len(idx_list)):
            for idx2 in range(idx1 + 1, len(idx_list)):
                i = idx_list[idx1]
                j = idx_list[idx2]
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
    # How the Stack is used: As we iterate through the chronologically sorted sessions, we push them onto the stack. For each new session, we check it against the session at the top of the stack. If the new session's start time overlaps with the top session's end time, we have found the first conflict. If there is no overlap, the top session has concluded, so we pop it off and continue.
    active_sessions = []
    
    for session in room_sessions:
        curr_idx, curr_start, curr_end = session
        
        while len(active_sessions) > 0:
            top_idx, top_start, top_end = active_sessions[-1]
            
            # Check for conflict
            if curr_start < top_end:
                # We found the first conflict!
                # Ensure we return the indices in (smaller, larger) order
                return (min(top_idx, curr_idx), max(top_idx, curr_idx))
            else:
                # No conflict, this previous session has ended before the current one started
                active_sessions.pop()
                
        active_sessions.append(session)
        
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
        Grouping step: O(N) -- iterating over the session list takes linear time.
        Pairwise comparison per room: O(K^2) -- where K is the number of scheduled sessions for a particular room.
        Overall worst case: O(N^2) -- if the university schedules every single exam into one giant room, we are forced to compare all N(N-1)/2 possibilities.
        Space complexity: O(N) -- memory used for the dictionary keys (rooms) and the lists of indices will roughly scale linearly with the number of sessions.

    Improvement via sort + linear scan:
        Sorting the sessions by start time allows us to completely avoid nested loop comparisons. We just walk through the array sequentially and compare adjacent elements.
        New overall complexity: O(N log N) -- grouping takes O(N), sorting the largest room takes O(N log N), and the single linear pass takes O(N). The dominant term is O(N log N).

    BST vs sorted array for conflict detection:
        While a BST (keyed by start_time) allows for efficient O(log N) dynamic insertions and overlap queries, it is overkill for a static scheduling problem where all exams are known upfront. Sorting an array takes O(N log N) and is much more memory efficient since it avoids the overhead of node objects and tree pointers.
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
