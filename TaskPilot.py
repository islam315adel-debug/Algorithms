import heapq
import random


class MaxHeap:
    """Array-based max-heap built by hand (INSERT and EXTRACT-MAX are O(log n))."""

    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def peek(self):
        return self.data[0] if self.data else None

    def insert(self, item):
        self.data.append(item)
        self._sift_up(len(self.data) - 1)

    def extract_max(self):
        if not self.data:
            return None
        top = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._sift_down(0)
        return top

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.data[parent] >= self.data[i]:
                break
            self.data[parent], self.data[i] = self.data[i], self.data[parent]
            i = parent

    def _sift_down(self, i):
        n = len(self.data)
        while True:
            left, right, biggest = 2 * i + 1, 2 * i + 2, i
            if left < n and self.data[left] > self.data[biggest]:
                biggest = left
            if right < n and self.data[right] > self.data[biggest]:
                biggest = right
            if biggest == i:
                return
            self.data[i], self.data[biggest] = self.data[biggest], self.data[i]
            i = biggest


class TaskScheduler:
    """Runs the highest priority task first. Ties: the earliest added runs first."""

    def __init__(self):
        self.heap = MaxHeap()
        self.counter = 0

    def add_task(self, name, priority):
        # tuple order: priority first, then earlier tasks win ties (-counter is bigger)
        self.heap.insert((priority, -self.counter, name))
        self.counter += 1

    def run_next(self):
        item = self.heap.extract_max()
        if item is None:
            return None
        priority, _, name = item
        return name, priority

    def next_task(self):
        item = self.heap.peek()
        return (item[2], item[0]) if item else None

    def pending(self):
        return len(self.heap)

    def show_heap(self):
        print("heap array:", [(p, name) for p, _, name in self.heap.data])


def run_tests():
    s = TaskScheduler()
    assert s.run_next() is None and s.next_task() is None
    for name, p in [("write report", 5), ("fix bug", 9), ("reply email", 2), ("deploy", 9)]:
        s.add_task(name, p)
    assert s.pending() == 4
    assert s.next_task() == ("fix bug", 9)
    order = [s.run_next()[0] for _ in range(4)]
    assert order == ["fix bug", "deploy", "write report", "reply email"]
    # compare with Python's heapq on random data
    for _ in range(50):
        pr = [random.randint(1, 20) for _ in range(random.randint(1, 60))]
        sch, ref = TaskScheduler(), []
        for i, p in enumerate(pr):
            sch.add_task(f"t{i}", p)
            heapq.heappush(ref, (-p, i))
        while sch.pending():
            name, p = sch.run_next()
            rp, ri = heapq.heappop(ref)
            assert (p, name) == (-rp, f"t{ri}")
    print("All tests passed.\n")


if __name__ == "__main__":
    run_tests()
    sched = TaskScheduler()
    tasks = [("Submit assignment", 8), ("Check email", 3), ("Fix server crash", 10),
             ("Backup files", 5), ("Team meeting", 7), ("Update docs", 2)]
    for name, priority in tasks:
        sched.add_task(name, priority)
        print(f"added {name!r} (priority {priority})")
    print()
    sched.show_heap()
    print("next up:", sched.next_task(), "\n")
    step = 1
    while sched.pending():
        name, priority = sched.run_next()
        print(f"{step}. running {name!r} (priority {priority}), {sched.pending()} left")
        step += 1
