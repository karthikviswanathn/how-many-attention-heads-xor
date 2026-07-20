"""Standalone exact verification of the two integer tChow certificates.

Checks, in pure integer arithmetic with no dependencies, that

    P(x) = theta * prod_h D_h(x) + sum_h N_h(x) * prod_{g != h} D_g(x)

strictly sign-represents the target function (P > 0 exactly on f = 1), and
that the minimum signed value sigma(x) * P(x) matches the value recorded in
each JSON file.

Run:  python3 verify_certificates.py
"""

import json
import os
from math import prod

HERE = os.path.dirname(os.path.abspath(__file__))


def affine(coeffs, bits):
    return coeffs[0] + sum(c * b for c, b in zip(coeffs[1:], bits))


def cleared_score(theta, D, N, bits):
    d = [affine(row, bits) for row in D]
    n = [affine(row, bits) for row in N]
    total = theta * prod(d)
    for h in range(len(D)):
        total += n[h] * prod(d[g] for g in range(len(D)) if g != h)
    return total


def check(path, n_bits, f):
    cert = json.load(open(os.path.join(HERE, path)))
    theta, D, N = cert["theta"], cert["D"], cert["N"]
    signed_min = None
    for code in range(1 << n_bits):
        bits = [(code >> i) & 1 for i in range(n_bits)]
        sigma = 2 * f(code, bits) - 1
        signed = sigma * cleared_score(theta, D, N, bits)
        assert signed > 0, f"{path}: sign violated at code {code}"
        signed_min = signed if signed_min is None else min(signed_min, signed)
    assert signed_min == cert["min_signed_value"], (
        f"{path}: min signed value {signed_min} != recorded "
        f"{cert['min_signed_value']}"
    )
    print(f"{path}: H={len(D)} verified on all {1 << n_bits} points, "
          f"min signed value {signed_min}")


def f6(code, bits):
    return (sum(bits) % 2) ^ (1 if code in (21, 38, 41) else 0)


def f8(code, bits):
    hamming = sum(bits[i] ^ bits[i + 4] for i in range(4))
    return 1 if hamming >= 2 else 0


if __name__ == "__main__":
    check("tchow4_f6_integer_certificate.json", 6, f6)
    check("tchow2_f8_integer_certificate.json", 8, f8)
    print("all certificates verified exactly")
