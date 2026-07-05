# BCP 210: Data Structures and Algorithms I
# Coursework Assignment 2 — Part C: Linked Lists, Stacks, and Queues
# Academic Year 2025/2026
#
# Instructions:
#   - Implement all TODO sections.
#   - Do NOT change class or function signatures.
#   - Do NOT import any external library. collections.deque is permitted for C6 only.
# ============================================================================

from collections import deque


# ============================================================================
# C1 (3 Marks)
# Define the Booking node and the ShuttleList class.
# ShuttleList must maintain BOTH a head and a tail pointer.
# ============================================================================

class Booking:
    """
    A single node in the doubly linked shuttle booking list.

    Attributes:
        booking_id   (int):  Unique booking identifier.
        student_name (str):  Full name of the student.
        destination  (str):  Shuttle destination stop.
        next         (Booking | None): Reference to the next node.
        prev         (Booking | None): Reference to the previous node.
    """
    def __init__(self, booking_id, student_name, destination):
        self.booking_id = booking_id
        self.student_name = student_name
        self.destination = destination
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"Booking({self.booking_id}, '{self.student_name}', '{self.destination}')"


class ShuttleList:
    """
    A doubly linked list of Booking nodes with head and tail pointers.
    """
    def __init__(self):
        self.head = None
        self.tail = None

    # -------------------------------------------------------------------------
    # C2 (4 Marks)
    # Add a new booking to the END of the list.
    # Correctly update both next and prev pointers, and advance self.tail.
    # -------------------------------------------------------------------------
    def add_booking(self, booking_id, student_name, destination):
        """
        Append a new Booking node to the end of the doubly linked list.

        Time complexity with tail pointer:    O(1)
        Time complexity WITHOUT tail pointer: O(N)
        (Fill in your answer in the docstring.)
        """
        new_node = Booking(booking_id, student_name, destination)
        
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    # -------------------------------------------------------------------------
    # C3 (4 Marks)
    # Remove the booking with the given booking_id from ANY position:
    #   - Head node
    #   - Tail node
    #   - Interior node
    # Return True if found and deleted, False if booking_id does not exist.
    # -------------------------------------------------------------------------
    def cancel_booking(self, booking_id):
        """
        Remove the booking node with the given booking_id.

        Returns:
            bool: True if deleted, False if not found.
        """
        current = self.head
        
        while current is not None:
            if current.booking_id == booking_id:
                # Case 1: Removing the head
                if current == self.head:
                    self.head = current.next
                    if self.head is not None:
                        self.head.prev = None
                    else:
                        self.tail = None # The list became empty
                # Case 2: Removing the tail
                elif current == self.tail:
                    self.tail = current.prev
                    if self.tail is not None:
                        self.tail.next = None
                # Case 3: Removing an interior node
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    
                return True
                
            current = current.next
            
        return False

    # -------------------------------------------------------------------------
    # C4 (4 Marks)
    # Locate the two nodes with id1 and id2, then swap their DATA fields
    # (booking_id, student_name, destination) without relinking any pointers.
    # Return True on success, False if either ID is not found.
    # -------------------------------------------------------------------------
    def find_and_swap(self, id1, id2):
        """
        Swap the data of two booking nodes without changing pointer structure.

        Returns:
            bool: True if both IDs found and swapped, False otherwise.

        Time complexity: O(N)  -- fill in your answer.
        Why swap data instead of relinking pointers? (write your answer in a comment below)
        """
        node1 = None
        node2 = None
        current = self.head
        
        # Traverse list once to find both nodes
        while current is not None:
            if current.booking_id == id1:
                node1 = current
            elif current.booking_id == id2:
                node2 = current
                
            if node1 and node2:
                break
                
            current = current.next
            
        if node1 is None or node2 is None:
            return False
            
        # Answer: swapping data is preferred because relinking pointers in a doubly linked list requires updating up to 8 pointer references (prev/next for both nodes and their neighbors) and handling complex edge cases (adjacent nodes, head, tail). Swapping data avoids all pointer logic.
        
        # Swap data fields
        node1.booking_id, node2.booking_id = node2.booking_id, node1.booking_id
        node1.student_name, node2.student_name = node2.student_name, node1.student_name
        node1.destination, node2.destination = node2.destination, node1.destination
        
        return True

    # -------------------------------------------------------------------------
    # Helper: traverse and print the list (provided — do not modify)
    # -------------------------------------------------------------------------
    def display(self):
        current = getattr(self, "head", None)
        if current is None:
            print("  (empty list)")
            return
        while current:
            print(f"  {current.booking_id} | {current.student_name} | {current.destination}")
            current = current.next


# ============================================================================
# C5 (5 Marks)
# Implement a Stack-backed route-change history for the dispatch office.
# Operations: push, pop_undo, peek.
# All operations must be O(1).
# ============================================================================

