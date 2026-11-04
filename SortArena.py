import csv
import random
import time

from InsertionSort import insertion_sort


def merge_sort(arr):
    count = 0

    def sort(a):
        nonlocal count
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left, right = sort(a[:mid]), sort(a[mid:])
        out, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            count += 1
            if left[i] <= right[j]:
                out.append(left[i]); i += 1
            else:
                out.append(right[j]); j += 1
        return out + left[i:] + right[j:]

    return sort(arr), count


def quick_sort(arr):
    a = arr[:]
    count = 0

    def qs(lo, hi):
        nonlocal count
        while lo < hi:
            m = (lo + hi) // 2
            a[m], a[hi] = a[hi], a[m]
            pivot, s = a[hi], lo
            for i in range(lo, hi):
                count += 1
                if a[i] < pivot:
                    a[i], a[s] = a[s], a[i]
                    s += 1
            a[s], a[hi] = a[hi], a[s]
            if s - lo < hi - s:
                qs(lo, s - 1); lo = s + 1
            else:
                qs(s + 1, hi); hi = s - 1

    qs(0, len(a) - 1)
    return a, count


def heap_sort(arr):
    a = arr[:]
    n = len(a)
    count = 0

    def sift_down(i, end):
        nonlocal count
        while True:
            l, r, big = 2 * i + 1, 2 * i + 2, i
            if l < end:
                count += 1
                if a[l] > a[big]: big = l
            if r < end:
                count += 1
                if a[r] > a[big]: big = r
            if big == i:
                return
            a[i], a[big] = a[big], a[i]
            i = big

    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(0, end)
    return a, count


def insertion(arr):
    result, comparisons, _ = insertion_sort(arr)
    return result, comparisons


ALGORITHMS = {"insertion": insertion, "merge": merge_sort,
              "quick": quick_sort, "heap": heap_sort}


def make_input(kind, n):
    if kind == "sorted":
        return list(range(n))
    if kind == "reversed":
        return list(range(n, 0, -1))
    return [random.randint(0, n * 10) for _ in range(n)]


def run_benchmark(sizes=(100, 500, 1000, 2000, 5000), repeats=3):
    rows = []
    print(f"{'n':>6} {'input':<9} {'algorithm':<10} {'time (ms)':>10} {'comparisons':>12}")
    for n in sizes:
        for kind in ("sorted", "reversed", "random"):
            data = make_input(kind, n)
            expected = sorted(data)
            for name, func in ALGORITHMS.items():
                best = float("inf")
                for _ in range(repeats):
                    start = time.perf_counter()
                    result, comparisons = func(data)
                    best = min(best, (time.perf_counter() - start) * 1000)
                assert result == expected, f"{name} gave a wrong answer"
                rows.append({"n": n, "input": kind, "algorithm": name,
                             "time_ms": round(best, 3), "comparisons": comparisons})
                print(f"{n:>6} {kind:<9} {name:<10} {best:>10.2f} {comparisons:>12}")
        print()
    return rows


def save_csv(rows, path="results.csv"):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to {path}")


def plot(rows, kind="random"):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Install matplotlib to see the plot: pip install matplotlib")
        return
    plt.figure(figsize=(8, 5))
    for name in ALGORITHMS:
        pts = sorted((r["n"], r["time_ms"]) for r in rows
                     if r["algorithm"] == name and r["input"] == kind)
        plt.plot([p[0] for p in pts], [p[1] for p in pts], marker="o", label=name)
    plt.xlabel("n")
    plt.ylabel("time (ms)")
    plt.title(f"Running time on {kind} input")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("benchmark.png", dpi=150)
    print("Saved plot to benchmark.png")
    plt.show()


if __name__ == "__main__":
    results = run_benchmark()
    save_csv(results)
    plot(results, "random")
