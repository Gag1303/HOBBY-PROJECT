"""Financial calculator maths, the same as an HP 10bII / Casio FC-200V.

Cash-flow sign convention (as on those calculators): money you pay out is negative, money you
receive is positive. E.g. saving 5,000 a month: PMT = -5000, and the FV comes out positive.

TVM equation, with i = rate per payment period and t = 1 for BGN (payments at the start of each
period) or 0 for END:

    PV * (1+i)^N  +  PMT * (1 + i*t) * ((1+i)^N - 1) / i  +  FV  =  0
"""

import math

import numpy as np


def periodic_rate(iy: float, py: int, cy: int) -> float:
    """Rate per payment period from I/Y (% per year, nominal), P/Y and C/Y."""
    return (1 + iy / 100 / cy) ** (cy / py) - 1


def annual_rate(i: float, py: int, cy: int) -> float:
    """I/Y (% per year, nominal) from the rate per payment period. Inverse of periodic_rate."""
    return cy * ((1 + i) ** (py / cy) - 1) * 100


def _annuity(i: float, n: float, bgn: bool) -> float:
    """Value at period N of 1 paid every period: (1 + i*t) * ((1+i)^N - 1) / i."""
    if abs(i) < 1e-12:
        return n
    return (1 + i * bgn) * ((1 + i) ** n - 1) / i


def tvm_balance(n: float, i: float, pv: float, pmt: float, fv: float, bgn: bool) -> float:
    """Left side of the TVM equation; 0 when the five values are consistent."""
    return pv * (1 + i) ** n + pmt * _annuity(i, n, bgn) + fv


def solve_fv(n, i, pv, pmt, bgn=False):
    return -(pv * (1 + i) ** n + pmt * _annuity(i, n, bgn))


def solve_pv(n, i, pmt, fv, bgn=False):
    return -(fv + pmt * _annuity(i, n, bgn)) / (1 + i) ** n


def solve_pmt(n, i, pv, fv, bgn=False):
    return -(pv * (1 + i) ** n + fv) / _annuity(i, n, bgn)


def solve_n(i, pv, pmt, fv, bgn=False):
    if abs(i) < 1e-12:
        return -(pv + fv) / pmt
    p = pmt * (1 + i * bgn) / i
    ratio = (p - fv) / (p + pv)
    if ratio <= 0:
        raise ValueError("No solution: with these values the money never reaches the target.")
    return math.log(ratio) / math.log(1 + i)


def solve_i(n, pv, pmt, fv, bgn=False) -> float:
    """Rate per period that balances the TVM equation (searched numerically)."""
    f = lambda i: tvm_balance(n, i, pv, pmt, fv, bgn)
    # Scan for a sign change, then bisect. Rates from -99% to +1000% per period.
    grid = np.concatenate([np.linspace(-0.99, 0, 200, endpoint=False), np.geomspace(1e-9, 10, 400)])
    values = [f(x) for x in grid]
    for (a, fa), (b, fb) in zip(zip(grid, values), zip(grid[1:], values[1:])):
        if fa == 0:
            return a
        if fa * fb < 0:
            for _ in range(200):
                m = (a + b) / 2
                if f(a) * f(m) <= 0:
                    b = m
                else:
                    a = m
            return (a + b) / 2
    raise ValueError("No solution: check the signs (money paid out must be negative).")


def schedule(n: int, i: float, pv: float, pmt: float, bgn: bool = False):
    """Balance period by period: interest earned/charged and the balance after each period."""
    rows, balance = [], pv
    for k in range(1, n + 1):
        if bgn:
            balance += pmt
        interest = balance * i
        balance += interest
        if not bgn:
            balance += pmt
        rows.append({"Period": k, "Payment": pmt, "Interest": interest, "Balance": balance})
    return rows


# ---------- cash flows ----------

def npv(rate: float, cash_flows: list[float]) -> float:
    """Net present value. cash_flows[0] is CF0 (today), cash_flows[k] at the end of period k."""
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cash_flows))


def irr(cash_flows: list[float]) -> float:
    """Internal rate of return per period (the rate where NPV = 0)."""
    f = lambda r: npv(r, cash_flows)
    grid = np.concatenate([np.linspace(-0.99, 0, 200, endpoint=False), np.geomspace(1e-9, 10, 400)])
    values = [f(x) for x in grid]
    for (a, fa), (b, fb) in zip(zip(grid, values), zip(grid[1:], values[1:])):
        if fa == 0:
            return a
        if fa * fb < 0:
            for _ in range(200):
                m = (a + b) / 2
                if f(a) * f(m) <= 0:
                    b = m
                else:
                    a = m
            return (a + b) / 2
    raise ValueError("No IRR: cash flows need at least one negative and one positive amount.")


# ---------- rate conversion ----------

def effective_rate(nominal: float, m: int | None) -> float:
    """Effective annual rate (%) from a nominal annual rate (%) compounded m times a year.
    m=None means continuous compounding."""
    r = nominal / 100
    return (math.exp(r) - 1) * 100 if m is None else ((1 + r / m) ** m - 1) * 100


def nominal_rate(effective: float, m: int | None) -> float:
    """Nominal annual rate (%) compounded m times a year that gives this effective rate (%)."""
    e = effective / 100
    return math.log(1 + e) * 100 if m is None else m * ((1 + e) ** (1 / m) - 1) * 100
