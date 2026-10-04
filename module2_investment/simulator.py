"""CFP Module 2 (Investment Planning) - investment simulator page.

Back-test Lump sum, DCA and VCA on a portfolio of Thai mutual funds using their real NAV
history. The calculations live in simulate.py; this file is only the page.
"""

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

# ---------- portfolio ----------

st.markdown("#### Portfolio")
by_amount = st.radio(
    "Enter the portfolio as", ["Weight %", "Amount (THB)"], horizontal=True, key="sim_mode",
    help="Weight %: choose how to split, then the total amount under Strategy. "
         "Amount (THB): type how much goes into each fund; the split comes from the amounts.",
) == "Amount (THB)"

# Each way of entering has its own table, so switching back and forth keeps both.
col = "Amount (THB)" if by_amount else "Weight %"
table_key, editor_key = ("sim_portfolio_thb", "sim_editor_thb") if by_amount else ("sim_portfolio", "sim_editor")
if table_key not in st.session_state:
    a, b = (3_000, 2_000) if by_amount else (60, 40)
    st.session_state[table_key] = pd.DataFrame([
        {"Fund": by_symbol.get("ES-GQG"), col: a},
        {"Fund": by_symbol.get("SCBSET"), col: b},
    ]).dropna()
value_column = (
    st.column_config.NumberColumn(col, min_value=0, step=500, format="%d", required=True)
    if by_amount else
    st.column_config.NumberColumn(col, min_value=0, max_value=100, step=5, format="%d%%", required=True)
)
edited = st.data_editor(
    st.session_state[table_key], key=editor_key, num_rows="dynamic", hide_index=True,
    use_container_width=True,
    column_config={
        "Fund": st.column_config.SelectboxColumn("Fund (type to search)", options=options,
                                                 required=True, width="large"),
        col: value_column,
    },
)
how = ("Amount = THB per fund: invested once for Lump sum, each period for DCA, target growth "
       "each period for VCA. " if by_amount else "")
st.caption(f"{how}Add a row with the + under the table, delete with the checkbox and 🗑. "
           f"Up to {MAX_FUNDS} funds.")

rows = edited.dropna(subset=["Fund", col])
rows = rows[rows[col] > 0]
weights = rows.groupby(rows["Fund"].map(symbol_of), sort=False)[col].sum()  # merge duplicates
if weights.empty:
    st.info(f"Add at least one fund with {'an amount' if by_amount else 'a weight'} above 0.")
    st.stop()
if len(weights) > MAX_FUNDS:
    st.warning(f"Only the first {MAX_FUNDS} funds are used.")
    weights = weights.iloc[:MAX_FUNDS]
total = weights.sum()
split = ", ".join(f"{s} {w / total * 100:.1f}%" for s, w in weights.items())
if by_amount:
    if len(weights) > 1:
        st.caption(f"Total {total:,.0f} THB, split {split}.")
elif abs(total - 100) > 0.01:
    st.info(f"Weights add up to {total:g}%, so they are scaled to 100% ({split}).")
weights = weights / total * 100

with st.spinner("Loading fund history ..."):
    histories = {s: load_full_history(s, last_date) for s in weights.index}
missing = [s for s, h in histories.items() if len(h) < 2]
if missing:
    st.warning(f"No history for: {', '.join(missing)}")
    st.stop()
prices = align_prices({s: h.set_index("navDate")["growth"] for s, h in histories.items()})
if len(prices) < 2:
    st.warning("These funds have no dates in common.")
    st.stop()

first_day, last_day = prices.index[0].date(), prices.index[-1].date()
default_start = max(first_day, (prices.index[-1] - pd.DateOffset(years=5)).date())
youngest = max(histories, key=lambda s: histories[s]["navDate"].iloc[0])

# ---------- strategy ----------

st.markdown("#### Strategy")
c1, c2, c3 = st.columns([2, 1, 1])
strategy = c1.radio("Strategy", STRATEGIES, index=1, horizontal=True, label_visibility="collapsed")
start = c2.date_input("Start", value=default_start, min_value=first_day, max_value=last_day)
end = c3.date_input("End", value=last_day, min_value=first_day, max_value=last_day)
note = f"Data starts {first_day:%d %b %Y}"
if len(weights) > 1:
    note += f" (the youngest fund, {youngest}, launched then)"
st.caption(f"{STRATEGY_HELP[strategy]} {note}.")

c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
label = {"Lump sum": "Amount (THB)", "DCA": "Amount each period (THB)",
         "VCA": "Target growth each period (THB)"}[strategy]
if by_amount:
    amount = total  # the sum of the amounts in the portfolio table
    c1.text_input(label, value=f"{amount:,.0f}", disabled=True,
                  help="Sum of the amounts in the portfolio table. Change them there.")
elif strategy == "Lump sum":
    amount = c1.number_input(label, min_value=100, value=100_000, step=1_000, format="%d")
else:
    amount = c1.number_input(label, min_value=100, value=5_000, step=500, format="%d")
if strategy == "Lump sum":
    frequency, allow_sell = "Monthly", False
else:
    frequency = c2.selectbox("Every", list(FREQUENCIES))
    allow_sell = strategy == "VCA" and c4.toggle(
        "Sell when above target", help="Off: when the portfolio is above target you just skip "
                                       "that period. On: you sell the part above target.")
rebalance = "None"
if len(weights) > 1:
    choices = REBALANCING if strategy != "Lump sum" else ["None", "Yearly"]
    rebalance = c3.selectbox("Rebalance", choices, help=REBALANCE_HELP)

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
