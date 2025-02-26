class Node:
    def __init__(self, priority, value):
        self.priority = priority
        self.value = value

    def __lt__(self, other):
        return self.priority < other.priority

class MaxPQ:
    def __init__(self):
        self._pq = [None]  # Initialize with a dummy element at index 0
        self._size = 0
    
    def is_empty(self):
        return self._size == 0
    
    def size(self):
        return self._size
    
    def insert(self, priority, value):
        self._pq.append(Node(priority, value))
        self._size += 1
        self._swim(self._size)
    
    def _swim(self, k):
        while k > 1 and self._pq[k] > self._pq[k // 2]:
            self._pq[k], self._pq[k // 2] = self._pq[k // 2], self._pq[k]
            k //= 2

    def peek(self):
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return self._pq[1].value

    def del_max(self):
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        max_node = self._pq[1]
        self._pq[1] = self._pq[self._size]
        self._pq.pop()
        self._size -= 1
        self._sink(1)
        return max_node.value
    
    def _sink(self, k):
        left = 2 * k
        right = 2 * k + 1
        largest = k
        if left <= self._size and self._pq[left] > self._pq[largest]:
            largest = left
        if right <= self._size and self._pq[right] > self._pq[largest]:
            largest = right
        if largest != k:
            self._pq[k], self._pq[largest] = self._pq[largest], self._pq[k]
            self._sink(largest)

class MinPQ:
    """
    A minimum priority queue implemented using a binary heap.
    Methods:
        __init__():
            Initializes an empty priority queue.
        is_empty() -> bool:
        size() -> int:
        insert(priority: int, value: Any):
        peek() -> Any:
        del_min() -> Any:
    """
    def __init__(self):
        self._pq = [None]  # Initialize with a dummy element at index 0
        self._size = 0
    
    def is_empty(self):
        """
        Check if the priority queue is empty.

        Returns:
            bool: True if the priority queue is empty, False otherwise.
        """
        return self._size == 0
    
    def size(self):
        """
        Returns the number of elements in the priority queue.

        Returns:
            int: The number of elements in the priority queue.
        """
        return self._size
    
    def insert(self, priority, value):
        """
        Insert a new value with the given priority into the priority queue.

        Args:
            priority (int): The priority of the value to be inserted.
            value (Any): The value to be inserted.
        """
        self._pq.append(Node(priority, value))
        self._size += 1
        self._swim(self._size)
    
    def _swim(self, k):
        while k > 1 and self._pq[k] < self._pq[k // 2]:
            self._pq[k], self._pq[k // 2] = self._pq[k // 2], self._pq[k]
            k //= 2

    def peek(self):
        """
        Return the value of the highest priority item without removing it from the priority queue.

        Raises:
            IndexError: If the priority queue is empty.

        Returns:
            The value of the highest priority item in the priority queue.
        """
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return self._pq[1].value

    def del_min(self):
        """
        Removes and returns the minimum element from the priority queue.

        This method assumes that the priority queue is implemented as a binary heap.
        It raises an IndexError if the priority queue is empty. The minimum element
        is determined by the natural ordering of the elements.

        Returns:
            The value of the minimum element in the priority queue.

        Raises:
            IndexError: If the priority queue is empty.
        """
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        min_node = self._pq[1]
        self._pq[1] = self._pq[self._size]
        self._pq.pop()
        self._size -= 1
        self._sink(1)
        return min_node.value
    
    def _sink(self, k):
        while 2 * k <= self._size:
            j = 2 * k
            if j < self._size and self._pq[j + 1] < self._pq[j]:
                j += 1
            if not self._pq[k] > self._pq[j]:
                break
            self._pq[k], self._pq[j] = self._pq[j], self._pq[k]
            k = j