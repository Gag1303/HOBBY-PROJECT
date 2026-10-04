"""CFP Module 2 (Investment Planning) - investment simulator page.

Back-test Lump sum, DCA and VCA on a portfolio of Thai mutual funds using their real NAV
history. The calculations live in simulate.py; this file is only the page.
"""

from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from module2_investment.common import (
    DATA_NOTE, SERIES_COLORS, fund_label, last_date_or_stop, load_full_history, load_market,
    signed, symbol_of,
)
from module2_investment.simulate import (
    FREQUENCIES, REBALANCING, STRATEGIES, align_prices, simulate, trade_dates,
)

MAX_FUNDS = len(SERIES_COLORS)  # one distinct color per fund

STRATEGY_HELP = {
    "Lump sum": "Invest the whole amount once, on the start date.",
    "DCA": "Dollar cost averaging: invest the same amount every period, whatever the price.",
    "VCA": "Value averaging: the portfolio should grow by a fixed amount every period. Each period you "
           "top up whatever is needed to reach the target, so you buy more when prices fall and "
           "less (or nothing) when they rise.",
}
REBALANCE_HELP = ("Every amount invested is split by the target weights. Over time the funds that "
                  "grew most take a bigger share. Rebalancing sells some of those and buys the "
                  "others to get back to the target weights.")

st.title("📈 Investment simulator")
st.caption("What would have happened if you had invested in a portfolio of funds with Lump sum, "
           "DCA or VCA? Uses the funds' real NAV history, dividends reinvested.")
st.sidebar.caption(DATA_NOTE)

last_date = last_date_or_stop()
with st.spinner("Loading fund list ..."):
    market = load_market(last_date)
funds = market.sort_values("symbol")
options = [fund_label(s, n) for s, n in zip(funds["symbol"], funds["nameEn"])]
by_symbol = {symbol_of(o): o for o in options}

# ---------- strategy ----------

st.markdown("#### Strategy")
c1, c2, c3 = st.columns([2, 1, 1])
strategy = c1.radio("Strategy", STRATEGIES, index=1, horizontal=True, label_visibility="collapsed")
if strategy == "Lump sum":
    frequency, allow_sell = "Monthly", False
else:
    frequency = c2.selectbox("Every", list(FREQUENCIES))
    allow_sell = strategy == "VCA" and c3.toggle(
        "Sell when above target", help="Off: when the portfolio is above target you just skip "
                                       "that period. On: you sell the part above target.")
st.caption(STRATEGY_HELP[strategy])

# ---------- portfolio: total money box, fund table, summary ----------

st.markdown("#### Portfolio")
label, default_total = {
    "Lump sum": ("Total amount to invest (THB)", 100_000),
    "DCA": ("Total amount each period (THB)", 5_000),
    "VCA": ("Total target growth each period (THB)", 5_000),
}[strategy]
total_box = st.number_input(label, min_value=0, value=default_total, step=500, format="%d",
                            key=f"sim_total_{strategy}",
                            help="Funds entered as % get that share of this amount.")

if "sim_portfolio" not in st.session_state:
    st.session_state["sim_portfolio"] = pd.DataFrame([
        {"Fund": by_symbol.get("ES-GQG"), "Amount (THB)": 0, "Weight %": 60.0},
        {"Fund": by_symbol.get("SCBSET"), "Amount (THB)": 0, "Weight %": 40.0},
    ]).dropna(subset=["Fund"])
edited = st.data_editor(
    st.session_state["sim_portfolio"], key="sim_editor", num_rows="dynamic", hide_index=True,
    use_container_width=True,
    column_config={
        "Fund": st.column_config.SelectboxColumn("Fund (type to search)", options=options,
                                                 required=True, width="large"),
        "Amount (THB)": st.column_config.NumberColumn("Amount (THB)", min_value=0, step=500,
                                                      format="%d", default=0),
        "Weight %": st.column_config.NumberColumn("or Weight %", min_value=0, max_value=100,
                                                  step=5, format="%g%%", default=0),
    },
)
st.caption("For each fund fill in **either** a THB amount **or** a weight % of the total above, "
           "and leave the other at 0 (if both are filled, the THB amount is used). Add a row with the + under the table, "
           f"delete with the checkbox and 🗑. Up to {MAX_FUNDS} funds.")

