"""CFP Module 2 (Investment Planning) - investment simulator page.

Back-test Lump sum, DCA and VCA on any Thai mutual fund's real NAV history.
The calculations live in simulate.py; this file is only the page.
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from module2_investment.common import (
    DATA_NOTE, SERIES_COLORS, last_date_or_stop, load_full_history, load_market, signed,
)
from module2_investment.simulate import FREQUENCIES, STRATEGIES, simulate, trade_dates

STRATEGY_HELP = {
    "Lump sum": "Invest the whole amount once, on the start date.",
    "DCA": "Dollar cost averaging: invest the same amount every period, whatever the price.",
    "VCA": "Value averaging: the portfolio should grow by a fixed amount every period. Each period you "
           "top up whatever is needed to reach the target, so you buy more when prices fall and "
           "less (or nothing) when they rise.",
}

st.title("📈 Investment simulator")
st.caption("What would have happened if you had invested in a fund with Lump sum, DCA or VCA? "
           "Uses the fund's real NAV history, dividends reinvested.")
st.sidebar.caption(DATA_NOTE)

last_date = last_date_or_stop()
with st.spinner("Loading fund list ..."):
    market = load_market(last_date)

funds = market.sort_values("symbol")
labels = dict(zip(funds["symbol"], funds["symbol"] + "  ·  " + funds["nameEn"].fillna("")))
choices = list(labels)
if st.session_state.get("sim_symbol") not in labels:  # first visit, or fund no longer listed
    st.session_state["sim_symbol"] = "ES-GQG" if "ES-GQG" in labels else choices[0]
sym = st.selectbox("Fund (type to search)", choices, format_func=labels.get, key="sim_symbol")

with st.spinner(f"Loading full history of {sym} ..."):
    hist = load_full_history(sym, last_date)
if len(hist) < 2:
    st.warning("Not enough history for this fund.")
    st.stop()

prices = hist.set_index("navDate")["growth"]
first_day, last_day = prices.index[0].date(), prices.index[-1].date()
default_start = max(first_day, (prices.index[-1] - pd.DateOffset(years=5)).date())

c1, c2, c3 = st.columns([2, 1, 1])
strategy = c1.radio("Strategy", STRATEGIES, index=1, horizontal=True)
start = c2.date_input("Start", value=default_start, min_value=first_day, max_value=last_day)
end = c3.date_input("End", value=last_day, min_value=first_day, max_value=last_day)
st.caption(f"{STRATEGY_HELP[strategy]} Data for {sym} starts {first_day:%d %b %Y}.")

c1, c2, c3 = st.columns([2, 1, 1])
if strategy == "Lump sum":
    amount = c1.number_input("Amount (THB)", min_value=100, value=100_000, step=1_000, format="%d")
    frequency, allow_sell = "Monthly", False
else:
    label = "Amount each period (THB)" if strategy == "DCA" else "Target growth each period (THB)"
    amount = c1.number_input(label, min_value=100, value=5_000, step=500, format="%d")
    frequency = c2.selectbox("Every", list(FREQUENCIES))
    allow_sell = strategy == "VCA" and c3.toggle(
        "Sell when above target", help="Off: when the portfolio is above target you just skip "
                                       "that period. On: you sell the part above target.")

if start >= end:
    st.warning("Start date must be before the end date.")
    st.stop()
timeline, trades, s = simulate(prices, start, end, strategy, amount, frequency, allow_sell)
if not s:
    st.warning("Not enough NAV data in this period.")
    st.stop()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Money invested", f"{s['Money in']:,.0f} THB")
m2.metric("Value at end", f"{s['Value now']:,.0f} THB")
m3.metric("Profit", f"{s['Profit']:,.0f} THB", signed(s["Profit %"]))
m4.metric("Return per year", signed(s["Return per year %"]),
          help="Money-weighted return (IRR, like Excel XIRR). Fair for comparing strategies "
               "that put money in at different times.")
if s["Money out (sold)"] > 0:
    st.caption(f"Includes {s['Money out (sold)']:,.0f} THB taken out by selling above target.")

fig = go.Figure([
    go.Scatter(x=timeline.index, y=timeline["value"], name="Portfolio value",
               line=dict(width=2, color=SERIES_COLORS[0]),
               hovertemplate="%{y:,.0f} THB<extra>Portfolio value</extra>"),
    go.Scatter(x=timeline.index, y=timeline["invested"], name="Money invested",
               line=dict(width=2, color=SERIES_COLORS[1], shape="hv"),
               hovertemplate="%{y:,.0f} THB<extra>Money invested</extra>"),
])
fig.update_layout(height=420, margin=dict(l=0, r=0, t=30, b=0), hovermode="x unified",
                  yaxis=dict(title="THB", tickformat=","),
                  legend=dict(orientation="h", y=1.02, x=1, xanchor="right", yanchor="bottom"))
st.plotly_chart(fig, use_container_width=True)

nav = hist.set_index("navDate")["navPerUnit"]
with st.expander(f"Every buy / sell ({s['Trades']})"):
    rows = trades.assign(nav=trades["date"].map(nav))[["date", "nav", "cash", "valueAfter"]]
    rows = rows[rows["cash"] != 0].style.format(
        {"date": "{:%d %b %Y}", "nav": "{:.4f}", "cash": "{:+,.0f}", "valueAfter": "{:,.0f}"})
    st.dataframe(rows, hide_index=True, use_container_width=True, column_config={
        "date": "Date",
        "nav": "NAV",
        "cash": "Cash in (+) / out (−)",
        "valueAfter": "Portfolio value after",
    })

# Same period, all three strategies, with comparable amounts.
per_period = amount
if strategy == "Lump sum":
    n = len(trade_dates(prices, start, end, frequency))
    per_period = amount / max(n, 1)
dca = simulate(prices, start, end, "DCA", per_period, frequency)[2]
results = {
    "Lump sum": simulate(prices, start, end, "Lump sum", dca["Money in"])[2],
    "DCA": dca,
    "VCA": simulate(prices, start, end, "VCA", per_period, frequency, allow_sell)[2],
}
table = pd.DataFrame(results).T[["Money in", "Value now", "Profit", "Profit %",
                                 "Return per year %", "Largest single top-up"]]
st.markdown(f"#### All strategies · same period ({frequency.lower()}, "
            f"{per_period:,.0f} THB per period)")
money_cols = ["Money in", "Value now", "Profit", "Largest single top-up"]
styled = (table.style.format("{:,.0f}", subset=money_cols)
          .format(signed, subset=["Profit %", "Return per year %"]))
st.dataframe(styled, use_container_width=True, column_config={"Value now": "Value at end"})
st.caption("Lump sum invests the same total as DCA, all on the first day. VCA's target grows by "
           "the same amount per period, so the money it needs is different. Dividends are "
           "reinvested; fees and taxes are not included. Past performance does not guarantee "
           "future results.")
