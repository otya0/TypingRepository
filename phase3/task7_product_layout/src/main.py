"""Task 7: Product Layout - Optimal product placement using simulated annealing."""
import sys
import math
import random
from collections import deque, defaultdict


# ---------------------------------------------------------------------------
# Direction helpers
# ---------------------------------------------------------------------------
DIR_MAP = {"E": (1, 0), "W": (-1, 0), "N": (0, 1), "S": (0, -1)}
MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]


# ---------------------------------------------------------------------------
# Grid / Store model
# ---------------------------------------------------------------------------
class Store:
    """Represents the physical store grid."""

    def __init__(self, W, H, shelves):
        """
        W, H: grid size
        shelves: list of (x, y, direction_str)
        """
        self.W = W
        self.H = H
        self.shelves = shelves  # [(x, y, d_str), ...]

        # Precompute the access cell for each shelf
        # Access cell = cell the customer stands on to pick up the product
        self.shelf_access = {}  # (x,y) -> (ax, ay)
        for x, y, d in shelves:
            dx, dy = DIR_MAP[d]
            self.shelf_access[(x, y)] = (x + dx, y + dy)

        # Build blocked set
        self.blocked = set()
        # Bottom row blocked except entrance/exit
        for x in range(W):
            if (x, 0) not in ((1, 0), (W - 2, 0)):
                self.blocked.add((x, 0))
        # Corners
        for cx, cy in [(0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1)]:
            self.blocked.add((cx, cy))
        # Shelf cells
        for x, y, _ in shelves:
            self.blocked.add((x, y))

        self.entrance = (1, 0)
        self.exit = (W - 2, 0)

    def passable(self, x, y):
        return 0 <= x < self.W and 0 <= y < self.H and (x, y) not in self.blocked


# ---------------------------------------------------------------------------
# BFS shortest paths
# ---------------------------------------------------------------------------
def bfs_from(store, start):
    """BFS from start cell. Returns dist dict."""
    dist = {start: 0}
    q = deque([start])
    while q:
        cx, cy = q.popleft()
        for dx, dy in MOVES:
            nx, ny = cx + dx, cy + dy
            if (nx, ny) not in dist and store.passable(nx, ny):
                dist[(nx, ny)] = dist[(cx, cy)] + 1
                q.append((nx, ny))
    return dist


