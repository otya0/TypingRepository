"""Task 5: Route Simulation (Generalized)"""
import sys
from collections import deque


DIRECTION_MAP = {
    "E": (1, 0),
    "W": (-1, 0),
    "N": (0, 1),
    "S": (0, -1),
}

MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]

INF = float("inf")


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
    for c in [(0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1)]:
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

    def bfs_from(start):
        """BFS from start, returns dict of (x,y) -> distance for all reachable cells."""
        dist = {start: 0}
        queue = deque([start])
        while queue:
            cx, cy = queue.popleft()
            d = dist[(cx, cy)]
            for mx, my in MOVES:
                nx, ny = cx + mx, cy + my
                if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in blocked and (nx, ny) not in dist:
                    dist[(nx, ny)] = d + 1
                    queue.append((nx, ny))
        return dist

    results = []
    for _ in range(Q):
        M = int(input_data[idx]); idx += 1
        products = []
        for _ in range(M):
            products.append(input_data[idx]); idx += 1

        # Gather pickup locations for this query
        pickups = [product_pickup[p] for p in products]

        # Key nodes: 0 = entrance, 1..M = pickup locations, M+1 = exit
        # We need BFS distances between all pairs of these nodes.
        nodes = [entrance] + pickups + [exit_pos]
        num_nodes = len(nodes)

        # BFS from each unique node position
        bfs_cache = {}
        for pos in nodes:
            if pos not in bfs_cache:
                bfs_cache[pos] = bfs_from(pos)

        # Build distance matrix
        dist = [[INF] * num_nodes for _ in range(num_nodes)]
        for i in range(num_nodes):
            dists_i = bfs_cache[nodes[i]]
            for j in range(num_nodes):
                if nodes[j] in dists_i:
                    dist[i][j] = dists_i[nodes[j]]

        # Bitmask DP over the M product pickups (indices 1..M)
        # dp[mask][i] = shortest distance from entrance, having picked up
        #               the subset 'mask' of products, currently at pickup i
        #               (i is 0-indexed into pickups, so node index = i+1)
        full_mask = (1 << M) - 1
        dp = [[INF] * M for _ in range(1 << M)]

        # Initialize: go from entrance (node 0) to each pickup i (node i+1)
        for i in range(M):
            dp[1 << i][i] = dist[0][i + 1]

        # Fill DP
        for mask in range(1, 1 << M):
            for i in range(M):
                if dp[mask][i] == INF:
                    continue
                if not (mask & (1 << i)):
                    continue
                # Try extending to pickup j not yet visited
                for j in range(M):
                    if mask & (1 << j):
                        continue
                    new_mask = mask | (1 << j)
                    cost = dp[mask][i] + dist[i + 1][j + 1]
                    if cost < dp[new_mask][j]:
                        dp[new_mask][j] = cost

        # Find minimum: full_mask achieved, then go to exit (node M+1)
        ans = INF
        for i in range(M):
            cost = dp[full_mask][i] + dist[i + 1][M + 1]
            if cost < ans:
                ans = cost

        results.append(ans)

    print("\n".join(str(r) for r in results))


if __name__ == "__main__":
    solve()
