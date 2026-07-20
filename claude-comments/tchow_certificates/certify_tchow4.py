"""Exact rational certification of a tChow-4 sign-representation of f_6.

Loads the best hit JSON, rounds all parameters to rationals, and verifies
sign(P(x)) = sigma(x) at all 64 points in exact Fraction arithmetic.
"""
from fractions import Fraction
import json, glob
import numpy as np

hits = []
for fn in glob.glob("tchow_hit_*.json"):
    with open(fn) as fh:
        d = json.load(fh)
    if "D-H5" in fn:
        continue
    hits.append((d["margin"], fn, d))
hits.sort(key=lambda z: -z[0])
margin, fn, d = hits[0]
print(f"best H=4 hit: {fn}  float margin {margin:.6e}")

Dc = d["D"]                      # 4 x 7
sol = d["sol"]                   # theta + 28 N coeffs
theta_f, N_f = sol[0], sol[1:]

def rat(v, q=10**6):
    return Fraction(v).limit_denominator(q)

theta = rat(theta_f)
D = [[rat(Dc[h][k]) for k in range(7)] for h in range(4)]
N = [[rat(N_f[7*h + k]) for k in range(7)] for h in range(4)]

E = {21, 38, 41}
def sigma_of(c):
    par = bin(c).count("1") & 1
    fv = par ^ (1 if c in E else 0)
    return 1 if fv else -1

def aff(coeffs, c):
    v = coeffs[0]
    for i in range(6):
        if (c >> i) & 1:
            v += coeffs[i + 1]
    return v

min_signed = None
ok = True
for c in range(64):
    Dv = [aff(D[h], c) for h in range(4)]
    P = theta * Dv[0] * Dv[1] * Dv[2] * Dv[3]
    for h in range(4):
        Mh = Fraction(1)
        for g in range(4):
            if g != h:
                Mh *= Dv[g]
        P += aff(N[h], c) * Mh
    s = sigma_of(c)
    signed = s * P
    if min_signed is None or signed < min_signed:
        min_signed = signed
    if signed <= 0:
        ok = False
        print(f"  FAIL at x={c:06b} (code {c}): sigma={s}, P={P}")

print(f"exact min signed value sigma(x)*P(x) over 64 points: {min_signed} "
      f"(~{float(min_signed):.6e})")
print("CERTIFIED: exact tChow-4 sign-representation of f_6" if ok and min_signed > 0
      else "NOT certified")

if ok and min_signed > 0:
    out = {
        "theta": [str(theta)],
        "D": [[str(v) for v in row] for row in D],
        "N": [[str(v) for v in row] for row in N],
        "min_signed_value": str(min_signed),
        "convention": "affine coeffs [c0, c1..c6], form value = c0 + sum ci*xi, x in {0,1}^6; "
                      "P = theta*D1*D2*D3*D4 + sum_h N_h*prod_{g!=h} D_g; "
                      "f_6 = parity XOR [code in {21,38,41}], code = sum x_i 2^i",
    }
    with open("tchow4_f6_exact_certificate.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("exact certificate written to tchow4_f6_exact_certificate.json")