rows = edited.dropna(subset=["Fund"]).copy()
rows["Amount (THB)"] = pd.to_numeric(rows["Amount (THB)"], errors="coerce").fillna(0)
rows["Weight %"] = pd.to_numeric(rows["Weight %"], errors="coerce").fillna(0)
rows["by_amount"] = rows["Amount (THB)"] > 0
rows["THB"] = rows["Amount (THB)"].where(rows["by_amount"], rows["Weight %"] / 100 * total_box)
rows = rows[rows["THB"] > 0]
rows["symbol"] = rows["Fund"].map(symbol_of)
alloc = rows.groupby("symbol", sort=False).agg(  # merge duplicate funds
    Fund=("Fund", "first"), THB=("THB", "sum"),
    entered=("by_amount", lambda b: "THB" if b.all() else ("%" if not b.any() else "THB + %")))
if alloc.empty:
    st.info("Add at least one fund with a THB amount or a weight above 0.")
    st.stop()
if len(alloc) > MAX_FUNDS:
    st.warning(f"Only the first {MAX_FUNDS} funds are used.")
    alloc = alloc.iloc[:MAX_FUNDS]

amount = alloc["THB"].sum()
alloc["Share"] = alloc["THB"] / amount * 100
summary = pd.concat([
    alloc[["Fund", "entered", "THB", "Share"]],
    pd.DataFrame([{"Fund": "Total invested", "entered": "", "THB": amount, "Share": 100.0}]),
], ignore_index=True)
st.dataframe(summary.style.format({"THB": "{:,.0f}", "Share": "{:.1f}%"}), hide_index=True,
             use_container_width=True,
             column_config={"Fund": "Investment summary", "entered": "Entered as",
                            "THB": {"Lump sum": "Amount (THB)", "DCA": "Each period (THB)",
                                    "VCA": "Target growth each period (THB)"}[strategy],
                            "Share": "Share"})

leftover = total_box - amount
if not rows["by_amount"].all():  # the total box matters only when some fund uses %
    if leftover > 0.5:
        st.info(f"{leftover:,.0f} THB of the {total_box:,.0f} THB total is not given to any fund, "
                f"so it is not invested. Simulating {amount:,.0f} THB.")
    elif leftover < -0.5:
        st.warning(f"The funds add up to {amount:,.0f} THB, which is {-leftover:,.0f} THB more "
                   f"than the {total_box:,.0f} THB total. Simulating {amount:,.0f} THB.")
else:
    st.caption(f"Every fund has a THB amount, so the total box isn't used. "
               f"Simulating {amount:,.0f} THB.")
weights = alloc["THB"] / amount * 100

with st.spinner("Loading fund history ..."):
    histories = {s: load_full_history(s, last_date) for s in weights.index}
missing = [s for s, h in histories.items() if len(h) < 2]
if missing:
    st.warning(f"No history for: {', '.join(missing)}")
    st.stop()
prices = align_prices({s: h.set_index("navDate")["growth"] for s, h in histories.items()})
# Leave out today's NAV: funds can still revise it, and many funds haven't published it yet.
prices = prices[prices.index < pd.Timestamp(date.today())]
if len(prices) < 2:
    st.warning("These funds have no dates in common.")
    st.stop()

first_day, last_day = prices.index[0].date(), prices.index[-1].date()
default_start = max(first_day, (prices.index[-1] - pd.DateOffset(years=5)).date())
youngest = max(histories, key=lambda s: histories[s]["navDate"].iloc[0])

# ---------- period and rebalancing ----------

