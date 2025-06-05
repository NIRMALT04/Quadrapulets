def find_cube_quadruplets(a, n):
    d = a + n
    target = d**3 - a**3
    results = []

    # Try all possible b and c such that b^3 + c^3 = target
    for b in range(a - 1, 1, -1):
        for c in range(b - 1, 0, -1):
            if b**3 + c**3 == target:
                results.append((a, b, c, d))

    return results

# Example usage:
a_input = 500
n_input = 200

quadruplets = find_cube_quadruplets(a_input, n_input)

if quadruplets:
    print(f"KK's Cube Quadruplets for a={a_input} and n={n_input}:")
    for a, b, c, d in quadruplets:
        print(f"a={a}, b={b}, c={c}, d={d} -> {a}^3 + {b}^3 + {c}^3 = {d}^3")
else:
    print(f"No KK's Cube Quadruplets found for a={a_input} and n={n_input}.")
    