"""Test data generator for Task 4: Relevant Pairs of Products (Large Data).

Generates valid input within constraints:
  1 <= N <= 10000, 1 <= M <= 20, 1 <= len(product_name) <= 10, 1 <= Q <= 10
  No duplicate products within a single customer.

Usage:
  python generator.py              # default: N=10000, M=20 (worst case)
  python generator.py 100 5        # custom N and M
  python generator.py 10000 20 5   # custom N, M, and Q
"""
import random
import string
import sys


def random_product_name(length=None):
    """Generate a random product name of length 1..10."""
    if length is None:
        length = random.randint(1, 10)
    return "".join(random.choices(string.ascii_lowercase, k=length))


def generate(n=10000, m=20, q=5, pool_size=200):
    """Generate test input.

    Args:
        n: number of customers
        m: max products per customer (each customer gets exactly m products)
        q: number of queries
        pool_size: size of the product name pool (controls overlap between customers)
    """
    # Pre-generate a pool of unique product names
    product_pool = set()
    while len(product_pool) < pool_size:
        product_pool.add(random_product_name())
    product_pool = list(product_pool)

    lines = [str(n)]
    for _ in range(n):
        # Pick m unique products for this customer from the pool
        chosen = random.sample(product_pool, min(m, len(product_pool)))
        lines.append(f"{len(chosen)} " + " ".join(chosen))

    # Calculate total possible pairs for query bounds
    # Upper bound: C(pool_size, 2) but actual count may be less
    # For safety, compute from the data (but we just need a valid range)
    max_pairs = pool_size * (pool_size - 1) // 2

    lines.append(str(q))
    for _ in range(q):
        a = random.randint(1, max(1, max_pairs - 10))
        b = random.randint(a, min(a + 20, max_pairs))
        lines.append(f"{a} {b}")

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    args = sys.argv[1:]
    n = int(args[0]) if len(args) > 0 else 10000
    m = int(args[1]) if len(args) > 1 else 20
    q = int(args[2]) if len(args) > 2 else 5

    print(generate(n=n, m=m, q=q), end="")
