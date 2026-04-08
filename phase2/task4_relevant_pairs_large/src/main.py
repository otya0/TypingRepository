"""Task 4: Relevant Pairs of Products (Large Data)"""
import sys
from collections import defaultdict
from itertools import combinations


def solve():
    data = sys.stdin.buffer.read().decode()
    tokens = data.split()
    idx = 0

    N = int(tokens[idx]); idx += 1

    pair_count = defaultdict(int)

    for _ in range(N):
        M = int(tokens[idx]); idx += 1
        products = sorted(set(tokens[idx:idx + M]))
        idx += M

        for p1, p2 in combinations(products, 2):
            pair_count[(p1, p2)] += 1

    # Sort: descending by count, then lexicographically by pair
    sorted_pairs = sorted(pair_count.items(), key=lambda x: (-x[1], x[0]))

    Q = int(tokens[idx]); idx += 1

    out = []
    for _ in range(Q):
        a = int(tokens[idx]); idx += 1
        b = int(tokens[idx]); idx += 1
        for i in range(a - 1, b):
            count = sorted_pairs[i][1]
            p1, p2 = sorted_pairs[i][0]
            out.append(f"{count} {p1} {p2}")

    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    solve()
