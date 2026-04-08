"""Task 3: Route Simulation"""
import sys
from collections import deque


DIRECTION_MAP = {
    "E": (1, 0),
    "W": (-1, 0),
    "N": (0, 1),
    "S": (0, -1),
}

MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def solve():
    input_data = sys.stdin.read().split()
    idx = 0

    W = int(input_data[idx]); idx += 1
    H = int(input_data[idx]); idx += 1
    N = int(input_data[idx]); idx += 1

    # Build blocked set and product lookup
    blocked = set()
    product_pickup = {}  # symbol -> (pickup_x, pickup_y)

    # Block corners
    corners = [(0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1)]
    for c in corners:
        blocked.add(c)

    # Block bottom row y=0 except entrance (1,0) and exit (W-2,0)
    entrance = (1, 0)
    exit_pos = (W - 2, 0)
    for x in range(W):
        if (x, 0) != entrance and (x, 0) != exit_pos:
            blocked.add((x, 0))

    # Read products
    for _ in range(N):
        px = int(input_data[idx]); idx += 1
        py = int(input_data[idx]); idx += 1
        ps = input_data[idx]; idx += 1
        pd = input_data[idx]; idx += 1

        # Shelf cell is blocked
        blocked.add((px, py))

        # Compute pickup cell
        dx, dy = DIRECTION_MAP[pd]
        pickup_x = px + dx
        pickup_y = py + dy
        product_pickup[ps] = (pickup_x, pickup_y)

    Q = int(input_data[idx]); idx += 1

    def bfs(start, goal):
        """BFS shortest path from start to goal on the grid, avoiding blocked cells."""
        if start == goal:
            return 0
        visited = set()
        visited.add(start)
        queue = deque()
        queue.append((start[0], start[1], 0))
        while queue:
            cx, cy, dist = queue.popleft()
            for mx, my in MOVES:
                nx, ny = cx + mx, cy + my
                if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in blocked and (nx, ny) not in visited:
                    nd = dist + 1
                    if (nx, ny) == goal:
                        return nd
                    visited.add((nx, ny))
                    queue.append((nx, ny, nd))
        return -1  # unreachable

    results = []
    for _ in range(Q):
        M = int(input_data[idx]); idx += 1
        products = []
        for _ in range(M):
            products.append(input_data[idx]); idx += 1

        # M=1: entrance -> pickup -> exit
        pickup = product_pickup[products[0]]
        d1 = bfs(entrance, pickup)
        d2 = bfs(pickup, exit_pos)
        results.append(d1 + d2)

    print("\n".join(str(r) for r in results))


if __name__ == "__main__":
    solve()
