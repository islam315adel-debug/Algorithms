import random
from collections import deque


def neighbors(r, c, rows, cols, diagonal=False):
    steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if diagonal:
        steps += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dr, dc in steps:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            yield nr, nc


def count_islands_dfs(grid, diagonal=False):
    """Iterative DFS. Returns (number_of_islands, list_of_island_sizes)."""
    if not grid:
        return 0, []
    rows, cols = len(grid), len(grid[0])
    seen = [[False] * cols for _ in range(rows)]
    sizes = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not seen[r][c]:
                seen[r][c] = True
                stack, size = [(r, c)], 0
                while stack:
                    cr, cc = stack.pop()
                    size += 1
                    for nr, nc in neighbors(cr, cc, rows, cols, diagonal):
                        if grid[nr][nc] == 1 and not seen[nr][nc]:
                            seen[nr][nc] = True
                            stack.append((nr, nc))
                sizes.append(size)
    return len(sizes), sizes


def label_islands_bfs(grid, diagonal=False):
    """BFS flood fill. Returns (labels, count); water = 0, islands = 1..count."""
    if not grid:
        return [], 0
    rows, cols = len(grid), len(grid[0])
    labels = [[0] * cols for _ in range(rows)]
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and labels[r][c] == 0:
                count += 1
                labels[r][c] = count
                queue = deque([(r, c)])
                while queue:
                    cr, cc = queue.popleft()
                    for nr, nc in neighbors(cr, cc, rows, cols, diagonal):
                        if grid[nr][nc] == 1 and labels[nr][nc] == 0:
                            labels[nr][nc] = count
                            queue.append((nr, nc))
    return labels, count


def random_grid(rows, cols, land_probability=0.4, seed=None):
    rng = random.Random(seed)
    return [[1 if rng.random() < land_probability else 0 for _ in range(cols)]
            for _ in range(rows)]


def show(grid):
    for row in grid:
        print(" ".join("#" if x else "." for x in row))


def show_labels(labels):
    symbols = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for row in labels:
        print(" ".join(symbols[(x - 1) % len(symbols)] if x else "." for x in row))


def run_tests():
    g1 = [[1, 1, 0, 0, 0],
          [1, 1, 0, 0, 0],
          [0, 0, 1, 0, 0],
          [0, 0, 0, 1, 1]]
    assert count_islands_dfs(g1)[0] == 3
    assert label_islands_bfs(g1)[1] == 3
    assert count_islands_dfs([])[0] == 0
    assert count_islands_dfs([[0, 0], [0, 0]])[0] == 0
    assert count_islands_dfs([[1, 1], [1, 1]]) == (1, [4])
    # diagonal neighbours: two islands become one when diagonals count
    g2 = [[1, 0], [0, 1]]
    assert count_islands_dfs(g2)[0] == 2
    assert count_islands_dfs(g2, diagonal=True)[0] == 1
    # DFS and BFS must always agree
    for seed in range(50):
        g = random_grid(8, 10, 0.45, seed)
        assert count_islands_dfs(g)[0] == label_islands_bfs(g)[1]
    print("All tests passed.\n")


if __name__ == "__main__":
    run_tests()
    grid = random_grid(10, 20, land_probability=0.4, seed=7)
    print("Grid (# = land, . = water):")
    show(grid)
    n_dfs, sizes = count_islands_dfs(grid)
    labels, n_bfs = label_islands_bfs(grid)
    print(f"\nDFS found {n_dfs} islands, BFS found {n_bfs} islands")
    print(f"Island sizes: {sorted(sizes, reverse=True)}")
    print(f"Largest island: {max(sizes) if sizes else 0} cells")
    print("\nLabeled islands:")
    show_labels(labels)
    print(f"\nWith diagonal connections: {count_islands_dfs(grid, diagonal=True)[0]} islands")
