"""Amundson constant computation — G(n) = n^(n+1)/(n+1)^n, A_G = lim G(n+1)/G(n)."""
from decimal import Decimal, getcontext

def G(n: int, precision: int = 100) -> Decimal:
    getcontext().prec = precision + 20
    d = Decimal(n)
    return (d ** (d + 1)) / ((d + 1) ** d)

def compute_A_G(precision: int = 100) -> Decimal:
    getcontext().prec = precision + 50
    n = Decimal(10) ** 6
    g_n = (n ** (n + 1)) / ((n + 1) ** n)
    g_n1 = ((n+1) ** (n + 2)) / ((n + 2) ** (n+1))
    return g_n1 / g_n

def e_limit_series(n: int) -> dict:
    getcontext().prec = 50
    d = Decimal(n)
    base = (1 + 1/d) ** d
    exact_e = d / base
    e = Decimal("2.718281828459045235360287471352662497757247093699959574966")
    correction = Decimal(1) / (2 * e)
    return {
        "n": n,
        "n_over_base": float(exact_e),
        "n_over_e": float(d / e),
        "correction_1_2e": float(correction),
        "gap": float(exact_e - d/e),
    }

def verify_identity_1(n: int) -> bool:
    """G(n) * (1 + 1/n)^n = n * G(n-1) for n >= 2"""
    getcontext().prec = 50
    if n < 2:
        return False
    gn = G(n, 50)
    gn1 = G(n-1, 50)
    d = Decimal(n)
    lhs = gn * (1 + 1/d) ** d
    rhs = d * gn1
    return abs(lhs - rhs) < Decimal("1e-30")

if __name__ == "__main__":
    print(f"G(10) = {G(10)}")
    print(f"G(100) = {G(100)}")
    print(f"A_G (approx) = {compute_A_G(50)}")
    print(f"e-limit for n=1000: {e_limit_series(1000)}")
    print(f"Identity 1 verified for n=10: {verify_identity_1(10)}")
