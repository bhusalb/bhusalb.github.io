"""Illustrate clipping-induced polar-factor rotation in two dimensions.

Run with Python 3: python3 clipping_polar_geometry.py
This deterministic example is not a private optimizer or a DP-Muon-IM
implementation. It uses no data, noise mechanism, or privacy accountant.
"""

from math import atan2, degrees, hypot, sqrt


def scale(matrix, factor):
    return tuple(tuple(factor * x for x in row) for row in matrix)


def mean(left, right):
    return tuple(tuple((x + y) / 2 for x, y in zip(a, b)) for a, b in zip(left, right))


def frobenius_norm(matrix):
    return sqrt(sum(x * x for row in matrix for x in row))


def clip(matrix, threshold):
    if threshold <= 0:
        raise ValueError("The clipping threshold must be positive.")
    norm = frobenius_norm(matrix)
    factor = min(1.0, threshold / norm) if norm else 1.0
    return scale(matrix, factor), factor


def polar_factor_2x2(matrix):
    """Return Q in A = QH for a real 2x2 matrix with positive determinant.

    This closed form handles the tutorial's full-rank examples only;
    it is not a general singular value decomposition implementation.
    """
    (a, b), (c, d) = matrix
    if a * d - b * c <= 0:
        raise ValueError("This example requires a positive determinant.")
    denominator = hypot(a + d, c - b)
    cosine = (a + d) / denominator
    sine = (c - b) / denominator
    return ((cosine, -sine), (sine, cosine))


def report(label, matrix):
    polar = polar_factor_2x2(matrix)
    angle = degrees(atan2(polar[1][0], polar[0][0]))
    print(label)
    for row in matrix:
        print("  [" + ", ".join(f"{x:.6f}" for x in row) + "]")
    print(f"  polar rotation = {angle:.6f} degrees")
    return polar


def main():
    first = ((4.0, 0.0), (0.0, 0.0))
    second = ((0.0, 1.0), (0.0, 1.0))
    clipped_first, first_factor = clip(first, 1.0)
    clipped_second, second_factor = clip(second, 1.0)
    original = mean(first, second)
    clipped = mean(clipped_first, clipped_second)
    print(f"Clipping factors: {first_factor:.6f}, {second_factor:.6f}")
    original_polar = report("Original mean:", original)
    clipped_polar = report("Mean after per-example clipping:", clipped)
    report("Common positive rescaling (0.25 times original mean):", scale(original, 0.25))
    difference = tuple(
        tuple(x - y for x, y in zip(a, b))
        for a, b in zip(original_polar, clipped_polar)
    )
    print(f"Polar-factor Frobenius distance: {frobenius_norm(difference):.6f}")


if __name__ == "__main__":
    main()
