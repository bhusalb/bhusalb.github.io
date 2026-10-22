"""Exact finite-output DP example for epsilon = log(2).

Run with Python 3: python3 finite_output_privacy.py
This checks one specified neighboring pair, not an arbitrary program.
"""

from fractions import Fraction
from itertools import combinations


def directed_gap(p, q, likelihood_factor):
    """Return max_S (P(S) - likelihood_factor * Q(S)) and a witness.

    Probabilities and likelihood_factor must be exact Fraction values.
    likelihood_factor represents exp(epsilon); using it avoids an
    inexact floating-point evaluation of exp(log(2)).
    """
    if set(p) != set(q):
        raise ValueError("Use the same output labels, including zero masses.")
    if not isinstance(likelihood_factor, Fraction) or likelihood_factor < 1:
        raise ValueError("The likelihood factor must be a Fraction >= 1.")
    for distribution in (p, q):
        if any(not isinstance(x, Fraction) for x in distribution.values()):
            raise TypeError("Use Fraction values for exact probabilities.")
        if any(x < 0 for x in distribution.values()):
            raise ValueError("Probabilities must be nonnegative.")
        if sum(distribution.values()) != 1:
            raise ValueError("Probabilities must sum to one.")
    witness = tuple(y for y in p if p[y] > likelihood_factor * q[y])
    gap = sum((p[y] - likelihood_factor * q[y] for y in witness), Fraction(0))
    return gap, witness


def enumerate_gap(p, q, likelihood_factor):
    """Enumerate all events to independently inspect this tiny example."""
    labels = tuple(p)
    return max(
        sum((p[y] - likelihood_factor * q[y] for y in event), Fraction(0))
        for size in range(len(labels) + 1)
        for event in combinations(labels, size)
    )


def main():
    p = {"a": Fraction(9, 20), "b": Fraction(7, 20), "c": Fraction(4, 20)}
    q = {"a": Fraction(4, 20), "b": Fraction(3, 20), "c": Fraction(13, 20)}
    factor = Fraction(2)  # exp(epsilon) = 2, so epsilon = log(2).
    forward, forward_event = directed_gap(p, q, factor)
    reverse, reverse_event = directed_gap(q, p, factor)
    assert forward == enumerate_gap(p, q, factor) == Fraction(1, 10)
    assert reverse == enumerate_gap(q, p, factor) == Fraction(1, 4)
    required_delta = max(forward, reverse)
    print(f"P -> Q: delta = {forward}; witness = {forward_event}")
    print(f"Q -> P: delta = {reverse}; witness = {reverse_event}")
    print(f"Both directions: minimum delta = {required_delta}")
    for proposed_delta in (Fraction(1, 10), Fraction(1, 4)):
        print(f"delta = {proposed_delta}: passes = {required_delta <= proposed_delta}")


if __name__ == "__main__":
    main()
