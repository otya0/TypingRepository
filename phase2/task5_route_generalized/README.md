# Task 5: Route Simulation (Generalized)

## Overview
Extend route simulation to handle multiple products per customer. Calculate shortest path to collect all products.

## Input
- Same format as Task 3, but M can be > 1.

## Output
- Shortest path distance for each customer to collect all products and exit.

## Constraints
- 4 <= W,H <= 100, 1 <= N <= 20, 1 <= Q <= 20, 1 <= M <= N

## Notes
- With M=20 products, brute-force permutations (20!) is infeasible. Need TSP-like optimization (e.g., bitmask DP).
