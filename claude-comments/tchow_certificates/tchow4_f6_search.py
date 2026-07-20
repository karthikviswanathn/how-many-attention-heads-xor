"""Search for a tChow-4 representation of f_6 (six-bit parity with flips at E={21,38,41}).

P(x) = theta * prod_h D_h(x) + sum_h N_h(x) * prod_{g!=h} D_g(x),  D_h, N_h affine.
Feasible iff sign(P(x)) = sigma(x) for all 64 x, sigma = +1 iff f_6(x)=1.

Strategy: for fixed D (4 affine forms, 28 params), feasibility in (theta, N) is an LP
(29 vars + margin). Outer search over D via random restarts + Powell polish on LP margin.
"""
import numpy as np
from scipy.optimize import linprog, minimize
import sys, json, time

rng = np.random.default_rng(20260717)

# ---------- f_6 ----------
X = np.array([[(c >> i) & 1 for i in range(6)] for c in range(64)], dtype=float)  # x_i = bit i
w = X.sum(axis=1)
E = {21, 38, 41}
f = ((w.astype(int) % 2) == 1).astype(int)
for c in E:
    f[c] ^= 1
sigma = 2 * f - 1  # +-1

A1 = np.hstack([np.ones((64, 1)), X])  # affine evaluation: A1 @ coeffs(7) = values at 64 pts

def lp_margin(Dc):
    """Dc: (4,7) denominator coeffs. Returns (t*, theta, Nc(4,7)) maximizing margin t
    s.t. sigma * P >= t, |theta|<=1, |N coeffs|<=1."""
    Dv = A1 @ Dc.T                      # (64,4) values of D_h
    M = np.empty((64, 4))               # M_h = prod_{g!=h} D_g
    for h in range(4):
        M[:, h] = np.prod(Dv[:, [g for g in range(4) if g != h]], axis=1)
    Pi = np.prod(Dv, axis=1)            # (64,) full product
    # variables: theta(1), Nc flat (28), t(1)
    # constraint: -sigma*(theta*Pi + sum_h (A1@Nc_h)*M_h) + t <= 0
    cols = [(-sigma * Pi)[:, None]]
    for h in range(4):
        cols.append(-sigma[:, None] * (A1 * M[:, h][:, None]))
    Aub = np.hstack(cols + [np.ones((64, 1))])
    bub = np.zeros(64)
    c = np.zeros(30); c[-1] = -1.0      # maximize t
    bounds = [(-1, 1)] * 29 + [(None, None)]
    r = linprog(c, A_ub=Aub, b_ub=bub, bounds=bounds, method="highs")
    if not r.success:
        return -np.inf, None, None
    t = r.x[-1]
    return t, r.x[0], r.x[1:29].reshape(4, 7)

def norm_rows(Dc):
    n = np.linalg.norm(Dc, axis=1, keepdims=True)
    n[n == 0] = 1
    return Dc / n

def sample_D(kind):
    if kind == 0:
        return rng.standard_normal((4, 7))
    if kind == 1:
        return rng.integers(-2, 3, size=(4, 7)).astype(float)
    if kind == 2:  # centered forms: D = c0 + sum c_i (x_i - 1/2)
        Dc = rng.integers(-2, 3, size=(4, 7)).astype(float)
        Dc[:, 0] = Dc[:, 0] - Dc[:, 1:].sum(axis=1) / 2
        return Dc
    Dc = rng.standard_normal((4, 7))
    Dc[:, 0] += rng.uniform(1, 3, size=4)  # biased positive constants
    return Dc

def polish(Dc0, maxiter=400):
    def neg_t(flat):
        t, _, _ = lp_margin(norm_rows(flat.reshape(4, 7)))
        return -t
    r = minimize(neg_t, Dc0.flatten(), method="Powell",
                 options={"maxiter": maxiter, "xtol": 1e-10, "ftol": 1e-12})
    return -r.fun, norm_rows(r.x.reshape(4, 7))

if __name__ == "__main__":
    n_samples = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    n_polish = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    t0 = time.time()
    cands = []
    for i in range(n_samples):
        Dc = norm_rows(sample_D(i % 4))
        t, _, _ = lp_margin(Dc)
        cands.append((t, Dc))
    cands.sort(key=lambda z: -z[0])
    print(f"[{time.time()-t0:6.1f}s] sampled {n_samples}: best margins "
          f"{[f'{t:.3e}' for t, _ in cands[:5]]}", flush=True)
    best = (-np.inf, None)
    for t, Dc in cands[:n_polish]:
        tp, Dp = polish(Dc)
        print(f"[{time.time()-t0:6.1f}s] polish {t:.3e} -> {tp:.3e}", flush=True)
        if tp > best[0]:
            best = (tp, Dp)
    tb, Db = best
    print(f"BEST margin {tb:.6e}")
    if tb > 0:
        t, theta, Nc = lp_margin(Db)
        out = {"margin": t, "theta": theta, "D": Db.tolist(), "N": Nc.tolist()}
        with open(sys.argv[3] if len(sys.argv) > 3 else "tchow4_f6_solution.json", "w") as fh:
            json.dump(out, fh, indent=1)
        print("FEASIBLE candidate written")
