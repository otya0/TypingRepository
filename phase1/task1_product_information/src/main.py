"""Task 1: Product Information"""
import sys
from collections import Counter


def solve():
    input_data = sys.stdin.read().split("\n")
    idx = 0

    N = int(input_data[idx])
    idx += 1

    product_count = Counter()

    for _ in range(N):
        parts = input_data[idx].split()
        idx += 1
        M = int(parts[0])
        products = parts[1 : M + 1]
        for p in products:
            product_count[p] += 1

    # Sort by count descending, then by name ascending
    sorted_products = sorted(product_count.items(), key=lambda x: (-x[1], x[0]))

    Q = int(input_data[idx])
    idx += 1

    results = []
    for _ in range(Q):
        a, b = map(int, input_data[idx].split())
        idx += 1
        for i in range(a - 1, b):
            results.append(f"{sorted_products[i][1]} {sorted_products[i][0]}")

    print("\n".join(results))


if __name__ == "__main__":
    solve()
