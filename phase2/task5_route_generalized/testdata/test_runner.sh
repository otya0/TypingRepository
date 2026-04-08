#!/bin/bash
# Run from the task5_route_generalized directory
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "=== Testing Task 5: Route Simulation (Generalized) ==="
actual=$(python3 src/main.py < testdata/sample_input.txt)
expected=$(cat testdata/sample_output.txt)

if [ "$actual" = "$expected" ]; then
    echo "PASS: Sample test"
else
    echo "FAIL: Sample test"
    echo "Expected:"
    echo "$expected"
    echo "Got:"
    echo "$actual"
fi