st.markdown("#### Period")
c1, c2, c3 = st.columns([1, 1, 1])
start = c1.date_input("Start", value=default_start, min_value=first_day, max_value=last_day)
end = c2.date_input("End", value=last_day, min_value=first_day, max_value=last_day)
rebalance = "None"
if len(weights) > 1:
    choices = REBALANCING if strategy != "Lump sum" else ["None", "Yearly"]
    rebalance = c3.selectbox("Rebalance", choices, help=REBALANCE_HELP)
note = f"Data starts {first_day:%d %b %Y}"
if len(weights) > 1:
    note += f" (the youngest fund, {youngest}, launched then)"
note += f". Latest date {last_day:%d %b %Y}: today's NAV is left out because it may not be final yet."
st.caption(note)

if start >= end:
    st.warning("Start date must be before the end date.")
    st.stop()
run = dict(frequency=frequency, weights=weights.to_dict(), rebalance=rebalance)
timeline, trades, s, by_fund = simulate(prices, start, end, strategy, amount,
                                        allow_sell=allow_sell, **run)
if not s:
    st.warning("Not enough NAV data in this period.")
    st.stop()

# ---------- results ----------

st.markdown("#### Result")
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

if len(weights) > 1:
    # Per-fund breakdown: where the money ended up, and how far the weights drifted.
    window = prices.loc[timeline.index]
    end_values = by_fund.iloc[-1]
    breakdown = pd.DataFrame({
        "Fund": [by_symbol.get(f, f) for f in weights.index],
        "Target weight": weights.values,
        "Value at end": end_values[weights.index].values,
        "Weight at end": (end_values / end_values.sum() * 100)[weights.index].values,
        "Fund return in period": ((window.iloc[-1] / window.iloc[0] - 1) * 100)[weights.index].values,
    })
    st.markdown("#### By fund")
    st.dataframe(
        breakdown.style.format({"Target weight": "{:.1f}%", "Value at end": "{:,.0f}",
                                "Weight at end": "{:.1f}%", "Fund return in period": signed}),
        hide_index=True, use_container_width=True,
    )

    fig = go.Figure([
        go.Scatter(x=by_fund.index, y=by_fund[f], name=f, stackgroup="funds", mode="lines",
                   line=dict(width=1, color=SERIES_COLORS[i]),
                   hovertemplate=f"%{{y:,.0f}} THB<extra>{f}</extra>")
        for i, f in enumerate(weights.index)
    ])
    fig.update_layout(title="Value by fund", height=380, margin=dict(l=0, r=0, t=40, b=0),
                      hovermode="x unified", yaxis=dict(title="THB", tickformat=","),
                      legend=dict(orientation="h", y=1.02, x=1, xanchor="right", yanchor="bottom",
                                  traceorder="normal"))  # same order as the table
    st.plotly_chart(fig, use_container_width=True)

with st.expander(f"Every buy / sell ({s['Trades']})"):
    rows = trades[trades["cash"] != 0].style.format(
        {"date": "{:%d %b %Y}", "cash": "{:+,.0f}", "valueAfter": "{:,.0f}"})
    st.dataframe(rows, hide_index=True, use_container_width=True, column_config={
        "date": "Date", "cash": "Cash in (+) / out (−)", "valueAfter": "Portfolio value after",
    })

# Same period and portfolio, all three strategies, with comparable amounts.
per_period = amount
if strategy == "Lump sum":
    per_period = amount / max(len(trade_dates(prices, start, end, frequency)), 1)
dca = simulate(prices, start, end, "DCA", per_period, **run)[2]
results = {
    "Lump sum": simulate(prices, start, end, "Lump sum", dca["Money in"],
                         **{**run, "rebalance": "None" if rebalance == "Every period" else rebalance})[2],
    "DCA": dca,
    "VCA": simulate(prices, start, end, "VCA", per_period, allow_sell=allow_sell, **run)[2],
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
