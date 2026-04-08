"""Task 6: Route Simulation (Path Information)"""
import sys
from collections import deque


def solve():
    data = sys.stdin.read().split()
    pos = 0

    def rd():
        nonlocal pos
        v = data[pos]; pos += 1; return v

    W, H, N = int(rd()), int(rd()), int(rd())
    DIR = {'E': (1, 0), 'W': (-1, 0), 'N': (0, 1), 'S': (0, -1)}

    blocked = set()
    for x in range(W):
        if x != 1 and x != W - 2:
            blocked.add((x, 0))
    blocked.add((0, 0))
    blocked.add((W - 1, 0))
    blocked.add((0, H - 1))
    blocked.add((W - 1, H - 1))

    prod_info = []
    name_to_pidx = {}
    pickup_to_prods = {}

    for i in range(N):
        sx, sy, name, d = int(rd()), int(rd()), rd(), rd()
        dx, dy = DIR[d]
        px, py = sx + dx, sy + dy
        prod_info.append((sx, sy, name, d, px, py))
        name_to_pidx[name] = i
        blocked.add((sx, sy))
        pickup_to_prods.setdefault((px, py), []).append(i)

    entrance = (1, 0)
    exit_cell = (W - 2, 0)

    def valid(x, y):
        return 0 <= x < W and 0 <= y < H and (x, y) not in blocked

    def bfs(src):
        dist = {src: 0}
        q = deque([src])
        while q:
            cx, cy = q.popleft()
            d = dist[(cx, cy)]
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = cx + dx, cy + dy
                if valid(nx, ny) and (nx, ny) not in dist:
                    dist[(nx, ny)] = d + 1
                    q.append((nx, ny))
        return dist

    all_pickup_cells = list(set(
        (prod_info[i][4], prod_info[i][5]) for i in range(N)
    ))

    key_cells = list(set([entrance, exit_cell] + all_pickup_cells))
    dist_from = {}
    for kc in key_cells:
        dist_from[kc] = bfs(kc)

    def get_dist(a, b):
        if a in dist_from:
            return dist_from[a].get(b, float('inf'))
        return float('inf')

    # For each pair of key cells, compute the set of product visibility bitmasks
    # achievable on shortest paths between them.
    seg_masks_cache = {}

    def get_seg_masks(a_cell, b_cell):
        key = (a_cell, b_cell)
        if key in seg_masks_cache:
            return seg_masks_cache[key]

        d_ab = get_dist(a_cell, b_cell)
        if d_ab == float('inf'):
            seg_masks_cache[key] = [0]
            return [0]

        # Compatible pickup cells
        compat = []
        for pc in all_pickup_cells:
            da = get_dist(a_cell, pc)
            db = get_dist(pc, b_cell)
            if da != float('inf') and db != float('inf') and da + db == d_ab:
                compat.append(pc)

        # Base mask: products at endpoints (always visited)
        base = 0
        for pidx in pickup_to_prods.get(a_cell, []):
            base |= (1 << pidx)
        for pidx in pickup_to_prods.get(b_cell, []):
            base |= (1 << pidx)

        if not compat:
            seg_masks_cache[key] = [base]
            return [base]

        nc = len(compat)
        cell_pmask = []
        for pc in compat:
            m = 0
            for pidx in pickup_to_prods.get(pc, []):
                m |= (1 << pidx)
            cell_pmask.append(m)

        if nc > 15:
            total = base
            for m in cell_pmask:
                total |= m
            seg_masks_cache[key] = [total]
            return [total]

        INF = float('inf')
        dp_s = [[INF] * nc for _ in range(1 << nc)]
        for i in range(nc):
            dp_s[1 << i][i] = get_dist(a_cell, compat[i])

        for cm in range(1, 1 << nc):
            for last in range(nc):
                if not (cm & (1 << last)) or dp_s[cm][last] == INF:
                    continue
                cur = dp_s[cm][last]
                for nxt in range(nc):
                    if cm & (1 << nxt):
                        continue
                    d_ln = get_dist(compat[last], compat[nxt])
                    if d_ln == INF:
                        continue
                    ncm = cm | (1 << nxt)
                    nd = cur + d_ln
                    if nd < dp_s[ncm][nxt]:
                        dp_s[ncm][nxt] = nd

        valid_pmasks = set()
        valid_pmasks.add(base)

        for cm in range(1, 1 << nc):
            for last in range(nc):
                if not (cm & (1 << last)) or dp_s[cm][last] == INF:
                    continue
                db = get_dist(compat[last], b_cell)
                if dp_s[cm][last] + db == d_ab:
                    pm = base
                    for i in range(nc):
                        if cm & (1 << i):
                            pm |= cell_pmask[i]
                    valid_pmasks.add(pm)

        # Pareto-filter: keep only maximal masks
        masks_list = sorted(valid_pmasks, key=lambda m: bin(m).count('1'), reverse=True)
        maximal = []
        for m in masks_list:
            if not any((m2 & m) == m for m2 in maximal):
                maximal.append(m)

        seg_masks_cache[key] = maximal
        return maximal

    Q = int(rd())
    results = []

    for _ in range(Q):
        M = int(rd())
        req_names = [rd() for __ in range(M)]

        req_cells_set = set()
        for name in req_names:
            pidx = name_to_pidx[name]
            pc = (prod_info[pidx][4], prod_info[pidx][5])
            req_cells_set.add(pc)
        req_cells = list(req_cells_set)
        n_req = len(req_cells)

        pos_list = [entrance] + req_cells + [exit_cell]
        n_pos = len(pos_list)
        pdist = [[get_dist(pos_list[i], pos_list[j]) for j in range(n_pos)] for i in range(n_pos)]

        full_mask = (1 << n_req) - 1
        INF = float('inf')

        # Phase 1: shortest distance via bitmask DP
        dp = [[INF] * n_pos for _ in range(1 << n_req)]
        dp[0][0] = 0

        for mask in range(1 << n_req):
            for u in range(n_pos):
                if dp[mask][u] == INF:
                    continue
                for j in range(n_req):
                    if mask & (1 << j):
                        continue
                    v = j + 1
                    nd = dp[mask][u] + pdist[u][v]
                    nm = mask | (1 << j)
                    if nd < dp[nm][v]:
                        dp[nm][v] = nd

        shortest = min(dp[full_mask][u] + pdist[u][n_pos - 1] for u in range(n_pos))

        # Phase 2: maximize visibility among shortest tours.
        # DP state: (required_mask, last_pos_idx)
        # Value: (min_dist, set of Pareto-optimal vis_masks at that dist)
        #
        # For each transition (u -> v), we try ALL valid segment masks
        # (not just the best one), to correctly handle cases where a
        # suboptimal per-segment choice leads to a better global result.

        # Precompute segment masks for all position pairs used
        seg_masks_by_pos = {}
        for i in range(n_pos):
            for j in range(n_pos):
                if i == j or pdist[i][j] == INF:
                    seg_masks_by_pos[(i, j)] = [0]
                else:
                    seg_masks_by_pos[(i, j)] = get_seg_masks(pos_list[i], pos_list[j])

        # dp2[mask][u] = (dist, set_of_vis_masks)
        # Only keep entries where dist == optimal for that (mask, u) state
        dp2_dist = [[INF] * n_pos for _ in range(1 << n_req)]
        dp2_vis = [[None] * n_pos for _ in range(1 << n_req)]

        init_vis = 0
        for pidx in pickup_to_prods.get(entrance, []):
            init_vis |= (1 << pidx)
        dp2_dist[0][0] = 0
        dp2_vis[0][0] = {init_vis}

        for mask in range(1 << n_req):
            for u in range(n_pos):
                if dp2_dist[mask][u] == INF:
                    continue
                cd = dp2_dist[mask][u]
                cv_set = dp2_vis[mask][u]
                for j in range(n_req):
                    if mask & (1 << j):
                        continue
                    v = j + 1
                    nd = cd + pdist[u][v]
                    nm = mask | (1 << j)
                    if nd > dp2_dist[nm][v]:
                        continue
                    # Generate new vis masks
                    new_vis_set = set()
                    for cv in cv_set:
                        for sm in seg_masks_by_pos[(u, v)]:
                            new_vis_set.add(cv | sm)

                    if nd < dp2_dist[nm][v]:
                        dp2_dist[nm][v] = nd
                        dp2_vis[nm][v] = new_vis_set
                    else:
                        # nd == dp2_dist[nm][v], merge vis sets
                        dp2_vis[nm][v] |= new_vis_set

                    # Pareto-filter to keep manageable
                    if len(dp2_vis[nm][v]) > 200:
                        dp2_vis[nm][v] = _pareto_filter(dp2_vis[nm][v])
                        # If still too many after Pareto, keep top by popcount
                        if len(dp2_vis[nm][v]) > 200:
                            sorted_m = sorted(dp2_vis[nm][v],
                                              key=lambda m: bin(m).count('1'),
                                              reverse=True)
                            dp2_vis[nm][v] = set(sorted_m[:200])

        # Find best visibility at the end
        best_vis_mask = 0
        best_cnt = -1
        best_names = None

        for u in range(n_pos):
            td = dp2_dist[full_mask][u] + pdist[u][n_pos - 1]
            if td != shortest:
                continue
            if dp2_vis[full_mask][u] is None:
                continue
            for cv in dp2_vis[full_mask][u]:
                for sm in seg_masks_by_pos[(u, n_pos - 1)]:
                    tv = cv | sm
                    cnt = bin(tv).count('1')
                    names = sorted(prod_info[k][2] for k in range(N) if tv & (1 << k))
                    if cnt > best_cnt or (cnt == best_cnt and (best_names is None or names < best_names)):
                        best_cnt = cnt
                        best_names = names
                        best_vis_mask = tv

        visible = sorted(prod_info[k][2] for k in range(N) if best_vis_mask & (1 << k))
        results.append(f"{shortest} {' '.join(visible)}")

    sys.stdout.write('\n'.join(results) + '\n')


def _pareto_filter(masks_set):
    """Keep only maximal masks (no mask is a proper subset of another)."""
    masks_list = sorted(masks_set, key=lambda m: bin(m).count('1'), reverse=True)
    maximal = []
    for m in masks_list:
        if not any((m2 & m) == m for m2 in maximal):
            maximal.append(m)
    return set(maximal)


if __name__ == "__main__":
    solve()