class RouteHistory:
    """
    A Stack that records shuttle route changes and supports undo.
    Backed by a Python list (used as a stack).
    """
    def __init__(self):
        self._stack = []

    def push(self, change):
        """
        Record a new route change string.
        Time complexity: O(1)
        """
        self._stack.append(change)

    def pop_undo(self):
        """
        Undo and return the most recent route change.
        Return None if there is nothing to undo.
        Time complexity: O(1)
        """
        if len(self._stack) == 0:
            return None
        return self._stack.pop()

    def peek(self):
        """
        Return the most recent route change without removing it.
        Return None if the history is empty.
        Time complexity: O(1)
        """
        if len(self._stack) == 0:
            return None
        return self._stack[-1]


# ============================================================================
# C6 (5 Marks)
# Implement a Queue for managing boarding order at a shuttle stop.
# Use collections.deque as the backing data structure.
# Explain in a comment WHY deque is better than a plain list for this purpose.
# ============================================================================

class BoardingQueue:
    """
    A FIFO queue managing the boarding order at a shuttle stop.
    Backed by collections.deque.

    Why deque instead of list?
    # A plain Python list has O(N) time complexity for removing from the front (index 0) because all other elements must shift left. A collections.deque is implemented as a doubly linked list internally, making removal from the front O(1).
    """
    def __init__(self):
        self._queue = deque()

    def join(self, student_name):
        """
        A student joins the back of the queue.
        Time complexity: O(1)
        """
        self._queue.append(student_name)

    def board(self):
        """
        The next student boards (removed from the front).
        Return None if the queue is empty.
        Time complexity: O(1)
        """
        if len(self._queue) == 0:
            return None
        return self._queue.popleft()

    def peek_next(self):
        """
        Return the name of the next student to board without removing them.
        Return None if the queue is empty.
        Time complexity: O(1)
        """
        if len(self._queue) == 0:
            return None
        return self._queue[0]

    def size(self):
        """
        Return the number of students currently in the queue.
        Time complexity: O(1)
        """
        return len(self._queue)


# ============================================================================
# TEST HARNESS — do not modify
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Part C: Linked Lists, Stacks, and Queues")
    print("=" * 60)

    # ---- C1/C2 — ShuttleList: add_booking ----
    print("\n--- C2: add_booking ---")
    sl = ShuttleList()
    sl.add_booking(101, "Ama Mensah",   "Airport")
    sl.add_booking(102, "Kofi Osei",    "Tema Station")
    sl.add_booking(103, "Efua Boateng", "Circle")
    sl.add_booking(104, "Yaw Darko",    "Kaneshie")
    sl.display()
    print(f"  head: {getattr(sl, 'head', 'NOT SET')}  tail: {getattr(sl, 'tail', 'NOT SET')}")

    # ---- C3 — cancel_booking ----
    print("\n--- C3: cancel_booking ---")
    print(f"  cancel 101 (head): {sl.cancel_booking(101)}")  # expect True
    print(f"  cancel 104 (tail): {sl.cancel_booking(104)}")  # expect True
    print(f"  cancel 102 (inner): {sl.cancel_booking(102)}")  # expect True
    print(f"  cancel 999 (missing): {sl.cancel_booking(999)}")  # expect False
    print("  Remaining list:")
    sl.display()

    # ---- C4 — find_and_swap ----
    print("\n--- C4: find_and_swap ---")
    sl2 = ShuttleList()
    sl2.add_booking(201, "Alice",  "North Campus")
    sl2.add_booking(202, "Bob",    "South Campus")
    sl2.add_booking(203, "Charlie","East Gate")
    print("  Before swap:")
    sl2.display()
    sl2.find_and_swap(201, 203)
    print("  After swapping bookings 201 and 203:")
    sl2.display()

    # ---- C5 — RouteHistory (Stack) ----
    print("\n--- C5: RouteHistory Stack ---")
    history = RouteHistory()
    history.push("Route A -> Route B")
    history.push("Route B -> Route C")
    history.push("Route C -> Route D")
    print(f"  peek:     {history.peek()}")          # expect Route C -> Route D
    print(f"  pop_undo: {history.pop_undo()}")      # expect Route C -> Route D
    print(f"  pop_undo: {history.pop_undo()}")      # expect Route B -> Route C
    print(f"  peek:     {history.peek()}")          # expect Route A -> Route B
    print(f"  pop_undo: {history.pop_undo()}")      # expect Route A -> Route B
    print(f"  pop_undo: {history.pop_undo()}")      # expect None (empty)

    # ---- C6 — BoardingQueue ----
    print("\n--- C6: BoardingQueue ---")
    bq = BoardingQueue()
    bq.join("Silas")
    bq.join("Ama")
    bq.join("Kofi")
    print(f"  Queue size: {bq.size()}")             # expect 3
    print(f"  peek_next:  {bq.peek_next()}")        # expect Silas
    print(f"  board:      {bq.board()}")            # expect Silas
    print(f"  board:      {bq.board()}")            # expect Ama
    print(f"  Queue size: {bq.size()}")             # expect 1
    print(f"  board:      {bq.board()}")            # expect Kofi
    print(f"  board:      {bq.board()}")            # expect None (empty)
