import random
import time


def insertion_sort(arr, verbose=False):
    """Sort a copy of arr. Returns (sorted_list, comparisons, shifts)."""
    a = arr[:]
    comparisons = 0
    shifts = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]      # shift the bigger element right
                shifts += 1
                j -= 1
            else:
                break
        a[j + 1] = key
        if verbose:
            print(f"  pass {i}: {a}")
    return a, comparisons, shifts


def run_tests():
    assert insertion_sort([]) == ([], 0, 0)
    assert insertion_sort([7]) == ([7], 0, 0)
    # worst case (reversed): n(n-1)/2 comparisons and shifts
    assert insertion_sort([4, 3, 2, 1]) == ([1, 2, 3, 4], 6, 6)
    # best case (sorted): n-1 comparisons, 0 shifts
    assert insertion_sort([1, 2, 3, 4]) == ([1, 2, 3, 4], 3, 0)
    # duplicates and random data
    assert insertion_sort([3, 1, 3, 2, 1])[0] == [1, 1, 2, 3, 3]
    for _ in range(100):
        data = [random.randint(-50, 50) for _ in range(random.randint(0, 40))]
        assert insertion_sort(data)[0] == sorted(data)
    print("All tests passed.\n")


def make_input(kind, n):
    if kind == "sorted":
        return list(range(n))
    if kind == "reversed":
        return list(range(n, 0, -1))
    return [random.randint(0, n * 10) for _ in range(n)]


def timed(data):
    start = time.perf_counter()
    result, comparisons, shifts = insertion_sort(data)
    ms = (time.perf_counter() - start) * 1000
    assert result == sorted(data)
    return ms, comparisons, shifts


def experiment(sizes=(100, 500, 1000, 2000, 5000)):
    print(f"{'n':>6} {'case':<9} {'comparisons':>12} {'shifts':>12} {'time (ms)':>10}")
    for n in sizes:
        for kind in ("sorted", "reversed", "random"):
            ms, c, s = timed(make_input(kind, n))
            print(f"{n:>6} {kind:<9} {c:>12} {s:>12} {ms:>10.2f}")
        print()


def growth_demo(n=1000):
    """Quadratic growth: 3x the size should take about 9x the time."""
    t1 = min(timed(make_input("reversed", n))[0] for _ in range(3))
    t3 = min(timed(make_input("reversed", 3 * n))[0] for _ in range(3))
    print(f"n={n}: {t1:.2f} ms   n={3 * n}: {t3:.2f} ms   ratio = {t3 / t1:.1f}x (expected about 9x)")


if __name__ == "__main__":
    run_tests()
    print("Step by step on [5, 2, 4, 6, 1, 3]:")
    insertion_sort([5, 2, 4, 6, 1, 3], verbose=True)
    print()
    experiment()
    growth_demo()