# ---------------------------------------------------------------------------
# Bitmask DP for TSP-like multi-product route
# ---------------------------------------------------------------------------
def route_cost(store, access_cells):
    """
    Compute shortest route: entrance -> visit all access_cells -> exit.
    Uses bitmask DP over the access cells.
    access_cells: list of (x, y) that must be visited.
    Returns the minimum total distance, or float('inf') if unreachable.
    """
    if not access_cells:
        # Just entrance to exit
        d = bfs_from(store, store.entrance)
        return d.get(store.exit, float("inf"))

    n = len(access_cells)
    # Key points: entrance + access_cells + exit
    points = [store.entrance] + list(access_cells) + [store.exit]
    num_points = len(points)

    # Precompute pairwise BFS distances among key points
    pair_dist = [[float("inf")] * num_points for _ in range(num_points)]
    for i in range(num_points):
        d = bfs_from(store, points[i])
        for j in range(num_points):
            if points[j] in d:
                pair_dist[i][j] = d[points[j]]

    # Bitmask DP: dp[mask][i] = min cost to reach access_cells[i]
    # having visited the set of access_cells indicated by mask
    # Indices 1..n are access_cells, 0 = entrance, n+1 = exit
    full_mask = (1 << n) - 1
    INF = float("inf")
    dp = [[INF] * n for _ in range(1 << n)]

    # Start: from entrance (index 0) to each access cell
    for i in range(n):
        dp[1 << i][i] = pair_dist[0][i + 1]

    for mask in range(1, 1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            if dp[mask][last] == INF:
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue
                new_mask = mask | (1 << nxt)
                cost = dp[mask][last] + pair_dist[last + 1][nxt + 1]
                if cost < dp[new_mask][nxt]:
                    dp[new_mask][nxt] = cost

    # Find best: full_mask -> exit
    best = INF
    for last in range(n):
        cost = dp[full_mask][last] + pair_dist[last + 1][n + 1]
        if cost < best:
            best = cost

    return best


# ---------------------------------------------------------------------------
# Layout representation & evaluation
# ---------------------------------------------------------------------------
class Layout:
    """
    A mapping of products to shelves.
    assignment[i] = shelf index for product i  (0-indexed)
    """

    def __init__(self, assignment):
        self.assignment = list(assignment)

    def copy(self):
        return Layout(list(self.assignment))


def evaluate_layout(store, layout, products, histories):
    """
    Evaluate a layout by computing the average route cost for all customers.
    products: list of product names (index = product id)
    histories: list of lists of product names per customer
    layout.assignment[i] = shelf index for product i

    Returns average route cost (lower = better).
    """
    product_to_id = {name: i for i, name in enumerate(products)}

    # Map product -> shelf -> access cell
    shelf_list = store.shelves  # [(x, y, d), ...]
    product_access = {}  # product_id -> access cell
    for pid, sid in enumerate(layout.assignment):
        sx, sy, sd = shelf_list[sid]
        product_access[pid] = store.shelf_access[(sx, sy)]

    total_cost = 0.0
    count = 0
    for history in histories:
        # Get product ids for this customer
        pids = []
        for pname in history:
            if pname in product_to_id:
                pid = product_to_id[pname]
                if pid < len(layout.assignment):
                    pids.append(pid)
        if not pids:
            continue
        # Deduplicate access cells
        access_cells = list(set(product_access[pid] for pid in pids))
        cost = route_cost(store, access_cells)
        total_cost += cost
        count += 1

    if count == 0:
        return 0.0
    return total_cost / count


# ---------------------------------------------------------------------------
# Purchase history analysis
# ---------------------------------------------------------------------------
def analyze_purchases(products, histories):
    """
    Analyze purchase histories to get:
    - product_freq: how often each product is purchased
    - copurchase_freq: how often each pair is co-purchased
    """
    product_to_id = {name: i for i, name in enumerate(products)}
    P = len(products)
    product_freq = [0] * P
    copurchase_freq = defaultdict(int)

    for history in histories:
        pids = set()
        for pname in history:
            if pname in product_to_id:
                pid = product_to_id[pname]
                if pid < P:
                    pids.add(pid)
                    product_freq[pid] += 1
        pid_list = sorted(pids)
        for i in range(len(pid_list)):
            for j in range(i + 1, len(pid_list)):
                copurchase_freq[(pid_list[i], pid_list[j])] += 1

    return product_freq, copurchase_freq


# ---------------------------------------------------------------------------
# Initial layout heuristic
# ---------------------------------------------------------------------------
def initial_layout(store, products, histories):
    """
    Create an initial layout placing popular products near entrance/exit,
    and co-purchased products near each other.
    """
    P = len(products)
    S = len(store.shelves)
    product_freq, copurchase_freq = analyze_purchases(products, histories)

    # Rank shelves by distance to entrance (prefer closer to entrance/exit)
    entrance_dist = bfs_from(store, store.entrance)
    exit_dist = bfs_from(store, store.exit)

    shelf_scores = []
    for sid, (sx, sy, sd) in enumerate(store.shelves):
        ac = store.shelf_access[(sx, sy)]
        d_ent = entrance_dist.get(ac, float("inf"))
        d_ext = exit_dist.get(ac, float("inf"))
        # Score: lower combined distance = better shelf for popular items
        shelf_scores.append((min(d_ent, d_ext), sid))
    shelf_scores.sort()

    # Sort products by popularity (most popular first)
    product_order = sorted(range(P), key=lambda i: -product_freq[i])

    # Assign most popular products to best shelves
    assignment = [0] * P
    used_shelves = set()
    for pid in product_order:
        for _, sid in shelf_scores:
            if sid not in used_shelves:
                assignment[pid] = sid
                used_shelves.add(sid)
                break

    return Layout(assignment)


# ---------------------------------------------------------------------------
# Simulated annealing optimization
# ---------------------------------------------------------------------------
def simulated_annealing(store, products, histories, layout, max_iter=5000,
                        t_start=50.0, t_end=0.1):
    """
    Optimize layout using simulated annealing with swap moves.
    """
    P = len(products)
    S = len(store.shelves)
    random.seed(42)

    current = layout.copy()
    current_score = evaluate_layout(store, current, products, histories)
    best = current.copy()
    best_score = current_score

    # Set of shelves not used by any product (available for swaps)
    used_shelves = set(current.assignment)
    free_shelves = [s for s in range(S) if s not in used_shelves]

    for iteration in range(max_iter):
        t = t_start * ((t_end / t_start) ** (iteration / max(max_iter - 1, 1)))

        # Choose a random move: swap two products or move a product to a free shelf
        candidate = current.copy()
        if P >= 2 and (not free_shelves or random.random() < 0.7):
            # Swap two products
            i, j = random.sample(range(P), 2)
            candidate.assignment[i], candidate.assignment[j] = (
                candidate.assignment[j],
                candidate.assignment[i],
            )
        else:
            # Move a product to a free shelf
            if free_shelves:
                pid = random.randint(0, P - 1)
                old_shelf = candidate.assignment[pid]
                new_shelf = random.choice(free_shelves)
                candidate.assignment[pid] = new_shelf
                # Update free shelves for next iteration tracking
            else:
                continue

        new_score = evaluate_layout(store, candidate, products, histories)
        delta = new_score - current_score

        if delta < 0 or random.random() < math.exp(-delta / max(t, 1e-10)):
            current = candidate
            current_score = new_score
            # Update free shelves
            used_shelves = set(current.assignment)
            free_shelves = [s for s in range(S) if s not in used_shelves]

            if current_score < best_score:
                best = current.copy()
                best_score = current_score

    return best, best_score


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split()
    idx = 0

    def next_token():
        nonlocal idx
        val = data[idx]
        idx += 1
        return val

    # Read grid dimensions and shelf count
    W = int(next_token())
    H = int(next_token())
    S = int(next_token())

    # Read shelves
    shelves = []
    for _ in range(S):
        x = int(next_token())
        y = int(next_token())
        d = next_token()
        shelves.append((x, y, d))

    # Read products
    P = int(next_token())
    products = []
    for _ in range(P):
        products.append(next_token())

    # Read purchase histories
    N = int(next_token())
    histories = []
    for _ in range(N):
        M = int(next_token())
        history = []
        for _ in range(M):
            history.append(next_token())
        histories.append(history)

    # Build store
    store = Store(W, H, shelves)

    # Create initial layout
    layout = initial_layout(store, products, histories)
    init_score = evaluate_layout(store, layout, products, histories)

    # Optimize with simulated annealing
    # Adjust iterations based on problem size
    max_iter = min(10000, max(1000, P * S * 20))
    best_layout, best_score = simulated_annealing(
        store, products, histories, layout,
        max_iter=max_iter, t_start=50.0, t_end=0.01,
    )

    # Output: for each product, print shelf position, product name, direction
    for pid in range(P):
        sid = best_layout.assignment[pid]
        sx, sy, sd = shelves[sid]
        print(f"{sx} {sy} {products[pid]} {sd}")

    # Output evaluation metrics
    print(f"# Initial score (avg route cost): {init_score:.2f}")
    print(f"# Optimized score (avg route cost): {best_score:.2f}")
    if init_score > 0:
        improvement = (init_score - best_score) / init_score * 100
        print(f"# Improvement: {improvement:.1f}%")


if __name__ == "__main__":
    solve()
