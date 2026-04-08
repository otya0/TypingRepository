"""Task 2: Relevant Pairs of Products"""
import sys
from collections import defaultdict
from itertools import combinations


def solve():
    input_data = sys.stdin.read().split()
    idx = 0

    N = int(input_data[idx]); idx += 1

    pair_count = defaultdict(int)

    for _ in range(N):
        M = int(input_data[idx]); idx += 1
        products = []
        for _ in range(M):
            products.append(input_data[idx]); idx += 1

        # Generate all pairs from this customer's products
        unique_products = sorted(set(products))
        for p1, p2 in combinations(unique_products, 2):
            # p1 < p2 already guaranteed by sorted order
            pair_count[(p1, p2)] += 1

    # Sort pairs: descending by count, then lexicographically by (name1, name2)
    sorted_pairs = sorted(pair_count.items(), key=lambda x: (-x[1], x[0]))

    Q = int(input_data[idx]); idx += 1

    results = []
    for _ in range(Q):
        a = int(input_data[idx]); idx += 1
        b = int(input_data[idx]); idx += 1
        for i in range(a - 1, b):
            count = sorted_pairs[i][1]
            p1, p2 = sorted_pairs[i][0]
            results.append(f"{count} {p1} {p2}")

    print("\n".join(results))


if __name__ == "__main__":
    solve()
