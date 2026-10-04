"""Financial calculator page (Tools): TVM, cash flows (NPV/IRR) and rate conversion.

Works like the HP 10bII / Casio FC-200V financial calculators used in the CFP exam.
The maths is in fincalc.py; this file is only the page.
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from calculators.fincalc import (
    annual_rate, effective_rate, irr, nominal_rate, npv, periodic_rate, schedule, solve_fv,
    solve_i, solve_n, solve_pmt, solve_pv,
)

TVM_KEYS = ["N", "I/Y", "PV", "PMT", "FV"]
PER_YEAR = [1, 2, 4, 12, 52, 365]
TVM_HELP = {
    "N": "Number of payment periods (e.g. 10 years of monthly payments = 120).",
    "I/Y": "Interest rate per year, in % (nominal).",
    "PV": "Present value: money at the start. Paid out = negative, received = positive.",
    "PMT": "Payment each period. Paid out = negative, received = positive.",
    "FV": "Future value: money at the end.",
}

# Ready-made exercises: (solve for, P/Y, BGN?, values). The solved value is ignored.
EXAMPLES = {
    "Save 5,000 a month for 10 years at 5%: how much at the end?":
        ("FV", 12, False, {"N": 120, "I/Y": 5.0, "PV": 0.0, "PMT": -5000.0, "FV": 0.0}),
    "Home loan 3,000,000 THB, 6%, 30 years: monthly payment?":
        ("PMT", 12, False, {"N": 360, "I/Y": 6.0, "PV": 3_000_000.0, "PMT": 0.0, "FV": 0.0}),
    "Want 10,000,000 THB in 25 years at 6%: how much to save each month?":
        ("PMT", 12, False, {"N": 300, "I/Y": 6.0, "PV": 0.0, "PMT": 0.0, "FV": 10_000_000.0}),
    "Retirement: spend 30,000 a month for 25 years, money earns 4%: how much needed at retirement?":
        ("PV", 12, True, {"N": 300, "I/Y": 4.0, "PV": 0.0, "PMT": 30_000.0, "FV": 0.0}),
    "1,000,000 THB grows to 2,000,000 in 10 years: what yearly return?":
        ("I/Y", 1, False, {"N": 10, "I/Y": 0.0, "PV": -1_000_000.0, "PMT": 0.0, "FV": 2_000_000.0}),
    "Save 10,000 a month at 5%: how long to reach 1,000,000?":
        ("N", 12, False, {"N": 0, "I/Y": 5.0, "PV": 0.0, "PMT": -10_000.0, "FV": 1_000_000.0}),
}

# Defaults, set once per session (the first example).
if "tvm_init" not in st.session_state:
    st.session_state["tvm_init"] = True
    solve, py, bgn, values = next(iter(EXAMPLES.values()))
    st.session_state.update({f"tvm_{k}": float(v) for k, v in values.items()})
    st.session_state.update(tvm_solve=solve, tvm_py=py, tvm_cy=py, tvm_mode="END")


def load_example():
    solve, py, bgn, values = EXAMPLES[st.session_state["tvm_example"]]
    st.session_state.update({f"tvm_{k}": float(v) for k, v in values.items()})
    st.session_state.update(tvm_solve=solve, tvm_py=py, tvm_cy=py, tvm_mode="BGN" if bgn else "END")


st.title("🧮 Financial calculator")
st.caption("Works like the HP 10bII / Casio FC-200V used in the CFP exam. Sign rule: money you "
           "**pay out is negative**, money you **receive is positive**.")

tab_tvm, tab_cf, tab_rate = st.tabs(["⏳ TVM (N, I/Y, PV, PMT, FV)", "💵 Cash flows (NPV / IRR)",
                                      "🔁 Interest rate conversion"])

# ---------- TVM ----------

with tab_tvm:
    st.selectbox("Load an example", list(EXAMPLES), index=None, key="tvm_example",
                 on_change=load_example, placeholder="Pick a practice question (optional)")

    c1, c2, c3, c4 = st.columns(4)
    solve_for = c1.selectbox("Solve for", TVM_KEYS, key="tvm_solve")
    py = c2.selectbox("P/Y (payments per year)", PER_YEAR, key="tvm_py")
    cy = c3.selectbox("C/Y (compounding per year)", PER_YEAR, key="tvm_cy",
                      help="How often interest is added. Usually the same as P/Y.")
    mode = c4.radio("Payments at", ["END", "BGN"], key="tvm_mode", horizontal=True,
                    help="END: at the end of each period (loans, most savings). "
                         "BGN: at the start (rent, insurance premiums, retirement spending).")
    bgn = mode == "BGN"

    cols = dict(zip(TVM_KEYS, st.columns(5)))
    values, slots = {}, {}
    for k in TVM_KEYS:
        if k == solve_for:
            slots[k] = cols[k].empty()  # filled with the answer below
        else:
            fmt = "%.4f" if k == "I/Y" else "%.2f"
            values[k] = cols[k].number_input(k, key=f"tvm_{k}", format=fmt, help=TVM_HELP[k],
                                             step=1.0 if k in ("N", "I/Y") else 1000.0)

    try:
        if solve_for == "I/Y":
            i = solve_i(values["N"], values["PV"], values["PMT"], values["FV"], bgn)
            answer = annual_rate(i, py, cy)
        else:
            i = periodic_rate(values["I/Y"], py, cy)
            if solve_for == "N":
                answer = solve_n(i, values["PV"], values["PMT"], values["FV"], bgn)
            elif solve_for == "PV":
                answer = solve_pv(values["N"], i, values["PMT"], values["FV"], bgn)
            elif solve_for == "PMT":
                answer = solve_pmt(values["N"], i, values["PV"], values["FV"], bgn)
            else:
                answer = solve_fv(values["N"], i, values["PV"], values["PMT"], bgn)
        values[solve_for] = answer
        # Keep the answer, like the calculator does: switch "Solve for" and it's still there.
        st.session_state[f"tvm_{solve_for}"] = float(answer)
        shown = f"{answer:,.4f}%" if solve_for == "I/Y" else f"{answer:,.2f}"
        slots[solve_for].metric(f"{solve_for} =", shown)
    except (ValueError, ZeroDivisionError, OverflowError) as e:
        slots[solve_for].metric(f"{solve_for} =", "–")
        st.warning(str(e) if str(e) else "No solution for these values. Check the signs.")
        st.stop()

    n, years = values["N"], values["N"] / py
    st.info(
        f"**{solve_for} = {shown}**  ·  N = {n:,.2f} periods = {years:,.2f} years  ·  "
        f"rate per period {i * 100:.4f}%  ·  effective rate per year "
        f"{effective_rate(values['I/Y'], cy):.4f}%  ·  payments at {mode}"
    )

    if 0 < n <= 1200 and abs(n - round(n)) < 1e-6:
        rows = pd.DataFrame(schedule(int(round(n)), i, values["PV"], values["PMT"], bgn))
        with st.expander(f"Schedule: balance period by period ({int(round(n))} periods)"):
            fig = go.Figure(go.Scatter(x=rows["Period"], y=rows["Balance"], mode="lines",
                                       line=dict(width=2, color="#2a78d6"),
                                       hovertemplate="Period %{x}<br>Balance %{y:,.2f}<extra></extra>"))
            fig.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0),
                              xaxis_title="Period", yaxis=dict(title="Balance", tickformat=","))
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(rows.style.format({"Payment": "{:,.2f}", "Interest": "{:,.2f}",
                                            "Balance": "{:,.2f}"}),
                         hide_index=True, use_container_width=True)
            st.caption(f"Total payments {rows['Payment'].sum():,.2f} · total interest "
                       f"{rows['Interest'].sum():,.2f}. Signs follow the calculator's rule: when "
                       "saving, the balance is negative (money you have put in, worth FV at the "
                       "end); for a loan it is positive (money you still owe, 0 when paid off).")

# ---------- cash flows ----------

with tab_cf:
    st.caption("CF0 is today (usually the money you put in, negative). The following rows come at "
               "the end of each period. **Times** repeats a cash flow, like Nj on the calculator.")
    if "cf_table" not in st.session_state:
        st.session_state["cf_table"] = pd.DataFrame({
            "Cash flow (THB)": [-100_000.0, 30_000.0, 50_000.0],
            "Times": [1, 3, 1],
        })
    flows = st.data_editor(
        st.session_state["cf_table"], key="cf_editor", num_rows="dynamic", use_container_width=True,
        column_config={
            "Cash flow (THB)": st.column_config.NumberColumn(format="%.2f", required=True),
            "Times": st.column_config.NumberColumn(min_value=1, max_value=600, step=1, format="%d",
                                                   default=1, required=True),
        },
    )
    flows = flows.dropna()
    expanded = [cf for cf, times in zip(flows["Cash flow (THB)"], flows["Times"]) for _ in range(int(times))]
    rate = st.number_input("Discount rate per period (%)", value=8.0, step=0.5, format="%.4f")

    if len(expanded) < 2:
        st.info("Enter CF0 and at least one later cash flow.")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("NPV", f"{npv(rate / 100, expanded):,.2f}",
                  help="Value today of all cash flows at the discount rate. Above 0 = worth doing.")
        try:
            m2.metric("IRR per period", f"{irr(expanded) * 100:.4f}%",
                      help="The rate at which NPV = 0.")
        except ValueError as e:
            m2.metric("IRR per period", "–")
            st.warning(str(e))
        m3.metric("Periods", f"{len(expanded) - 1}")
        st.caption("Cash flows in order: " + ", ".join(f"{cf:,.0f}" for cf in expanded[:24])
                   + (" …" if len(expanded) > 24 else ""))

# ---------- rate conversion ----------

with tab_rate:
    options = {"Yearly (1)": 1, "Half-yearly (2)": 2, "Quarterly (4)": 4, "Monthly (12)": 12,
               "Weekly (52)": 52, "Daily (365)": 365, "Continuous": None}
    left, right = st.columns(2)
    with left:
        st.markdown("**Nominal → effective (EAR)**")
        nom = st.number_input("Nominal rate per year (%)", value=12.0, step=0.25, format="%.4f")
        m = options[st.selectbox("Compounded", list(options), index=3, key="rate_m1")]
        st.metric("Effective rate per year", f"{effective_rate(nom, m):.4f}%")
    with right:
        st.markdown("**Effective → nominal**")
        eff = st.number_input("Effective rate per year (%)", value=12.0, step=0.25, format="%.4f")
        m2 = options[st.selectbox("Compounded", list(options), index=3, key="rate_m2")]
        st.metric("Nominal rate per year", f"{nominal_rate(eff, m2):.4f}%")
    st.caption("A bank quoting 12% compounded monthly really pays 12.68% a year. Compare offers "
               "using the effective rate.")
